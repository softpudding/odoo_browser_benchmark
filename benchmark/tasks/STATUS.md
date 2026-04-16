# Benchmark Task Status

Tracks all benchmark tasks. Update when adding new tasks or running evaluations.

**Status:** `WIP` (oracle or eval incomplete) | `Done` (oracle passes, eval recorded)

Last eval: 2026-04-16 | Oracle: 28/28 (100%) | Browser-Use: 11/28 (39%)

---

## Tasks

### account.complete_customer_tax_id_then_post
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Accounting (Invoicing)

**What the agent must do:** Open a draft invoice identified by origin `VAT-302` (two similar invoices exist as distractors). Read a VAT value embedded in the invoice's Terms and Conditions field, navigate to the customer record, set the Tax ID field, return to the invoice via breadcrumb, set Customer Reference, and post the invoice.

**Capability tested:** Cross-record round-trip (invoice → customer form → back via breadcrumb); reading a value embedded in a non-obvious text field; distractor record selection; multi-field edit before posting.

---

### account.create_credit_note_and_reconcile
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Accounting (Invoicing)

**What the agent must do:** Open a specific posted invoice (`CN-TARGET-01`), create a partial credit note via the Credit Note wizard, fill in exact reason text and a specific date, then edit the draft credit note's quantity from 18 to 10 before posting.

**Capability tested:** Multi-field wizard interaction (reason + date); post-wizard editing of a generated draft; distinguishing two similar customer names (Lakeview Partners vs Lakeview Projects).

---

### account.partial_refund_service_credit_note
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Accounting (Invoicing)

**What the agent must do:** Open invoice `CN-SERVICE-01`, create a credit note via wizard (reason + date), then edit the draft: delete the Onsite Training line and set Warehouse Audit quantity to 1, then post.

**Capability tested:** Post-wizard line-level editing (deleting a line, adjusting quantity); distractor invoice with similar customer name; precise partial-refund workflow.

---

### account.repair_and_post_invoice
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Accounting (Invoicing), Products

**What the agent must do:** Find draft invoice `APR-OPS` among two Beacon Design invoices. For each product, navigate to the product form and read the Sales Description field to get the correct Qty and Discount values. Return to the invoice, fix all lines, set Customer Reference, and post.

**Capability tested:** Cross-module data lookup (invoice lines → product forms → back to invoice); reading structured data from a non-standard field; multi-line correction before posting.

---

### account.switch_negative_invoice_repair_credit_note
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Accounting (Invoicing), Products

**What the agent must do:** Find draft invoice `RET-508` (negative total), use the Action menu to convert it to a credit note type, then look up correct Qty/Discount for each line from product Sales Description fields, fix all lines, set Customer Reference, and post.

**Capability tested:** Action-menu document type conversion; cross-module data lookup; combining document-type switch with line-level repair; distractor invoice for same customer.

---

### account.switch_negative_invoice_to_credit_note
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Accounting (Invoicing)

**What the agent must do:** Find draft invoice `RET-204` (negative total), use the Action menu to convert it to a credit note type, set Customer Reference, and post.

**Capability tested:** Action-menu document type conversion without any line editing; simpler than `repair_credit_note` variant but tests the same Action menu path.

---

### calendar.edit_single_recurrence_occurrence
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Calendar

**What the agent must do:** Navigate to week of April 27 in the calendar, click the specific Ops Standup occurrence, change its Location, and in the recurrence save dialog choose "This Event" (not "This and Following" or "All Events").

**Capability tested:** Calendar week navigation; recurrence split dialog with non-default radio choice ("This Event"); not inadvertently modifying the whole series.

---

### calendar.make_single_occurrence_all_day
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Calendar

**What the agent must do:** Navigate to the May 19 occurrence of a weekly recurring event, enable All Day, change Location, and save only "This Event" in the recurrence dialog.

**Capability tested:** Combining field edits (All Day toggle + location) on a single recurrence; recurrence save dialog with "This Event" choice; similar to `edit_single_recurrence_occurrence` but adds an All Day boolean toggle.

---

### calendar.schedule_recurring_steering_sync
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Calendar

**What the agent must do:** Create a new recurring weekly meeting (title, times, attendees, location, description, recurrence ends after 3 occurrences), then edit only the second occurrence to change its location.

