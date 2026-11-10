# Product Knowledge : AI Plus Agent for Exact Globe+ (Flippy Globe+)

> **Source Reference**: Official GLM Systems Documentation (`docs.glmsystems.com/aiplusagent/globeplus/`).  
> **Brand Persona**: Flippy, the AI assistant embedded directly in Exact Globe+.  
> **Target Audience**: Financial controllers, warehouse managers, procurement officers, sales operations, and Globe+ system administrators.  
> **Tone**: Professional, practical, context-aware, reassuring. No technical jargon where plain business language works.

---

## 1. Overview and Core Architecture

**Flippy** is an AI assistant embedded directly in **Exact Globe+**. It appears as a floating chat button beside your active Globe+ window, allowing users to interact with ERP data using everyday conversational language without special syntax.

* **Context-Aware Engine**:
  - Automatically identifies the active company in Globe+.
  - Reads the active Globe+ screen, customer card, or transaction record currently open on the user's desktop.
  - Strictly operates within the user's existing Globe+ function rights and role permissions.
* **Core Value**:
  - Eliminates manual menu navigation across deep ERP trees.
  - Speeds up transaction entry, stock checks, and management reporting.
  - Generates verified, interactive data tables with clickable links that jump straight to the source record.

---

## 2. Installation and Initial Setup

| Step | Action Description | Visual Reference Asset |
| :--- | :--- | :--- |
| **Step 1** | Double-click `GLMSys.AIPlus.Agent.ExactGlobe+` installer. | [`01-install-wizard.webp`](../../assets/brand-kit/graphics/products/globeplus/01-install-wizard.webp) |
| **Step 2** | Choose destination folder and click Next. | [`02-install-destination.webp`](../../assets/brand-kit/graphics/products/globeplus/02-install-destination.webp) |
| **Step 3** | Setup executes file extraction and integration. | [`03-install-setup-status.webp`](../../assets/brand-kit/graphics/products/globeplus/03-install-setup-status.webp) |
| **Step 4** | Click Finish to conclude setup. | [`04-install-finish.webp`](../../assets/brand-kit/graphics/products/globeplus/04-install-finish.webp) |
| **Step 5** | Launch Exact Globe+; Flippy icon appears in the system tray. | [`05-install-icon-launcher.webp`](../../assets/brand-kit/graphics/products/globeplus/05-install-icon-launcher.webp) |
| **Step 6** | Circular Flippy button mounts in the bottom-right corner of Globe+. | [`06-install-flippy-button.webp`](../../assets/brand-kit/graphics/products/globeplus/06-install-flippy-button.webp) |

* **Starting a New Chat**: Click the **New Chat** button to start a fresh conversation and clear previous context.  
  Visual: [`07-new-chat-button.webp`](../../assets/brand-kit/graphics/products/globeplus/07-new-chat-button.webp).

---

## 3. Configuration & Settings Submenus

The Settings menu ([`08-settings-menu.webp`](../../assets/brand-kit/graphics/products/globeplus/08-settings-menu.webp)) contains 5 configuration sections:

### A. Display Modes & Screen Placement
Flippy supports 5 distinct layout positions configured via Settings > Display or `/position` commands:

| Layout Mode | Description and Window Geometry | Visual Reference |
| :--- | :--- | :--- |
| **Left Panel** | Docks on the left side, occupying 25% of Globe+ window width (resizable up to 50%). Globe+ resizes. | [`09-display-layout-left.webp`](../../assets/brand-kit/graphics/products/globeplus/09-display-layout-left.webp) |
| **Right Panel** | Docks on the right side, occupying 25% of Globe+ window width (resizable up to 50%). Globe+ resizes. | [`10-display-layout-right.webp`](../../assets/brand-kit/graphics/products/globeplus/10-display-layout-right.webp) |
| **Right Overlay** | Overlays the right side of Globe+ without resizing the underlying ERP interface. | [`11-display-layout-overlay.webp`](../../assets/brand-kit/graphics/products/globeplus/11-display-layout-overlay.webp) |
| **Bottom Right (Default)** | Floating widget in the bottom-right corner while Globe+ remains full screen. | [`12-display-layout-bottom-right.webp`](../../assets/brand-kit/graphics/products/globeplus/12-display-layout-bottom-right.webp) |
| **Floating Window** | Separate, movable, and resizable window with remembered dimensions. | [`13-display-layout-floating.webp`](../../assets/brand-kit/graphics/products/globeplus/13-display-layout-floating.webp) |

