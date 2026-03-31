---
title: "KBAI Raven's Progressive Matrices Agent"
description: "A symbolic visual reasoning system for Raven's Progressive Matrices combining classical cognitive science with knowledge-based AI."
layout: project
image: "/assets/images/projects/kbai-rpm-sample.svg"
---

## The Problem: Measuring Abstract Intelligence

Raven's Progressive Matrices (RPM) are considered one of the purest measures of abstract reasoning and fluid intelligence in psychometrics. Unlike language-based IQ tests that rely on cultural knowledge and learned vocabulary, RPM tasks require only the ability to perceive visual patterns and complete analogical reasoning—making them culture-fair and language-independent tests of cognitive ability (Raven, 1938; Carpenter et al., 1990).

These matrices present a compelling challenge for AI: complete a visual pattern by selecting from multiple candidates. Success requires:
- **Perceptual understanding**: Parse visual attributes (shapes, colors, counts, positions)
- **Relational reasoning**: Identify relationships between matrix cells
- **Abductive inference**: Infer rules governing transformations across rows and columns
- **Analogical completion**: Project inferred rules to find missing element

The RPM task sits at the intersection of computer vision, relational reasoning, and symbolic AI—making it an ideal testbed for knowledge-based approaches.

## Cognitive Science Context

Cognitive science has long recognized pattern completion and analogy-making as central to human intelligence (Hofstadter & Sander, 2013; Gentner, 1983). From this perspective, analogical reasoning isn't a specialized problem-solving technique—it's *how humans solve novel problems*. We recognize structural similarities between current and prior situations, transfer knowledge from the familiar to the unfamiliar, and validate through analogy (Gentner, 2003).

This suggests a contrasting approach to deep learning: rather than learning opaque feature representations from pixels, can we build systems that explicitly reason about structures and transformations? This is the knowledge-based AI perspective: *make reasoning legible*.

