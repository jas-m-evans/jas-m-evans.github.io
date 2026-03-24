---
title: "wav2vec 2.0: Learning to Listen Without Labels"
description: "Fine-tuned Meta's self-supervised wav2vec 2.0 model for automatic speech recognition, exploring how a network trained on raw audio without transcriptions learns acoustic representations powerful enough to enable high-accuracy transcription with only a fraction of the labeled data a conventional system requires."
layout: project
image: "/assets/images/projects/wav2vec-pipeline.svg"
---

![wav2vec 2.0 training pipeline diagram](/assets/images/projects/wav2vec-pipeline.svg)

*Two-phase approach: learn the structure of audio without any transcriptions, then fine-tune on a small labeled dataset.*

## The Big Idea (No Math Required)

Think about how a baby learns to understand language. Long before they can read a single word, they've heard thousands of hours of speech — absorbing the rhythms, sounds, and patterns of their language. By the time they start matching sounds to written words, they already have an incredibly rich internal model of what speech *sounds like*.

wav2vec 2.0 works the same way.

**Phase 1 — Learning to "hear" (no labels needed):** The model is trained on hundreds of hours of raw audio with no transcriptions. It learns by playing a fill-in-the-blank game: mask out a portion of the audio, then predict what sound should go there from a set of candidates. There are no right-or-wrong answers from a human — just the structure of the audio itself. After this phase, the model has a sophisticated internal vocabulary of acoustic patterns.

**Phase 2 — Learning to transcribe (tiny labeled dataset):** Now you add a thin layer on top and fine-tune on actual (audio, text) pairs. Because the model already understands the sound of speech deeply, it only needs a *tiny* amount of labeled data — as little as 10 minutes — to learn to transcribe.

The payoff is dramatic. Traditional speech recognition required 960 hours of human-transcribed audio. wav2vec 2.0 matched its performance with just 10 minutes — a **5,760× reduction** in labeling cost. For rare languages with little transcribed data, this is the difference between having a working system and having nothing at all.

## The Labeling Problem in Speech AI

Building a speech recognition system the traditional way is an expensive proposition. You need audio recordings. Then you need transcriptions of those recordings — every word, timed to the second, verified for accuracy. Depending on the language and domain, a single hour of transcribed audio can cost hundreds of dollars to produce and requires significant linguistic expertise to do right. For well-resourced languages like English, this is a manageable cost. For low-resource languages — of which there are thousands — it is often a prohibitive one.