**Capability tested:** Full recurring event creation with all fields; then a second-occurrence-only edit (recurrence dialog again); attendee management.

---

### crm.merge_duplicate_opportunities_cleanup
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** CRM

**What the agent must do:** Switch to list view, select exactly two duplicate opportunities for the same contact, merge via Action menu, then set stage, expected revenue, and schedule a Call activity on the merged record.

**Capability tested:** Multi-record selection and Action-menu merge; post-merge field editing; activity scheduling with specific type/date/summary.

---

### crm.qualify_lead_and_prepare_quote
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** CRM, Sales

**What the agent must do:** Select correct lead by email (not by name), convert to opportunity linking to existing customer, set stage/revenue/tag, schedule a Call activity, then create a quotation from the opportunity and set Customer Reference and Expiration on it.

**Capability tested:** Lead-to-opportunity conversion dialog; linking to existing customer; cross-module transition (CRM → Sales quotation); multi-field setup across both modules.

---

### hr_recruitment.new_applicant_schedule_interview
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Recruitment

**What the agent must do:** Navigate into a specific job position, create a new applicant with exact personal details and salary expectation, then schedule a Call activity with specific summary, due date, and assigned user.

**Capability tested:** Recruitment kanban navigation; new applicant form with Details tab fields; activity scheduling widget (type badge selection, date, assignee).

---

### project.configure_launch_milestones
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.71

**Odoo modules:** Project

**What the agent must do:** Enable Milestones on a project via Settings tab, create two named milestones with deadlines, create three tasks each assigned to a milestone and placed in specific stages, then write a summary in the project Description tab.

**Capability tested:** Feature enablement via project settings; milestone CRUD; task creation with stage assignment; project description editing; multi-step setup across multiple UI surfaces.

---

### project.read_update_status
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Project

**What the agent must do:** Remove the default "Open" filter to see all tasks, count total tasks and Done-stage tasks, then open project settings and write the count in the Description field as "X of Y tasks complete".

**Capability tested:** Filter removal to reveal hidden records; counting/reading state across kanban/list; writing computed text into a description field; read-then-write reasoning.

---

### purchase.cancel_reissue_wrong_vendor
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.33

**Odoo modules:** Purchase

**What the agent must do:** Cancel a confirmed PO (wrong vendor), then create a new PO for the correct vendor with identical product lines (same products, quantities, unit prices) and confirm it.

**Capability tested:** Confirmed-PO cancellation flow; re-creation with exact line replication; vendor correction workflow. Purchase counterpart of `sale.cancel_reissue_wrong_customer`.

---

### purchase_stock.receive_and_complete_backorder
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Purchase, Inventory (Stock)

**What the agent must do:** Open a PO, receive a partial shipment (specific done quantities), choose "Create Backorder" in the validation dialog, then open the backorder receipt and receive the remaining quantities.

**Capability tested:** Partial receipt workflow; backorder creation dialog (non-default action); finding and completing the auto-created backorder receipt; cross-module PO → Inventory navigation.

---

### purchase_stock.receive_partial_without_backorder
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Purchase, Inventory (Stock)

**What the agent must do:** Receive only part of a PO's quantities and in the validation dialog choose "No Backorder" to deliberately close the remaining demand.

**Capability tested:** Partial receipt workflow; "No Backorder" choice in the validation dialog (contrasts with `receive_and_complete_backorder`); understanding that short-shipment is intentional and final.

---

### sale.cancel_reissue_wrong_customer
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Sales

**What the agent must do:** Cancel a confirmed SO (wrong customer), create a new quotation for the correct customer with identical product lines, set Customer Reference, and confirm.

**Capability tested:** Confirmed-SO cancellation flow (requires ConfirmationDialog); re-creation with exact line replication; customer correction workflow. Sales counterpart of `purchase.cancel_reissue_wrong_vendor`.

---

### sale.confirm_correct_order
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Sales

**What the agent must do:** Among four draft quotations for the same customer, open each to inspect order lines and confirm only the one that contains both "Standing Desk" and "Office Chair".

**Capability tested:** Multi-record inspection before acting; avoiding confirmation of distractor quotations; content-based record identification (line items not visible in list view).

---

### sale.create_quotation_and_send_email
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 1.0

**Odoo modules:** Sales (Email compose wizard)

