# Benchmark Task Status

Tracks all benchmark tasks. Update when adding new tasks or running evaluations.

**Status values:** `WIP` — oracle or eval incomplete | `Done` — oracle passes, eval recorded

Last eval: 2026-04-16 | Oracle: 28/28 (100%) | Browser-Use: 11/28 (39%)

## Summary

| # | Task | Status | Oracle | Browser-Use | F1 |
|---|------|--------|--------|-------------|-----|
| 1 | account.complete_customer_tax_id_then_post | Done | PASS | FAIL | 0.0 |
| 2 | account.create_credit_note_and_reconcile | Done | PASS | PASS | 1.0 |
| 3 | account.partial_refund_service_credit_note | Done | PASS | FAIL | 0.0 |
| 4 | account.repair_and_post_invoice | Done | PASS | FAIL | 0.0 |
| 5 | account.switch_negative_invoice_repair_credit_note | Done | PASS | FAIL | 0.0 |
| 6 | account.switch_negative_invoice_to_credit_note | Done | PASS | FAIL | 0.0 |
| 7 | calendar.edit_single_recurrence_occurrence | Done | PASS | FAIL | 0.0 |
| 8 | calendar.make_single_occurrence_all_day | Done | PASS | FAIL | 0.0 |
| 9 | calendar.schedule_recurring_steering_sync | Done | PASS | PASS | 1.0 |
| 10 | crm.merge_duplicate_opportunities_cleanup | Done | PASS | PASS | 1.0 |
| 11 | crm.qualify_lead_and_prepare_quote | Done | PASS | PASS | 1.0 |
| 12 | hr_recruitment.new_applicant_schedule_interview | Done | PASS | FAIL | 0.0 |
| 13 | project.configure_launch_milestones | Done | PASS | FAIL | 0.71 |
| 14 | project.read_update_status | Done | PASS | PASS | 1.0 |
| 15 | purchase.cancel_reissue_wrong_vendor | Done | PASS | FAIL | 0.33 |
| 16 | purchase_stock.receive_and_complete_backorder | Done | PASS | PASS | 1.0 |
| 17 | purchase_stock.receive_partial_without_backorder | Done | PASS | PASS | 1.0 |
| 18 | sale.cancel_reissue_wrong_customer | Done | PASS | FAIL | 0.0 |
| 19 | sale.confirm_correct_order | Done | PASS | PASS | 1.0 |
| 20 | sale.create_quotation_and_send_email | Done | PASS | FAIL | 1.0 |
| 21 | sale.exact_total_quotation | Done | PASS | FAIL | 0.5 |
| 22 | sale.find_highest_duplicate | Done | PASS | FAIL | 0.0 |
| 23 | sale.revise_target_quote_lines | Done | PASS | FAIL | 0.0 |
| 24 | sale_project.confirm_quote_and_update_generated_project | Done | PASS | PASS | 1.0 |
| 25 | sale_project.confirm_rollout_quote_update_generated_project | Done | PASS | PASS | 1.0 |
| 26 | website.edit_careers_spotlight | Done | PASS | PASS | 1.0 |
| 27 | website_hr_recruitment.apply_and_triage_ops_role | Done | PASS | PASS | 1.0 |
| 28 | website_hr_recruitment.apply_guru_job | Done | PASS | PASS | 1.0 |

---

## account.complete_customer_tax_id_then_post

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Invoices, Contacts |
| **Workflow** | Find draft invoice by origin `VAT-302` among two similar distractors. Read VAT value from Terms and Conditions field, navigate to the customer record, set Tax ID, return via breadcrumb, set Customer Reference, and post. |
| **Capability tested** | Cross-record round-trip (invoice → customer → back via breadcrumb); reading a value embedded in a non-obvious text field; distractor record avoidance. |

---

## account.create_credit_note_and_reconcile

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Accounting — Invoices |
| **Workflow** | Open posted invoice `CN-TARGET-01`. Create a partial credit note via wizard (exact reason text + specific date). Edit the generated draft: reduce quantity from 18 to 10. Post. |
| **Capability tested** | Multi-field wizard interaction (reason + date); post-wizard editing of a generated draft; similar customer names as distractors (Lakeview Partners vs Lakeview Projects). |

---

## account.partial_refund_service_credit_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Invoices |
| **Workflow** | Open invoice `CN-SERVICE-01`. Create credit note via wizard (reason + date). Edit draft: delete the Onsite Training line, set Warehouse Audit quantity to 1. Post. |
| **Capability tested** | Post-wizard line deletion and quantity adjustment; distractor invoice with similar customer name. |

---

## account.repair_and_post_invoice

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Invoices, Products |
| **Workflow** | Find draft invoice `APR-OPS` among two Beacon Design invoices. For each product, open the product form and read Sales Description to get correct Qty and Discount. Return to invoice, fix all lines, set Customer Reference, post. |
| **Capability tested** | Cross-module data lookup (invoice → product form → back); reading structured data from a non-standard field; multi-line correction before posting. |