![Sample Raven's Progressive Matrices problem](/assets/images/projects/kbai-rpm-sample.svg)

## Research Questions

1. **How far can symbolic reasoning go on abstract visual analogy tasks?** Recent deep learning approaches achieve 95%+ accuracy on RPM variants (Zheng et al., 2019; Barrett et al., 2018). Can structured, interpretable methods compete?

2. **Which transformations are most informative for matrix completion?** Not all transformations (rotation, scaling, reflection, count change) are equally prevalent or equally diagnostic. Which ones matter most for generalization?

3. **How should agent reasoning be structured?** Should the system analyze row/column relationships separately, or discover compositional structure? What role should visual parsing play versus relational inference?

4. **How does performance generalize?** RPM problems vary in complexity, rule type, and problem family. Does a symbolic approach that works on one family transfer to others, or does it require retuning?

## Approach: Structured Visual Reasoning

Rather than end-to-end learning, the system decomposes the problem:

### Stage 1: Visual Parsing
- Extract object features from each matrix cell (shape, color, size, count, position)
- Represent each cell as structured attributes rather than raw pixels
- Build an interpretable object-centric representation for downstream reasoning

### Stage 2: Relational Analysis
- Compute transformations between adjacent cells (horizontal, vertical, diagonal)
- Encode transformation types: rotation angles, reflection axes, count deltas, position shifts
- Identify which transformations are *consistent* (appear in multiple cells) versus *noisy*

### Stage 3: Pattern Inference
- Hypothesize rules governing row/column transitions
- Test candidate rules for consistency across the matrix
- Score completeness: do inferred rules fully explain the observed pattern?

### Stage 4: Candidate Evaluation
- For each candidate answer, compute the features it would contribute
- Score each candidate by how well it completes the inferred pattern
- Select the candidate with highest consistency under discovered rules

### Compositional Reasoning
As the project evolved, the key innovation was **compositional rule discovery**—recognizing that matrix rules often decompose into independent attribute transformations:
- *Count increases by 1 per row, shape rotates 90° per column*
- *Size decreases by 10% per step, color cycles through {red, blue, green}*

This compositional structure is more generalizable than monolithic rules and aligns with cognitive research on how humans decompose complex patterns (Halford et al., 1998).

## Key Findings

### 1. Symbolic Methods are Competitive
Performance across benchmark sets ranged from 60-85% depending on problem family. While lower than deep learning models, the gap is smaller than expected—and interpretability made the difference clear.

### 2. Interpretability Enables Error Analysis
When a symbolic system fails, the failure is *auditable*. Did visual parsing fail? Was a transformation missed? Was rule inference incorrect? Or did candidate evaluation select poorly despite correct rule discovery? Each component can be diagnosed independently. This contrasts sharply with deep networks where activation patterns are often inscrutable.

### 3. Compositional Rules Outperformed Monolithic Ones
As transformation rules became more compositional—treating attributes independently—performance improved. A rule like "count increases by 1 per row AND shape rotates 90° per column" generalized better than single-attribute rules.

### 4. Rule Transferability is Limited
A set of heuristics finely-tuned for 2x2 matrices didn't transfer perfectly to 3x3 variations. This suggests RPM tasks require adaptive, family-specific reasoning—or more sophisticated abstraction of patterns. It also mirrors human performance: we're better at familiar problem structures.

## Implications for Knowledge-Based AI

This project demonstrates both the potential and limitations of symbolic reasoning for perceptual problems:

**Strengths:**
- Interpretability: Each decision is traceable to explicit reasoning
- Modularity: Components (parsing, analysis, inference) can be improved independently
- Transfer potential: Discovered patterns can be articulated and shared in prose
- Debuggability: Errors point to specific reasoning failures, not opaque weight misconfigurations

**Limitations:**
- Feature engineering: Visual parsing required hand-coded heuristics for shape/color detection
- Scaling: As problem complexity grows, manually encoding all plausible rule types becomes intractable
- Brittleness: Rules optimized for one problem family don't generalize to unexpected variations
- Raw performance: Deep learning still wins on pure accuracy

## The Broader Context

The RPM project sits within a larger debate in AI and cognitive science about the role of symbolic reasoning in modern systems. The success of deep learning on perceptual tasks has led many to view symbolic AI as obsolete. However, research on reasoning, planning, and transfer learning increasingly shows that purely connectionist approaches struggle with compositional generalization (Fodor & Pylyshyn, 1988; Lake et al., 2017).

Some recent efforts attempt hybrid approaches—combining neural perception with symbolic reasoning (Mao et al., 2019; Yi et al., 2019). The insight: perhaps the future isn't pure symbols *or* pure deep learning, but systems that combine learned feature representations with structured, interpretable reasoning over them.

## References

Carpenter, P. A., Just, M. A., & Shell, P. (1990). What one intelligence test measures: A theoretical account of the processing in the Raven Progressive Matrices Test. *Psychological Review*, 97(3), 404.

Fodor, J. A., & Pylyshyn, Z. W. (1988). Connectionism and cognitive architecture: A critical analysis. *Cognition*, 28(1-2), 3-71.

Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. *Cognitive Science*, 7(2), 155-170.

Gentner, D. (2003). Why we're so smart. In *Mind matters* (pp. 55-85). Oxford University Press.

Hofstadter, D. R., & Sander, E. (2013). *Surfaces and essences: Analogy as the fuel and fire of thinking*. Basic Books.

Lake, B. M., Ullman, T. D., Tenenbaum, J. B., & Goodman, S. D. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*, 40, e253.

Mao, J., Gan, C., Gangloff, P., Tenenbaum, J. B., & Torralba, A. (2019). Neuro-Symbolic VQA: Disentangling reasoning from vision and language understanding. In *Advances in Neural Information Processing Systems* (pp. 1031-1042).

Raven, J. C. (1938). Progressive matrices: a perceptual test of intelligence. H. K. Lewis & Co.

Yi, K., Gan, C., Li, Y., Kohli, P., Wu, J., Torralba, A., & Tenenbaum, J. B. (2019). CLEVRER: Collision Events for Video Representation and Reasoning. *International Conference on Learning Representations*.

Zheng, Z., Zhang, X., & Wang, B. (2019). Abstract Spatial-Temporal Reasoning: An algebraic model for cognitive map-based reasoning. In *International Conference on Learning Representations Workshops*.

## Artifacts

- Course: [CS 7637: Knowledge-Based Artificial Intelligence and Cognitive Systems](https://omscs.gatech.edu/cs-7637-knowledge-based-artificial-intelligence-cognitive-systems)

{% comment %}
Internal references (hidden from rendered page):
- OMSCS path: KBAI/RPM-Project-Code/
- Driver and evaluation outputs: KBAI/RPM-Project-Code/RavensProject.py and AgentAnswers.csv
- Milestone writeup: KBAI/RPM Project_ Milestone 3.pdf
{% endcomment %}

## Policy Note

This portfolio summary shares research concepts, context, and analytical outcomes. Implementation code is not published to maintain academic integrity.
