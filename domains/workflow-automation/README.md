# workflow-automation

The workflow-automation domain covers the orchestration and execution of repetitive developer and operational team routines. This includes issue tracker synchronization, task board automation (such as Exact Synergy Kanban, Jira, and GitHub Projects), automated worklog and standup synthesis from local version control evidence, and productivity system integrations. It focuses on turning raw daily activity into clean, policy-compliant updates across enterprise tools. For general software architecture and product requirements, see `software-engineering`; for codebase quality and security reviews, see `auditing`.

Core persona: the domain's `the-<persona>` skill, if one exists. Specialized skills are named descriptively, without `the-`.

## Skills

<!-- skills:start -->
| Skill | Type | Version | Summary |
|---|---|---|---|
| [`/kanban-updater`](kanban-updater/) | specialized | 3.0.1 | Write daily work logs for Exact Synergy Kanban cards from git and card history, fill them without saving, track EoD points, on a weekday schedule. |
<!-- skills:end -->