---

## account.switch_negative_invoice_repair_credit_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Invoices, Products |
| **Workflow** | Find draft invoice `RET-508` (negative total). Use Action menu to convert to credit note type. Look up correct Qty/Discount from product Sales Description fields. Fix all lines, set Customer Reference, post. |
| **Capability tested** | Action-menu document type conversion combined with cross-module line repair; distractor invoice for same customer. |

---

## account.switch_negative_invoice_to_credit_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Invoices |
| **Workflow** | Find draft invoice `RET-204` (negative total). Use Action menu to convert to credit note type. Set Customer Reference. Post. |
| **Capability tested** | Action-menu document type conversion (simpler variant of `switch_negative_invoice_repair_credit_note` — no line editing). |

---

## calendar.edit_single_recurrence_occurrence

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Navigate to week of April 27. Click the specific "Ops Standup" occurrence. Change its Location. In the recurrence save dialog, choose "This Event" (not the series). |
| **Capability tested** | Calendar week navigation; recurrence split dialog with non-default radio choice; avoiding accidental modification of the whole series. |

---

## calendar.make_single_occurrence_all_day

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Navigate to May 19 occurrence of a weekly recurring event. Enable All Day, change Location, save with "This Event" in the recurrence dialog. |
| **Capability tested** | Recurrence "This Event" dialog (same as `edit_single_recurrence_occurrence`) plus an All Day boolean toggle on a single occurrence. |

---

## calendar.schedule_recurring_steering_sync

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Create a new recurring weekly meeting (title, times, specific attendees, location, description, ends after 3 occurrences). Then edit only the second occurrence to change its location. |
| **Capability tested** | Full recurring event creation with all fields; attendee management (invite one, exclude another); second-occurrence-only edit via recurrence dialog. |

---

## crm.merge_duplicate_opportunities_cleanup

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | CRM |
| **Workflow** | Switch to list view, select exactly two duplicate opportunities by contact email, merge via Action menu. Set stage and Expected Revenue on the merged record. Schedule a Call activity (summary + due date). |
| **Capability tested** | Multi-record selection; Action-menu merge; post-merge field editing; activity scheduling. |

---

## crm.qualify_lead_and_prepare_quote

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | CRM, Sales |
| **Workflow** | Select correct lead by email (not name). Convert to opportunity, link to existing customer. Set stage/revenue/tag. Schedule Call activity. Create a quotation from the opportunity; set Customer Reference and Expiration. Leave as draft. |
| **Capability tested** | Lead-to-opportunity conversion dialog; cross-module CRM → Sales navigation; multi-field setup across both modules. |

---

## hr_recruitment.new_applicant_schedule_interview

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Recruitment |
| **Workflow** | Open a specific job position, create a new applicant with exact details (name, email, phone, recruiter, salary expectation in Details tab). Schedule a Call activity with specific summary, due date, and assignee. |
| **Capability tested** | Recruitment kanban navigation; multi-tab form (Details tab for salary); activity scheduling widget (type badge, date, assignee). |

---

## project.configure_launch_milestones

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.71 |
| **Odoo modules** | Project |
| **Workflow** | Enable Milestones in project Settings tab. Create two milestones with deadlines. Create three tasks each assigned to a milestone and placed in specific stages. Write a summary in the project Description tab. |
| **Capability tested** | Feature enablement via settings; milestone CRUD; task creation with stage and milestone assignment; multi-surface setup within one module. |

---

## project.read_update_status

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Project |
| **Workflow** | Remove the default "Open" filter to reveal all tasks including Done. Count total tasks and Done-stage tasks. Open project settings and write "X of Y tasks complete" in the Description field. |
| **Capability tested** | Filter removal to reveal hidden records; read-then-write reasoning (count tasks, compose result string); project settings navigation. |

---

## purchase.cancel_reissue_wrong_vendor

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.33 |
| **Odoo modules** | Purchase |
| **Workflow** | Cancel a confirmed PO sent to the wrong vendor. Create a new PO for the correct vendor with identical product lines (same products, quantities, prices). Confirm the new PO. |
| **Capability tested** | Confirmed-PO cancellation flow; re-creation with exact line replication; vendor correction. Purchase counterpart of `sale.cancel_reissue_wrong_customer`. |

---

## purchase_stock.receive_and_complete_backorder

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase, Inventory |
| **Workflow** | Open PO, receive a partial shipment with specific done quantities, choose "Create Backorder" in the validation dialog. Then open the auto-created backorder receipt and receive the remaining quantities. |
| **Capability tested** | Partial receipt workflow; "Create Backorder" dialog choice; finding and completing the backorder; cross-module PO → Inventory navigation. |

---

## purchase_stock.receive_partial_without_backorder

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase, Inventory |
| **Workflow** | Receive only part of a PO's quantities. In the validation dialog choose "No Backorder" to close remaining demand permanently. |
| **Capability tested** | "No Backorder" dialog choice (contrasts with `receive_and_complete_backorder`); understanding that the short-shipment is intentional and final. |

