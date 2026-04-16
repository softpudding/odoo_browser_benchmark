# Benchmark Task Status

This file tracks the status of all benchmark tasks. Update it when adding new tasks or running evaluations.

**Status values:** `WIP` (oracle or eval incomplete) | `Done` (oracle passes, browser-use eval recorded)

**Test results legend:** `PASS` / `FAIL` | F1 = state-diff F1 score (1.0 = perfect state match)

Last eval run: 2026-04-16 | Oracle: 28/28 (100%) | Browser-Use: 11/28 (39%)

---

## Tasks

| # | Task | Description | Status | Oracle | Browser-Use | F1 |
|---|------|-------------|--------|--------|-------------|-----|
| 1 | account.complete_customer_tax_id_then_post | Find draft invoice by origin VAT-302, navigate to customer, set Tax ID, return, set customer reference, post invoice | Done | PASS | FAIL | 0.0 |
| 2 | account.create_credit_note_and_reconcile | Create a credit note for a specific posted invoice and reconcile it against an open balance | Done | PASS | PASS | 1.0 |
| 3 | account.partial_refund_service_credit_note | Issue a partial credit note (refund) for a service line on a posted invoice | Done | PASS | FAIL | 0.0 |
| 4 | account.repair_and_post_invoice | Find draft invoice by origin APR-OPS, fix a wrong invoice line, and post it | Done | PASS | FAIL | 0.0 |
| 5 | account.switch_negative_invoice_repair_credit_note | Convert a negative draft invoice (origin RET-508) to a credit note and fix the amount | Done | PASS | FAIL | 0.0 |
| 6 | account.switch_negative_invoice_to_credit_note | Convert a negative draft invoice (origin RET-204) to a credit note | Done | PASS | FAIL | 0.0 |
| 7 | calendar.edit_single_recurrence_occurrence | Edit only one occurrence of a weekly recurring "Ops Standup" event without affecting others | Done | PASS | FAIL | 0.0 |
| 8 | calendar.make_single_occurrence_all_day | Change a single occurrence of a weekly recurring event to all-day | Done | PASS | FAIL | 0.0 |
| 9 | calendar.schedule_recurring_steering_sync | Create a new recurring meeting with specific recurrence settings | Done | PASS | PASS | 1.0 |
| 10 | crm.merge_duplicate_opportunities_cleanup | Merge two duplicate CRM opportunities for the same contact into one | Done | PASS | PASS | 1.0 |
| 11 | crm.qualify_lead_and_prepare_quote | Qualify a CRM lead by email, convert to opportunity, and create a quotation | Done | PASS | PASS | 1.0 |
| 12 | hr_recruitment.new_applicant_schedule_interview | Create a new job applicant and schedule an interview activity for them | Done | PASS | FAIL | 0.0 |
| 13 | project.configure_launch_milestones | Enable milestones on a project and create named milestones with deadlines | Done | PASS | FAIL | 0.71 |
| 14 | project.read_update_status | Read task statuses across stages in a project and update a specific task's state | Done | PASS | PASS | 1.0 |
| 15 | purchase.cancel_reissue_wrong_vendor | Cancel a PO sent to the wrong vendor and re-issue it to the correct vendor | Done | PASS | FAIL | 0.33 |
| 16 | purchase_stock.receive_and_complete_backorder | Receive a partial shipment and then receive the backorder to complete the PO | Done | PASS | PASS | 1.0 |
| 17 | purchase_stock.receive_partial_without_backorder | Receive a partial shipment and explicitly cancel the backorder (no more items coming) | Done | PASS | PASS | 1.0 |
| 18 | sale.cancel_reissue_wrong_customer | Cancel a confirmed SO for the wrong customer and re-issue it to the correct customer | Done | PASS | FAIL | 0.0 |
| 19 | sale.confirm_correct_order | Among multiple quotations, identify and confirm only the one matching specific products | Done | PASS | PASS | 1.0 |
| 20 | sale.create_quotation_and_send_email | Create a new quotation from scratch and send it by email to the customer | Done | PASS | FAIL | 1.0 |
| 21 | sale.exact_total_quotation | Read correct unit prices from product internal notes and update a quotation to hit an exact total | Done | PASS | FAIL | 0.5 |
| 22 | sale.find_highest_duplicate | Find the customer with both draft quotations and a confirmed SO, identify the highest-value duplicate | Done | PASS | FAIL | 0.0 |
| 23 | sale.revise_target_quote_lines | Find a quotation by customer reference OPS-042 and update specific order line quantities/prices | Done | PASS | FAIL | 0.0 |
| 24 | sale_project.confirm_quote_and_update_generated_project | Confirm a service quotation and update the auto-generated project settings | Done | PASS | PASS | 1.0 |
| 25 | sale_project.confirm_rollout_quote_update_generated_project | Confirm a rollout service quotation and update the auto-generated project settings | Done | PASS | PASS | 1.0 |
| 26 | website.edit_careers_spotlight | Edit website careers page content using the inline website editor | Done | PASS | PASS | 1.0 |
| 27 | website_hr_recruitment.apply_and_triage_ops_role | Submit a job application via the public jobs page and triage the applicant in the backend | Done | PASS | PASS | 1.0 |
| 28 | website_hr_recruitment.apply_guru_job | Submit a job application for the Guru position via the public website | Done | PASS | PASS | 1.0 |

---

## Notes

- Task #20 (`sale.create_quotation_and_send_email`): F1=1.0 (state matches) but Browser-Use FAIL — side-effect check fails (email send requires wkhtmltopdf stub).
- Task #13 (`project.configure_launch_milestones`): Browser-Use partial state match (F1=0.71), milestone fields partially set.
- Task #15 (`purchase.cancel_reissue_wrong_vendor`): Browser-Use partial match (F1=0.33), reissue step incomplete.
