# Product Knowledge : AI Plus Agent for Exact Synergy (Flippy Synergy)

> **Source Reference**: Official GLM Systems Documentation (`docs.glmsystems.com/aiplusagent/agentsynergy/`).  
> **Brand Persona**: Flippy, the AI assistant embedded in Exact Synergy.  
> **Target Audience**: Operations directors, HR coordinators, project managers, sales account executives, and Synergy administrators.  
> **Tone**: Professional, collaborative, agile, transparent. Focused on workflow speed, zero bureaucracy, and automated accountability.

---

## 1. Product Overview and Value Proposition

**AI Plus Agent for Exact Synergy** embeds Flippy directly into the web-based **Exact Synergy** portal. It brings the exact same conversational ease to workflow requests, CRM accounts, project management, and HRM as it does to ERP transactions in Globe+.

* **Unified Experience**:
  - Provides a single conversational language interface across Globe+ and Synergy.
  - Users familiar with Flippy in Globe+ can instantly use Flippy in Synergy without additional training.
* **Core Value**:
  - Eliminates cumbersome portal navigation through multi-step request forms, document trees, and CRM tabs.
  - Automates workflow request generation (leave requests, expense approvals, task dispatch).
  - Surfaces real-time employee, project, and pipeline intelligence instantly.

---

## 2. Installation & Setup Workflow

| Step | Action Description | Visual Reference Asset |
| :--- | :--- | :--- |
| **Step 1** | Open Synergy installation folder, locate `GLMSysAddOnInstaller`, and launch it. | [`01-install-synergy-addon-installer.webp`](../../assets/brand-kit/graphics/products/synergy/01-install-synergy-addon-installer.webp) |
| **Step 2** | Select Synergy Installation Directory and click Start. | [`02-install-synergy-directory.webp`](../../assets/brand-kit/graphics/products/synergy/02-install-synergy-directory.webp) |
| **Step 3** | Wait for "Installation Complete" notification. | [`03-install-synergy-complete.webp`](../../assets/brand-kit/graphics/products/synergy/03-install-synergy-complete.webp) |
| **Step 4** | In Synergy, navigate to `Modules > AI Plus Agent > Setup > License > Update`. | [`04-license-modules-setup-menu.webp`](../../assets/brand-kit/graphics/products/synergy/04-license-modules-setup-menu.webp) |
| **Step 5** | Drag and drop the license file and click Validate & Continue. | [`05-license-drag-drop-file.webp`](../../assets/brand-kit/graphics/products/synergy/05-license-drag-drop-file.webp) |
| **Step 6** | Verify the `AIPlus` add-on is active and click Continue & Apply. | [`06-license-validated-update-screen.webp`](../../assets/brand-kit/graphics/products/synergy/06-license-validated-update-screen.webp) |

---

## 3. Configuration & Provider Settings

Configured under `Modules > AI Plus Agent > Setup > LLM Settings` ([`07-llm-settings-menu.webp`](../../assets/brand-kit/graphics/products/synergy/07-llm-settings-menu.webp)):

* **Debugging Options**:
  - Toggle **Show Tool Calls Debug Information** to review underlying tools executed during AI agent interactions.  
    Visual: [`08-llm-debugging-tool-calls.webp`](../../assets/brand-kit/graphics/products/synergy/08-llm-debugging-tool-calls.webp).
* **Provider Connections**:
  - Enter GLM Systems LLM username and password.
  - Click **Save Provider**, then click **Test Connection**. Displays confirmation: *"Connection successful! GLM AI Agent - GLM Systems Sdn Bhd endpoint is reachable."*  
    Visual: [`09-llm-provider-connection-test.webp`](../../assets/brand-kit/graphics/products/synergy/09-llm-provider-connection-test.webp).

---

## 4. Interface Entry & Module Suggestions

* **Module Contextual Prompts**: Inside supported modules (such as Quotations), Flippy automatically surfaces adaptive suggested prompt chips tailored to the active task.  
  Visual: [`10-module-quotation-suggestions.webp`](../../assets/brand-kit/graphics/products/synergy/10-module-quotation-suggestions.webp).
* **The Flippy Header Button**: The circular Flippy button is anchored in the top-right header between **Preferences** and **About**.  
  Visual: [`11-flippy-button-header.webp`](../../assets/brand-kit/graphics/products/synergy/11-flippy-button-header.webp).
* **Welcome Card**: Opens a clean introduction panel outlining supported queries, record types, and capabilities.  
  Visual: [`12-welcome-what-flippy-can-do.webp`](../../assets/brand-kit/graphics/products/synergy/12-welcome-what-flippy-can-do.webp).

---

## 5. Core Synergy Functional Capabilities & Visual Proof

### 1. Interactive Queries & Direct Record Links
* Query data across Requests, Resources, Accounts, Projects, Items, and Orders.
* Displays results in clean tables with record links that open the source Synergy card directly.  
  Visuals:
  - User queries table: [`13-query-user-queries-table.webp`](../../assets/brand-kit/graphics/products/synergy/13-query-user-queries-table.webp)
  - Opening record directly: [`14-query-open-record-directly.webp`](../../assets/brand-kit/graphics/products/synergy/14-query-open-record-directly.webp)

### 2. Conversational Request Creation
* Create leave requests, task assignments, or approval tickets directly via chat without manually opening form definitions.
* Prompt: *"Create a leave request for next Monday"*.
* Flippy generates the request, populates routing rules, and displays a confirmation card with status and request ID.  
  Visuals:
  - Create request prompt: [`15-request-create-leave-prompt.webp`](../../assets/brand-kit/graphics/products/synergy/15-request-create-leave-prompt.webp)
  - Request created confirmation: [`16-request-created-confirmation.webp`](../../assets/brand-kit/graphics/products/synergy/16-request-created-confirmation.webp)

### 3. Slash Commands (`/`) & Suggestion Auto-Select
* Type `/` followed by `Tab` to trigger inline suggestions for rapid record selection or actions.  
  Visuals:
  - Slash command trigger: [`17-slash-commands-trigger.webp`](../../assets/brand-kit/graphics/products/synergy/17-slash-commands-trigger.webp)
  - Select suggestion: [`18-slash-commands-select-suggestion.webp`](../../assets/brand-kit/graphics/products/synergy/18-slash-commands-select-suggestion.webp)

### 4. Dynamic Data Sorting & Status Filtering
* Natural language sorting and filtering of query tables on the fly.
* Prompts:
  - *"Sort this list by date, newest first"*  
    Visual: [`19-data-sorting-result.webp`](../../assets/brand-kit/graphics/products/synergy/19-data-sorting-result.webp)
  - *"Show only requests with status Open"*  
    Visual: [`20-data-filtering-result.webp`](../../assets/brand-kit/graphics/products/synergy/20-data-filtering-result.webp)

---

## 6. Multi-Modal Input & Quick Reference Prompts

* **Keyboard Input**: Natural conversational queries in plain English.
* **Document Attachments**: Drag and drop PDFs and contracts for instant summarization.
* **Voice Input**: Dictate requests without typing.

```text
Requests: "Show my pending leave requests"
Requests: "Create a leave request for next Monday"
Requests: "Show only requests with status Open"
Resources: "Show resource information for John Tan"
Accounts: "Find account Exact"
Contacts: "Show contacts for account Nico"
Quotations: "Open Quotation 1071"
Pipeline: "List my open opportunities"
Audit Log: "Show the data log for this account"
Documents: "Summarize the attached document"
Sorting: "Sort this list by date, newest first"
Help: "What can you do?"
```