---

## sale.cancel_reissue_wrong_customer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales |
| **Workflow** | Cancel a confirmed SO for the wrong customer. Create a new quotation for the correct customer with identical product lines. Set Customer Reference. Confirm. |
| **Capability tested** | Confirmed-SO cancellation (ConfirmationDialog required); re-creation with exact line replication; customer correction. Sales counterpart of `purchase.cancel_reissue_wrong_vendor`. |

---

## sale.confirm_correct_order

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales |
| **Workflow** | Among four draft quotations for the same customer, open each to inspect order lines and confirm only the one containing both "Standing Desk" and "Office Chair". |
| **Capability tested** | Multi-record inspection before acting; content-based record identification (line items not visible in list view); avoiding confirmation of distractor quotations. |

---

## sale.create_quotation_and_send_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 1.0 (state match) |
| **Odoo modules** | Sales, Email |
| **Workflow** | Create a new quotation from scratch (customer, two product lines with exact qty/price, expiration date). Send via "Send by Email" compose wizard. Final status must be "Quotation Sent". |
| **Capability tested** | Full quotation creation; email compose wizard interaction. Note: Browser-Use FAIL is a side-effect check failure (state matches but email delivery check fails). |

---

## sale.exact_total_quotation

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.5 |
| **Odoo modules** | Sales, Products |
| **Workflow** | For each product on a draft quotation, open the product form and read the Internal Notes field to find the correct unit price. Return to the quotation and fix each line's price. Save without confirming. |
| **Capability tested** | Cross-module data lookup (quotation → product Internal Notes → back); reading a value from a non-standard field; multi-line price correction. |

---

## sale.find_highest_duplicate

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales |
| **Workflow** | Remove "My Quotations" filter. Identify the customer with the highest total value of confirmed Sales Orders. Among that customer's draft quotations, duplicate the one with the smallest untaxed amount. |
| **Capability tested** | Aggregation and comparison across records (sum confirmed orders by customer); two-step filter reasoning; Duplicate action on the correct target. |

---

## sale.revise_target_quote_lines

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales, Products |
| **Workflow** | Find quotation `OPS-042` among several Aurora Interiors quotations. For each product, look up Sales Description to get the line description text and discount. Apply both to every line. Set Payment Terms. Save. |
| **Capability tested** | Cross-module data lookup (quotation lines → product Sales Description); per-line discount and description override; Payment Terms selection. |

---

## sale_project.confirm_quote_and_update_generated_project

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Project |
| **Workflow** | Confirm quotation `SERV-PROJ-17`. Open the auto-generated project. Rename two tasks and move them to specific stages. Write description text. Return to SO and update Customer Reference. |
| **Capability tested** | Cross-module round-trip (Sales → auto-generated Project → back to Sales); task rename + stage change; multi-step navigation across two modules. |

---

## sale_project.confirm_rollout_quote_update_generated_project

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Project |
| **Workflow** | Confirm quotation `ROLL-PROJ-31`. Open the auto-generated project. Rename two tasks and move them to specific stages. Write description text. Return to SO and update Customer Reference. |
| **Capability tested** | Same cross-module round-trip pattern as `confirm_quote_and_update_generated_project` with different project/task names — tests robustness across similar rollout workflows. |

---

## website.edit_careers_spotlight

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Website (inline editor) |
| **Workflow** | In the website editor, edit only the middle card of a three-card row (title, body text, button label). Use Site > Properties to set the page title and URL slug. Save. |
| **Capability tested** | Website inline editor interaction (iframe content); positional card targeting (middle of three); page properties dialog. |

---

## website_hr_recruitment.apply_and_triage_ops_role

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Website, Recruitment |
| **Workflow** | Find a job by description text ("pager rotation"), add two custom form fields via website editor. Then apply to a different role ("renewals") filling all fields including custom ones. Triage the applicant in the Recruitment backend (stage + evaluation). |
| **Capability tested** | Content-based job identification; website form editor (adding custom fields); public job application with custom fields; full public-to-backend round-trip. |

---

## website_hr_recruitment.apply_guru_job

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Website, Recruitment |
| **Workflow** | Navigate to public Jobs page, find the "Guru" position, fill out the application form with exact personal details, and submit. |
| **Capability tested** | Public website navigation; job application form submission. Simpler variant of `apply_and_triage_ops_role` — no backend triage, no custom fields. |

---

## Adding New Tasks

Before creating a new task, read all entries above and check for overlap on three dimensions:

| Dimension | Question |
|---|---|
| **Odoo modules** | Does the new task use the same module(s)? |
| **Workflow** | Is the agent doing the same kind of action (cancel+reissue, cross-module lookup, wizard interaction, etc.)? |
| **Capability tested** | Does the failure pattern overlap with an existing task? |

**A new task must be distinct in at least two of the three dimensions.**

When adding a new task, append a form block (same format as above) with `Status: WIP` and dashes for test results, then commit and push immediately — this is the team's duplicate-prevention signal.
