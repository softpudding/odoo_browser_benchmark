# Benchmark Task Status

Tracks all benchmark tasks. Update when adding new tasks or running evaluations.

**Status values:** `WIP` — oracle or eval incomplete | `Done` — oracle passes, eval recorded

Last eval: 2026-04-17 | Oracle: 165/165 (100%) | Browser-Use: 57/165 (34.5%) | New WIP: 88 (45 medium + 24 easy + 19 hard)

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
| 39 | sale.set_payment_terms_confirm [medium] | Done | PASS | FAIL | 0.0 |
| 40 | account.create_vendor_bill_confirm [medium] | Done | PASS | FAIL | 0.0 |
| 41 | crm.edit_opportunity_schedule_call [medium] | Done | PASS | PASS | 1.0 |
| 42 | hr.update_work_information [medium] | Done | PASS | PASS | 1.0 |
| 43 | project.create_task_assign_stage [medium] | Done | PASS | FAIL | 0.0 |
| 44 | stock.confirm_and_validate_receipt [medium] | Done | PASS | PASS | 1.0 |
| 45 | purchase.update_rfq_add_line_confirm [medium] | Done | PASS | FAIL | 0.0 |
| 46 | contacts.update_address_add_tag [medium] | Done | PASS | PASS | 1.0 |
| 47 | calendar.create_single_event [medium] | Done | PASS | FAIL | 0.0 |
| 48 | hr_recruitment.advance_applicant_stage [medium] | Done | PASS | PASS | 1.0 |
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
| 59 | purchase.confirm_rfq [easy] | Done | PASS | PASS | 1.0 |
| 60 | hr.update_employee_work_phone [easy] | Done | PASS | PASS | 1.0 |
| 61 | sale.add_note_to_quotation [easy] | Done | PASS | PASS | 1.0 |
| 62 | crm.set_priority_on_opportunity [easy] | Done | PASS | FAIL | 1.0 |
| 63 | contacts.update_contact_email [easy] | Done | PASS | PASS | 1.0 |
| 64 | account.update_vendor_bill_reference_post [medium] | Update a draft vendor bill's date and reference, then confirm it | Done | PASS | PASS | 1.0 |
| 65 | contacts.update_company_with_supplier_tag [medium] | Update an existing company contact's address, website, and Supplier tag | Done | PASS | FAIL | 0.0 |
| 66 | crm.create_opportunity_tag_schedule_call [medium] | Create a CRM opportunity, set revenue and priority, then schedule a call | Done | PASS | FAIL/PASS | 1.0 |
| 67 | project.rename_task_assign_deadline [medium] | Rename a project task, set its deadline, and move it to In Progress | Done | PASS | PASS | 1.0 |
| 68 | purchase.set_order_deadline_schedule_call_confirm [medium] | Update an RFQ vendor reference, schedule a call, and confirm the order | Done | PASS | PASS | 1.0 |
| 69 | website.update_contact_info [easy] | Done | PASS | FAIL | 0.0 |
| 70 | stock.update_product_internal_reference [easy] | Done | PASS | FAIL | 0.0 |
| 71 | hr.update_employee_department [easy] | Done | PASS | PASS | 1.0 |
| 72 | sale.add_discount_line [easy] | Done | PASS | FAIL | 0.0 |
| 73 | project.add_task_subtask [easy] | Done | PASS | PASS | 1.0 |
| 74 | account.update_customer_invoice_terms_post [medium] | Update a draft customer invoice's date, payment terms, reference, and one existing line quantity before posting | Done | PASS | PASS/PASS | 1.0 |
| 75 | crm.update_opportunity_revenue_priority_won [medium] | Update an opportunity's expected revenue, set medium priority with the star widget, and mark it Won | Done | PASS | FAIL/FAIL | 0.0 |
| 76 | hr.update_work_location_schedule_activity [medium] | Update an employee's phone and work location, then schedule a Call activity | Done | PASS | PASS/FAIL | 1.0 |
| 77 | purchase.update_rfq_reference_deadline_confirm [medium] | Update an RFQ vendor reference and order deadline, adjust one line quantity, and confirm it | Done | PASS | PASS/PASS | 1.0 |
| 78 | contacts.create_linked_contact_add_finance_tag [medium] | Create a linked person contact with exact address fields and the Finance tag | Done | PASS | FAIL/PASS | 1.0 |
| 79 | account.pay_invoice_with_memo [medium] | Register a payment on a posted invoice with a specific memo/reference | Done | PASS | — | 1.0 |
| 80 | project.set_project_deadline_tags [medium] | Set project deadline to June 30 2026 and add Launch and Q3 tags | Done | PASS | — | 1.0 |
| 81 | sale.set_commitment_date [medium] | Cancel, reset to draft, set delivery date to May 20 2026, then re-confirm sales order | Done | PASS | — | 1.0 |
| 82 | stock.update_reorder_rule [medium] | Update min qty to 50 and max qty to 200 for a specific product reorder rule | Done | PASS | — | 1.0 |
| 83 | hr.add_employee_skill [medium] | Add Python skill (IT Skills / Advanced) to employee Priya Mehta via Resume tab | Done | PASS | — | 1.0 |
| 84 | inventory.scrap_product [easy] | Done | PASS | FAIL | 0.0 |
| 85 | hr.schedule_employee_activity [easy] | Done | PASS | FAIL | 0.0 |
| 86 | project.set_task_deadline [easy] | Done | PASS | FAIL | 0.0 |
| 87 | sale.duplicate_quotation_change_customer [medium] | Duplicate a quotation, switch the customer on the copy, and save it in draft | Done | PASS | PASS/PASS | 1.0 |
| 88 | purchase.duplicate_rfq_change_vendor_confirm [medium] | Done | PASS | FAIL | 0.0 |
| 89 | project.archive_task_with_log_note [medium] | Post a log note on a project task, then archive it from the Action menu | Done | PASS | PASS | 1.0 |
| 90 | crm.convert_lead_to_opportunity_simple [medium] | Done | PASS | FAIL | 0.0 |
| 91 | hr.unarchive_employee_update_department [medium] | Done | PASS | FAIL | 0.0 |
| 92 | stock.validate_delivery_shipment [medium] | Done | PASS | FAIL | 0.0 |
| 93 | account.create_bill_from_confirmed_po [medium] | Create and post a vendor bill from a confirmed purchase order | Done | PASS | PASS | 1.0 |
| 94 | sale.cancel_quotation_log_reason [medium] | Post a cancellation reason as a log note, then cancel the quotation | Done | PASS | PASS/FAIL | 1.0/0.0 |
| 95 | hr_recruitment.refuse_applicant_with_reason [medium] | Refuse an applicant with the correct refuse reason and no email | Done | PASS | PASS/PASS | 1.0 |
| 96 | crm.mark_opportunity_won_update_revenue [medium] | Done | PASS | FAIL | 0.0 |
| 97 | account.create_customer_invoice_post [medium] | Done | PASS | FAIL | 0.0 |
| 98 | account.partial_pay_vendor_bill_with_memo [medium] | Done | PASS | FAIL | 0.0 |
| 99 | calendar.create_all_day_event_with_attendee [medium] | Done | PASS | FAIL | 0.0 |
| 100 | contacts.create_company_add_supplier_tag [medium] | Create a company contact with address details and the Supplier tag | Done | PASS | FAIL | 0.0 |
| 101 | crm.create_lead_priority_schedule_call [medium] | Removed | FAIL (spec) | — | — |
| 102 | hr.assign_manager_set_work_location [medium] | Update an employee's manager, work location, and work phone | Done | PASS | PASS/PASS | 1.0 |
| 103 | hr_recruitment.schedule_interview_for_applicant [medium] | Done | PASS | FAIL | 0.0 |
| 104 | project.duplicate_task_assign_deadline [medium] | Done | PASS | FAIL | 0.0 |
| 105 | purchase.cancel_rfq_log_note [medium] | Log an internal note on an RFQ, then cancel it | Done | PASS | PASS | 1.0 |
| 106 | sale.update_salesperson_validity_confirm [medium] | Done | PASS | FAIL | 0.0 |
| 107 | crm.convert_lead_link_customer_schedule_call [medium] | Done | PASS | FAIL | 0.0 |
| 108 | purchase_stock.confirm_rfq_receive_full [medium] | Done | PASS | FAIL | 0.0 |
| 109 | sale.create_invoice_register_payment_memo [medium] | Done | PASS | PASS | 1.0 |
| 110 | contacts.create_company_add_supplier_finance_tags [medium] | Done | PASS | PASS | 1.0 |
| 111 | project.create_subtask_assign_deadline [medium] | Done | PASS | PASS | 1.0 |
| 112 | crm.convert_lead_qualify [medium] | Done | PASS | PASS | 1.0 |
| 113 | project.convert_task_to_subtask [medium] | Done | PASS | PASS/PASS | 1.0 |
| 114 | hr.add_resume_line_update_location [medium] | Done | PASS | FAIL | 0.0 |
| 115 | hr_recruitment.add_skill_move_stage [medium] | Done | PASS | FAIL/FAIL | 0.0 |
| 116 | contacts.create_company_set_supplier_tag [medium] | Done | PASS | PASS* | — |
| 117 | account.update_invoice_reference [easy] | Done | PASS | PASS | 1.0 |
| 118 | contacts.update_contact_phone [easy] | Done | PASS | PASS | 1.0 |
| 119 | crm.update_opportunity_revenue [easy] | Done | PASS | PASS | 1.0 |
| 120 | hr.update_employee_job_title [easy] | Done | PASS | PASS | 1.0 |
| 121 | purchase.update_rfq_source [easy] | Done | PASS | PASS | 1.0 |
| 122 | sale.create_quotation_down_payment_invoice [hard] | Down payment wizard with non-default % option, navigate to invoice, edit, confirm | Done | PASS | — | — |
| 123 | account.create_refund_modify_reissue [hard] | Credit note "Reverse and Create Invoice" button, edit new draft lines, post | Done | PASS | — | — |
| 124 | purchase.create_rfq_confirm_receive_backorder [hard] | Create PO with exact lines, confirm, partial receive, Create Backorder dialog | Done | PASS | — | — |
| 125 | stock.return_delivery_create_credit_note [hard] | Open delivery, return wizard, validate return, navigate to create credit note | Done | PASS | — | — |
| 126 | crm.create_opportunity_add_quotation_send [hard] | Create opportunity, add quotation with exact lines, send by email wizard | Done | PASS | — | — |
| 127 | sale_stock.confirm_order_deliver_partial_backorder [hard] | Confirm SO, navigate to delivery, partial validate with Create Backorder | Done | PASS | — | — |
| 128 | hr_recruitment.create_applicant_add_skills_refuse [hard] | Create applicant with skills, then refuse with specific reason wizard | Done | PASS | — | — |
| 129 | sale.cancel_confirmed_recreate_send_email [hard] | Cancel confirmed SO, create new quotation with exact lines, send by email | Done | PASS | — | — |
| 130 | calendar.create_recurring_edit_two_occurrences [hard] | Create recurring event, then edit two occurrences separately with "This Event" | Done | PASS | — | — |
| 131 | website.edit_page_update_text_set_properties [hard] | Edit webpage text in website editor, set page title via Properties dialog | Done | PASS | — | — |
| 132 | calendar.create_event_add_description_attendee [medium] | Create one event with exact attendee, location, and description | Done | PASS | FAIL | 0.0 |
| 133 | contacts.create_linked_contact_set_title_phone [medium] | Add a linked contact under a company with title, phone, and email | Done | PASS | PASS | 1.0 |
| 134 | crm.create_opportunity_set_close_date_priority [medium] | Create an opportunity with revenue, closing date, and star priority | Done | PASS | FAIL | 0.0 |
| 135 | hr.add_resume_line_update_mobile [medium] | Update employee mobile and add one exact resume entry | Done | PASS | FAIL | 0.0 |
| 136 | hr_recruitment.create_applicant_set_email_stage [medium] | Create an applicant, set contact fields, and move to a target stage | Done | PASS | FAIL | 0.0 |
| 137 | project.create_task_assign_tags_deadline [medium] | Create a project task with assignee, tags, and deadline | Done | PASS | FAIL | 0.0 |
| 138 | project.rename_task_assign_tags_priority [medium] | Rename one task, add a tag, and change its priority | Done | PASS | PASS | 1.0 |
| 139 | purchase.update_rfq_note_quantity_confirm [medium] | Edit an RFQ note and quantity, then confirm it | Done | PASS | PASS | 1.0 |
| 140 | sale.update_quote_payment_terms_validity_confirm [medium] | Set payment terms, validity, and quantity before confirmation | Done | PASS | FAIL | 0.0 |
| 141 | stock.update_delivery_scheduled_date_validate [medium] | Change a delivery scheduled date, then validate it | Done | PASS | PASS | 1.0 |
| 142 | hr_holidays.allocate_leave_days [easy] | Allocate 15 days of Sick Time Off to an employee | WIP | — | — | — |
| 143 | hr_holidays.request_time_off_approve [medium] | Create Sick Time Off for employee, fill dates, save, and validate | Done | PASS | FAIL/PASS | 1.0 |
| 144 | hr_holidays.refuse_leave_request [medium] | Refuse a pending time-off request as manager | Done | PASS | PASS | 1.0 |
| 145 | hr_holidays.create_leave_type [medium] | Create a new Time Off Type with manager approval | Done | PASS | PASS | 1.0 |
| 146 | hr_holidays.cancel_approved_leave [medium] | Cancel an approved leave request via cancel wizard | WIP | — | — | — |
| 147 | mrp.create_bom_confirm_mo [medium] | Create a Bill of Materials with 3 components, then create and confirm a Manufacturing Order for 10 units | Done | PASS | FAIL | 0.0 |
| 148 | hr_expense.create_expense_report_submit [medium] | Create an expense line, attach it to a new expense report, and submit it for approval | Done | PASS | PASS | 1.0 |
| 149 | event.create_event_add_ticket [medium] | Create an event with one paid ticket and attendee limits | Done | PASS | FAIL | 0.0 |
| 150 | fleet.create_vehicle_log_odometer [medium] | Add a vehicle, record its odometer reading, and save the vehicle in service | Done | PASS | FAIL | 0.0 |
| 151 | website_sale.publish_product_set_price [medium] | Publish a product to the website shop and set its sales price and description | Done | PASS | PASS | 1.0 |
| 152 | point_of_sale.open_session_sell_product_cash [medium] | Open a POS session, ring up one product, and complete a cash payment | Done | PASS | PASS | 1.0 |
| 153 | im_livechat.create_channel_add_canned_response [medium] | Create a live chat channel and canned response from the Live Chat app | Done | PASS | PASS | 1.0 |
| 154 | website.create_blog_post_publish [medium] | Create and publish a blog post with title, cover image, and body content | WIP | — | — | — |
| 155 | website.add_menu_item_reorder [medium] | Add a website menu item and reorder it within the navigation hierarchy | WIP | — | — | — |
| 156 | website.create_contact_form_block [hard] | Edit a website page to add and configure a contact form block | WIP | — | — | — |
| 157 | stock.scrap_product_from_receipt [medium] | Open a stock receipt and scrap part of a received product from the operation flow | WIP | — | — | — |
| 158 | stock.adjust_inventory_with_location_filter [medium] | Adjust inventory for a target product in one location while leaving other locations unchanged | WIP | — | — | — |
| 159 | stock.receive_serial_tracked_product [hard] | Validate a receipt by assigning exact serial numbers to tracked units | WIP | — | — | — |
| 160 | mrp.update_bom_component_quantity [medium] | Update one component quantity on an existing bill of materials and save it | WIP | — | — | — |
| 161 | mrp.create_mo_consume_produce_done [hard] | Create a manufacturing order, record component consumption, and mark production done | WIP | — | — | — |
| 162 | mrp.unbuild_product_partial [hard] | Unbuild part of a manufactured product quantity and verify the resulting stock moves | WIP | — | — | — |
| 163 | hr_expense.submit_report_with_receipt_approve [medium] | Create an expense with a receipt, submit it in a report, then approve it | Done | PASS | FAIL | 0.0 |
| 164 | website_sale.configure_variant_publish_product [medium] | Configure website product variants, publish the product, and verify it on the shop | Done | PASS | PASS | 1.0 |
| 165 | event.publish_event_register_attendee [hard] | Publish an event, register a public attendee, and verify the backend registration | Done | PASS | FAIL | 0.0 |
| 166 | fleet.create_vehicle_assign_driver_contract [medium] | Create a vehicle, assign a driver, and add a dated contract record | Done | PASS | FAIL | 0.0 |
| 167 | mail.create_channel_pin_message_invite_member [medium] | Create a private channel, invite a member, post a message, and pin the conversation | Done | PASS | FAIL | 0.0 |
| 168 | mrp.produce_and_close_mo [easy] | Open a confirmed MO, click Produce All to complete production | Done | PASS | PASS/PASS | 1.0 |
| 169 | mrp.produce_mo_partial_backorder [medium] | Produce partial qty on a confirmed MO and split the remainder into a backorder | Done | PASS | PASS/FAIL | 1.0/0.0 |
| 170 | contacts.add_bank_account_iban [medium] | Open a partner, add a bank account with a specific IBAN via the Invoicing tab, and save | Done | PASS | PASS/PASS | 1.0 |
| 171 | hr_expense.approve_submitted_report [medium] | Manager opens a submitted expense among a distractor and approves only the target | Done | PASS | PASS/PASS | 1.0 |
| 172 | stock.receive_lot_tracked_product [hard] | Open a receipt for a lot-tracked product, enter the exact lot in the Details popup, then Validate | Done | PASS | FAIL/FAIL | 0.0 |
| 173 | contacts.archive_duplicate_transfer_fields [medium] | Copy phone and email from a duplicate partner to the primary, then archive the duplicate via the Actions menu | Done | PASS | PASS/PASS | 1.0 |
| 174 | mrp.create_routing_set_workcenter [medium] | Create a workcenter and link it as an operation on an existing BOM | Done | PASS | PASS | 1.0 |
| 175 | mrp.scrap_component_during_production [hard] | Scrap one consumed component from a running MO via the component action menu | WIP | — | — | — |
| 176 | mrp.convert_bom_to_kit_type [easy] | Change an existing BOM's type from Manufacture This Product to Kit | Done | PASS | PASS | 1.0 |
| 177 | mrp.create_variant_specific_bom [hard] | Create a BOM that applies only to a single product variant via attribute filter | WIP | — | — | — |
| 178 | mrp.configure_mo_operation_time_finish [medium] | Open a work order on an MO, set expected duration, and mark it finished | WIP | — | — | — |
| 179 | point_of_sale.sell_two_products_apply_discount [medium] | Ring up two POS products, apply a 10% line discount, pay cash | WIP | — | — | — |
| 180 | point_of_sale.refund_previous_order [hard] | Refund a prior POS order partially from the Orders menu | WIP | — | — | — |
| 181 | point_of_sale.attach_customer_mid_sale [easy] | Open a POS session, add a product, attach existing customer, pay cash | WIP | — | — | — |
| 182 | point_of_sale.close_session_reconcile_cash_diff [medium] | Close a POS session with a counted cash amount different from expected | WIP | — | — | — |
| 183 | website_sale.add_product_to_cart_checkout_portal [medium] | As a public user, add a product to cart and complete checkout with address | WIP | — | — | — |
| 184 | website_sale.apply_promo_code_at_checkout [medium] | Create a coupon program in backend then apply the code on the storefront | WIP | — | — | — |
| 185 | website_sale.edit_product_image_gallery [easy] | Add an extra image to a published product via the shop editor | WIP | — | — | — |
| 186 | website_sale.configure_delivery_method_weight [medium] | Create a delivery method with weight-based pricing rules | WIP | — | — | — |
| 187 | website.create_new_page_publish [medium] | Create a blank new website page, add a heading, and publish it | WIP | — | — | — |
| 188 | website.set_page_seo_fields [easy] | Use the Promote dialog to set meta title, description, and keywords on a page | WIP | — | — | — |
| 189 | website.add_image_snippet_swap_source [medium] | Drag an Image snippet into a page and swap its source image | WIP | — | — | — |
| 190 | website.duplicate_page_rename_unpublish [easy] | Duplicate an existing website page, rename the copy, and leave unpublished | WIP | — | — | — |
| 191 | hr_holidays.approve_multiple_requests_bulk [hard] | Multi-select pending time-off requests in list view and bulk approve | WIP | — | — | — |
| 192 | hr_holidays.request_leave_with_attachment [medium] | Request leave and attach a PDF justification via the chatter | WIP | — | — | — |
| 193 | hr_expense.split_expense_analytic_distribution [hard] | Split one expense line 50/50 across two analytic accounts | WIP | — | — | — |
| 194 | hr_expense.refuse_report_with_reason_chatter [medium] | Refuse a submitted expense report and post the reason to chatter | WIP | — | — | — |
| 195 | hr_expense.post_approved_expense_to_journal [medium] | Manager posts an approved expense report to its journal entry | WIP | — | — | — |
| 196 | mail.star_and_reply_inbox_message [easy] | Star an inbox message and post a reply | WIP | — | — | — |
| 197 | mail.mark_message_done_archive_notification [easy] | Mark Done on an inbox notification to remove it from Inbox | WIP | — | — | — |
| 198 | mail.create_group_channel_upload_attachment [medium] | Create a private channel, invite a member, and upload a file attachment | WIP | — | — | — |
| 199 | im_livechat.add_canned_response_send_in_chat [medium] | Create a canned response shortcut and send it in an operator chat | WIP | — | — | — |
| 200 | fleet.log_service_cost_record [easy] | Add a service cost record (oil change) to an existing vehicle | Done | PASS (32.1s) | FAIL (142.4s) | 0.00 |
| 201 | fleet.assign_vehicle_tags_category [easy] | Add two tags and set a category on a vehicle | Done | PASS | PASS | 1.0 |
| 202 | fleet.transfer_vehicle_new_driver [medium] | Change a vehicle's driver and set the new assignment date | WIP | — | — | — |
| 203 | event.add_event_questions_to_registration [medium] | Add two custom questions to an existing event registration form | WIP | — | — | — |
| 204 | event.create_event_tracks_session_schedule [hard] | Add two conference tracks with times to a published event | WIP | — | — | — |
| 205 | event.set_ticket_seat_availability_limit [easy] | Set total seat limit and per-ticket max for an event | Done | PASS | FAIL | 0.4 |
| 206 | stock.create_internal_transfer_between_locations [medium] | Create an internal transfer between two locations, add a line, and validate | WIP | — | — | — |
| 207 | stock.create_putaway_rule_for_product [hard] | Configure a putaway rule routing a product to a specific sub-location | WIP | — | — | — |
| 208 | stock.count_inventory_apply_with_date [medium] | Make an inventory adjustment with a specific counted date | WIP | — | — | — |
| 209 | stock.set_storage_category_capacity [medium] | Define a storage category with capacity and assign it to a location | WIP | — | — | — |
| 210 | account.create_manual_journal_entry_balanced [hard] | Create a misc journal entry with three balanced debit/credit lines and post | WIP | — | — | — |
| 211 | account.reconcile_bank_statement_line_manual [hard] | Open a bank statement line and reconcile it against a suggested invoice | WIP | — | — | — |
| 212 | account.create_recurring_entry_template [medium] | Save a journal entry as a recurring entry template | WIP | — | — | — |
| 213 | account.lock_books_set_period_lock_date [medium] | Set the Non-Advisors Lock Date in accounting settings | WIP | — | — | — |
| 214 | crm.set_lost_reason_reassign_salesperson [medium] | Mark opportunity Lost with specific reason then reassign salesperson | WIP | — | — | — |
| 215 | crm.pivot_view_opportunities_by_stage_revenue [easy] | Switch CRM pipeline to Pivot view, group by stage, measure expected revenue | WIP | — | — | — |
| 216 | project.kanban_drag_task_between_stages [easy] | Drag a task kanban card from one stage to another | Done | PASS | FAIL | 0.0 |
| 217 | project.create_project_from_template_duplicate [medium] | Duplicate an existing project keeping its tasks | WIP | — | — | — |
| 218 | project.recurring_task_configure_frequency [medium] | Configure an existing task as recurring with weekly frequency | WIP | — | — | — |
| 219 | contacts.add_bank_account_to_partner [easy] | Add an IBAN bank account to an existing partner via Accounting tab | WIP | — | — | — |
| 220 | contacts.archive_partner_then_unarchive_filter [easy] | Archive a contact then unarchive it via the Archived search filter | WIP | — | — | — |
| 221 | calendar.invite_external_attendee_by_email [easy] | Create a calendar event inviting an external email address not in partners | Done | PASS | PASS | 1.0 |
| 222 | survey.create_survey_one_page_publish_share [medium] | Create a 3-question survey, publish it, and copy the share link | WIP | — | — | — |
| 223 | project_todo.create_note_add_tag_checklist [easy] | In the To-Do app, create a note with a tag and a checklist item | WIP | — | — | — |
| 224 | hr_holidays.request_annual_leave [easy] | Done | PASS | PASS | 1.0 |
| 225 | hr_holidays.approve_leave_as_manager [medium] | N/A | — | — | — |
| 226 | hr_holidays.refuse_leave_with_reason [medium] | Done | PASS | PASS | 1.0 |
| 227 | hr_expense.create_expense_with_receipt [medium] | Done | PASS | PASS | 1.0 |
| 228 | hr_expense.submit_report_for_approval [medium] | N/A | — | — | — |
| 229 | mail.create_channel_invite_members [easy] | N/A | — | — | — |
| 230 | mail.pin_and_reply_in_chatter [easy] | Done | PASS | PASS | 1.0 |
| 231 | contacts.merge_duplicate_contacts [hard] | Done | PASS | PASS | 1.0 |
| 232 | contacts.archive_then_unarchive [easy] | Done | PASS | FAIL | 0.00 |
| 233 | website.create_blog_post_publish [medium] | N/A | — | — | — |
| 234 | website.edit_menu_add_page_link [medium] | N/A | — | — | — |
| 235 | stock.create_putaway_rule [hard] | N/A | — | — | — |
| 236 | stock.transfer_lot_tracked_product [hard] | N/A | — | — | — |
| 237 | mrp.create_bom_three_components [medium] | N/A | — | — | — |
| 238 | mrp.confirm_produce_close_mo [hard] | N/A | — | — | — |
| 239 | website_sale.publish_shop_product [medium] | N/A | — | — | — |
| 240 | appointment.create_type_set_slots [medium] | N/A | — | — | — |
| 241 | event.create_event_configure_ticket [medium] | N/A | — | — | — |
| 242 | helpdesk.create_ticket_assign_priority [medium] | N/A | — | — | — |
| 243 | fleet.register_vehicle_log_odometer [easy] | N/A | — | — | — |
| 244 | hr_holidays.allocate_sick_leave_to_employee [easy] | Done | PASS | PASS | 1.0 |
| 245 | hr_holidays.request_half_day_morning [easy] | N/A | — | — | — |
| 246 | hr_holidays.cancel_approved_leave_and_reallocate [hard] | Done | PASS | PASS | 1.0 |
| 247 | hr_expense.reject_expense_report_with_feedback [medium] | Done | PASS | PASS | 1.0 |
| 248 | hr_expense.submit_approve_post_accounting [hard] | Done | PASS | FAIL | 0.0 |
| 249 | mail.send_direct_message_to_user [easy] | Done | PASS | PASS | 1.0 |
| 250 | mail.star_message_filter_starred [easy] | Done | PASS | PASS | 1.0 |
| 251 | mail.mark_message_as_todo_and_resolve [medium] | Done | PASS | FAIL | 0.67 |
| 252 | fleet.schedule_vehicle_service_activity [easy] | Done | PASS | PASS | 1.0 |
| 253 | fleet.log_fuel_refill_with_cost [medium] | Done | PASS | FAIL | 0.0 |
| 254 | event.register_attendee_confirm_check_in [medium] | Done | PASS | PASS | 1.0 |
| 255 | event.configure_three_ticket_tiers [medium] | Done | PASS | FAIL | 0.86 |
| 256 | mrp.unbuild_finished_goods_to_recover_components [medium] | Done | PASS | PASS | 1.0 |
| 257 | mrp.surgical_bom_component_qty_edit [medium] | Done | PASS | PASS | 1.0 |
| 258 | stock.internal_transfer_between_locations [medium] | Done | PASS | PASS | 1.0 |
| 259 | calendar.create_private_meeting_with_video_link [medium] | Create a private meeting with attendees and an exact video call link | Done | PASS | FAIL | 0.0 |
| 260 | fleet.create_contract_set_renewal_activity [medium] | Create a vehicle contract with renewal dates, then schedule a follow-up activity | Done | PASS | FAIL | 0.0 |
| 261 | hr_expense.create_mileage_expense_submit_report [medium] | Create a mileage expense, add it to a report, and submit the report | Done | PASS | FAIL | 0.0 |
| 262 | mail.create_channel_set_description_pin_welcome [medium] | Create a private Discuss channel, set its description, and pin a welcome message | Done | PASS | FAIL | 0.0 |
| 263 | hr_holidays.allocate_leave_then_request_against_balance [hard] | Allocate sick leave to Marc Demo, then create and approve a request against that balance | Done | PASS | FAIL | 0.0 |
| 264 | contacts.create_company_with_invoice_and_delivery_addresses [medium] | Create a company with linked invoice and delivery child addresses | Done | PASS | FAIL | 0.0 |
| 265 | survey.branching_quiz_publish_share_link [hard] | Create a branching one-page quiz survey and leave it ready for public sharing | Done | PASS | FAIL | 0.0 |
| 266 | project_todo.duplicate_note_retag_archive_original [easy] | Duplicate the seeded To-Do note, retag the copy, and archive the original | Done | PASS | FAIL | 0.0 |
| 267 | website_sale.configure_optional_products_add_upsell_to_cart [medium] | Configure an optional webshop product, publish the upsell item, and add both to a website cart | Done | PASS | FAIL | 0.0 |
| 268 | hr_recruitment.schedule_second_interview_with_feedback [medium] | Move an applicant to Second Interview, schedule the meeting, and save the requested feedback | Done | PASS | FAIL | 0.0 |
| 269 | delivery.configure_fixed_rate_carrier_confirm_sale [medium] | Create a fixed-price delivery method, apply it to the target quotation, and confirm the order | Done | PASS | FAIL | 0.0 |
| 270 | hr_attendance.check_in_break_resume_check_out [medium] | Check in, take a break, resume, and check out from Attendances | Removed | FAIL (spec) | — | — |
| 271 | maintenance.create_request_assign_technician_mark_repaired [medium] | Create a maintenance request, assign the technician, and mark it repaired | Done | PASS | FAIL | 0.0 |
| 272 | website_blog.create_post_with_cover_tag_publish [medium] | Create a tagged blog post with a cover image and publish it | Done | PASS | FAIL | 0.0 |
| 273 | website_slides.create_course_add_lesson_publish [medium] | Create an eLearning course, add a lesson, and publish the course | Done | PASS | FAIL | 0.0 |

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
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Navigate to Operations > Physical Inventory. Set on-hand quantities for 3 specific products (Steel Bracket 12", Copper Wire 100m, Safety Harness XL) to exact target values while leaving 2 distractor products unchanged. Click Apply All. |
| **Capability tested** | Inline tree editing — agent must click into quantity cells in a list view and type values; fails by entering wrong row or not interacting with inline-editable cells correctly. |

---

## hr.create_employee_complete_profile

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Create a new employee "Jordan Mercer" filling fields across three areas: main form (name, job position, work phone), Work Information tab (work location, working hours), and Private Information tab (certificate level, marital status). |
| **Capability tested** | Create-from-scratch with multi-tab form — agent typically fills only the main form and saves without visiting Work Information or Private Information tabs. |

---

## purchase.new_rfq_three_lines_date

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase |
| **Workflow** | Create a new RFQ for vendor Meridian Supply Co with exactly 3 product lines (Rubber Gasket 200×$1.50, Stainless Bolt M8 500×$0.75, Hex Nut M8 500×$0.40) and set Order Deadline to May 30, 2026 via the date picker. Confirm. |
| **Capability tested** | Create-from-scratch with exact lines + date picker manipulation — agent leaves a phantom empty 4th line after entering the 3rd product, and/or sets wrong date via date picker widget. |

---

## project.complete_task_log_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/FAIL |
| **F1** | 1.0/0.0 |
| **Odoo modules** | Project |
| **Workflow** | In project "Omega Platform Launch", find task "Write API integration spec" in In Progress stage. Move it to Done stage. Then post an internal log note (not a regular message) with exact text via the chatter. |
| **Capability tested** | Chatter "Log note" vs "Send message" distinction (unexploited pattern) — agent uses wrong chatter button or skips the note step after moving the stage. |

---

## contacts.create_company_with_contacts

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Create company "Vantage Industrial Group" with full address details. Then create two individual contacts (Patricia Drum — Procurement Manager, Steven Okafor — Logistics Coordinator) both linked to the company with exact emails and mobile numbers. |
| **Capability tested** | Multi-record create sequence with company linkage — agent correctly creates the company and first contact, but leaves missing or incorrect fields on the second contact, or fails to link one contact to the parent company. |

---

## sale.change_validity_date

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open draft quotation BENCH-VALID-01 for Lakeview Partners. Change the Expiration date to May 15, 2026. Click Save. |
| **Capability tested** | Simple field edit + save — single date field change on a clearly identified draft quotation via date picker. |

---

## account.register_payment_defaults

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Accounting — Invoices |
| **Workflow** | Open posted invoice BENCH-PAY-01 for Lakeview Partners. Click Pay button. Accept all defaults in the Register Payment wizard. Click Create Payment. Verify invoice shows "Paid" status. |
| **Capability tested** | Accept-defaults wizard — open payment registration dialog, click Create Payment without changing any fields, verify payment registered. |

---

## crm.move_opportunity_stage

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
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
| **Oracle** | PASS |
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
| **Oracle** | PASS |
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
| **Oracle** | PASS |
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
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Find employee "Sofia Chen". On the Work tab set Work Location to "Home"; on the Settings tab set Timezone to "America/New_York"; on the Personal tab set Certificate Level to "Master". Save. |
| **Capability tested** | Multi-tab form navigation — agent must visit two different tabs and update fields on each before saving. Different from hr.create_employee (editing existing vs creating new). |

---

## project.create_task_assign_stage

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Project |
| **Workflow** | In "Omega Platform Launch" project, create task "Design Landing Page Mockup" with assignee Administrator, deadline May 15, 2026, priority Urgent, and description text. Place in "In Progress" stage. |
| **Capability tested** | Multi-field task creation with stage placement — agent must fill 5+ fields and ensure the task ends up in the correct kanban column. |

---

## stock.confirm_and_validate_receipt

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | PASS |
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
| **Oracle** | PASS |
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
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Contacts |
| **Workflow** | Find company "Brookfield Dynamics". Update address (street, city, state, ZIP), add "Supplier" tag, set Website to "https://brookfielddynamics.com". Save. |
| **Capability tested** | Multi-field address update + tag addition (many2many widget) + text field. Different from contacts.create_company_with_contacts (editing existing vs multi-record creation). |

---

## calendar.create_single_event

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | PASS |
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
| **Oracle** | PASS |
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

## purchase.confirm_rfq

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase |
| **Workflow** | Open draft RFQ `BENCH-CONFIRM-01` for vendor `Nimbus Industrial Supply` and click **Confirm Order** to convert it into a Purchase Order. |
| **Capability tested** | Single-record confirmation of an existing RFQ with no wizard choices or line edits. Distinct from purchase.reset_draft_edit_reconfirm (rollback + edit + confirm) and purchase.new_rfq_three_lines_date (record creation). |

---

## hr.update_employee_work_phone

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Open employee `Sofia Chen`, change **Work Phone** to `+1 555 0211`, and save. |
| **Capability tested** | Simple single-field update on an existing employee record. Distinct from hr.update_work_information (multi-tab editing) and hr.schedule_employee_activity (activity modal). |

---

## sale.add_note_to_quotation

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open draft quotation BENCH-NOTE-01 for Azure Interior. Click Log note in the chatter (NOT Send message). Type exact text and click Log. |
| **Capability tested** | Chatter "Log note" vs "Send message" distinction — agent must select the correct chatter tab and post an internal note. Different from project.post_chatter_message (Send message) and project.complete_task_log_note (stage change + log note). |

---

## crm.set_priority_on_opportunity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 1.0 |
| **Odoo modules** | CRM — Pipeline |
| **Workflow** | Find opportunity `Beacon Analytics Deal`. Set Priority to **2 stars** using the star widget and save. |
| **Capability tested** | Star widget interaction for priority setting — different from crm.move_opportunity_stage (kanban stage change) and crm.edit_opportunity_schedule_call (multi-field edit + activity). |

---

## contacts.update_contact_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Open contact `Avery Dalton`, change **Email** to `avery.dalton+ops@example.com`, and save. |
| **Capability tested** | Simple single-field update on an existing contact record. Distinct from contacts.update_address_add_tag (multi-field edit + tag) and contacts.create_linked_contact_add_tag (new-record creation). |

---

## website.update_contact_info

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Website — Pages |
| **Workflow** | Go to Website app, open the "About Us" page in the editor. Find the contact information section and change the phone number to "+1 555 987 6543". Save the page. |
| **Capability tested** | Website inline editor — find and edit a specific text field within page content. Different from website.edit_careers_spotlight (card editing on careers page). |

---

## stock.update_product_internal_reference

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Inventory — Products |
| **Workflow** | Go to Inventory app. Open product "Steel Bracket 12" from the Products list. Change the Internal Reference field to "SB-12-BENCH". Click Save. |
| **Capability tested** | Simple text field edit on product form. Different from stock.adjust_inventory_quantities (inline tree editing) and inventory.scrap_product (wizard). |

---

## hr.update_employee_department

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Go to Employees app. Find employee "Sofia Chen". Change the Department field to "Engineering". Click Save. |
| **Capability tested** | Simple dropdown field edit on existing employee form. Different from hr.create_employee_complete_profile (multi-tab creation), hr.update_work_information (multi-tab editing), and hr.schedule_employee_activity (chatter dialog). |

---

## sale.add_discount_line

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Go to Sales app. Open draft quotation BENCH-DISC-01 for customer "Azure Interior". On the "Desk Organizer" line, set the Discount field to 10%. Click Save. |
| **Capability tested** | Inline order line editing with discount percentage field. Different from sale.change_validity_date (date field edit), sale.set_payment_terms_confirm (multi-field header edit), and sale.add_note_to_quotation (chatter interaction). |

---

## project.add_task_subtask

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Project — Tasks |
| **Workflow** | Go to Project app. Open project "Omega Platform Launch". Find task "Design Landing Page Mockup". In the Subtasks tab, add a new subtask titled "Create Wireframes". Save. |
| **Capability tested** | Subtask creation on existing task via subtasks tab. Different from project.post_chatter_message (chatter interaction), project.create_task_assign_stage (task creation), project.set_task_deadline (date edit), and project.complete_task_log_note (stage change + note). |

---

## account.update_customer_invoice_terms_post

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Accounting — Customer Invoices |
| **Workflow** | Open draft customer invoice `MED-CINV-01` for Brightstar Labs. Update invoice date, payment terms, customer reference, and the existing Support Review quantity, then post. |
| **Capability tested** | Existing-record edit inside Accounting with a header many2one, a date picker, one inline line change, and a distractor invoice that must stay untouched. |

---

## crm.update_opportunity_revenue_priority_won

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL/FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM — Pipeline |
| **Workflow** | Open opportunity `Northwind Renewal Review`, update Expected Revenue, set Priority to Medium with the star widget, and click Won. |
| **Capability tested** | Existing-record CRM editing with a star-priority control plus an explicit header workflow action, while a similarly named distractor must remain untouched. |

---

## hr.update_work_location_schedule_activity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/FAIL |
| **F1** | 1.0 |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Open employee `Avery Collins`, change Work Phone, switch to the Work tab to set Work Location to Home, save, then schedule a Call activity with an exact summary and due date. |
| **Capability tested** | Multi-area employee editing plus chatter activity scheduling in one flow, without changing the employee's job or department. |

---

## purchase.update_rfq_reference_deadline_confirm

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase — RFQs |
| **Workflow** | Open draft RFQ `MED-RFQ-REF-01` for North Coast Components. Update vendor reference, change the order deadline, adjust the existing Dock Seal Kit quantity, and confirm the order. |
| **Capability tested** | Purchase form editing that mixes header fields and inline line changes, plus a distractor RFQ that must remain in draft. |

---

## contacts.create_linked_contact_add_finance_tag

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Create a new child contact `Dana Patel` under `Lakeshore Manufacturing`, fill contact details and address, add the Finance tag, and save. |
| **Capability tested** | Contact creation with parent-company selection, address fields, and tag entry while avoiding a similarly named distractor company. |

---

## inventory.scrap_product

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Navigate to product `Steel Bracket 12` from the Products list. Click the Scrap button. In the Scrap dialog, set Quantity to `5` and accept the defaults. Click **Scrap** to confirm. |
| **Capability tested** | Accept-defaults wizard flow in Inventory: open the scrap dialog, enter one quantity, and confirm without changing other product data. |

---

## hr.schedule_employee_activity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Find employee `Sofia Chen`. Click **Schedule Activity** in the chatter. Set Activity Type to `Call`, Due Date to `May 10, 2026`, Summary to `Annual review discussion`, then click **Schedule Activity**. |
| **Capability tested** | Activity scheduling through the chatter modal with multiple fields in a compact dialog, distinct from simple employee form edits. |

---

## project.set_task_deadline

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project — Tasks |
| **Workflow** | Open project `Omega Platform Launch`, find task `Design Landing Page Mockup`, change the Deadline to `May 20, 2026` via the date picker, and save. |
| **Capability tested** | Existing-task date edit through the Project UI, focused on date-picker interaction without additional chatter or stage changes. |

---

## sale.duplicate_quotation_change_customer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open draft quotation `BENCH-DUP-01`, duplicate it via the Action menu, change the customer on the copy to a different partner, set a new customer reference, and save the duplicate in draft. |
| **Capability tested** | Action-menu Duplicate flow combined with swapping a many2one field on the copy while leaving the original untouched. |

---

## purchase.duplicate_rfq_change_vendor_confirm

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Purchase — RFQs |
| **Workflow** | Duplicate draft RFQ `BENCH-RFQ-DUP` (Meridian Supply Co), change vendor on the copy to Pinnacle Hardware, set vendor reference `PH-REISSUE-77`, then click Confirm Order. |
| **Capability tested** | Duplicate-and-reassign on purchase module followed by confirmation, testing whether the agent edits the copy (not the original) and confirms only the copy. |

---

## project.archive_task_with_log_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Project |
| **Workflow** | Open project `Nexus Platform Launch`, open the task `Retire beta build`, post a specific internal log note, then archive via the Action menu. |
| **Capability tested** | Combined chatter Log-note posting and Action-menu Archive on a project task with another task on the same project as distractor. |

---

## crm.convert_lead_to_opportunity_simple

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM — Leads/Pipeline |
| **Workflow** | Enable Leads setting, open lead `Spark Innovations - Pager SaaS`, click Convert to Opportunity, link to existing customer `Spark Innovations`, submit the wizard. |
| **Capability tested** | Lead-to-opportunity conversion wizard with existing-partner selection, distinct from scheduling or tagging flows. |

---

## hr.unarchive_employee_update_department

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | HR — Employees |
| **Workflow** | Apply the Archived filter, open employee `Avery Collins`, use Action menu Unarchive, then set Department to Engineering and save. |
| **Capability tested** | Filter toggle + Action-menu Unarchive + subsequent field edit, distinct from other hr tasks that only edit an active employee. |

---

## stock.validate_delivery_shipment

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Inventory — Transfers |
| **Workflow** | Open outgoing delivery `BENCH-DEL-01`, set done quantities on each move line to the planned values, click Validate. |
| **Capability tested** | Operations on outgoing delivery move lines with a distractor delivery that must stay in pending state. |

---

## account.create_bill_from_confirmed_po

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase → Accounting |
| **Workflow** | Open confirmed PO `BENCH-BILL-PO`, click the Create Bill stat button, set bill date and vendor reference on the draft bill, and Confirm (post) it. |
| **Capability tested** | Cross-module stat-button navigation from Purchase to Accounting, followed by filling bill-specific fields and posting. |

---

## sale.cancel_quotation_log_reason

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/FAIL |
| **F1** | 1.0/0.0 |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open draft quotation `BENCH-CANCEL-01` among two distractors, post a specific internal log note, then click Cancel and confirm the dialog. |
| **Capability tested** | Chatter Log-note posting combined with a state-changing Cancel action while keeping distractor quotations untouched. |

---

## hr_recruitment.refuse_applicant_with_reason

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment |
| **Workflow** | Open job `Senior Platform Engineer`, open applicant `Marcus Whitfield`, click Refuse, set Refuse Reason to `Does not fit the job requirements` in the wizard, uncheck Send Email, apply. |
| **Capability tested** | Refuse-wizard interaction with a non-default many2one and an explicit email-off toggle, distinct from applicant-creation and stage-move tasks. |

---

## crm.mark_opportunity_won_update_revenue

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM — Pipeline |
| **Workflow** | Open opportunity `Crestline Networks - Managed VPN` among similarly-named distractors, update expected revenue to 52000, then click the Won status-bar button. |
| **Capability tested** | Field edit + state-bar Won action on a single opportunity among look-alike distractors, distinct from lost/schedule-call CRM tasks. |

---

## account.create_customer_invoice_post

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Customer Invoices |
| **Workflow** | Create a new customer invoice for `Northwind Advisory`, set invoice date `2026-06-10`, set customer reference `NWA-AR-220`, add two exact product lines, then confirm it. |
| **Capability tested** | Accounting create-from-scratch flow on the customer-invoice form with multiple exact fields, distinct from vendor-bill creation and from edit-an-existing-invoice tasks. |

---

## account.partial_pay_vendor_bill_with_memo

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Accounting — Vendor Bills |
| **Workflow** | Open posted vendor bill `VB-PARTIAL-01`, register a payment, change the amount to a partial value, set memo `PARTIAL-JUN-600`, set payment date `2026-06-12`, and create the payment. |
| **Capability tested** | Payment wizard interaction with a non-default amount plus memo/date edits, distinct from the existing full-payment customer-invoice task. |

---

## calendar.create_all_day_event_with_attendee

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Create all-day event `Operations Offsite` on `2026-06-18`, set location and description, add `Marc Demo` as attendee, and save it as a one-time event. |
| **Capability tested** | Calendar creation flow using the all-day toggle plus attendee selection, distinct from timed event creation and from editing existing events. |

---

## contacts.create_company_add_supplier_tag

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Create company `North Coast Fabrication`, fill address and communication fields, add the `Supplier` tag, and save. |
| **Capability tested** | New-company creation with several address fields and a tag widget, distinct from editing an existing company and from creating a linked child contact. |

---

## crm.create_lead_priority_schedule_call

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (spec) |
| **Browser-Use** | — |
| **F1** | — |
| **Notes** | Removed because standard Odoo lead UI does not expose `expected_revenue` for records that remain `type = lead`, so the requested workflow is not browser-solvable without changing the task spec. |
| **Odoo modules** | CRM — Leads |
| **Workflow** | Create lead `Apex Warehouse Expansion`, set expected revenue and 2-star priority, then schedule a Call activity with exact summary and due date. |
| **Capability tested** | Lead creation plus star-priority control and activity scheduling, distinct from opportunity editing and from lead-conversion tasks. |

---

## hr.assign_manager_set_work_location

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Employees (hr) |
| **Workflow** | Open employee `Maya Ortiz`, set manager `Nadia Reyes`, set work location `HQ Annex`, update work phone, and save. |
| **Capability tested** | Multi-field employee edit centered on reporting-line and location fields, distinct from the repo's timezone/certificate and activity-scheduling HR tasks. |

---

## hr_recruitment.schedule_interview_for_applicant

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Recruitment |
| **Workflow** | Open applicant `Riley Mercer` under `Operations Analyst` and schedule a Call activity due `2026-06-17` with summary `Schedule first interview`. |
| **Capability tested** | Applicant-form activity scheduling without creation or stage movement, distinct from applicant creation, refusal, and stage-advance flows. |

---

## project.duplicate_task_assign_deadline

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Open task `Prepare webinar outline`, duplicate it from the Action menu, rename the copy to `Prepare webinar outline - APAC`, set a deadline, and move it to `In Progress`. |
| **Capability tested** | Project-task duplication followed by edits on the copy only, distinct from fresh task creation, subtask creation, and archive/log-note tasks. |

---

## purchase.cancel_rfq_log_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase — RFQs |
| **Workflow** | Open draft RFQ `P-RFQ-CANCEL-01`, post an internal log note with exact text, then cancel the RFQ. |
| **Capability tested** | RFQ cancellation paired with chatter log-note usage, distinct from purchase confirmation, duplicate-copy, and line-edit confirmation workflows. |

---

## sale.update_salesperson_validity_confirm

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales — Quotations |
| **Workflow** | Open quotation `S-QUOTE-VAL-01`, set salesperson `Marc Demo`, set expiration date `2026-06-25`, add customer reference `CGS-JUNE`, and confirm it. |
| **Capability tested** | Header-field edit plus confirmation without touching line items, distinct from discount-line editing, cancel/log-note flows, and duplicate-quotation tasks. |

---

## crm.convert_lead_link_customer_schedule_call

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM — Leads |
| **Workflow** | Find lead `Summit Ridge Support Rollout`, convert it with the opportunity wizard by linking existing customer `Summit Ridge Manufacturing`, set the stage to `Qualified`, and save if needed. |
| **Capability tested** | Lead-to-opportunity conversion through a wizard with existing-customer selection, distinct from simple opportunity edits and from win/loss stage tasks. |

---

## purchase_stock.confirm_rfq_receive_full

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Purchase, Inventory |
| **Workflow** | Open RFQ `MED-RECV-PO-01`, confirm it, follow the generated receipt, set Done quantities for both lines to the ordered amounts, and validate without creating a backorder. |
| **Capability tested** | Cross-app RFQ-to-receipt handoff plus exact stock receipt validation across multiple lines, distinct from simple purchase confirmation or single-form edits. |

---

## sale.create_invoice_register_payment_memo

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Accounting |
| **Workflow** | Open confirmed sales order `PAYFLOW-01`, create the draft invoice, confirm it, then register payment with the exact date `05/21/2026` and memo `PAYFLOW-MAY-SETTLEMENT`. |
| **Capability tested** | Sales-to-accounting document handoff with sequential invoice and payment wizards, distinct from quote confirmation and invoice line-adjustment tasks. |

---

## contacts.create_company_add_supplier_finance_tags

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Create company `Harborview Components`, set the exact phone and website, add the `Supplier` tag, and save while leaving the similarly named distractor company unchanged. |
| **Capability tested** | Fresh company creation with company/person mode selection, tag autocomplete, and duplicate avoidance, distinct from the repo's address-heavy company-creation and linked-contact tasks. |

---

## project.create_subtask_assign_deadline

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Project |
| **Workflow** | Open task `Prepare onboarding checklist`, create subtask `Draft kickoff agenda` from the Sub-tasks tab, assign it to `Administrator`, move it to `In Progress`, and save. |
| **Capability tested** | Inline one2many subtask creation with assignee and stage updates on the child task only, distinct from top-level task editing, duplication, or chatter-note project flows. |

---

## crm.convert_lead_qualify

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | CRM — Leads |
| **Workflow** | Open CRM Leads, find `Silver Maple Network Refresh`, convert it with the default opportunity wizard, then move it to `Qualified` without creating a quotation. |
| **Capability tested** | Lead-conversion wizard followed by a stage transition on the same record, distinct from customer-link conversion and from won/lost opportunity tasks. |

---

## project.convert_task_to_subtask

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/PASS |
| **F1** | 1.0 |
| **Odoo modules** | Project |
| **Workflow** | Open project `Atlas Support Rollout`, convert task `Vendor readiness checklist` into a sub-task, and set parent task `Launch coordination`. |
| **Capability tested** | Task action-menu conversion into a sub-task with exact parent assignment, distinct from duplicate-task and subtask-creation workflows. |

---

## hr.add_resume_line_update_location

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Employees |
| **Workflow** | Open employee `Marina Ortega`, change Work Location to `Home`, add one Resume entry in the `Certification` section, and save. |
| **Capability tested** | Cross-tab employee editing plus resume-widget creation with exact dates, distinct from simpler work-information and activity-scheduling employee tasks. |

---

## hr_recruitment.add_skill_move_stage

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL/FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Recruitment |
| **Workflow** | Open applicant `Jordan Park`, move them to `First Interview`, add one `Python` skill at `Advanced`, and save. |
| **Capability tested** | Applicant-stage transition plus skill-widget entry on the same form, distinct from stage-only recruitment tasks and interview-scheduling flows. |

---

## contacts.create_company_set_supplier_tag

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS* |
| **F1** | — |
| **Odoo modules** | Contacts |
| **Workflow** | Create company `Harborview Fabrication`, set email, phone, website, add the `Supplier` tag, and save. |
| **Capability tested** | Fresh company creation with core-field entry, tag autocomplete, and explicit company/person mode handling, distinct from address-heavy company creation and linked-contact tasks. |

Note: difficulty calibration used a shared-port browser-use validation on `benchmark_validate` / `127.0.0.1:8069`. Isolated-port runs were contaminated by the agent drifting to the shared `8069` server, so they were not used for the final medium-tier judgment.

## calendar.create_event_add_description_attendee

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Create one non-recurring calendar event with an exact attendee, location, and description, then save it at the requested date and time. |
| **Capability tested** | Fresh event creation with date/time entry plus attendee lookup and rich-text field entry, distinct from recurrence-edit and existing-event update calendar tasks. |

---

## contacts.create_linked_contact_set_title_phone

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Open a company contact, create one linked person contact beneath it, and set the linked contact's job position, phone, and email before saving. |
| **Capability tested** | Parent-child contact creation on an existing company form, distinct from company-creation and tag-focused contact tasks. |

---

## crm.create_opportunity_set_close_date_priority

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM |
| **Workflow** | Create a new opportunity with an exact expected revenue, set its expected closing date, and apply a star priority before saving. |
| **Capability tested** | Opportunity creation with mixed numeric, date-picker, and star-widget inputs, distinct from convert-lead and activity-scheduling CRM tasks. |

---

## hr.add_resume_line_update_mobile

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Employees |
| **Workflow** | Open an employee, change the mobile number, add one exact Resume entry on the Resume tab, and save. |
| **Capability tested** | Cross-tab employee editing that combines a standard field edit with resume-widget creation, distinct from skill-entry and work-location employee tasks. |

---

## hr_recruitment.create_applicant_set_email_stage

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Recruitment |
| **Workflow** | Create a new applicant for a named job opening, set the applicant email and phone, move the applicant to the requested stage, and save. |
| **Capability tested** | New applicant creation followed by a stage transition on the same record, distinct from interview-scheduling and refusal-wizard recruitment tasks. |

---

## project.create_task_assign_tags_deadline

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Open a target project, create one task with an exact title, assign it, add specified tags, set a deadline, and save. |
| **Capability tested** | New task creation with many2many tag entry and a deadline picker, distinct from subtask and archive-note project tasks. |

---

## project.rename_task_assign_tags_priority

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Project |
| **Workflow** | Open an existing task, rename it, assign one tag, change its priority, and save without changing its stage. |
| **Capability tested** | Targeted task editing with the star-priority widget and tag autocomplete, distinct from task-creation and activity-scheduling project tasks. |

---

## purchase.update_rfq_note_quantity_confirm

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Purchase |
| **Workflow** | Find the correct RFQ, update the internal notes field, change one existing line quantity, and confirm the order. |
| **Capability tested** | Same-record RFQ editing that mixes a multiline note field with inline order-line editing before confirmation, distinct from deadline-focused purchase tasks. |

---

## sale.update_quote_payment_terms_validity_confirm

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales |
| **Workflow** | Open the right quotation, set payment terms and a validity date, adjust one existing line quantity, and confirm it. |
| **Capability tested** | Quotation edit-and-confirm flow that combines many2one payment-term selection, date entry, and inline line editing, distinct from note-only and cancellation sales tasks. |

---

## stock.update_delivery_scheduled_date_validate

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Inventory / Stock |
| **Workflow** | Open an existing delivery, set a requested scheduled date, then validate the transfer without changing quantities. |
| **Capability tested** | Pick-and-validate stock workflow with a date edit on the transfer form, distinct from receipt validation, reorder-rule editing, and return/backorder stock tasks. |

---

## sale.create_quotation_down_payment_invoice

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales, Accounting |
| **Workflow** | Create new quotation for Ridgeline Automation with 2 exact product lines ($1200 + $350), confirm, open Create Invoice wizard, select "Down payment (percentage)" (not default "Regular invoice"), set 30%, create draft, set invoice date, confirm. |
| **Capability tested** | Non-default radio selection in wizard (advance_payment_method = 'percentage'), create-from-scratch with exact lines, cross-module Sales → Accounting navigation. |

---

## account.create_refund_modify_reissue

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Accounting |
| **Workflow** | Open posted invoice HLE-MOD-01, click Credit Note, click "Reverse and Create Invoice" (NOT default "Reverse"), edit new draft's Technical Audit line qty from 8 to 5, set invoice date, confirm. |
| **Capability tested** | Non-default button choice in credit note wizard (modify_moves vs refund_moves), post-wizard line editing, distractor invoice with similar name. |

---

## purchase.create_rfq_confirm_receive_backorder

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Purchase, Inventory |
| **Workflow** | Create new RFQ with 3 exact product lines, confirm, navigate to receipt via smart button, set partial done quantities, validate with "Create Backorder" dialog. |
| **Capability tested** | Create-from-scratch with 3 exact lines (phantom line issue), cross-module Purchase → Stock, backorder dialog with non-default choice, inline quantity editing. |

---

## stock.return_delivery_create_credit_note

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Inventory, Sales, Accounting |
| **Workflow** | Open done delivery, create partial return via wizard (4 of 10 units, skip other product), validate return, navigate to SO's invoice, create credit note with reason and date, confirm. |
| **Capability tested** | Return wizard quantity editing, cross-module Stock → Sales → Accounting round-trip, credit note creation from reversed invoice. |

---

## crm.create_opportunity_add_quotation_send

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | CRM, Sales |
| **Workflow** | Create CRM opportunity with exact fields, move to Qualified, click New Quotation, add 2 exact product lines ($8500 + $12000), set ref and expiration, send by email with custom subject. |
| **Capability tested** | Cross-module CRM → Sales, create-from-scratch quotation lines, email compose wizard, kanban quick-create then full form editing. |

---

## sale_stock.confirm_order_deliver_partial_backorder

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales, Inventory |
| **Workflow** | Confirm draft SO with 3 lines, navigate to delivery via smart button, set partial done quantities (15/25, 40/40, 6/20), validate, choose "Create Backorder". |
| **Capability tested** | Cross-module Sales → Stock via smart button, inline quantity editing on stock moves, backorder dialog with non-default choice. |

---

## hr_recruitment.create_applicant_add_skills_refuse

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Recruitment |
| **Workflow** | Open job position, create new applicant with exact details, add skill via cascading selects (Languages/Python/Advanced), save, then refuse via wizard with specific reason and unchecked email. |
| **Capability tested** | Skill widget cascading selects, refuse wizard with non-default many2one, combined create + wizard flow, distractor applicant with similar name. |

---

## sale.cancel_confirmed_recreate_send_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales |
| **Workflow** | Cancel confirmed SO (confirmation dialog), create new quotation for different customer with modified quantities, set ref and expiration, send by email with custom subject. |
| **Capability tested** | Cancel confirmation dialog, create-from-scratch with exact lines (phantom line issue), email compose wizard. |

---

## calendar.create_recurring_edit_two_occurrences

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Calendar |
| **Workflow** | Create weekly recurring event (6 occurrences) with attendees, then navigate to 2 different future occurrences and edit each one's location, choosing "This Event" in the recurrence dialog each time. |
| **Capability tested** | Full recurring event creation with date/time pickers, TWO separate recurrence "This Event" dialog interactions, calendar navigation to specific dates. |

---

## website.edit_page_update_text_set_properties

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Website |
| **Workflow** | In website editor, edit heading and paragraph text within the iframe, then use Site > Properties dialog to change page title and URL slug, save. |
| **Capability tested** | Website editor iframe interaction, text editing in complex DOM, Page Properties dialog, combined content + metadata editing. |

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

---

## appointment.portal_reschedule_and_cancel_booking

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Notes** | Removed because the `appointment` addon is not present in this checkout, so the workflow cannot be implemented or validated on branch `odoo_benchmark` in the current environment. |
| **Odoo modules** | Appointments, Website/Portal |
| **Workflow** | Create an appointment configuration, book a portal slot, then reschedule and cancel the booking from the portal. |
| **Capability tested** | Backend-to-portal handoff with public booking plus portal reschedule/cancel actions. |

---

## helpdesk.create_ticket_tag_schedule_activity_resolve

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Notes** | Removed because the `helpdesk` addon is not present in this checkout, so the workflow cannot be implemented or validated on branch `odoo_benchmark` in the current environment. |
| **Odoo modules** | Helpdesk |
| **Workflow** | Create a helpdesk ticket, apply a tag, schedule a follow-up activity, and resolve the ticket. |
| **Capability tested** | Ticket lifecycle edits combining tagging, activity scheduling, and resolution state change. |

---

## survey.branching_quiz_publish_share_link

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Survey |
| **Workflow** | Create a survey with branching or scoring behavior, publish it, and copy the share link. |
| **Capability tested** | Survey builder navigation with multi-step question setup, logic/scoring configuration, publication, and link retrieval. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## project_todo.duplicate_note_retag_archive_original

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | To-Do |
| **Workflow** | Duplicate an existing To-Do note, retag the duplicate, and archive the original note only. |
| **Capability tested** | Action-menu duplication plus selective archive and tag editing across original vs duplicate records. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## im_livechat.configure_offline_form_and_test_widget

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Live Chat, Website |
| **Workflow** | Configure a live chat channel's offline behavior, then verify the website widget shows the offline contact form path. |
| **Capability tested** | Backend chat-channel settings plus public website widget verification across two UI surfaces. |

---

## point_of_sale.split_payment_email_receipt

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Point of Sale |
| **Workflow** | Open a POS session, ring up a sale, split the payment across two methods, and email the receipt to the customer. |
| **Capability tested** | Full-screen kiosk interaction, keypad payment entry, multi-payment flow, and receipt-delivery workflow. |

---

## website_sale.configure_optional_products_add_upsell_to_cart

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website Sale, Website |
| **Workflow** | Configure optional products for a webshop item, publish it, and add the upsell combination to the storefront cart. |
| **Capability tested** | Backend ecommerce configuration followed by public storefront add-to-cart with optional-product selection. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## fleet.create_contract_set_renewal_activity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Fleet |
| **Workflow** | Create or update a vehicle contract, set renewal metadata, and schedule a renewal reminder activity. |
| **Capability tested** | Fleet contract management with date fields and chatter activity scheduling on the same vehicle record. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment, so the task needs cross-review before being marked Done. |

---

## hr_recruitment.schedule_second_interview_with_feedback

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Recruitment |
| **Workflow** | Move a target applicant forward, schedule a second interview, and record the requested interviewer feedback. |
| **Capability tested** | Recruitment stage progression combined with interview planning and evaluation note handling. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## calendar.create_private_meeting_with_video_link

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Create a private calendar meeting with attendees and an exact video-call link. |
| **Capability tested** | Event creation using privacy controls, attendee selection, and conferencing metadata. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment, so the task needs cross-review before being marked Done. |

---

## mail.create_channel_set_description_pin_welcome

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Discuss |
| **Workflow** | Create a discussion channel, set its description, post a welcome message, and pin that message. |
| **Capability tested** | Discuss channel creation plus channel-settings edit and in-thread message pinning. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## hr_expense.create_mileage_expense_submit_report

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Expenses |
| **Workflow** | Create a mileage-based expense entry, attach it to an expense report, and submit it for approval. |
| **Capability tested** | Expense form creation with mileage-specific fields and report-submission workflow. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment, so the task needs cross-review before being marked Done. |

---

## hr_holidays.allocate_leave_then_request_against_balance

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Time Off |
| **Workflow** | Allocate leave days to an employee, then switch context and request time off against that new balance. |
| **Capability tested** | Manager-to-employee workflow handoff combining allocation and subsequent request creation. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## contacts.create_company_with_invoice_and_delivery_addresses

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Create a company contact and add distinct invoice and delivery child addresses beneath it. |
| **Capability tested** | Parent-company creation with multiple child-contact address types and nested save flow. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## mrp.plan_workorder_block_resume_finish_mo

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Manufacturing |
| **Workflow** | Confirm a manufacturing order, start a work order, block it with a reason, resume it, and finish production. |
| **Capability tested** | Work-order execution controls with state transitions beyond BOM or MO creation alone. |

---

## stock.package_products_validate_delivery

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Inventory |
| **Workflow** | Open an outgoing delivery, package the products into a package, and validate the shipment. |
| **Capability tested** | Delivery operation handling with package creation and final stock validation. |

---

## barcodes.receive_product_via_scan_validate

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Barcode, Inventory |
| **Workflow** | Open a barcode receipt flow, scan or enter the target product, and validate the received quantity. |
| **Capability tested** | Scanner-style inventory interaction rather than standard backend list/form editing. |

---

## delivery.configure_fixed_rate_carrier_confirm_sale

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Delivery, Sales |
| **Workflow** | Configure a fixed-price delivery method, apply it on a sales order, and confirm the quotation. |
| **Capability tested** | Shipping-method configuration followed by sales-order fulfillment setup on a quotation. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## hr_attendance.check_in_break_resume_check_out

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (spec) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Attendances |
| **Workflow** | Check in, start a break, resume work, and check out in the attendance interface. |
| **Capability tested** | Time-clock style attendance interactions with sequential status transitions. |
| **Notes** | Removed because this checkout's `hr_attendance` addon does not expose a break/resume workflow to implement or validate. |

---

## maintenance.create_request_assign_technician_mark_repaired

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Maintenance |
| **Workflow** | Create a maintenance request, assign the technician, and mark the request repaired. |
| **Capability tested** | Service-ticket style workflow with assignment and repair-state progression. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## repair.create_repair_order_add_parts_complete_invoice

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Repairs |
| **Workflow** | Create a repair order, add repair parts, complete the repair, and create the resulting invoice. |
| **Capability tested** | Repair-order lifecycle with part lines and downstream accounting side effect. |

---

## mass_mailing.build_campaign_send_test_schedule

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Email Marketing |
| **Workflow** | Build an email campaign, send a test email, and schedule the campaign for later delivery. |
| **Capability tested** | Campaign composer plus test-send and schedule actions in email marketing. |

---

## sale_loyalty.create_program_apply_reward_on_quotation

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales, Loyalty |
| **Workflow** | Create a loyalty or coupon program, then apply the reward on a target quotation. |
| **Capability tested** | Cross-configuration from loyalty setup into quotation-side reward application. |

---

## website_blog.create_post_with_cover_tag_publish

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Blog, Website |
| **Workflow** | Create a blog post with a cover image and tag, then publish it on the website. |
| **Capability tested** | Blog content authoring with metadata and website publication. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## website_slides.create_course_add_lesson_publish

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | eLearning, Website |
| **Workflow** | Create an eLearning course, add a lesson, and publish the course. |
| **Capability tested** | Structured course authoring with nested content creation and publication state management. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## event.create_event_add_ticket_publish [medium]

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Events |
| **Workflow** | Create an event with a specific date, add a paid ticket type, and set it to published. |
| **Capability tested** | Event form creation with nested ticket line and publication toggle. |

---

## fleet.add_vehicle_log_odometer [easy]

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Fleet |
| **Workflow** | Create a new vehicle record, then log an odometer reading via the dedicated odometer action. |
| **Capability tested** | Multi-step vehicle setup plus smart-button odometer logging action. |

---

## mrp.create_bom_with_components [medium]

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Manufacturing |
| **Workflow** | Create a Bill of Materials for a product with three specific components and quantities. |
| **Capability tested** | BOM form creation with multiple component lines and exact quantity values. |

---

## website_sale.publish_product_shop [easy]

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | eCommerce |
| **Workflow** | Find an unpublished product in the backend, set its sales price and publish it to the shop. |
| **Capability tested** | Backend product form edit with price field plus website publication toggle. |

---

## hr_holidays.allocate_leave_days [easy]

| Field | Value |
|---|---|
| **Status** | WIP |
| **Oracle** | — |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Time Off |
| **Workflow** | Create a leave allocation for a specific employee for Annual Leave and approve it. |
| **Capability tested** | Leave allocation form creation and manager approval action. |
