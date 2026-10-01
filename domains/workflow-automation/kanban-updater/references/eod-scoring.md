# End-of-Day (EoD) Update Scoring SOP

This document defines the rules for formulating high-quality daily work remarks and scoring them according to the team's End-of-Day reporting Standard Operating Procedure (SOP). All factual statements must be grounded in verified Git evidence and user notes.

---

## 1. Per-Task Score (Maximum 5 Points)

Each eligible task entry receives a score based on three dimensions:

$$\text{Task Score} = \text{Consistency} + \text{Timeliness} + \text{Quality} \quad (\le 5.0)$$

### A. Consistency (Max 1.0 Point)
* **+1.0**: Logged on an official weekday (Monday through Friday).
* **0.0**: Logged on a weekend (weekends are excluded from standard score calculations).

### B. Timeliness (Max 1.0 Point)
Measured against the employee's official start time plus 9 hours (the standard shift end):
* **+1.0**: Submitted on or before $\text{Start Time} + 9\text{ hours}$.
* **+0.5**: Submitted within the grace hour ($\text{Start Time} + 9\text{h}$ to $+10\text{h}$).
* **0.0**: Submitted later than 1 hour past shift end.
* *Note:* Requires verified employee start time and local timezone; if unknown, label timeliness as unverified rather than assuming full marks.

### C. Quality (Max 3.0 Points)
* **0.5**: Minimal text (< 10 characters) or generic filler ("same as yesterday", "continue task").
* **1.0**: Short, incomplete text (< 5 words), vague activity without technical context.
* **2.0 – 3.0**: Structured, descriptive technical updates containing:
  * **+0.5**: Explicit progress/behavior change.
  * **+0.5**: Explicit validation or testing performed (or noted pending checks).
  * **+0.5**: Identified blockers, constraints, or pending checks.
  * **+0.5**: Clear, proposed next steps.
  * **+0.5**: Clean technical formatting and structured labels.
  * *Quality score is strictly capped at 3.0 points.*

---

## 2. Weekly Adjustments & Eligibility

* **Weekly Bonus (+2.0 points)**: Awarded if the employee records valid task updates on all 5 weekdays in the reporting week.
* **Repetition Penalty (-5.0 points)**: Deducted if 3 or more consecutive workdays have nearly identical remarks ($\ge 95\%$ text similarity).
* **Waiting Task Exclusion**: Tasks marked with status `Waiting` do not generate task points and do not count as active update days. Do not artificially move tasks out of Waiting solely to gain points.
* **Zero Padding**: Never artificially split a single task into multiple tickets or pad entries with filler to inflate metrics.

---

## 3. Weekly Employee Summary Metrics

$$\text{Final Weekly Score} = \sum \text{Eligible Task Scores} + \text{Bonus} - \text{Penalty}$$
$$\text{Average Score / Day} = \frac{\text{Final Weekly Score}}{\text{Total Valid Update Days}}$$

* **Total Task Entries**: Count of distinct tasks updated with valid remarks.
* **Total EoD Update Days**: Number of distinct weekdays with at least one verified update.
* If update days $= 0$, average score is `N/A` (do not divide by zero).

---

## 4. Evidence-Based Remark Template

When writing task updates, use structured labels that directly map to verified evidence:

```markdown
- Progress: [Concrete behavior changes, commits, or user notes]
- Validation: [Verified tests, clean builds, or diff comparisons performed]
- Pending checks: [Items not yet verified, e.g. browser tests or manual QA]
- Proposed next step: [Concrete action planned for the next session]
```

### Faithful Writing Example

* **User Note**: "tadi pagi bantuin Andika benerin fail install AI Agent, sekarang udah kelar."
* **Faithful Remark**:
  ```markdown
  - Progress: Assisted Andika in diagnosing and resolving the AI Agent installation failure.
  - Validation: Installation verified successfully in the target environment.
  ```
* **Anti-Pattern (Hallucination)**: "Fixed missing registry key in agent installer with Andika and Budi; deployed update to production." *(Never invent unmentioned collaborators, unverified root causes, or undeployed releases).*