* **Application Focus Behavior**: Chat automatically hides when Globe+ loses focus and reopens cleanly upon return.
* **Closing Borderless Windows**: Close using the `✕` header icon or by typing `/close`, `/exit`, or `/quit`.

### B. LLM Settings & Debugging
* Enter GLM Systems username and password; click **Test connection** to verify reachable endpoint.
* **Show Tool Calls Debug Information**: Toggle switch to display underlying tool execution and payloads in real time for administration.  
  Visual: [`14-llm-settings-connection.webp`](../../assets/brand-kit/graphics/products/globeplus/14-llm-settings-connection.webp).

### C. License & Role 501 Verification
* Upload XML license file via **Settings > License**.
* Must verify status: `Current user has role 501: Yes`.  
  Visual: [`15-license-role-status.webp`](../../assets/brand-kit/graphics/products/globeplus/15-license-role-status.webp).

### D. Documents (PDF Output Methods)
* Configure PDF generation engine:
  - **Microsoft Print to PDF**: Windows built-in virtual printer.
  - **Crystal PDF Export**: Uses Crystal Reports PDF export functionality.  
  Visual: [`16-documents-pdf-export.webp`](../../assets/brand-kit/graphics/products/globeplus/16-documents-pdf-export.webp).

### E. About & Version Checks
* Displays current version and provides **Check for updates** button.  
  Visual: [`17-about-version-updates.webp`](../../assets/brand-kit/graphics/products/globeplus/17-about-version-updates.webp).

---

## 4. Multi-Company & Role 501 Security

### Multi-Company Selection
* Open **Settings > Change Company** or switch companies directly from the chat header dropdown when multiple databases are open.  
  Visuals: [`18-select-company-menu.webp`](../../assets/brand-kit/graphics/products/globeplus/18-select-company-menu.webp) and [`19-select-company-switch.webp`](../../assets/brand-kit/graphics/products/globeplus/19-select-company-switch.webp).

### Assigning Role 501 (`AIPlusAgentUser`)
* Administrators are auto-assigned. For standard users:
  1. In Globe+, navigate to `System > HR & Security > People` ([`20-assign-role-system-menu.webp`](../../assets/brand-kit/graphics/products/globeplus/20-assign-role-system-menu.webp)).
  2. Select the user card ([`21-assign-role-people-security.webp`](../../assets/brand-kit/graphics/products/globeplus/21-assign-role-people-security.webp)).
  3. Under **Rights**, assign the `AIPlusAgentUser` role (Role 501) and save ([`22-assign-role-role-501.webp`](../../assets/brand-kit/graphics/products/globeplus/22-assign-role-role-501.webp)).
* **Security Guardrail**: Flippy strictly respects Globe+ function rights. If a user asks for something outside their permissions, Flippy explains why without bypasses. Ask *"What rights do I have?"* for a readable summary ([`23-security-permissions-query.webp`](../../assets/brand-kit/graphics/products/globeplus/23-security-permissions-query.webp)).

---

## 5. Detailed Feature Breakdown & Visual Proof

### 1. Conversational Chat & Query
* Retrieves data into interactive, sortable tables.
* Dynamic column modification (*"Add the Authorized column"*).
* User-scoped filters (*"Show my sales orders"*).  
  Visuals:
  - Sales Orders table: [`24-query-sales-orders-table.webp`](../../assets/brand-kit/graphics/products/globeplus/24-query-sales-orders-table.webp)
  - Budget Scenario totals: [`25-query-budget-totals.webp`](../../assets/brand-kit/graphics/products/globeplus/25-query-budget-totals.webp)
  - International customer filter: [`26-query-filtered-orders.webp`](../../assets/brand-kit/graphics/products/globeplus/26-query-filtered-orders.webp)
  - Dynamic Authorized column: [`27-query-add-authorized-column.webp`](../../assets/brand-kit/graphics/products/globeplus/27-query-add-authorized-column.webp)

