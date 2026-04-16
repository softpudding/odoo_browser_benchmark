# Benchmark Task Status

Tracks all benchmark tasks. Update when adding new tasks or running evaluations.

**Status values:** `WIP` — oracle or eval incomplete | `Done` — oracle passes, eval recorded

Last eval: 2026-04-16 | Oracle: 48/48 (100%) | Browser-Use: 23/48 (48%) | New WIP: 20 (15 medium + 5 easy)

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
| 29 | stock.adjust_inventory_quantities | Done | PASS | FAIL | 0.0 |
| 30 | hr.create_employee_complete_profile | Done | PASS | FAIL | 0.0 |
| 31 | purchase.new_rfq_three_lines_date | Done | PASS | FAIL | 0.0 |
| 32 | project.complete_task_log_note | Done | PASS | FAIL | 0.0 |
| 33 | contacts.create_company_with_contacts | Done | PASS | FAIL | 0.0 |
| 34 | sale.change_validity_date [easy] | Done | PASS | PASS | 1.0 |
| 35 | account.register_payment_defaults [easy] | Done | PASS | PASS | 1.0 |
| 36 | crm.move_opportunity_stage [easy] | Done | PASS | PASS | 1.0 |
| 37 | purchase.reset_draft_edit_reconfirm [easy] | Done | PASS | PASS | 1.0 |
| 38 | project.post_chatter_message [easy] | Done | PASS | PASS | 1.0 |
| 39 | sale.set_payment_terms_confirm [medium] | WIP | — | — | — |
| 40 | account.create_vendor_bill_confirm [medium] | WIP | — | — | — |
| 41 | crm.edit_opportunity_schedule_call [medium] | WIP | — | — | — |
| 42 | hr.update_work_information [medium] | WIP | — | — | — |
| 43 | project.create_task_assign_stage [medium] | WIP | — | — | — |
| 44 | stock.confirm_and_validate_receipt [medium] | WIP | — | — | — |
| 45 | purchase.update_rfq_add_line_confirm [medium] | WIP | — | — | — |
| 46 | contacts.update_address_add_tag [medium] | WIP | — | — | — |
| 47 | calendar.create_single_event [medium] | WIP | — | — | — |
| 48 | hr_recruitment.advance_applicant_stage [medium] | WIP | — | — | — |
| 49 | account.send_invoice_with_extra_recipient [hard] | Done | PASS | PASS | 1.0 |
| 50 | crm.batch_mark_lost_with_reason [hard] | Done | PASS | FAIL | 1.0 |
| 51 | hr_recruitment.refuse_duplicate_applications [hard] | Done | PASS | FAIL | 0.0 |
| 52 | purchase_stock.return_partial_receipt_to_vendor [hard] | Done | PASS | FAIL | 0.0 |
| 53 | sale.confirm_order_within_credit_limit [hard] | Done | PASS | PASS | 1.0 |
| 54 | sale.create_invoice_adjust_quantity_post [medium] | Done | PASS | PASS | 1.0 |
| 55 | purchase.confirm_order_send_po_message [medium] | Done | PASS | FAIL | 0.0 |
| 56 | project.update_task_assign_deadline_activity [medium] | Done | PASS | FAIL | 0.0 |
| 57 | calendar.reschedule_event_update_location_attendee [medium] | Done | PASS | PASS | 1.0 |
| 58 | contacts.create_linked_contact_add_tag [medium] | Done | PASS | PASS | 1.0 |
| 59 | inventory.scrap_product [easy] | WIP | — | — | — |
| 60 | hr.schedule_employee_activity [easy] | WIP | — | — | — |
| 61 | sale.add_note_to_quotation [easy] | WIP | — | — | — |
| 62 | crm.set_priority_on_opportunity [easy] | WIP | — | — | — |
| 63 | project.set_task_deadline [easy] | WIP | — | — | — |
| 64 | account.update_vendor_bill_reference_post [medium] | WIP | — | — | — |
| 65 | contacts.create_company_with_supplier_tag [medium] | WIP | — | — | — |
| 66 | crm.create_opportunity_tag_schedule_call [medium] | WIP | — | — | — |
| 67 | project.duplicate_task_assign_deadline [medium] | WIP | — | — | — |
| 68 | purchase.set_order_deadline_schedule_call_confirm [medium] | WIP | — | — | — |

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

