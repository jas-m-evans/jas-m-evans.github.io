---
title: "wav2vec Speech Recognition"
description: "Fine-tuning and applying Meta's wav2vec 2.0 model for automatic speech recognition tasks."
layout: project
---

## Overview

This project explores the application of [wav2vec 2.0](https://arxiv.org/abs/2006.11477) — Meta's self-supervised speech representation model — for automatic speech recognition (ASR). The work includes fine-tuning pre-trained checkpoints on domain-specific audio data and evaluating transcription quality.

## Approach

- Load a pre-trained `facebook/wav2vec2-base` checkpoint via Hugging Face Transformers
- Fine-tune on a labelled speech dataset using CTC (Connectionist Temporal Classification) loss
- Evaluate using Word Error Rate (WER) as the primary metric
- Experiment with data augmentation (noise injection, speed perturbation) to improve robustness

## Tech Stack

- Python, PyTorch
- Hugging Face Transformers & Datasets
- torchaudio for audio preprocessing
- Weights & Biases for experiment tracking

## Key Results

*Results and findings will be updated as experiments progress.*