**What the agent must do:** Create a new quotation from scratch (customer, two product lines with exact qty/price, expiration date), then send it via the "Send by Email" compose wizard.

**Capability tested:** Full quotation creation; email compose wizard interaction (Send button); result status should be "Quotation Sent". Note: F1=1.0 (state matches) but browser-use FAIL due to side-effect check on email delivery.

---

### sale.exact_total_quotation
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.5

**Odoo modules:** Sales, Products

**What the agent must do:** For each product on a draft quotation, navigate to the product form and read the Internal Notes field to find the correct unit price, then return and update each line's price. Save without confirming.

**Capability tested:** Cross-module data lookup (quotation → product form → back); reading a value from Internal Notes (not a standard display field); multi-line price correction; similar to `repair_and_post_invoice` but in Sales and without posting.

---

### sale.find_highest_duplicate
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Sales

**What the agent must do:** Remove "My Quotations" filter, identify the customer with the highest total confirmed Sales Orders, then among that customer's draft quotations duplicate the one with the smallest untaxed amount.

**Capability tested:** Aggregation/comparison across records (sum by customer); two-step filter reasoning (confirmed orders first, then draft quotations); using the Duplicate action on the correct record.

---

### sale.revise_target_quote_lines
**Status:** Done | Oracle: PASS | Browser-Use: FAIL | F1: 0.0

**Odoo modules:** Sales, Products

**What the agent must do:** Find quotation `OPS-042` among several Aurora Interiors quotations, look up each product's Sales Description to get line description text and discount, apply both to every line, set Payment Terms, and save.

**Capability tested:** Cross-module data lookup (quotation lines → product Sales Description); applying per-line discounts and description overrides; multi-field update; Payment Terms selection.

---

### sale_project.confirm_quote_and_update_generated_project
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Sales, Project

**What the agent must do:** Confirm quotation `SERV-PROJ-17`, open the auto-generated project, rename two tasks and move them to specific stages, write a description, then return to the SO and update Customer Reference.

**Capability tested:** Cross-module round-trip (Sales → auto-generated Project → back to Sales); task rename + stage change; description writing; round-trip navigation between two modules.

---

### sale_project.confirm_rollout_quote_update_generated_project
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Sales, Project

**What the agent must do:** Confirm quotation `ROLL-PROJ-31`, open the auto-generated project, rename two tasks and move them to specific stages, write a description, then return to SO and update Customer Reference.

**Capability tested:** Same cross-module round-trip pattern as `confirm_quote_and_update_generated_project` but with different project/task names — tests robustness across similar rollout workflow.

---

### website.edit_careers_spotlight
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Website (inline editor)

**What the agent must do:** In the website editor, edit only the middle card of a three-card row (title, body text, button label), then use Site > Properties to set the page title and URL slug, and save.

**Capability tested:** Website inline editor interaction (iframe content editing); card targeting by position (middle, not first or third); page properties dialog; save workflow.

---

### website_hr_recruitment.apply_and_triage_ops_role
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Website, Recruitment

**What the agent must do:** Find a job by description text (mentions "pager rotation"), add two custom form fields to its application page via website editor, then apply to a different role (mentions "renewals") filling all fields including the new custom ones, and finally triage the applicant in the Recruitment backend.

**Capability tested:** Content-based job identification (reading descriptions, not titles); website form editor (adding custom fields); public job application with custom fields; backend triage (stage + evaluation update). Full public-to-backend round-trip.

---

### website_hr_recruitment.apply_guru_job
**Status:** Done | Oracle: PASS | Browser-Use: PASS | F1: 1.0

**Odoo modules:** Website, Recruitment

**What the agent must do:** Navigate to the public Jobs page, find the "Guru" position, fill out the application form with exact personal details, and submit.

**Capability tested:** Public website navigation; job application form submission with all required fields; simpler than `apply_and_triage_ops_role` (no backend triage, no custom fields).

---

## Adding New Tasks

Before creating a new task, check this file:
1. Does any existing task already use the same Odoo module + workflow combination?
2. Does the "What the agent must do" description overlap significantly with an existing task?
3. Does the "Capability tested" row name the same failure pattern?

Tasks must be **distinct** in at least two of: Odoo module, workflow type, and capability tested.
See `skills/create-benchmark-task.md` for the full creation guide.
