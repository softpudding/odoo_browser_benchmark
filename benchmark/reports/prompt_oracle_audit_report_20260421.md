# Prompt vs Oracle Audit Report

Date: 2026-04-21
Tasks audited: 424 (2 rounds)
Worker: xiao

## Summary

- **Round 1** (original checklist): 19 discrepancies found
- **Round 2** (expanded checklist with misguidance categories): 34 discrepancies found (15 overlap with round 1)
- **Total unique discrepancies**: 38
- **All fixed**

## Round 2 — New Discrepancies Found by Expanded Checklist

These were missed in round 1 and caught by the new "misguidance on where to find information" categories:

### Wrong Tab for Field (category 4a)
| Task | Problem | Fix |
|---|---|---|
| calendar.create_all_day_event_with_attendee | "description" field is on Options tab, not Notes tab | Added "(on the Options tab)" hint |
| calendar.create_event_add_description_attendee | Same Options tab issue | Added tab hint |
| hr.create_employee_complete_profile | Working Hours listed under Work tab, actually on Payroll tab | Moved to Payroll tab section |
| maintenance.fill_description_schedule_window_move_to_repaired | Description in Notes tab, not form body | Changed to "Notes tab" |

### Wrong Field Label (category 4b)
| Task | Problem | Fix |
|---|---|---|
| account.lock_books_set_period_lock_date | "Non-Advisors Lock Date" → "Global Lock Date" | Fixed primary label |
| crm.set_priority_on_opportunity | "Important" → "High" for 2 stars | Fixed label |
| fleet.log_fuel_refill_with_cost | "Total Price" → "Cost" | Fixed |
| fleet.log_service_cost_record | "Total Price" → "Cost" | Fixed |
| hr_expense.create_expense_with_receipt | "Internal Notes" label doesn't exist | Removed label reference |
| hr_expense.create_mileage_expense_submit_report | "total" but mileage shows "Quantity" | Changed to quantity |
| mail.create_alias_route_to_record | "Document Model" → "Aliased Model" | Fixed |
| maintenance.create_request_from_equipment_schedule_followup | "Maintenance Team"→"Team"; "Technician"→"Responsible" | Fixed both |
| maintenance.fill_description_schedule_window_move_to_repaired | "End Date" → "Scheduled End" | Fixed |
| mrp.create_routing_set_workcenter | "Expected Duration" → "Default Duration" | Fixed |
| mrp.create_variant_specific_bom | "Apply on Variants" → "Product Variant" | Fixed |
| project.add_task_subtask | "Subtasks" → "Sub-tasks" (hyphenated) | Fixed |
| project.set_project_deadline_tags | "Deadline" → "Planned Date" | Fixed |
| project.update_task_priority | "Important (1 star)" → "Medium priority" | Fixed |
| stock.update_product_internal_reference | "Internal Reference" → "Reference" (view override) | Fixed |
| website_sale.configure_delivery_method_weight | "Sale Base Price"/"Sale Price" → "Delivery Cost" | Fixed |
| website_slides.create_course_add_certification_toggle_visibility | "Short Description" doesn't exist | Changed to "Description" |
| website_slides.create_course_add_lesson_publish | "Short Description" doesn't exist | Changed to "Description" |

### Non-existent Menu/Navigation (category 3)
| Task | Problem | Fix |
|---|---|---|
| account.reconcile_bank_statement_line_manual | "Journal Entries → Bank Statement Lines" doesn't exist | Removed specific path |
| account.reverse_journal_entry_from_general_ledger | "Miscellaneous Operations" menu doesn't exist | Removed specific path |
| hr_expense.post_approved_expense_to_journal | "All Expenses" menu doesn't exist | Changed to "My Expenses" |
| hr_expense.split_expense_analytic_distribution | "All Expenses" menu doesn't exist | Changed to "My Expenses" |
| project.create_milestone_assign_tasks_reach | "embedded Milestones tab" doesn't exist | Removed reference |
| project.read_update_status | Breadcrumb ⋮ menu doesn't exist | Changed to kanban card menu |

### Non-existent Button Label (category 1)
| Task | Problem | Fix |
|---|---|---|
| hr_expense.submit_approve_post_accounting | "Submit to Manager" → "Submit" | Fixed |
| hr_expense.submit_report_for_approval | "Submit to Manager" → "Submit" | Fixed |
| mrp_account.confirm_mo_check_account_move | Two-step "Produce + Mark as Done" → single "Produce All" | Fixed |