## stock.adjust_inventory_quantities

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Navigate to Operations > Physical Inventory. Set on-hand quantities for 3 specific products (Steel Bracket 12", Copper Wire 100m, Safety Harness XL) to exact target values while leaving 2 distractor products unchanged. Click Apply All. |
| **Capability tested** | Inline tree editing — agent must click into quantity cells in a list view and type values; fails by entering wrong row or not interacting with inline-editable cells correctly. |

---

## hr.create_employee_complete_profile

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Create a new employee "Jordan Mercer" filling fields across three areas: main form (name, job position, work phone), Work Information tab (work location, working hours), and Private Information tab (certificate level, marital status). |
| **Capability tested** | Create-from-scratch with multi-tab form — agent typically fills only the main form and saves without visiting Work Information or Private Information tabs. |

---

## purchase.new_rfq_three_lines_date

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Purchase |
| **Workflow** | Create a new RFQ for vendor Meridian Supply Co with exactly 3 product lines (Rubber Gasket 200×$1.50, Stainless Bolt M8 500×$0.75, Hex Nut M8 500×$0.40) and set Order Deadline to May 30, 2026 via the date picker. Confirm. |
| **Capability tested** | Create-from-scratch with exact lines + date picker manipulation — agent leaves a phantom empty 4th line after entering the 3rd product, and/or sets wrong date via date picker widget. |

---

## project.complete_task_log_note

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Project |
| **Workflow** | In project "Omega Platform Launch", find task "Write API integration spec" in In Progress stage. Move it to Done stage. Then post an internal log note (not a regular message) with exact text via the chatter. |
| **Capability tested** | Chatter "Log note" vs "Send message" distinction (unexploited pattern) — agent uses wrong chatter button or skips the note step after moving the stage. |

---

## contacts.create_company_with_contacts

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Contacts |
| **Workflow** | Create company "Vantage Industrial Group" with full address details. Then create two individual contacts (Patricia Drum — Procurement Manager, Steven Okafor — Logistics Coordinator) both linked to the company with exact emails and mobile numbers. |
| **Capability tested** | Multi-record create sequence with company linkage — agent correctly creates the company and first contact, but leaves missing or incorrect fields on the second contact, or fails to link one contact to the parent company. |

---

## sale.change_validity_date

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open draft quotation BENCH-VALID-01 for Lakeview Partners. Change the Expiration date to May 15, 2026. Click Save. |
| **Capability tested** | Simple field edit + save — single date field change on a clearly identified draft quotation via date picker. |

---

## account.register_payment_defaults

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Accounting — Invoices |
| **Workflow** | Open posted invoice BENCH-PAY-01 for Lakeview Partners. Click Pay button. Accept all defaults in the Register Payment wizard. Click Create Payment. Verify invoice shows "Paid" status. |
| **Capability tested** | Accept-defaults wizard — open payment registration dialog, click Create Payment without changing any fields, verify payment registered. |

---

## crm.move_opportunity_stage

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | CRM — Pipeline |
| **Workflow** | Find the "Acme Corporation" opportunity in the CRM pipeline. Move it from the "New" stage to the "Qualified" stage. |
| **Capability tested** | Kanban stage change — direct drag or selector change on a single clearly identified opportunity. |

---

## purchase.reset_draft_edit_reconfirm

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Purchase — Orders |
| **Workflow** | Open confirmed PO BENCH-PO-RESET for Meridian Supply Co. Reset to Draft. Change Terms & Conditions to "Updated via browser". Click Confirm Order. |
| **Capability tested** | Reset-to-draft → edit → re-confirm — linear 3-step sequence with single text field change. |

---

## project.post_chatter_message

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Project — Tasks |
| **Workflow** | Open task "Write API integration spec" in project "Omega Platform Launch". Post a message in the chatter with exact text: "Backend team has reviewed the spec. Moving forward with implementation." |
| **Capability tested** | Chatter message posting — type text in the chatter composer and click Send. Simple send message (not log note distinction). |

---

## sale.set_payment_terms_confirm

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Find draft quotation BENCH-PMT-01 for Azure Interior. Set Payment Terms to "30 Net Days", change Desk Organizer line quantity from 5 to 12, update Customer Reference to "AZ-2026-Q2", and click Confirm. |
| **Capability tested** | Multi-field form edit (relational field + inline line qty + text field) followed by confirmation action. No cross-module hop, but requires correct interaction with payment terms dropdown and order line editing. |

---

## account.create_vendor_bill_confirm

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Accounting — Vendor Bills |
| **Workflow** | Navigate to Vendor Bills, create new bill for Meridian Supply Co with 2 product lines (Cable Tray ×100 @ $12.50, Junction Box ×50 @ $8.00), set Bill Date to May 1, 2026, set reference MSC-INV-4421, and Confirm. |
| **Capability tested** | Create-from-scratch in accounting module with date picker and 2 product lines. Fewer lines than hard-level create tasks but the accounting form layout differs from sales. |

---

## crm.edit_opportunity_schedule_call

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | CRM — Pipeline |
| **Workflow** | Find opportunity "Beacon Analytics Deal", update Expected Revenue to 75000 and Probability to 60%, then schedule a Call activity for May 10, 2026 with summary "Follow up on proposal". |
| **Capability tested** | Multi-field edit on opportunity form plus activity scheduling via the popover widget. The activity popover has multiple fields (type, date, summary) in a compact UI. |

---

## hr.update_work_information

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Find employee "Sofia Chen". Navigate to Work Information tab, set Work Location to "Home" and Timezone to "America/New_York". Navigate to Private Information tab, set Certificate Level to "Master". Save. |
| **Capability tested** | Multi-tab form navigation — agent must visit two different tabs and update fields on each before saving. Different from hr.create_employee (editing existing vs creating new). |

---

## project.create_task_assign_stage

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Project |
| **Workflow** | In "Omega Platform Launch" project, create task "Design Landing Page Mockup" with assignee Mitchell Admin, deadline May 15, 2026, priority Urgent, and description text. Place in "In Progress" stage. |
| **Capability tested** | Multi-field task creation with stage placement — agent must fill 5+ fields and ensure the task ends up in the correct kanban column. |

---

## stock.confirm_and_validate_receipt

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Find receipt BENCH-RCV-01 in transfers. Set Done quantities for Steel Bracket 12" (20) and Copper Wire 100m (10) to match demand. Click Validate. |
| **Capability tested** | Inline quantity editing on stock move lines followed by validation. Different from stock.adjust_inventory (receipt validation vs physical inventory; different UI for setting quantities). |

---

## purchase.update_rfq_add_line_confirm

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Purchase |
| **Workflow** | Open draft RFQ BENCH-RFQ-UPD for Pinnacle Hardware. Add new line (Hex Wrench Set ×25 @ $15.00). Change Order Deadline to May 20, 2026. Confirm Order. |
| **Capability tested** | Add product line to existing record + date picker + confirm. Different from purchase.new_rfq_three_lines_date (edit existing vs create from scratch) and purchase.cancel_reissue_wrong_vendor (no cancel/reissue). |

---

## contacts.update_address_add_tag

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Contacts |
| **Workflow** | Find company "Brookfield Dynamics". Update address (street, city, state, ZIP), add "Supplier" tag, set Job Position to "Procurement Partner". Save. |
| **Capability tested** | Multi-field address update + tag addition (many2many widget) + text field. Different from contacts.create_company_with_contacts (editing existing vs multi-record creation). |

---

## calendar.create_single_event

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Calendar |
| **Workflow** | Create one-time event "Q2 Strategy Review" on May 8, 2026, 2-4 PM, location "Conference Room A", with description and Marc Demo as attendee. |
| **Capability tested** | Multi-field event creation with date/time pickers and attendee selection. Different from calendar.schedule_recurring_steering_sync (one-time vs recurring, no recurrence dialog) and calendar.edit_single_recurrence_occurrence (create vs edit). |

---

## hr_recruitment.advance_applicant_stage

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Recruitment |
| **Workflow** | In "Experienced Developer" job, find applicant "Taylor Kim". Move from "Initial Qualification" to "First Interview" stage. Set Appreciation to "In Progress". Write application summary text. Save. |
| **Capability tested** | Kanban stage change + appreciation rating + description text. Different from hr_recruitment.new_applicant_schedule_interview (advancing existing vs creating new; no activity scheduling). |

---

## sale.create_invoice_adjust_quantity_post

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Accounting |
| **Workflow** | Find confirmed sales order `MED-INV-SO-01` for Northwind Studio. Click **Create Invoice**, keep the default draft-invoice option, set Invoice Date to May 12, 2026, set Payment Terms to `30 Net Days`, and confirm the invoice. |
| **Capability tested** | Related-module handoff from Sales to the generated invoice form plus a date field and many2one edit before posting. Distinct from pure quotation edits and from accounting-only invoice tasks. |

---

## purchase.confirm_order_send_po_message

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Purchase |
| **Workflow** | Find draft RFQ `MED-SEND-PO-01` for Sterling Components. Confirm it, then open **Send PO** and overwrite the subject and body before sending. |
| **Capability tested** | Confirm-order flow plus compose-wizard editing in Purchase. Distinct from RFQ line-edit tasks because the hard part is the send wizard, not inline line editing. |

---

## project.update_task_assign_deadline_activity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Open project `Customer Portal Refresh`, edit task `Revise FAQ copy`, move it to In Progress, and schedule a Call activity due May 20, 2026 with summary `Review FAQ revisions`. |
| **Capability tested** | Existing-task edit combined with chatter activity scheduling. Distinct from new task creation and from chatter-only message tasks. |

---

## calendar.reschedule_event_update_location_attendee

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Open one-time event `Warehouse Safety Briefing` on April 17, 2026. Set Location to `Training Room`, add Marc Demo as an attendee, and save. |
| **Capability tested** | Editing an existing event through the calendar surface and managing attendees without touching recurrence. Distinct from creating a new event and from recurrence-dialog tasks. |

---

## contacts.create_linked_contact_add_tag

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Create person contact `Leah Morgan`, link it to the existing company `Seabird Logistics`, fill job title, email, and phone, and save. |
| **Capability tested** | New-contact creation with correct parent-company linkage while avoiding a similarly named distractor company. Distinct from company creation and from simple address editing. |

---

## inventory.scrap_product

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Navigate to product "Steel Bracket 12"" from the Products list. Click the Scrap button. In the Scrap dialog, set Quantity to 5 and accept all defaults. Click Scrap to confirm. |
| **Capability tested** | Accept-defaults wizard — open scrap wizard, enter a quantity, and confirm. Different from stock.adjust_inventory (physical inventory inline editing) and stock.confirm_and_validate_receipt (receipt validation). |

---

## hr.schedule_employee_activity

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Find employee "Sofia Chen". Click Schedule Activity in the chatter. Set Activity Type to Call, Due Date to May 10, 2026, Summary to "Annual review discussion". Click Schedule Activity. |
| **Capability tested** | Activity scheduling via chatter dialog — multiple fields (type, date, summary) in a compact modal. Different from hr.create_employee (multi-tab form creation) and hr.update_work_information (tab navigation). |

---

## sale.add_note_to_quotation

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open draft quotation BENCH-NOTE-01 for Azure Interior. Click Log note in the chatter (NOT Send message). Type exact text and click Log. |
| **Capability tested** | Chatter "Log note" vs "Send message" distinction — agent must select the correct chatter tab and post an internal note. Different from project.post_chatter_message (Send message) and project.complete_task_log_note (stage change + log note). |

---

## crm.set_priority_on_opportunity

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | CRM — Pipeline |
| **Workflow** | Find opportunity "Beacon Analytics Deal". Set Priority to 3 stars (High) using the star widget. Click Save. |
| **Capability tested** | Star widget interaction for priority setting — different from crm.move_opportunity_stage (kanban stage change) and crm.edit_opportunity_schedule_call (multi-field edit + activity). |

---

## project.set_task_deadline

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Project — Tasks |
| **Workflow** | Open project "Omega Platform Launch", find task "Design Landing Page Mockup". Change Deadline to May 20, 2026 via date picker. Click Save. |
| **Capability tested** | Date picker field edit on an existing task — different from project.post_chatter_message (chatter interaction), project.create_task_assign_stage (task creation), and project.complete_task_log_note (stage change + note). |

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
