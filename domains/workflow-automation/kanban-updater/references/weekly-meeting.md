# Weekly Meeting script

How to turn a week of real work into the short spoken update the user reads out in the Team Weekly Meeting. The audience
is the team and the manager, not developers reviewing code: they want to know **what changed for users or customers,
why it matters, and where it stands**.

---

## 1. Period

Ask in the same round as the mode (Step 0), unless the request already says it:

| Option | Range |
|---|---|
| **Last 7 days including today** (default) | today − 6 days … today |
| **This week** | Monday … today |
| **Custom** | the user's dates |

Never present work from outside the period as this week's.

## 2. Evidence (read-only)

Collect, in this order, and keep a short list of facts per work item:

1. **Git**: `python <skill-dir>/scripts/git_activity.py --repo ... --since <start> --until <end>` over `work_log.repos`.
   Read commit bodies; merged-PR commits (`Merged PR 1234: #7262 : ...`) on the main branch mean **merged**.
2. **The user's own Kanban remarks**: `python <skill-dir>/scripts/synergy_fill.py entries --since <start> --until <end>`.
   These already describe the work in prose (problem, fix, tests, next step) and the card status. Read-only.
3. **The user's notes and documents** the user points to (plans, test reports, code reviews, meeting notes; never inside
   a repository). Use file dates to keep only the period.
4. **The conversation**: decisions, colleagues involved, status not visible in git ("PR created", "waiting for
   approval", "tested by QA").

Group the facts by **product or area** first (for example: the Kanban add-on, the Globe agent, server reports), then by
work item. Work without a commit still counts: reviews, investigations, analysis, test automation, design.

If the status of an item is unclear (PR created or not, merged or not), say what the evidence shows and ask, rather
than guess.

## 3. Wording structure

Write it the way the user speaks in the meeting:

* **Bullets**, one per topic, **1–4 sentences** each; **4–7 bullets** for a normal week. Readable aloud in about two
  minutes.
* **First person, plain spoken English**: "I've been working on …", "Also …", "For the …", "This feature will …".
* **Open each bullet with the product and the goal**: *"I've been working on <product>, <N> work items regarding
  <what>, to allow us to <benefit>."*
* **Explain the benefit and how it works for people** (customers, users, the team), not the implementation: what they
  will see, where they find it, what they can now do.
* **One concrete detail** that makes it real (where something lives, a shortcut name, what a pop-up shows), not a list
  of every change.
* **Close with the status and next step**: done and tested (and by whom), PR created / waiting for approval, merged,
  being tested, next step, or blocked and why.
* **No work item numbers, request numbers, branch, class, file or table names**, no SQL or code terms. Translate them:
  "parameterised queries" → "handled safely"; "AutomationId" → "fixed IDs so test tools can find them".
* Name colleagues the user names (who tested, who reported, whose PR was reviewed); never invent who did what.
* Correct grammar lightly but keep the user's phrasing and rhythm; do not turn it into marketing copy.
* Order: finished or most visible work first, then work in progress, then reviews / investigations / new work started.

## 4. Gold-standard example

The user's own wording (colleague name replaced). Match this register and structure.

```text
- I've been working on AIPlus Agent Globe+, 2 work items regarding the Flippy versioning during installation to allow
  us to know which Flippy version the customer is using and whether it is up to date, and it will be logged inside the
  LLM usage reports. This feature will be shared for the Globe and Synergy agent.
- The released version of the Flippy MSI installer will be available on our own Synergy server, so customers will be
  able to pull the file, download and install it. This feature will also show pop-up notifications in Globe+ when there
  is a new version of Flippy that can be downloaded, complete with the release notes showing the new features and
  fixes, directly from the Flippy Settings page.
- We can put our Flippy installer in Synergy by creating a document that contains "Version" fields and setting the
  security level to customer, so they can access and download the installer.
- It will also force customers to update their installer if their version is too old or we have critical fixes or
  changes. This feature is already done and tested on <colleague>'s side; I will create the PR for both work items.
```

What makes it work: product first, the benefit in the first sentence, how customers get it, one concrete mechanism
(a Synergy document with a "Version" field and customer security level), and a clear status with the next step.

## 5. Self-check before presenting

| Check | Pass when |
|---|---|
| Grounded | every claim traces to a commit, a remark, a document, or the user's words |
| In period | nothing older than the period start |
| No numbers or code names | no `#1234`, request numbers, branches, classes, files, tables |
| Benefit first | each bullet says why it matters to users, customers or the team |
| Status | each bullet ends with done / PR / merged / testing / next / blocked |
| Length | 4–7 bullets, 1–4 sentences each |
| Unknowns | unclear statuses are flagged to the user, not guessed |

## 6. Output

Present the script in chat, ready to read out, followed by a short **"Check before the meeting"** list of anything
uncertain (for example a PR whose status the evidence does not show). Save it to a file only when the user asks, and
never inside a repository.
