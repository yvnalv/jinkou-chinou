# Product Knowledge : AI Plus Agent for Exact Globe+ (Flippy Globe+)

> **Source Reference**: Official GLM Systems Documentation (`docs.glmsystems.com/aiplusagent/globeplus/`).  
> **Brand Persona**: Flippy, the AI assistant embedded directly in Exact Globe+.  
> **Target Audience**: Financial controllers, warehouse managers, procurement officers, sales operations, and Globe+ system administrators.  
> **Tone**: Professional, practical, context-aware, reassuring. No technical jargon where plain business language works.

---

## 1. Product Overview and Value Proposition

**Flippy** is an AI assistant embedded directly inside **Exact Globe+**. It appears as a floating action button beside the Globe+ window, allowing users to interact with their entire ERP database using conversational everyday language.

* **Context-Aware Architecture**:
  - Understands the currently active company in Globe+.
  - Reads the active Globe+ screen or master record currently open on the user's desktop.
  - Strictly abides by the user's Globe+ function rights and role permissions.
* **Core Value**:
  - Eliminates manual menu navigation across deep ERP hierarchies.
  - Speeds up transaction entry, stock queries, and reporting.
  - Delivers verified, interactive data tables with click-to-open record links.

---

## 2. Interface Layouts and Display Modes

Flippy supports 5 distinct layout positions configurable via `/settings` or `/position`:

| Display Layout | Screen Behavior and Window Dimensions |
| :--- | :--- |
| **Bottom Right (Default)** | Unobtrusive floating circular icon in the bottom-right corner of Globe+. |
| **Right Panel** | Fixed docked panel occupying 25% of window width (resizable up to 50%). Globe+ canvas resizes. |
| **Left Panel** | Fixed docked panel on the left occupying 25% to 50% of window width. |
| **Right Overlay** | Floating panel over the right side of Globe+ without resizing the underlying ERP interface. |
| **Floating Window** | Separate, movable, and freely resizable window with remembered dimensions. |

*Auto-Hide Behavior*: Chat automatically hides when Exact Globe+ loses application focus.

---

## 3. Core Feature Pillars

### Feature 1 : Context-Aware Chat & Data Queries
* Natural language queries retrieve ERP data directly into interactive, sortable chat tables.
* Users can add or remove columns dynamically (*"Add the Authorized column"*).
* Clickable record links in query tables instantly open the actual record in Globe+.
* User-scoped filtering (*"Show my sales orders"*, *"Budget totals for scenario 2025"*).

### Feature 2 : Transaction Creation with Confirmation Safeguards
* Conversational creation of ERP transactions:
  - Sales Orders and Purchase Orders
  - Quotations and Return Merchandise Authorizations (RMAs)
  - Bills of Materials (BOMs) and Production Orders
  - Financial General Ledger Entries
* **Confirmation Gate**: Flippy summarizes all transaction parameters (customer, items, quantities, pricing) and requires explicit user confirmation before writing to the database.

### Feature 3 : Dedicated Stock & Inventory Analytics
Beyond basic lookups, Flippy provides specialized inventory intelligence:
* **Current & Dated Stock**: Real-time stock levels per item, warehouse, and historical date.
* **Depletion Forecast**: Predicts stock depletion horizons with risk classifications:
  - `Stockout`
  - `At Risk`
  - `Healthy`
  - `Overstocked`
* **Movement Trends**: Explains reasons for inventory shifts and highlights largest movements over time.
* **Screen + Stock Synergy**: When viewing an open order on screen, asking *"Do I have enough stock for this order?"* reads the active screen lines and verifies warehouse availability automatically.

### Feature 4 : Screen Reader (Active View Context)
* Users can ask questions about whatever is currently open on their Globe+ screen.
* Summarizes active customer cards, purchase requisitions, or complex sales orders without manual input.

### Feature 5 : Automated Emailing (Review & Edit Tab)
* Converts query results or transaction tables into outgoing emails.
* Automatically prepares recipients (`To`, `Cc`, `Bcc`), subject line, body text, and attachments from queried data.
* Opens an embedded **Review & Edit Email** tab so the user verifies everything before hitting Send.

### Feature 6 : Recode (Controlled Master Data Renaming)
* Controlled alternative to error-prone manual mass updates across 15 supported master data entities:
  - Accounts, Assets, Cash Instruments, Cost Centres, Cost Units, General Ledger
  - Items, Journals, Projects, People, Selection Codes, Shipping Methods
  - GL Categories, Invoice Codes, Payment Conditions
* Supports single-code renaming or bulk recoding via Excel import.

### Feature 7 : Bulk Master Data Import & Export (Excel `.xlsx`)
* Upload `.xlsx` spreadsheets to create, update, or recode items and accounts in bulk.
* Visual **Map Excel Columns** dialog with reusable named mapping templates.
* Export any chat result table directly to `.xlsx` or copy formatted table to clipboard.

### Feature 8 : Instant Menu & Record Navigation
* Skips manual tree navigation: *"Go to Inventory"*, *"Open Sales Order Entry"*.
* Supports English and Dutch menu designations.
* Fast-path instant navigation executes without waiting for LLM completion.

### Feature 9 : Web Search Integration
* Combines ERP context with live web data (e.g., European VAT regulations, live currency exchange rates).

### Feature 10 : Helpful Fallbacks When No Data Found
* When queries return empty results (e.g., unknown budget scenario), Flippy offers to list valid options from Globe+ to help the user refine their request.

---

## 4. Enterprise Security and Rights Architecture

* **Role 501 (`AIPlusAgentUser`)**:
  - Flippy requires role 501 assigned to the user account in Globe+ (`System > HR & Security > People > Rights`).
* **Strict Function Rights Mirroring**:
  - Flippy never bypasses or escalates Globe+ rights.
  - If a user lacks rights to approve invoices or view financial journals, Flippy politely refuses and explains the exact permission boundary.
  - Summary prompt: *"What rights do I have?"* provides a clear breakdown of allowed actions.

---

## 5. Authentic Example Prompts

```text
Query: "Show my open sales orders"
Query: "Show pricelist for item BEK0003"
Query: "Which invoices are not paid yet?"
Stock: "Analyze movements for BEK0001 last quarter"
Stock: "Will we run out in 60 days?"
Stock: "Do I have enough stock for this order?"
Transaction: "Create a sales order for customer Cafe Hout with item BEK0003 quantity 5"
Screen Context: "Summarize this order on my screen"
Email: "Send this list to finance@client.com with subject Q3 Overdue Invoices"
Navigation: "Go to Inventory"
Master Data: "Create a new item ItemCode ITMNOV001 Description ItemNovember001 assortment 0"
Recode: "Recode item ABC to XYZ"
Rights Check: "What rights do I have?"
```

