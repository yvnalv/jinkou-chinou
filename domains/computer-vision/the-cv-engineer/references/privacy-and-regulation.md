# Privacy, Regulation, and Ethics

Cameras record people. This file covers what is prohibited, what is high-risk, and how to design vision systems that stay lawful and proportionate. Verified on 2026-09-11; laws change and vary by country. This is engineering guidance, not legal advice — involve legal counsel and, in the EU, your data protection officer before deploying anything that films people.

## Contents

1. First questions
2. EU AI Act
3. Data protection (GDPR and similar)
4. Other jurisdictions
5. Privacy by design
6. Fairness and accuracy across people
7. Documentation

---

## 1. First questions

Before the first camera goes up:

- [ ] Are people identifiable in the footage? (Faces, gait, plates, badges, uniforms, context can all identify.)
- [ ] What is the purpose, and is filming **necessary and proportionate** for it? Could a non-camera sensor do the job?
- [ ] Who is filmed: employees, customers, the public, children, patients?
- [ ] Is any **biometric** processing involved (recognizing or categorizing a person), or only anonymous detection ("a person is present")?
- [ ] Where is data stored and processed, for how long, and who can see it?
- [ ] Is there a lawful basis, and are people informed?

The distinction that matters most in practice: **detecting that a person is present** is ordinary personal-data processing; **identifying who they are, or inferring attributes about them**, is biometric processing with much stricter rules.

## 2. EU AI Act

**Prohibited (since 2 February 2025), with narrow exceptions:**

* Untargeted scraping of the internet or CCTV footage to build or expand facial-recognition databases.
* Emotion recognition in workplaces and educational institutions (outside medical or safety uses).
* Biometric categorization to infer protected characteristics (race, political opinions, trade-union membership, religion, sex life, sexual orientation).
* Real-time remote biometric identification in publicly accessible spaces for law-enforcement purposes (member-state exceptions with judicial authorization).
* Social scoring, and certain predictive-policing and manipulative systems.

**High-risk (Annex III)** includes remote biometric identification systems, biometric categorization, emotion recognition outside the prohibited contexts, and safety components of regulated products. High-risk duties (risk management, data governance, technical documentation, logging, human oversight, accuracy and robustness, conformity assessment, registration) apply from **2 December 2027** for Annex III systems and **2 August 2028** for Annex I products, after the 2026 Digital Omnibus agreement moved those dates.

**Transparency (Article 50)** applies from **2 August 2026**: people must be told when they interact with an AI system, and AI-generated or manipulated image, audio, and video content must be disclosed, with machine-readable marking of synthetic content from **2 December 2026**.

Most commercial analytics (counting people, detecting PPE, spotting defects, reading plates for access control) is **not** high-risk under the Act, but it is still personal-data processing under data-protection law.

## 3. Data protection (GDPR and similar)

* **Lawful basis:** usually legitimate interest (with a balancing test) or consent; consent is rarely workable for public spaces and is problematic for employees, where power imbalance undermines it.
* **Biometric data** (faces, gait, iris) used for identification is a special category: it generally needs an explicit legal basis such as explicit consent or substantial public interest.
* **Transparency:** clear signage at every entrance and in the area, a privacy notice explaining purpose, controller, retention, and rights.
* **DPIA** (data protection impact assessment) is required for systematic monitoring of public areas and for most biometric systems; do it before deployment and keep it updated.
* **Data minimization:** analyse on the edge and discard frames where possible; keep events and crops rather than continuous video; blur or mask what you do not need.
* **Retention:** the shortest period that serves the purpose (often days, not months, for routine footage); enforce automatic deletion.
* **Rights:** access, erasure, and objection requests must be answerable — which requires being able to find footage of a person without building a face database.
* **Workplace monitoring** has extra rules in many countries (works council agreements, prohibitions on continuous performance monitoring).

## 4. Other jurisdictions

* **United States:** no federal video-privacy law, but state biometric laws are strict and heavily litigated — Illinois BIPA (written consent before collecting face or fingerprint templates, private right of action, statutory damages), Texas and Washington equivalents, and comprehensive state privacy laws with biometric provisions. Some cities restrict public-sector facial recognition.
* **United Kingdom:** UK GDPR plus the surveillance-camera code; ICO guidance on video surveillance and facial recognition.
* **Elsewhere:** many countries require notice, registration, or consent for CCTV; some restrict cross-border transfer of footage. Check locally before deploying, and treat the strictest applicable rule as the design constraint for a multi-country rollout.

## 5. Privacy by design

Design choices that usually satisfy both lawyers and engineers:

| Technique | Effect |
|---|---|
| Process on the edge, transmit only events | Footage never leaves the site; bandwidth drops by orders of magnitude |
| Discard frames immediately after inference | Nothing to breach, subpoena, or leak |
| Blur or pixelate faces, plates, and screens before storage or review | Keeps evidence value, removes identification |
| Store crops, not full frames | Smaller surface, easier retention control |
| Aggregate counts instead of tracks | Occupancy and flow without following individuals |
| Short, enforced retention with automatic deletion | Limits exposure; simplifies rights requests |
| Access control, audit logs, and encryption at rest and in transit | Demonstrable control |
| No face embeddings unless identification is the purpose and is lawful | Avoids the strictest category entirely |
| Masked zones (windows into private property, neighbouring areas) | Proportionality, and often a legal requirement |

## 6. Fairness and accuracy across people

* Face and person models can perform unevenly across skin tone, age, gender presentation, body size, mobility aids, and clothing (including religious dress); cameras and lighting amplify this (exposure metering is often tuned for lighter skin).
* Measure per-group performance where you lawfully can, on data that represents the deployment population; if you cannot collect group labels, at least test across lighting, distance, and camera conditions that correlate with the differences.
* The harm of a false positive differs by context: a wrong alert in a security system can lead to a confrontation or an arrest. Require human review before consequential action, and design the review so the human has enough context to disagree.
* Be explicit about what the system cannot do (recognize intent, detect emotions reliably, identify people from low-resolution footage) and refuse to build claims on top of those.

## 7. Documentation

Keep, and keep current: purpose and lawful basis, DPIA, camera inventory with fields of view and masked zones, data flows and retention, model cards including per-slice performance, access and audit policy, signage and notice texts, human-oversight procedure, incident and rollback procedures, and a decision log for thresholds. If the system ever becomes high-risk under the AI Act, most of this is already required evidence.
