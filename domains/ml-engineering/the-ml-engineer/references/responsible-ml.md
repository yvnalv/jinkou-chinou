# Responsible ML: Fairness, Explainability, Privacy, Regulation

Models that make or support decisions about people carry obligations beyond accuracy. Regulatory facts verified on 2026-09-11; this is engineering guidance, not legal advice. Involve legal and domain experts for high-stakes uses.

## Contents

1. When this applies
2. Fairness
3. Explainability
4. Privacy and security
5. Documentation
6. Regulation

---

## 1. When this applies

Always consider it; treat it as mandatory when the model affects access to **credit, insurance, employment, education, housing, healthcare, public services, or legal outcomes**, or when it profiles people, sets prices per person, or moderates content.

## 2. Fairness

* **Define the harm first:** who could be treated worse, in what way (denied, over-flagged, under-served), and what the comparison groups are.
* **Measure** performance and outcomes per group: selection rate, false-positive and false-negative rates, calibration per group (`scripts/model_report.py --slices group_col`). Libraries such as Fairlearn provide standard metrics.
* **Fairness definitions conflict** (equal selection rates, equal error rates, and equal calibration generally cannot all hold when base rates differ). Choose deliberately with stakeholders and document why.
* **Removing a sensitive attribute is not enough:** proxies (postcode, name, school, device) carry the same information. You may need the attribute to measure fairness even if you don't use it to predict (subject to law and consent).
* Mitigations: better and more representative data, removing proxy features without legitimate purpose, constraints or post-processing (group-specific thresholds where legally permitted), and human review for borderline cases.
* Check historical labels for bias: a model trained on past decisions learns past discrimination.

## 3. Explainability

* **Global:** which features drive the model overall (permutation importance, SHAP summaries, partial dependence). **Local:** why this prediction (SHAP values, reason codes).
* Explanations describe the model, not causal reality; don't present them as causes of the outcome.
* Where people are entitled to reasons (for example adverse credit decisions), design reason codes early and test them for stability and understandability.
* If a simpler model is almost as accurate, its transparency may be worth more than the last point of accuracy.

## 4. Privacy and security

* Data minimization, pseudonymization, access control, retention limits, and a lawful basis for training on personal data.
* Models can memorize and leak training data (membership inference, model inversion), especially large models and small datasets; restrict access to model outputs with confidence scores when sensitive.
* Protect pipelines against data poisoning (validate data sources, monitor label distributions) and model artifacts against tampering (signed or checksummed artifacts, trusted storage).
* Adversarial manipulation: users may game features they control (fraud, spam); monitor for strategic behavior.

## 5. Documentation

* **Model card** (`references/MODEL_CARD.template.md`): intended use, out-of-scope uses, data, metrics overall and per slice, fairness analysis, limitations, ethical considerations, owners, and version.
* **Datasheet** for important datasets: motivation, composition, collection, preprocessing, known biases, and maintenance.
* Keep decision logs: why this metric, this threshold, this fairness definition.

## 6. Regulation

**EU AI Act** (after the Digital Omnibus provisional agreement of May 2026):

| Obligation | Applies from |
|---|---|
| Prohibited practices (for example social scoring, some biometric uses, manipulative techniques) | 2 February 2025 |
| Transparency duties (Article 50) | 2 August 2026 |
| High-risk systems in Annex III (for example employment and worker management, creditworthiness and credit scoring, access to education, essential public and private services, some insurance pricing) | 2 December 2027 |
| High-risk systems in Annex I (safety components of regulated products) | 2 August 2028 |

High-risk obligations include a risk-management system, data governance (representative, error-checked data), technical documentation, logging, transparency to deployers, human oversight, and accuracy, robustness, and cybersecurity requirements. If a model may fall into these categories, design for them from the start.

Also relevant: data-protection law (GDPR and equivalents: lawful basis, data minimization, and rights around automated decision-making), sector rules (credit, insurance, health, employment, anti-discrimination law), and frameworks such as the NIST AI Risk Management Framework and ISO/IEC 42001. Ask where the model is used and check current law.
