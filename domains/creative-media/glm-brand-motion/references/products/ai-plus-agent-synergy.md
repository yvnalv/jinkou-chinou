# Product Knowledge : AI Plus Agent for Exact Synergy (Flippy Synergy)

> **Source Reference**: Official GLM Systems Documentation (`docs.glmsystems.com/aiplusagent/agentsynergy/`).  
> **Brand Persona**: Flippy, the AI assistant embedded in Exact Synergy.  
> **Target Audience**: Operations directors, HR coordinators, project managers, sales account executives, and Synergy administrators.  
> **Tone**: Professional, collaborative, agile, transparent. Focused on workflow speed, zero bureaucracy, and automated accountability.

---

## 1. Product Overview and Value Proposition

**AI Plus Agent for Exact Synergy** embeds Flippy directly into the web-based **Exact Synergy** portal. It brings the exact same conversational ease to workflow, CRM, project management, and HRM as it does to ERP transactions in Globe+.

* **Unified Experience**:
  - Provides a single conversational language interface across Globe+ and Synergy.
  - Users familiar with Flippy in Globe+ can instantly use Flippy in Synergy without additional training.
* **Core Value**:
  - Eliminates cumbersome portal navigation through request forms, document trees, and CRM tabs.
  - Automates workflow request generation (leave requests, expense approvals, task dispatch).
  - Surfaces real-time employee, project, and pipeline intelligence instantly.

---

## 2. Architecture, Installation and Setup

* **Installer**: Executed via `GLMSysAddOnInstaller.exe` targeting the Synergy web root.
* **Licensing**: Validated under `Modules > AI Plus Agent > Setup > License > Update` via drag-and-drop license file with the `AIPlus` add-on activated.
* **LLM Provider Configuration**:
  - Configured at `Modules > AI Plus Agent > Setup > LLM Settings`.
  - Secure credential testing: Tests GLM Systems AI Agent endpoint with real-time reachability feedback.
  - Optional **Show Tool Calls Debug Information** toggle for administrative monitoring.
* **User Interface Entry**:
  - Prominent circular Flippy button positioned in the top-right Synergy header bar between **Preferences** and **About**.
  - Contextual prompt chips displayed directly inside supported modules.

---

## 3. Core Functional Areas and Entity Coverage

### Area 1 : Requests & Workflow Automation
* Search, open, and manage workflow requests (leave requests, sick reports, task tickets, purchase approvals).
* Filter requests by status (`Open`, `Approved`, `Realized`), request type, date range, or assignee.
* Create complete workflow requests directly from conversation without manually opening request definition screens.

### Area 2 : Resources & Human Resources
* Look up colleague profiles, contact details, departments, and job titles.
* Filter requests, tasks, and project activities by specific employee or resource ID.

### Area 3 : CRM, Accounts and Contacts
* Search customer, supplier, and prospect accounts.
* Inspect account details, address books, and associated contact persons.
* Retrieve audit logs and historical changes on account cards (*"Show the data log for this account"*).

### Area 4 : Sales Pipeline & Quotations
* Review sales opportunities and open pipeline lists (*"List my open opportunities"*).
* Inspect quotation headers and individual quotation lines (*"Show quotation lines for opportunity 123"*).

### Area 5 : Projects & Task Dispatch
* Access project master cards, milestone progress, and budget hours.
* Link workflow requests, activities, and task cards directly to customer projects.

### Area 6 : Inventory & Stock Lookups
* Real-time stock availability, movement histories, and usage trends per item directly from Synergy.

### Area 7 : Documents & Email Analysis
* Retrieve attached emails and stored document files.
* Summarize uploaded PDFs, contracts, and proposals (*"Summarize the attached document"*).

---

## 4. Multi-Modal Input and Fast-Path Controls

* **Natural Language Typing**: Plain English queries and commands.
* **Document & File Attachments**: Drag and drop documents directly into Flippy for content summarization.
* **Voice Input**: Dictate requests and questions without typing.
* **Slash Commands (`/`)**:
  - Type `/` followed by `Tab` to trigger inline suggestions for rapid record selection or actions.

---

## 5. Authentic Example Prompts

```text
Requests: "Show my pending leave requests"
Requests: "Create a leave request for next Monday"
Requests: "Show only requests with status Open"
Resources: "Show resource information for John Tan"
Accounts: "Find account Exact"
Contacts: "Show contacts for account Nico"
Quotations: "Open Quotation 1071"
Quotations: "Show quotation lines for opportunity 123"
Pipeline: "List my open opportunities"
Audit Log: "Show the data log for this account"
Documents: "Summarize the attached document"
Stock: "Show stock movement for item BEK0001 this month"
Sorting: "Sort this list by date, newest first"
Help: "What can you do?"
```