### 2. Transaction Creation with Confirmation Safeguards
* Supported transactions: Sales Orders, Purchase Orders, Quotations, RMAs, BOMs, Production Orders, Financial Entries.
* **Confirmation Gate**: Flippy outlines all parameters and requires user confirmation before committing to Globe+.  
  Visuals:
  - Create Sales Order prompt: [`28-transactions-create-sales-order.webp`](../../assets/brand-kit/graphics/products/globeplus/28-transactions-create-sales-order.webp)
  - Exact Globe+ Sales Order UI: [`29-transactions-globe-sales-order-ui.webp`](../../assets/brand-kit/graphics/products/globeplus/29-transactions-globe-sales-order-ui.webp)
  - Item Pricelist query: [`30-transactions-show-pricelist.webp`](../../assets/brand-kit/graphics/products/globeplus/30-transactions-show-pricelist.webp)
  - Unpaid Invoices query: [`31-transactions-unpaid-invoices.webp`](../../assets/brand-kit/graphics/products/globeplus/31-transactions-unpaid-invoices.webp)
  - Available BOMs query: [`32-transactions-available-boms.webp`](../../assets/brand-kit/graphics/products/globeplus/32-transactions-available-boms.webp)

### 3. Master Data Operations & Excel Bulk Engine
* **Single Records**: Create, update, or copy master data (Items, Projects, Accounts, Warehouses, Cost Centers, Journals).  
  Visuals: Prompt ([`33-masterdata-create-single-item.webp`](../../assets/brand-kit/graphics/products/globeplus/33-masterdata-create-single-item.webp)) and Confirmation ([`34-masterdata-confirm-creation.webp`](../../assets/brand-kit/graphics/products/globeplus/34-masterdata-confirm-creation.webp)).
* **Bulk Master Data via Excel**:
  - Drag and drop Excel file: [`35-masterdata-excel-upload.webp`](../../assets/brand-kit/graphics/products/globeplus/35-masterdata-excel-upload.webp)
  - Map Excel columns dialog: [`36-masterdata-excel-column-mapping.webp`](../../assets/brand-kit/graphics/products/globeplus/36-masterdata-excel-column-mapping.webp)
  - Created items summary: [`37-masterdata-excel-summary-created.webp`](../../assets/brand-kit/graphics/products/globeplus/37-masterdata-excel-summary-created.webp)
  - Update existing items: [`38-masterdata-excel-update-items.webp`](../../assets/brand-kit/graphics/products/globeplus/38-masterdata-excel-update-items.webp) and updated summary ([`39-masterdata-excel-summary-updated.webp`](../../assets/brand-kit/graphics/products/globeplus/39-masterdata-excel-summary-updated.webp))
  - Bulk recode items: [`40-masterdata-excel-recode-items.webp`](../../assets/brand-kit/graphics/products/globeplus/40-masterdata-excel-recode-items.webp) and recoded summary ([`41-masterdata-excel-summary-recoded.webp`](../../assets/brand-kit/graphics/products/globeplus/41-masterdata-excel-summary-recoded.webp))
  - Single item recode: [`42-masterdata-recode-single-item.webp`](../../assets/brand-kit/graphics/products/globeplus/42-masterdata-recode-single-item.webp)

### 4. Sales Invoice Lines Management
* Add or update lines on existing sales invoices with a single confirmation batch.  
  Visual: [`43-invoice-lines-add-change.webp`](../../assets/brand-kit/graphics/products/globeplus/43-invoice-lines-add-change.webp).

### 5. Dedicated Stock & Inventory Intelligence
* Real-time stock levels across warehouses: [`44-stock-current-levels.webp`](../../assets/brand-kit/graphics/products/globeplus/44-stock-current-levels.webp)
* Historical stock on specific date: [`45-stock-on-date.webp`](../../assets/brand-kit/graphics/products/globeplus/45-stock-on-date.webp)
* Movement analysis trends: [`46-stock-movement-analysis.webp`](../../assets/brand-kit/graphics/products/globeplus/46-stock-movement-analysis.webp)
* Depletion forecast (Stockout, At Risk, Healthy): [`47-stock-depletion-forecast.webp`](../../assets/brand-kit/graphics/products/globeplus/47-stock-depletion-forecast.webp)
* **Screen + Stock**: Asking *"Do I have enough stock for this order?"* reads active screen lines and matches warehouse balances.