This is the problem that [wav2vec 2.0](https://arxiv.org/abs/2006.11477), introduced by Meta AI Research in 2020, was designed to address. The model learns powerful acoustic representations from raw audio — without transcriptions, without language models, without any linguistic annotation at all — and then uses those representations as a foundation for fine-tuning on small labeled datasets. In benchmark experiments, wav2vec 2.0 trained on 10 minutes of labeled audio outperformed previous state-of-the-art systems trained on 960 hours.

This project explored that capability: loading a pretrained wav2vec 2.0 checkpoint, fine-tuning it on a labeled speech corpus, and evaluating transcription quality as a function of model and training configuration.

## What wav2vec 2.0 Actually Does

### The Self-Supervised Pretraining Objective

The pretraining phase is where the model learns without labels. It operates on raw 16 kHz waveforms and pursues a *contrastive objective*: given a masked portion of an audio signal, predict the correct quantized latent representation from a set of distractors.

The architecture has three main components:

**1. Feature Encoder** — A multi-layer convolutional network $f: \mathcal{X} \to \mathcal{Z}$ maps raw waveform inputs to a sequence of latent feature vectors at a lower temporal resolution (approximately one vector per 20 ms of audio). This network processes the raw signal without any linguistic prior.

**2. Quantization Module** — The encoder outputs are discretized through a learned codebook into quantized representations $\mathbf{q}_t$, using a product quantizer that operates over $G$ codebook groups:

$$\mathbf{q}_t = \text{concatenate}(\mathbf{e}_{g,v_g})_{g=1}^{G}, \qquad v_g = \arg\max_v \, \mathbf{z}_t^T \mathbf{e}_{g,v}$$

The codebook entries $\mathbf{e}_{g,v}$ are learned representations of acoustic units — the model's emergent "phoneme-like" vocabulary.

**3. Transformer Context Network** — A Transformer encoder $g: \mathcal{Z} \to \mathcal{C}$ receives the (partially masked) feature sequence and produces context representations $\mathbf{c}_t$ that integrate information across the full utterance. This is the component responsible for the model's long-range acoustic modeling.

The training objective asks the Transformer to identify the correct quantized target $\mathbf{q}_t$ among $K$ distractors $\tilde{\mathbf{q}}$ at each masked timestep:

$$\mathcal{L}_m = -\log \frac{\exp(\text{sim}(\mathbf{c}_t, \mathbf{q}_t) / \kappa)}{\sum_{\tilde{\mathbf{q}} \in \mathbf{Q}_t} \exp(\text{sim}(\mathbf{c}_t, \tilde{\mathbf{q}}) / \kappa)}$$

where $\text{sim}(\mathbf{a}, \mathbf{b}) = \mathbf{a}^T \mathbf{b} / (\|\mathbf{a}\| \cdot \|\mathbf{b}\|)$ is cosine similarity and $\kappa$ is a temperature parameter. The full loss adds a codebook diversity term to prevent codebook collapse (all inputs mapping to the same codes).

This objective forces the model to develop representations that are *predictive of the acoustic structure of speech* — without ever seeing a transcript. By the end of pretraining, the model has learned a rich internal vocabulary of acoustic units and a Transformer capable of contextualizing them.

### Fine-Tuning with CTC Loss

Once pretrained, the Transformer's output at each timestep is fed to a single linear projection head that predicts a distribution over the vocabulary (characters or subword units, plus a special blank token). This is fine-tuned end-to-end using **Connectionist Temporal Classification (CTC) loss**.

CTC handles a fundamental mismatch: the audio sequence has many more timesteps than the transcript has characters. A 3-second audio clip sampled at 20 ms intervals produces 150 frame predictions; the corresponding transcript might have only 40 characters. CTC marginalizes over all possible alignments between the frame predictions and the target transcript, computing:

$$\mathcal{L}_{\text{CTC}} = -\log \sum_{\pi \in \mathcal{B}^{-1}(\mathbf{y})} \prod_{t=1}^{T} p(\pi_t \mid \mathbf{x})$$

where $\mathbf{y}$ is the target character sequence, $\mathcal{B}^{-1}(\mathbf{y})$ is the set of all valid CTC paths that collapse to $\mathbf{y}$ (by merging repeated characters and removing blanks), and $p(\pi_t \mid \mathbf{x})$ is the model's prediction at timestep $t$. The sum is computed efficiently using dynamic programming via the forward-backward algorithm.

The elegant property of CTC is that it requires only paired (audio, transcript) data — no alignment annotations, no phoneme labels, no forced-alignment preprocessing. The model learns the alignment as a byproduct of minimizing the loss.

## Approach

The fine-tuning pipeline used Hugging Face's `transformers` and `datasets` libraries to load the `facebook/wav2vec2-base` checkpoint (95M parameters pretrained on 960 hours of LibriSpeech audio) and fine-tune it on a labeled speech corpus.

Key implementation choices:

- **Frozen feature encoder**: the convolutional feature extractor was frozen during fine-tuning, following the recommendation in the original paper. The CNN has already learned a good acoustic front-end; fine-tuning it on small data risks overfitting
- **CTC decoder**: a character-level CTC head was added above the Transformer's output
- **Processor**: the `Wav2Vec2Processor` handles both feature extraction (normalizing raw waveforms) and tokenization (mapping transcripts to character sequences)
- **Optimizer**: AdamW with a warm-up schedule matching the paper's setup for small-data fine-tuning

**Data augmentation** included noise injection (overlaying white noise and environmental background noise at varying SNR levels) and speed perturbation ($\pm$10% tempo shift without pitch change). These perturbations improve robustness to recording conditions and speaker variability without requiring additional transcribed data.

**Experiment tracking** was managed through Weights & Biases, logging loss curves, validation WER, and audio examples at each checkpoint to monitor qualitative degradation patterns alongside quantitative metrics.

## Evaluation: Word Error Rate

The primary evaluation metric is **Word Error Rate (WER)**, the standard benchmark in speech recognition research. WER is derived from the edit distance between the predicted transcript and the ground-truth transcript:

$$\text{WER} = \frac{S + D + I}{N}$$

where $S$ is the number of word substitutions, $D$ is the number of deletions, $I$ is the number of insertions, and $N$ is the total number of words in the reference transcript. WER is computed on word tokens, making it sensitive to how the model handles acoustically similar words and rare vocabulary.

State-of-the-art systems on LibriSpeech (the standard English ASR benchmark) achieve WER below 2% on clean audio and below 5% on noisy audio. Fine-tuned wav2vec 2.0 with 10 minutes of labeled data achieves WER around 4.8% on clean test audio — a remarkable result that would have been state-of-the-art just two years prior to the model's introduction.

## Tech Stack

- Python, PyTorch
- Hugging Face Transformers & Datasets
- torchaudio for waveform loading and augmentation
- Weights & Biases for experiment tracking
- `facebook/wav2vec2-base` pretrained checkpoint

## Why This Architecture Matters

wav2vec 2.0 is significant beyond its benchmark results. It represents a paradigm shift in how the field thinks about data efficiency in speech AI.

The traditional approach — collect labeled data, train a model, evaluate — implicitly assumes that the bottleneck is labeled data. If you need more performance, collect more transcriptions. wav2vec 2.0 challenges that assumption: *the bottleneck is not transcriptions, it is acoustic representations*. With enough unlabeled audio, a self-supervised model can learn representations rich enough that fine-tuning on tiny labeled datasets produces excellent results.

This has profound implications for low-resource language technology. A community that cannot afford thousands of hours of transcribed audio may still be able to collect hours of recorded speech. A pretrained model with strong acoustic features requires only a fraction of that transcribed data to adapt. The barriers to building functional speech technology for underserved languages fall dramatically.

The self-supervised pretraining framework also has a structural connection to the broader "foundation model" paradigm — large models pretrained on vast unlabeled corpora, then adapted to downstream tasks with minimal supervision. wav2vec 2.0 was among the early demonstrations of this approach in audio, and its architectural ideas have influenced subsequent models including HuBERT, WavLM, and Whisper.

## Why This Project Is Research-Relevant

This project connects a concrete engineering task — fine-tuning a pretrained ASR system — to the broader research questions around self-supervised learning, low-resource NLP, and representation quality. It demonstrates:

- **Working knowledge of Transformer-based architectures** in a sequence-to-sequence audio setting
- **Understanding of CTC loss** and its role in alignment-free sequence learning
- **Practical fine-tuning methodology** including frozen feature extraction, warm-up scheduling, and data augmentation
- **Critical engagement with the data-efficiency argument** underlying self-supervised pretraining
- **Experiment management skills** through structured tracking of training dynamics and qualitative output review

The gap between "I ran a fine-tuning script" and "I understand *why* the architecture enables low-resource learning" is where research literacy lives. This project sits in that gap.

## Artifacts and Provenance

- Base model: [facebook/wav2vec2-base](https://huggingface.co/facebook/wav2vec2-base) (Hugging Face Hub)
- Reference paper: [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477), Baevski et al. 2020
- Fine-tuning guide: [Fine-Tune Wav2Vec2 for English ASR](https://huggingface.co/blog/fine-tune-wav2vec2-english) (Hugging Face blog)

## Reader-Friendly TL;DR

Speech recognition normally requires thousands of hours of transcribed audio. wav2vec 2.0 changes that equation by pretraining on raw audio without transcriptions — learning what speech sounds like at a deep level — and then adapting to a specific language or domain with only minutes or hours of labeled data. This project fine-tuned that pretrained model, explored how to measure and improve its transcription quality, and examined why the self-supervised pretraining approach works as well as it does.

The answer involves a contrastive learning objective, quantized acoustic codebooks, Transformer context representations, and CTC loss for alignment-free training. Together, they add up to a model that can genuinely learn from sound alone.

## Policy Note

This project is an independent technical exploration, not a formal course assignment. Full implementation details are shared on the associated GitHub repository where applicable.