### Wrong State/Impossible Workflow (category 2/6)
| Task | Problem | Fix |
|---|---|---|
| event.register_attendee_confirm_check_in | Registration defaults to Registered, not Unconfirmed | Removed Confirm step |
| survey.branching_quiz_publish_share_link | Scoring invisible for survey_type='survey' | Added "use Custom type" |
| hr_expense.post_approved_expense_to_journal | Wrong currency (€ vs $ default) | Removed currency symbol |
| hr_expense.split_expense_analytic_distribution | Wrong currency (€ vs $ default) | Removed currency symbol |

### Other (missing spec)
| Task | Problem | Fix |
|---|---|---|
| sale.update_quote_payment_terms_validity_confirm | Customer Reference column hidden by default | Changed to use SO name |
| website_slides.create_course_add_lesson_publish | check.py requires "assembly point" not in prompt | Added content requirement |
| hr.add_skill_to_employee_with_level | "Skills tab" → "Resume" tab | Fixed |
| stock.scrap_product_from_receipt | Two-step flow doesn't exist | Changed to single button |

## Round 1 — Previously Found Discrepancies (still valid)

| Task | Problem | Fix |
|---|---|---|
| account.complete_customer_tax_id_then_post | "Other Info tab" for narration → "Invoice Lines tab" | Fixed |
| crm.create_lead_from_email_alias_log_message | "High (three stars)" → "Very High" | Fixed |
| crm.create_opportunity_set_close_date_priority | "High (3 stars)" → "Very High" | Fixed |
| crm.create_opportunity_tag_schedule_call | "High (3 stars)" → "Very High" | Fixed |
| crm.mark_opportunity_won_update_revenue | "Medium (2 stars)" → "High" | Fixed |
| crm.update_lead_phone | "Click Edit" but Odoo 19 has no Edit button | Fixed |
| crm.update_opportunity_revenue_priority_won | "Medium (2 stars)" → "High" | Fixed |
| event.create_event_add_ticket_publish | Publish toggle misdescribed | Fixed |
| event_sale.configure_paid_ticket_register_with_invoice | "Create Draft Invoice" → "Create Draft" | Fixed |
| hr.add_employee_skill | "Add a skill" → "Pick a skill from the list" | Fixed |
| hr.add_resume_line_update_mobile | Duplicate of update_location task | Noted (structural) |
| hr.create_employee_complete_profile | "Private Information tab" → "Personal" | Fixed |
| hr_holidays.request_half_day_morning | Half Day toggle forced by config | Fixed |
| hr_recruitment.advance_applicant_stage | "Appreciation" → "Evaluation" | Fixed |
| hr_recruitment.create_applicant_add_skills_refuse | "Responsible" → "Recruiter" | Fixed |
| hr_recruitment.create_applicant_set_email_stage | Duplicate + "Appreciation" → "Evaluation" | Fixed |
| im_livechat.create_channel_add_canned_response | "Content" → "Substitution" | Fixed |
| inventory.filtered_cycle_count_apply_single_line | "Inventory Adjustments" → "Physical Inventory" | Fixed |
| mrp.create_routing_set_workcenter | "Add a line" → generic "Add a new operation" | Fixed |
| mrp.produce_mo_partial_backorder | "Produce All" → "Produce" for partial qty | Fixed |
| project_todo.create_three_personal_with_specific_priorities | "two priority stars" → removed count | Fixed |
| purchase.update_rfq_deadline | "Order Date" → "Order Deadline" | Fixed |
| stock.scrap_specific_serial_unit | Non-existent "Reason" field | Removed |
| account.switch_negative_invoice_repair_credit_note | Missing price instruction | Fixed |
| calendar.create_private_meeting_with_video_link | check.py UTC comparison | Fixed |
| contacts.create_linked_contact_add_tag | Duplicate task | Noted |
| contacts.create_linked_contact_set_title_phone | Duplicate task | Noted |
| contacts.update_contact_mobile | Task name mismatch (mobile vs website) | Noted |
| website_blog.duplicate_post_localize_seo_slug_publish | SEO tab needs debug mode | Added note |
| website_blog.schedule_post_future_date_unpublish | Published pill is redirect button | Fixed to systray toggle |
| website_sale.apply_promo_code_at_checkout | "Send Coupon" → "Coupon Code" | Fixed |