### 6. Navigation & Screen Reading
* Fast-path menu jump: *"Go to Inventory"* ([`48-navigation-go-to-inventory.webp`](../../assets/brand-kit/graphics/products/globeplus/48-navigation-go-to-inventory.webp))
* Click linked order numbers in chat tables to open records directly in Globe+: [`49-navigation-click-record-link.webp`](../../assets/brand-kit/graphics/products/globeplus/49-navigation-click-record-link.webp)
* Active screen reading: Summarizes the record currently open: [`50-screen-reader-active-context.webp`](../../assets/brand-kit/graphics/products/globeplus/50-screen-reader-active-context.webp)

### 7. Automated Emailing via Review & Edit Tab
* Converts queried tables into formatted emails with automatic To, CC, Subject, Body, and attachments:
  - Command prompt: [`51-email-prompt-command.webp`](../../assets/brand-kit/graphics/products/globeplus/51-email-prompt-command.webp)
  - Embedded Review & Edit tab: [`52-email-review-edit-tab.webp`](../../assets/brand-kit/graphics/products/globeplus/52-email-review-edit-tab.webp)
  - Sent confirmation message: [`53-email-sent-confirmation.webp`](../../assets/brand-kit/graphics/products/globeplus/53-email-sent-confirmation.webp)
  - Delivered email sample: [`54-email-received-sample.webp`](../../assets/brand-kit/graphics/products/globeplus/54-email-received-sample.webp)

### 8. Excel Mapping Templates, Export & Copy
* Excel import dialog: [`55-excel-import-dialog.webp`](../../assets/brand-kit/graphics/products/globeplus/55-excel-import-dialog.webp)
* Saved mapping templates: [`56-excel-mapping-template.webp`](../../assets/brand-kit/graphics/products/globeplus/56-excel-mapping-template.webp)
* Copy to clipboard and Export to Excel buttons on tables: [`57-excel-export-and-copy.webp`](../../assets/brand-kit/graphics/products/globeplus/57-excel-export-and-copy.webp)
* Clean exported Excel workbook: [`58-excel-exported-spreadsheet.webp`](../../assets/brand-kit/graphics/products/globeplus/58-excel-exported-spreadsheet.webp)

### 9. Web Search & Regulatory Intelligence
* Queries Dutch VAT laws, exchange rates, and combines them with ERP data: [`59-web-search-vat-rates.webp`](../../assets/brand-kit/graphics/products/globeplus/59-web-search-vat-rates.webp).

### 10. Slash Commands & Fallback Assistance
* Inline autocomplete popup: [`60-slash-commands-suggestions.webp`](../../assets/brand-kit/graphics/products/globeplus/60-slash-commands-suggestions.webp)
* Switching positions via `/position`: [`61-slash-commands-position.webp`](../../assets/brand-kit/graphics/products/globeplus/61-slash-commands-position.webp)
* Autocomplete for budget scenarios: [`62-slash-commands-budget-scenario.webp`](../../assets/brand-kit/graphics/products/globeplus/62-slash-commands-budget-scenario.webp)
* Fallback suggestions when data is not found: [`63-fallback-no-data-suggestions.webp`](../../assets/brand-kit/graphics/products/globeplus/63-fallback-no-data-suggestions.webp)
* "What can you do?" capability list: [`64-help-what-can-you-do.webp`](../../assets/brand-kit/graphics/products/globeplus/64-help-what-can-you-do.webp)
* Exact product documentation links: [`65-help-exact-documentation-links.webp`](../../assets/brand-kit/graphics/products/globeplus/65-help-exact-documentation-links.webp)
* Exact website search results: [`66-help-exact-website-result.webp`](../../assets/brand-kit/graphics/products/globeplus/66-help-exact-website-result.webp)
* Quick reference card: [`67-help-quick-reference-card.webp`](../../assets/brand-kit/graphics/products/globeplus/67-help-quick-reference-card.webp)
