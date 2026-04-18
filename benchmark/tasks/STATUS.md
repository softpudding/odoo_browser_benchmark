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
| 142 | hr_holidays.allocate_leave_days [easy] | Allocate 15 days of Sick Time Off to an employee | Done (dup of 244) | — | — | — |
| 143 | hr_holidays.request_time_off_approve [medium] | Create Sick Time Off for employee, fill dates, save, and validate | Done | PASS | FAIL/PASS | 1.0 |
| 144 | hr_holidays.refuse_leave_request [medium] | Refuse a pending time-off request as manager | Done | PASS | PASS | 1.0 |
| 145 | hr_holidays.create_leave_type [medium] | Create a new Time Off Type with manager approval | Done | PASS | PASS | 1.0 |
| 146 | hr_holidays.cancel_approved_leave [medium] | Cancel an approved leave request via cancel wizard | Done (dup of 246) | — | — | — |
| 147 | mrp.create_bom_confirm_mo [medium] | Create a Bill of Materials with 3 components, then create and confirm a Manufacturing Order for 10 units | Done | PASS | FAIL | 0.0 |
| 148 | hr_expense.create_expense_report_submit [medium] | Create an expense line, attach it to a new expense report, and submit it for approval | Done | PASS | PASS | 1.0 |
| 149 | event.create_event_add_ticket [medium] | Create an event with one paid ticket and attendee limits | Done | PASS | FAIL | 0.0 |
| 150 | fleet.create_vehicle_log_odometer [medium] | Add a vehicle, record its odometer reading, and save the vehicle in service | Done | PASS | FAIL | 0.0 |
| 151 | website_sale.publish_product_set_price [medium] | Publish a product to the website shop and set its sales price and description | Done | PASS | PASS | 1.0 |
| 152 | point_of_sale.open_session_sell_product_cash [medium] | Open a POS session, ring up one product, and complete a cash payment | Done | PASS | PASS | 1.0 |
| 153 | im_livechat.create_channel_add_canned_response [medium] | Create a live chat channel and canned response from the Live Chat app | Done | PASS | PASS | 1.0 |
| 154 | website.create_blog_post_publish [medium] | Create and publish a blog post with title, cover image, and body content | Done | PASS | PASS | 1.0 |
| 155 | website.add_menu_item_reorder [medium] | Add a website menu item and reorder it within the navigation hierarchy | WIP | — | — | — |
| 156 | website.create_contact_form_block [hard] | Edit a website page to add and configure a contact form block | WIP | — | — | — |
| 157 | stock.scrap_product_from_receipt [medium] | Open a stock receipt and scrap part of a received product from the operation flow | WIP | — | — | — |
| 158 | stock.adjust_inventory_with_location_filter [medium] | Adjust inventory for a target product in one location while leaving other locations unchanged | WIP | — | — | — |
| 159 | stock.receive_serial_tracked_product [hard] | Validate a receipt by assigning exact serial numbers to tracked units | WIP | — | — | — |
| 160 | mrp.update_bom_component_quantity [medium] | Update one component quantity on an existing bill of materials and save it | Done (dup of 257) | — | — | — |
| 161 | mrp.create_mo_consume_produce_done [hard] | Create a manufacturing order, record component consumption, and mark production done | WIP | — | — | — |
| 162 | mrp.unbuild_product_partial [hard] | Unbuild part of a manufactured product quantity and verify the resulting stock moves | Done (near-dup of 256) | — | — | — |
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
| 188 | website.set_page_seo_fields [easy] | Use the Promote dialog to set meta title, description, and keywords on a page | Done | PASS | FAIL/FAIL | 0.6667 |
| 189 | website.add_image_snippet_swap_source [medium] | Drag an Image snippet into a page and swap its source image | WIP | — | — | — |
| 190 | website.duplicate_page_rename_unpublish [easy] | Duplicate an existing website page, rename the copy, and leave unpublished | Done | PASS | PASS/PASS | 1.0 |
| 191 | hr_holidays.approve_multiple_requests_bulk [hard] | Multi-select pending time-off requests in list view and bulk approve | WIP | — | — | — |
| 192 | hr_holidays.request_leave_with_attachment [medium] | Request leave and attach a PDF justification via the chatter | WIP | — | — | — |
| 193 | hr_expense.split_expense_analytic_distribution [hard] | Split one expense line 50/50 across two analytic accounts | WIP | — | — | — |
| 194 | hr_expense.refuse_report_with_reason_chatter [medium] | Refuse a submitted expense report and post the reason to chatter | WIP | — | — | — |
| 195 | hr_expense.post_approved_expense_to_journal [medium] | Manager posts an approved expense report to its journal entry | WIP | — | — | — |
| 196 | mail.star_and_reply_inbox_message [easy] | Star an inbox message and post a reply | Done | PASS | FAIL/FAIL | 0.0 |
| 197 | mail.mark_message_done_archive_notification [easy] | Mark Done on an inbox notification to remove it from Inbox | Done | PASS | FAIL/FAIL | 0.1667 |
| 198 | mail.create_group_channel_upload_attachment [medium] | Create a private channel, invite a member, and upload a file attachment | WIP | — | — | — |
| 199 | im_livechat.add_canned_response_send_in_chat [medium] | Create a canned response shortcut and send it in an operator chat | WIP | — | — | — |
| 200 | fleet.log_service_cost_record [easy] | Add a service cost record (oil change) to an existing vehicle | Done | PASS (32.1s) | FAIL (142.4s) | 0.00 |
| 201 | fleet.assign_vehicle_tags_category [easy] | Add two tags and set a category on a vehicle | Done | PASS | PASS | 1.0 |
| 202 | fleet.transfer_vehicle_new_driver [medium] | Change a vehicle's driver and set the new assignment date | WIP | — | — | — |
| 203 | event.add_event_questions_to_registration [medium] | Add two custom questions to an existing event registration form | WIP | — | — | — |
| 204 | event.create_event_tracks_session_schedule [hard] | Add two conference tracks with times to a published event | WIP | — | — | — |
| 205 | event.set_ticket_seat_availability_limit [easy] | Set total seat limit and per-ticket max for an event | Done | PASS | FAIL | 0.4 |
| 206 | stock.create_internal_transfer_between_locations [medium] | Create an internal transfer between two locations, add a line, and validate | Done (dup of 258) | — | — | — |
| 207 | stock.create_putaway_rule_for_product [hard] | Configure a putaway rule routing a product to a specific sub-location | WIP | — | — | — |
| 208 | stock.count_inventory_apply_with_date [medium] | Make an inventory adjustment with a specific counted date | WIP | — | — | — |
| 209 | stock.set_storage_category_capacity [medium] | Define a storage category with capacity and assign it to a location | WIP | — | — | — |
| 210 | account.create_manual_journal_entry_balanced [hard] | Create a misc journal entry with three balanced debit/credit lines and post | WIP | — | — | — |
| 211 | account.reconcile_bank_statement_line_manual [hard] | Open a bank statement line and reconcile it against a suggested invoice | WIP | — | — | — |
| 212 | account.create_recurring_entry_template [medium] | Save a journal entry as a recurring entry template | WIP | — | — | — |
| 213 | account.lock_books_set_period_lock_date [medium] | Set the Non-Advisors Lock Date in accounting settings | WIP | — | — | — |
| 214 | crm.set_lost_reason_reassign_salesperson [medium] | Mark opportunity Lost with specific reason then reassign salesperson | Done | PASS | — | — |
| 215 | crm.pivot_view_opportunities_by_stage_revenue [easy] | Switch CRM pipeline to Pivot view, group by stage, measure expected revenue | WIP | — | — | — |
| 216 | project.kanban_drag_task_between_stages [easy] | Drag a task kanban card from one stage to another | Done | PASS | FAIL | 0.0 |
| 217 | project.create_project_from_template_duplicate [medium] | Duplicate an existing project keeping its tasks | WIP | — | — | — |
| 218 | project.recurring_task_configure_frequency [medium] | Configure an existing task as recurring with weekly frequency | WIP | — | — | — |
| 219 | contacts.add_bank_account_to_partner [easy] | Add an IBAN bank account to an existing partner via Invoicing tab | Done | PASS | — | — |
| 220 | contacts.archive_partner_then_unarchive_filter [easy] | Archive a contact then unarchive it via the Archived search filter | Done (dup of 232) | — | — | — |
| 221 | calendar.invite_external_attendee_by_email [easy] | Create a calendar event inviting an external email address not in partners | Done | PASS | PASS | 1.0 |
| 222 | survey.create_survey_one_page_publish_share [medium] | Create a 3-question survey, publish it, and copy the share link | WIP | — | — | — |
| 223 | project_todo.create_note_add_tag_checklist [easy] | In the To-Do app, create a note with a tag and a checklist item | Done | PASS | PASS/FAIL | 0.5 |
| 224 | hr_holidays.request_annual_leave [easy] | Done | PASS | PASS | 1.0 |
| 225 | hr_holidays.approve_leave_as_manager [medium] | Approve a pending leave request from manager approvals view | Done | PASS | PASS | 1.0 |
| 226 | hr_holidays.refuse_leave_with_reason [medium] | Done | PASS | PASS | 1.0 |
| 227 | hr_expense.create_expense_with_receipt [medium] | Done | PASS | PASS | 1.0 |
| 228 | hr_expense.submit_report_for_approval [medium] | Create an expense and submit it to the manager for approval | Done | PASS | PASS | 1.0 |
| 229 | mail.create_channel_invite_members [easy] | Create a Discuss channel and invite internal users as members | Done | PASS | FAIL | 0.0 |
| 230 | mail.pin_and_reply_in_chatter [easy] | Done | PASS | PASS | 1.0 |
| 231 | contacts.merge_duplicate_contacts [hard] | Done | PASS | PASS | 1.0 |
| 232 | contacts.archive_then_unarchive [easy] | Done | PASS | FAIL | 0.00 |
| 233 | website.create_blog_post_publish [medium] | Duplicate of 154 | — | — | — |
| 234 | website.edit_menu_add_page_link [medium] | Add a new menu entry linked to an existing website page | Done | PASS | PASS | 1.0 |
| 235 | stock.create_putaway_rule [hard] | Create a putaway rule routing a product to a specific sub-location | Done | PASS | PASS | 1.0 |
| 236 | stock.transfer_lot_tracked_product [hard] | Validate a receipt for a lot-tracked product with specific lot number and quantity | Done | PASS | PASS | 1.0 |
| 237 | mrp.create_bom_three_components [medium] | Create a Bill of Materials for a product with three components | Done | PASS | FAIL | 0.0 |
| 238 | mrp.confirm_produce_close_mo [hard] | Confirm a draft MO and close it by producing the finished product | Done | PASS | PASS | 1.0 |
| 239 | website_sale.publish_shop_product [medium] | Open a storable product, set its list price and website description, and publish it to the shop | Done | PASS | FAIL | 0.0 |
| 240 | appointment.create_type_set_slots [medium] | Removed | — | — | — |
| 241 | event.create_event_configure_ticket [medium] | Create an event with dates and venue and configure a ticket type with price and seat limit | Done | PASS | FAIL | 0.7368 |
| 242 | helpdesk.create_ticket_assign_priority [medium] | Removed | — | — | — |
| 243 | fleet.register_vehicle_log_odometer [easy] | Register a new fleet vehicle and log an odometer reading for it | Done | PASS | PASS | 1.0 |
| 244 | hr_holidays.allocate_sick_leave_to_employee [easy] | Done | PASS | PASS | 1.0 |
| 245 | hr_holidays.request_half_day_morning [easy] | Done | PASS | PASS | 1.0 |
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
| 274 | delivery.configure_weight_rules_carrier_apply_to_so [medium] | Configure a weight-tier shipping carrier and apply the correct tier to a sale order | Done | PASS | PASS/FAIL | 0.5 |
| 275 | maintenance.create_equipment_assign_category_team [easy] | Create a new equipment record, assign it to a category and maintenance team | Done | PASS | FAIL | 0.0 |
| 276 | maintenance.schedule_preventive_plan_recurring [medium] | Schedule a recurring preventive maintenance plan with interval and team assignment | Done | PASS | PASS | 1.0 |
| 277 | sale_stock.partial_stock_warning_confirm_anyway [hard] | Confirm a sale order with insufficient stock and validate delivery as backorder | Done | PASS | FAIL | 0.857 |
| 278 | survey.create_feedback_survey_with_sections [medium] | Create a multi-section feedback (non-quiz) survey with time limit and publish | Done | PASS | PASS | 1.0 |
| 279 | survey.review_submitted_responses_filter [medium] | Open survey participations, filter results, and post a review note on a target response | Done | PASS | PASS | 1.0 |
| 280 | im_livechat.configure_url_rule_auto_message [medium] | Add a URL-match rule to a livechat channel that triggers an auto-greeting on a specific page | Done | PASS | PASS | 1.0 |
| 281 | sale_project.timesheet_task_mark_billable_log_hours [hard] | Log timesheet hours on a sale-generated project task, mark billable, and verify invoice-ready state | Removed | FAIL (spec) | — | — |
| 282 | project_todo.reorder_notes_add_due_dates_bulk [easy] | Set due dates on three seeded To-Do notes from the Kanban view | Done | PASS | PASS | 1.0 |
| 283 | website_hr_recruitment.publish_job_from_backoffice_then_apply_portal [hard] | Create and publish a job position in the back office, then apply to it from the public portal | Done | PASS | FAIL | 0.0 |
| 284 | mass_mailing.create_segmented_mailing_save_draft [medium] | Create an email mailing with a filtered Contacts recipient list and save as draft | Done | PASS | FAIL | 0.667 |
| 285 | event_sale.configure_paid_ticket_register_with_invoice [hard] | Configure a paid event ticket, register an attendee, confirm registration, and generate the invoice | Done | PASS | FAIL | 0.0 |
| 286 | inventory.run_replenishment_from_dashboard [medium] | Run replenishment for a low-stock product from the Replenishment dashboard | Done | PASS | PASS | 1.0 |
| 287 | sale_project.deliver_milestone_invoice_partially [hard] | Mark one of three SO milestones delivered and create an invoice for that milestone only | Done | PASS | PASS | 1.0 |
| 288 | website_sale.unpublish_archive_unarchive_publish_cycle [medium] | Take a published shop product through Unpublish → Archive → Unarchive → Publish | Done | PASS | PASS | 1.0 |
| 289 | website_blog.edit_post_change_author_add_tags_schedule [medium] | Edit a seeded blog post: change author, add two tags, and set the publish date | Done | PASS | FAIL | 0.0 |
| 290 | website_slides.add_quiz_lesson_to_existing_course [hard] | Add a multi-question quiz lesson with answers to an existing course and publish | Done | PASS | FAIL | 0.0 |
| 291 | sale_purchase.dropship_so_to_po_chain_validate [hard] | Confirm a dropship-routed SO and validate the auto-generated PO + receipt chain | Done | PASS | PASS | 1.0 |
| 292 | mail.create_channel_set_custom_avatar_pin_two_messages [medium] | Create a channel, upload a custom avatar, post messages, and pin two specific ones | Done | PASS | FAIL | 0.0 |
| 293 | fleet.transfer_vehicle_between_drivers_log_history [medium] | Transfer a vehicle to a new driver and verify the assignation log entry | Done | PASS | PASS | 1.0 |
| 294 | sale_loyalty.create_loyalty_program_apply_at_checkout [hard] | Create a Discount Code loyalty program (SPRING10, $150 min purchase, 10% on order, custom reward description) and apply it on /shop/cart so a discount line appears | Done | PASS | PASS | 1.0 |
| 295 | event_sale.add_seat_limited_ticket_register_until_full [medium] | Add a 5-seat limited ticket to an event and register attendees until the seats fill | Done | PASS | FAIL | 0.0 |
| 296 | sale_purchase.update_pol_alternative_vendor_compare [hard] | Open RFQ, add two alternative-vendor RFQs at different prices, then cancel the losers and confirm the cheapest via the alternative-warning wizard | Done | PASS | FAIL | 0.0 |
| 297 | delivery.set_third_party_carrier_print_label [medium] | Configure a fixed-price carrier, apply it to a confirmed delivery picking with tracking ref, validate and trigger Print | Done | PASS | PASS | 1.0 |
| 298 | inventory.create_storage_category_assign_to_location [medium] | Create a storage category with capacity rules and assign it to a stock location | Done | PASS | FAIL | 0.0 |
| 299 | sale_stock.deliver_partial_split_into_two_pickings [hard] | On a multi-line SO, deliver partial (force inline-cell edit), create backorder, then on the backorder edit Done from auto-reserved 5 to 0 and SAVE without validating | Done | PASS | FAIL | 0.0 |
| 300 | website_blog.create_blog_with_two_posts_archive_one [medium] | Create blog 'Bench Insights' + 2 published posts, then archive only March Notes (active=False, kept in DB) | Done | PASS | FAIL | 0.0 |
| 301 | website_slides.duplicate_lesson_to_new_section [medium] | Add Advanced section, duplicate Welcome Video lesson via Actions menu, move duplicate to Advanced and rename | Done | PASS | FAIL | 0.0 |
| 302 | im_livechat.assign_team_set_offline_form_message [medium] | Configure Live Chat channel via 3-dots Configure menu, switch Options tab, set notification text and welcome message | Done | PASS | PASS | 1.0 |
| 303 | maintenance.archive_equipment_create_replacement [medium] | Archive seeded 'Old Belt OB-99' via Actions, then create 'New Belt NB-100' with serial in same category | Done | PASS | PASS | 1.0 |
| 304 | project_todo.create_three_personal_with_specific_priorities [easy] | Create 3 personal to-dos; only Plan Sprint gets first priority star (Medium = '1'), others stay default | Done | PASS | FAIL | 0.0 |
| 305 | website_hr_recruitment.set_kanban_state_assign_recruiter [medium] | Open Diana Recruit, flip kanban_state ball to 'Ready for Next Stage', set Recruiter, post Log note | Done | PASS | PASS | 1.0 |
| 306 | purchase_stock.return_partial_with_distractor_lines [hard] | Multi-line PO return wizard: zero out 2 distractor lines and set qty=2 on third, then validate return | Done | PASS | FAIL | 0.0 |
| 307 | sale_project.invoice_completed_milestones_only [hard] | Open SO S-BENCH-MS-002, click Create Invoice, accept wizard's auto-detected qty=2, Create Draft | Done | PASS | PASS | 1.0 |
| 308 | survey.publish_share_via_link_get_url [easy] | Open seeded 'Customer Pulse Q2' survey, click Share, verify public /survey/start URL, close dialog | Done | PASS | PASS | 1.0 |
| 309 | point_of_sale.add_item_apply_global_discount_pay_cash [hard] | POS session: 2 items, open Actions popup, Discount 15%, pay cash, validate order | Done | PASS | PASS | 1.0 |
| 310 | mass_mailing.duplicate_existing_change_subject_recipients [medium] | Duplicate seeded 'Q1 Bulletin Template' via Actions→Duplicate, change subject and country=Germany filter | Done | PASS | FAIL | 0.0 |
| 311 | hr_holidays.refuse_then_re_request_other_type [hard] | Manager refuses Eves Paid Time Off, posts reason in chatter, then creates Sick Time Off on her behalf | Done | PASS | FAIL | 0.71 |
| 312 | calendar.create_event_with_two_organizers_recurring_weekly [medium] | Create weekly recurring Monday event 09:00-09:30 with 2 attendees and Discuss videocall link | Done | PASS | FAIL | 0.0 |
| 313 | mrp.scrap_component_during_partial_production [hard] | Open MO, cog Actions → Scrap (qty=2 ScrewA, tag Defective batch), validate scrap, then Produce All → Mark Done | Done | PASS | FAIL | 0.0 |
| 314 | crm.assign_team_change_salesperson_log_activity [medium] | Open Bench Big Deal, change Team to Channel + Salesperson Sara via Contacts tab, schedule Call activity | Done | PASS | PASS | 1.0 |
| 315 | website_sale.add_optional_at_cart_remove_main_keep_optional [hard] | Add Bench Camera + accept Tripod optional in modal, then remove only Camera at cart, leaving Tripod orphaned | Done | PASS | FAIL | 0.0 |
| 316 | hr_expense.create_with_currency_eur_to_usd [medium] | Create NYC Hotel expense in USD (200 USD = 185 EUR), employee paid, verify EUR conversion | Done | PASS | FAIL | 0.0 |
| 317 | event_product.create_event_product_link_to_ticket [medium] | Create Conference Pass Std service product (service_tracking=event), add Standard Pass ticket to Spring Summit | Done | PASS | PASS | 1.0 |
| 318 | website.create_contact_form_with_custom_field [hard] | Edit Contact Us page, add Selection field Inquiry Type with 3 options via website builder | Done | PASS | FAIL | 0.0 |
| 319 | contacts.merge_three_duplicates_keep_email [hard] | Merge 3 duplicate contacts into one, choosing email from a specific record | Done | PASS | FAIL | 0.0 |
| 320 | website_sale.create_gift_card_apply_in_cart [hard] | Configure Gift Card program, generate 1 €50 card code, apply in /shop/cart with €100 product | Done | PASS | PASS | 1.0 |
| 321 | hr.create_department_assign_manager_three_employees [medium] | Create Bench Engineering dept with manager Mike, then bulk assign 3 employees to it | Done | PASS | FAIL | 0.0 |
| 322 | stock.create_putaway_rule_for_specific_category [hard] | Create putaway rule routing a product category to a specific sub-location | Done | PASS | PASS | 1.0 |
| 323 | mail.invite_external_email_to_existing_channel [medium] | In existing channel, invite an external email (creates guest invitation) | Done | PASS | PASS | 1.0 |
| 324 | sale.add_line_with_optional_template_apply_discount [medium] | On a draft SO, add a line by selecting a template, then apply line-level 10% discount | Done | PASS | PASS | 1.0 |
| 325 | crm.create_lead_from_email_alias_log_message [hard] | Configure CRM team 'Inbound' alias + Accept-Emails-From, create lead with priority/tag, post chatter | Done | PASS | FAIL | 0.0 |
| 326 | project.create_kanban_stage_reorder_drag [medium] | In project Kanban view, create a new stage and reorder it before existing stages | Done | PASS | FAIL | 0.0 |
| 327 | account.create_recurring_journal_entry [hard] | Create a 3-line balanced journal entry (Rent 1000 + Tax 50 / Bank 1050), schedule To-Do activity for next month, Post | Done | PASS | PASS | 1.0 |
| 328 | website.add_image_carousel_to_homepage [hard] | In website editor, add Image Gallery (Carousel) snippet to a seeded page with 3 images | Done | PASS | PASS | 1.0 |
| 329 | hr_holidays.bulk_approve_two_pending_requests [hard] | Select 2 pending leave requests in list view, approve in bulk via action | Done | PASS | FAIL | 0.67 |
| 330 | event.add_track_with_speaker_publish [medium] | On existing event, add a track with speaker info and publish on website | Done | PASS | PASS | 1.0 |
| 331 | purchase.send_rfq_email_with_template_signature [hard] | On a draft RFQ click Send RFQ, switch template from 'Purchase: Request For Quotation' to 'Purchase: Purchase Order', append 'Please confirm by Friday.' to body, Send | Done | PASS | PASS | 1.0 |
| 332 | website_sale.set_product_seo_title_meta [easy] | Open product, set SEO title and meta description | Done | PASS | PASS | 1.0 |
| 333 | point_of_sale.attach_customer_apply_loyalty [hard] | In POS, attach a customer with loyalty card mid-sale and apply earned points | Done | PASS | PASS | 1.0 |
| 334 | website_blog.create_tag_assign_to_three_posts [medium] | Create a new tag, assign to 3 existing blog posts | Done | PASS | FAIL | 0.0 |
| 335 | hr_recruitment.skill_filter_then_send_offer [hard] | Filter applicants by skill='Python', open top match, send offer email | Done | PASS | PASS | 1.0 |
| 336 | sale.create_quotation_with_customer_pricelist [medium] | Create SO with a customer who has a specific pricelist; verify pricelist auto-applied | Done | PASS | PASS | 1.0 |
| 337 | calendar.invite_organize_with_event_agenda_attachment [hard] | Create calendar event 'Q2 Planning Session' 2026-05-20 14:00-15:30, add Alice+Bob attendees, upload agenda.txt via chatter paperclip | Done | PASS | FAIL | 0.0 |
| 338 | stock.cancel_picking_create_replacement_with_serial [hard] | Cancel an existing receipt picking, create a replacement with serial-tracked products | Done | PASS | FAIL | 0.0 |
| 339 | mrp_account.confirm_mo_check_account_move [medium] | Confirm an MO and verify the cost-of-production journal entry was created | Done | PASS | PASS | 1.0 |
| 340 | survey.invite_attendees_send_email [medium] | On existing survey, click Invite, enter 3 emails, customize subject, send | Done | PASS | PASS | 1.0 |
| 341 | hr.add_skill_to_employee_with_level [medium] | Open employee, add a skill with skill type and level | Done | PASS | PASS | 1.0 |
| 342 | website_event.publish_event_register_via_portal [hard] | Publish event website page, navigate to portal /events, register | Done | PASS | PASS | 1.0 |
| 343 | crm_sms.send_sms_to_opportunity [medium] | On opportunity, click Send SMS button, compose and send | Done | PASS | PASS | 1.0 |
| 344 | hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout [medium] | Check in via kiosk PIN, then fix the missing checkout from manager attendance view | Done | PASS | FAIL | 0.0 |
| 345 | point_of_sale.cash_in_sell_cash_out_close_session [hard] | In POS, perform cash in, complete a sale, record cash out, then close the session | Done | PASS | FAIL | 0.0 |
| 346 | delivery.country_rule_and_free_threshold_apply_to_so [medium] | Create a carrier with destination rules and free-shipping threshold, then apply it to a matching quotation | Done | PASS | PASS | 1.0 |
| 347 | inventory.cycle_count_two_locations_apply_selected_delta [medium] | Perform a cycle count across two locations and apply only the intended stock discrepancy | Done | PASS | FAIL | 0.0 |
| 348 | project_todo.create_note_set_color_deadline [easy] | Create a note, set a deadline, and apply a non-default kanban color | Done | PASS | FAIL | 0.0 |
| 349 | survey.create_certification_quiz_attempt_limit_publish [hard] | Build a certification quiz with passing score and attempt limit, then publish it | Done | PASS | FAIL | 0.0 |
| 350 | appointment.public_booking_reschedule_cancel_portal [hard] | Configure an appointment type, book it publicly, then reschedule and cancel it from the portal | Removed | FAIL (module unavailable) | — | — |
| 351 | helpdesk.team_sla_assign_escalate_close [hard] | Create a helpdesk team with SLA policy, process a ticket through assignment and escalation, then close it | Removed | FAIL (module unavailable) | — | — |
| 352 | marketing_automation.tag_trigger_drip_campaign [hard] | Build a tag-triggered marketing automation flow with delayed actions and a stop condition | Removed | FAIL (module unavailable) | — | — |
| 353 | event_product.sell_event_product_fill_attendee_details [medium] | Sell an event-linked product and complete attendee details for the generated registration | Done | PASS | FAIL | 1.0 |
| 354 | event_sale.multi_ticket_checkout_two_attendees [hard] | Configure two paid ticket types and complete one website checkout with separate attendee details | Done | PASS | PASS | 1.0 |
| 355 | sale_loyalty.buy_x_get_y_reward_in_cart [hard] | Configure a Buy X Get Y promotion and verify the free-product reward appears in the cart | Done | PASS | PASS | 1.0 |
| 356 | sale_purchase.mto_so_generate_po_change_vendor_confirm [hard] | Confirm an MTO sale order, inspect the generated PO, switch vendor, and continue the chain | Done | PASS | PASS | 1.0 |
| 357 | sale_stock.confirm_so_manual_reserve_validate_delivery [medium] | Confirm a sale order, manually reserve stock on its delivery, and validate the transfer | Done | PASS | PASS | 1.0 |
| 358 | website_blog.create_post_with_cta_seo_schedule [medium] | In the 'Bench News' blog, create a post with a CTA button block (Learn More, href='/shop'), fill Meta Title + Meta Description via the Optimize SEO dialog, and schedule publish for 2026-05-20 09:00 without publishing | Done | PASS | FAIL | 0.0 |
| 359 | im_livechat.configure_channel_then_handle_widget_chat [hard] | Reply to a seeded livechat session in Discuss via `::hello` canned-response shortcut (single-tab variant) | Done | PASS | PASS | 1.0 |
| 360 | website_hr_recruitment.apply_public_then_schedule_interview [hard] | Submit a public job application, then schedule that applicant’s interview from the backend | Done | PASS | PASS | 1.0 |
| 361 | purchase_stock.receive_partial_scrap_damaged_units [hard] | Receive part of a PO, scrap damaged units from the receipt, and finish the remainder correctly | Done | PASS | FAIL | 0.0 |
| 362 | maintenance.create_request_from_equipment_schedule_followup [medium] | Create a maintenance request from an equipment record and schedule a follow-up activity | Done | PASS | FAIL | 0.0 |
| 363 | point_of_sale.sell_pos_order_invoice_customer [hard] | Ring up a POS sale, attach a customer, toggle Invoice this Order, pay cash, and verify a posted account.move invoice was generated | Done | PASS | FAIL | 0.0 |
| 364 | repair.cancel_repair_log_internal_reason [medium] | Open an existing repair quotation, start it, then cancel via Action menu and log an internal note in the chatter explaining the cancellation reason | Done | PASS | PASS | 1.0 |
| 365 | survey.duplicate_survey_rename_archive_original [medium] | Duplicate a seeded survey via cog menu, rename the copy, then archive the original so only the renamed copy remains active | Done | PASS | PASS | 1.0 |
| 366 | maintenance.fill_description_schedule_window_move_to_repaired [medium] | Open an existing in-progress maintenance request, fill the description, set the scheduled start and end dates (logging the repair duration), and move it to the Repaired stage | Done | PASS | PASS | 1.0 |
| 367 | stock.scrap_specific_serial_unit [medium] | Scrap one specific serial-tracked unit (1 of 3 in stock) via Inventory Operations Scrap, leaving the other two in stock (originally hard, demoted after both browser-use runs passed) | Done | PASS | PASS | 1.0 |
| 368 | hr_expense.split_submitted_report_resubmit [hard] | Refuse the Gadget expense (reason 'Not compliant') in a 3-expense submitted batch (R-BENCH-SPLIT-001) and approve the remaining Meal + Taxi — Odoo 19 hr.expense.sheet is removed so sheets pivot to per-expense triage | Done | PASS | PASS | 1.0 |
| 369 | website_sale.apply_product_filter_clear_facets [medium] | On /shop, filter products by category and price range, then clear one facet and verify the other persists | Done | PASS | PASS | 1.0 |
| 370 | project_todo.bulk_move_tasks_between_projects [hard] | Move 3 specific tasks from project A to project B while leaving a distractor task in project A | Done | PASS | FAIL | 0.0 |
| 371 | website_hr_recruitment.edit_job_form_publish_preview [medium] | Edit a recruitment job posting's description and requirements, publish it, then preview on the portal | Done | PASS | PASS | 1.0 |
| 372 | fleet.log_service_cost_add_odometer_close [hard] | Log a service cost on a vehicle, add an odometer reading, then mark the service record as closed | Done | PASS | FAIL | 0.0 |
| 373 | maintenance.create_equipment_schedule_preventive_plan [medium] | Create 'Bench Press 01' equipment with on-the-fly Machinery category, assign technician Bench Tech, set Expected MTBF=30 days, save, then reopen and set Effective Date=06/01/2026 | Done | PASS | FAIL | 0.0 |
| 374 | product_expiry.receive_lot_set_expiry_date [medium] | Receive a lot-tracked perishable product and set its expiration and best-before dates | Done | PASS | PASS | 1.0 |
| 375 | website_sale_slides.assign_attendees_publish_course [hard] | Publish an eLearning course, set prerequisite, and assign enrolled attendees | Done | PASS | FAIL | 0.0 |
| 376 | calendar.configure_meeting_with_location_and_reminder [medium] | Create a calendar event with a physical location, attendees, and a 1-hour reminder | Done | PASS | PASS | 1.0 |
| 377 | mrp.bom_with_kit_component_confirm_mo [hard] | Create a BoM that uses a kit-type sub-component, confirm an MO, and verify kit expansion | Done | PASS | FAIL | 0.0 |
| 378 | mrp_subcontracting.receive_subcontracted_product_with_components [hard] | Receive a subcontracted serial-tracked product (qty=2) from its subcontractor via Detailed Operations popup (two serials) and verify components were back-flushed | Done | PASS | PASS | 1.0 |
| 379 | stock_landed_costs.add_cost_to_shipment_allocate [hard] | Create a landed cost with a freight line, apply to a completed receipt, validate | Done | PASS | PASS | 1.0 |
| 380 | hr_recruitment_survey.attach_survey_require_applicant_submit [medium] | Attach a screening survey to a job position and verify the Send Interview button becomes visible on the applicant | Done | PASS | PASS | 1.0 |
| 381 | website_customer.publish_customer_reference_on_public_page [medium] | Mark a customer reference as published and verify it appears on /customers | Done | PASS | PASS | 1.0 |
| 382 | pos_restaurant.open_table_order_mark_ready [hard] | In restaurant POS, open a table, take an order, and mark the course ready | Done | PASS | PASS | 1.0 |
| 383 | website_sale_stock.show_stock_availability_add_to_cart [medium] | On a /shop product with stock availability display enabled, verify availability shows and add to cart within limits | Done | PASS | PASS | 1.0 |
| 384 | lunch.create_vendor_product_order_for_today [medium] | Install Lunch, create vendor Bench Cafe + product Veggie Wrap, then order via /odoo/lunch kiosk | Done | PASS | FAIL | 0.0 |
| 385 | stock_sms.enable_delivery_sms_notification_validate [medium] | Enable SMS delivery notification on a picking type and validate a delivery to trigger it | Done | PASS | PASS | 1.0 |
| 386 | sale_management.create_quotation_template_apply_to_new_so [medium] | Create a quotation template with 2 default lines, then apply it to a new SO | Done | PASS | PASS | 1.0 |
| 387 | hr_skills_survey.link_certification_survey_to_skill [hard] | Create a certification survey, link it to a skill, and attempt completion | Removed | FAIL (feature unavailable) | — | — |
| 388 | project.create_milestone_assign_tasks_reach [medium] | Create a project milestone, assign 2 tasks to it, then mark reached | Done | PASS | FAIL | 0.0 |
| 389 | mass_mailing.duplicate_mailing_edit_subject_send [medium] | Duplicate an existing mass mailing, edit the subject, add a contact list, and send | Done | PASS | PASS | 1.0 |
| 390 | sale_timesheet.log_timesheet_on_so_invoice_delivered [hard] | Confirm a service SO with delivered-timesheet policy, log timesheet hours, create invoice for delivered qty | Done | PASS | PASS | 1.0 |
| 391 | project_sms.send_reminder_sms_to_task_followers [medium] | Send a reminder SMS to task followers from a project task log note | WIP | — | — | — |
| 392 | mrp.workorder_operation_scan_serial_complete [hard] | Start a work order, consume serial-tracked component via scan, mark operation done and finish MO | Done | PASS | FAIL | 0.0 |
| 393 | crm_iap_enrich.bulk_enrich_leads_from_list [hard] | From CRM Leads list view, multi-select 3 unenriched leads (skip 2 distractors) and run the Actions > Enrich server action | Done | PASS | PASS | 1.0 |
| 394 | website_forum.post_question_accept_answer [medium] | Post a question on the website forum, answer it, accept the answer | WIP | — | — | — |
| 395 | stock.transfer_reserved_to_ready_partial_backorder [hard] | Reserve qty on a delivery, validate only part of it, create backorder | WIP | — | — | — |
| 396 | website_sale_wishlist.add_product_share_to_email [medium] | Add a product to wishlist on the shop and share via email | WIP | — | — | — |
| 397 | purchase.create_rfq_receive_invoice_3way_match [hard] | Create RFQ with 2 lines, confirm, receive partially, then bill and reconcile | WIP | — | — | — |
| 398 | hr_attendance.clock_in_out_kiosk_mode [medium] | From Attendance kiosk, an employee clocks in and then clocks out | WIP | — | — | — |

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

## point_of_sale.sell_pos_order_invoice_customer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |

Hard task. Browser-use must open POS, ring up an order, attach a customer, enable the Invoice toggle on the payment screen, and validate to generate an actual posted account.move. Both runs failed at the kiosk POS UI: run 1 timed out after 7 stalled payment attempts, run 2 reached 401s with the order stuck in draft and no invoice generated.

## repair.cancel_repair_log_internal_reason

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |

Medium task. Open the seeded confirmed repair order, cancel it, then post an internal note (mail.mt_note subtype) with a specific reason. Both browser-use runs passed in ~57s.

## survey.duplicate_survey_rename_archive_original

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |

Medium task. Duplicate a survey, rename the copy without the "(copy)" suffix, then archive the original. Both browser-use runs passed in 81-99s.

## maintenance.fill_description_schedule_window_move_to_repaired

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |

Medium task. Open the maintenance request, fill a specific description paragraph, set scheduled start 04/15/2026 09:00 and end 11:00, move to Repaired stage. Both browser-use runs passed in 77-94s.

## stock.scrap_specific_serial_unit

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |

Medium task (originally drafted as hard, demoted after both browser-use runs passed cleanly in 73-113s). Open Inventory > Operations > Scrap, create a scrap for the serial-tracked product picking the middle serial SN-A002 out of three, validate.

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
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Live Chat, Website |
| **Workflow** | Configure a live chat channel's offline behavior, then verify the website widget shows the offline contact form path. |
| **Capability tested** | Backend chat-channel settings plus public website widget verification across two UI surfaces. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## point_of_sale.split_payment_email_receipt

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Point of Sale |
| **Workflow** | Open a POS session, ring up a sale, split the payment across two methods, and email the receipt to the customer. |
| **Capability tested** | Full-screen kiosk interaction, keypad payment entry, multi-payment flow, and receipt-delivery workflow. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

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
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Manufacturing |
| **Workflow** | Confirm a manufacturing order, start a work order, block it with a reason, resume it, and finish production. |
| **Capability tested** | Work-order execution controls with state transitions beyond BOM or MO creation alone. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## stock.package_products_validate_delivery

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Inventory |
| **Workflow** | Open an outgoing delivery, package the products into a package, and validate the shipment. |
| **Capability tested** | Delivery operation handling with package creation and final stock validation. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## barcodes.receive_product_via_scan_validate

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (spec) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Barcode, Inventory |
| **Workflow** | Open a barcode receipt flow, scan or enter the target product, and validate the received quantity. |
| **Capability tested** | Scanner-style inventory interaction rather than standard backend list/form editing. |
| **Notes** | Removed because this checkout has `barcodes` but does not include the stock barcode client addon needed for warehouse receipt scanning (`stock_barcodes` / equivalent inventory barcode app). |

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
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Repairs |
| **Workflow** | Create a repair order, add repair parts, complete the repair, and create the resulting invoice. |
| **Capability tested** | Repair-order lifecycle with part lines and downstream accounting side effect. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## mass_mailing.build_campaign_send_test_schedule

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Email Marketing |
| **Workflow** | Build an email campaign, send a test email, and schedule the campaign for later delivery. |
| **Capability tested** | Campaign composer plus test-send and schedule actions in email marketing. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

---

## sale_loyalty.create_program_apply_reward_on_quotation

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Sales, Loyalty |
| **Workflow** | Create a loyalty or coupon program, then apply the reward on a target quotation. |
| **Capability tested** | Cross-configuration from loyalty setup into quotation-side reward application. |
| **Notes** | Oracle passes. Browser-use gave up immediately with zero steps in this environment. |

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

---

## delivery.configure_weight_rules_carrier_apply_to_so

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS/FAIL (1 of 2) |
| **F1** | 0.5 |
| **Odoo modules** | Inventory (Delivery), Sales |
| **Workflow** | Configure a Based-on-Rules shipping carrier with two weight tiers (≤5 kg → 8.00, ≤20 kg → 18.00), then add the carrier to a seeded quotation and confirm the order. |
| **Capability tested** | Weight-bracket pricing rule configuration plus cross-module application onto a sale order — distinct from the existing fixed-rate carrier task. |
| **Notes** | Well-calibrated medium tier. Run 1 timed out before reaching the SO step; run 2 completed end-to-end. |

---

## maintenance.create_equipment_assign_category_team

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Maintenance |
| **Workflow** | Create a new equipment record "Dock Scanner DS-200" with serial number, category "Warehouse Gear", and team "Bench Maintenance". |
| **Capability tested** | Single-form equipment registry creation with two Many2one assignments — distinct from the existing maintenance request flow. |
| **Notes** | Easy tier but harder than expected. Browser-use consistently saved the equipment without setting the Maintenance Team Many2one. |

---

## maintenance.schedule_preventive_plan_recurring

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Maintenance |
| **Workflow** | Open the seeded "Conveyor Belt CB-7" equipment, set Expected MTBF=120, then create a Preventive maintenance request with recurring 30-day interval. |
| **Capability tested** | Editing a numeric equipment field plus creating a request with the non-default Preventive maintenance_type radio. |
| **Notes** | Calibrated below medium tier — both browser-use runs passed (target was ~60%). Odoo 19 dropped the legacy `period` field; task adapted to use `expected_mtbf` + recurring toggle. |

---

## sale_stock.partial_stock_warning_confirm_anyway

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.857 |
| **Odoo modules** | Sales, Inventory |
| **Workflow** | Confirm a sale order with insufficient on-hand stock (5 units available for a 10-unit order), open the auto-created delivery, change Done qty from 5 to 2, validate, and create a backorder for the remaining 8 units in the wizard. |
| **Capability tested** | Inline-cell quantity edit on a stock move plus the backorder wizard. Hard pattern: the inline qty edit must persist before validation. |
| **Notes** | Well-calibrated hard tier. Browser-use consistently reported "I changed Done to 2" but the inline-cell edit did not save, leaving Done=5 and triggering postcondition failures. |

---

## survey.create_feedback_survey_with_sections

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Surveys |
| **Workflow** | Create a non-quiz feedback survey "Q1 Workshop Feedback" with two sections, four questions of mixed types, public access, page-per-section layout, and a 10-minute time limit. |
| **Capability tested** | Multi-section survey authoring with mixed question types — distinct from the existing branching-quiz survey task. |
| **Notes** | Calibrated below medium tier — both browser-use runs passed. Odoo 19 hides the Time Limit field for `survey_type='survey'`; task uses `custom` to expose it. |

---

## survey.review_submitted_responses_filter

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Surveys |
| **Workflow** | Open the "Customer Pulse March" survey's Participations smart button, find the response with email reviewer-target@example.com (4 distractors present), and post a chatter message starting with "Reviewed:". |
| **Capability tested** | Read/analyze workflow on existing responses (vs. authoring) — distinct from all existing survey.* tasks which create surveys. |
| **Notes** | Calibrated below medium tier — both browser-use runs passed. Oracle uses JSON-RPC to bypass the fragile filter UI. |

---

## im_livechat.configure_url_rule_auto_message

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (run 1) / FAIL strict (run 2 reached correct state but timed out signalling Done) |
| **F1** | 1.0 |
| **Odoo modules** | Live Chat |
| **Workflow** | Open the seeded "Website Support" channel via the kanban dropdown → "Configure Channel" → Rules tab → add a rule with regex_url=/contact, action=auto_popup, auto_popup_timer=5. |
| **Capability tested** | Secondary-tab modal-form rule configuration distinct from existing canned-response and runtime-chat tasks. |
| **Notes** | Calibrated below medium tier — agent achieved correct state both runs. Discovery: kanban card opens chat session, not form; must use 3-dots → Configure Channel. |

---

## sale_project.timesheet_task_mark_billable_log_hours

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (spec) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Sales, Project (Sale-Project, Timesheet) |
| **Workflow** | Open the auto-generated project task from a confirmed services SO, log timesheet hours, and verify the SO line's delivered quantity updates so an invoice can be created. |
| **Capability tested** | Cross-module billable-time round-trip across Sales, Project, Timesheet, and Invoicing surfaces. |
| **Notes** | Aborted — the benchmark base snapshot does not include `hr_timesheet` or `sale_timesheet`, so service products cannot use `service_policy='delivered_timesheet'` and project tasks have no Timesheets tab. Re-enable when those modules are added to base_modules.txt. |

---

## project_todo.reorder_notes_add_due_dates_bulk

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | To-Do |
| **Workflow** | Open three seeded To-Do notes (Alpha, Beta, Gamma) and assign specific due dates: Alpha=2026-04-25, Beta=2026-04-30, Gamma=2026-05-02. The kanban auto-sorts by date_deadline asc. |
| **Capability tested** | Bulk targeted date assignment across personal To-Do entries. |
| **Notes** | Calibrated for easy tier — both browser-use runs passed. Drag-reorder was dropped from the original spec because the default kanban sort makes a sequence write indistinguishable from date-driven sorting. |

---

## website_hr_recruitment.publish_job_from_backoffice_then_apply_portal

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Recruitment, Website Recruitment |
| **Workflow** | Back-office: create job "Senior Widget Engineer" in Administration with target=2 and a description, then publish it. Portal: open /jobs, click the new job, click Apply Now, fill the applicant form (incl. LinkedIn to satisfy client-side validation), and submit. |
| **Capability tested** | Cross-surface round-trip between admin back-office and public portal — distinct from existing tasks that start from already-published jobs. |
| **Notes** | Well-calibrated hard tier. Browser-use missed setting the Department field because the kanban "New" opens a stub modal — the full form is only reachable via "Configure" on the kanban card afterward. |

---

## mass_mailing.create_segmented_mailing_save_draft

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.667 |
| **Odoo modules** | Email Marketing |
| **Workflow** | Create a new mass mailing with subject "Berlin April Bulletin", recipients = Contact filtered by City="Berlin" (returns 2 of 3 seeded partners), set body, save as draft (do not send). |
| **Capability tested** | Domain filter wizard configuration — first task in this previously untouched module. |
| **Notes** | Well-calibrated medium. BU created a duplicate mailing with subject pollution (subject ended with email_from text) and run 2 hit a parallel-cleanup env crash. |

---

## event_sale.configure_paid_ticket_register_with_invoice

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Events, Sales |
| **Workflow** | Add paid ticket "Professional Pass" (€150, 50 seats) to seeded event, register attendee "Berta Attendee" via the Sales→event-configurator path, then through the registrations wizard, then click Create Invoice in the wizard. |
| **Capability tested** | Cross-module event→sale→invoice round-trip with mandatory attendee-detail override in a wizard. |
| **Notes** | Well-calibrated hard tier. BU consistently skipped the attendee-name override in the registration wizard, leaving the partner's billing name on the registration. First task targeting the event_sale bridge. |

---

## inventory.run_replenishment_from_dashboard

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Inventory, Purchase |
| **Workflow** | Open Inventory → Operations → Procurement → Replenishment, find the seeded "Bench Reorder Widget" row (on-hand=2 vs need=28), click the "Order" button on that row to auto-create a draft PO for vendor "Bench Supplies Ltd". |
| **Capability tested** | Replenishment dashboard navigation + per-row action button. |
| **Notes** | Calibrated below medium target — both BU runs solved cleanly. The button is "Order" not "Replenish" in Odoo 19, and the orderpoint auto-deletes after qty_to_order reaches 0. |

---

## sale_project.deliver_milestone_invoice_partially

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Project (Sale-Project) |
| **Workflow** | Open the auto-generated project for an SO with `service_policy=delivered_milestones`. Mark only "Design Phase" milestone reached (not Build or Launch). Navigate back to SO and create a Regular Invoice for the delivered third only. |
| **Capability tested** | Selective milestone delivery + cross-module invoice generation, distinct from existing project-generation-only tasks. |
| **Notes** | Calibrated below hard target — milestone checkbox + accept-default wizard proved straightforward for browser-use. |

---

## website_sale.unpublish_archive_unarchive_publish_cycle

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (re-run after env crashes) |
| **F1** | 1.0 |
| **Odoo modules** | Website (eCommerce) |
| **Workflow** | Take seeded "Bench Cycle Gadget" through Unpublish (toggle on Sales tab) → Archive (cog menu) → switch to Archived filter → Unarchive → Publish back → also set Internal Reference to "BCG-RESTORED" on General tab. |
| **Capability tested** | 5-step state cycle across kanban/list views, cog menu, and multiple form tabs. |
| **Notes** | First two BU runs crashed mid-eval from sibling worktrees' parallel cleanup; sequential re-run after batch settled completed in 224s. Despite UI complexity, BU solved it. |

---

## website_blog.edit_post_change_author_add_tags_schedule

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (Blog) |
| **Workflow** | Open seeded post "Spring Planning Recap" → change Author Many2one to "Alice Authoress" (in Publishing Options group) → add tags Planning + Quarterly (NOT Retrospective distractor) → set Publish on = 2026-04-25 09:00:00 → save. Do NOT publish. |
| **Capability tested** | Multi-field edit with side-group Many2one, m2m tag picker, and datetime field. |
| **Notes** | Well-calibrated medium. BU run 1 typed the datetime imprecisely (2026-04-25 09:00:30 vs expected 09:00:00) — exactly the medium-tier failure mode designed for. Subsequent runs hit env crashes. |

---

## website_slides.add_quiz_lesson_to_existing_course

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (re-run after env crashes) |
| **F1** | 0.0 |
| **Odoo modules** | Website (eLearning) |
| **Workflow** | Open seeded "Bench Onboarding Course" → Add Content → set Type=Quiz, title "Chapter 1 Quiz" → in Questions tab, add 3 questions each with 3 answers, mark exact correct answer (Blue, Daily, Platform) → publish slide. Distractor "Welcome Video" must remain unchanged. |
| **Capability tested** | Nested polymorphic form (slide.question + slide.answer rows) with correct-answer flag per question. |
| **Notes** | Well-calibrated hard. Re-run BU marked wrong correct answer (Never instead of Daily on Q2) and timed out at 480s on a third try. Initial parallel runs crashed environmentally. |

---

## sale_purchase.dropship_so_to_po_chain_validate

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Purchase, Stock (Dropshipping) |
| **Workflow** | Seed creates a confirmed SO for a Dropship-routed product (auto-installs `stock_dropshipping`). Agent navigates SO → Purchase smart button → Confirm PO → Dropship smart button → Validate the dropship picking. |
| **Capability tested** | Smart-button chain across SO → PO → dropship picking with state transitions. |
| **Notes** | Calibrated below hard target — explicit smart-button hints in the prompt made navigation obvious. Designer flagged: drop labels and add distractors to push BU pass rate down. First sale_purchase task. |

---

## mail.create_channel_set_custom_avatar_pin_two_messages

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Discuss |
| **Workflow** | Create channel "engineering-hub" with description, upload custom 4×4 PNG avatar from seed_artifacts, post 3 specific messages in order, pin exactly 2 (standup + retro) — NOT the PR review message. |
| **Capability tested** | File upload (avatar) + selective pin among 3 messages by content. |
| **Notes** | Well-calibrated medium. BU run 1 created channel + name fields then failed file upload and never posted messages. Run 2 created a duplicate channel. Discuss auto-creates an Administrator/OdooBot DM that pollutes state-diff F1 (oracle check.py is the source of truth). |

---

## fleet.transfer_vehicle_between_drivers_log_history

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Fleet |
| **Workflow** | Open vehicle "Bench Sedan BS-1001" assigned to Driver Alice → change Driver Many2one to Driver Bob with effective date 2026-04-18 → save. Verify the system-created `fleet.vehicle.assignation.log` entry. |
| **Capability tested** | Driver Many2one swap that auto-creates an audit log entry. |
| **Notes** | Brittle calibration — `fleet.vehicle.write` auto-sets `date_start = today`, and 2026-04-18 happens to be today's date in this run window, so BU only needed to change driver and save. Will become genuinely medium on any other date. |

---

## delivery.set_third_party_carrier_print_label

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Delivery, Stock, Sale |
| **Workflow** | Configure carrier "Bench Express" (delivery_type=fixed, fixed_price=12, delivery product "Bench Express Shipping" created via the create-and-edit shortcut). Open the outgoing delivery picking for SO S-BENCH-DLV-002 (Ready, 1 move `Bench Express Crate` x 3), set Shipping Method = "Bench Express", Tracking Reference = "BX-TRACK-002", click Validate, then click the header Print button. |
| **Capability tested** | Smart-button print action + manual tracking-ref population on a confirmed delivery picking; cross-module Delivery-Methods → Inventory round-trip. |
| **Notes** | Fixed-price provider does NOT auto-generate a tracking number (`fixed_send_shipping` returns `tracking_number: False`); the only built-in providers in base are `fixed` and `base_on_rule`, both return False — so the task has the agent type the tracking ref manually. BU solved in ~156s / 21 steps, handling the create-and-edit modal and the "Concatenation detected" auto-retry on the Fixed Price numeric input; Print header button opens the delivery-slip report in-app. Calibrates slightly easier than target medium; could be hardened by requiring a specific weight / destination on the picking before validate. Seed pins `sale.order.name = 'S-BENCH-DLV-002'` so the picking's `origin` matches the deterministic entity_key; oracle uses JSON-RPC with `skip_backorder=True` and writes `stock.move.quantity` + `picked=True` to get a clean `button_validate`. |

---

## event_sale.add_seat_limited_ticket_register_until_full

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Events / event_sale |
| **Workflow** | Seed creates 'Spring Q2 Workshop' with no real ticket types. Agent (1) adds VIP Seat ticket with seats_max=5, price=200; (2) registers VIP-1..VIP-5 one-at-a-time via the Attendees stat button → New, setting `event_ticket_id=VIP Seat` on each registration; (3) attempts to register VIP-6 with the same ticket — Odoo's `_check_seats_availability` constrains state in ('open','done'), so saving raises a ValidationError "There are not enough seats available". Agent must discard the 6th draft. |
| **Capability tested** | Repetitive form fills (5 round-trips event → Attendees → New → Save), per-row non-default `event_ticket_id` selection, and recognition of a hard server-side seat-limit block on the 6th attempt. |
| **Notes** | Well-calibrated medium. Oracle passes cleanly with F1=1.0 (24/24 atomic edits matched). Browser-Use failed: it created a duplicate 'VIP-1', omitted `event_ticket_id` on every registration (so seats_max was never enforced), and successfully created VIP-6 because no ticket meant no seat-limit constraint. Postcondition catches both the duplicate and the missing-ticket-link, F1 collapses to 0.0. Cookbook quirk discovered: BU drops the `event_ticket_id` Many2one on `event.registration.create` when registering from the event's Attendees view because the field is empty by default and the registration is still valid (just unconstrained) — drives both the seat-limit bypass and the duplicate-name re-attempts. |

---

## sale_loyalty.create_loyalty_program_apply_at_checkout

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sale, Loyalty, Sale Loyalty, Website Sale, Website Sale Loyalty |
| **Workflow** | On `Discount & Loyalty`, create a new program "Spring 10% Discount", `program_type=Discount Code`, conditional rule with `Code=SPRING10` and `Minimum Purchase=150.00`, single 10% Order discount reward with description "Spring Sale Discount". Save. Then visit `/shop/cart` (admin's seeded draft cart, $200 of two products), enter `SPRING10` in the Discount code box and Apply. A reward line of -$20 must appear, total = $180. A distractor program "Holiday Bonus 5%" must remain untouched. |
| **Capability tested** | Cross-module workflow: backend program creation (with two embedded subforms — rule and reward — each with non-default fields) followed by switching from `/odoo` to the public web shop and applying the code through the cart's coupon form. |
| **Calibration note** | Hardened from base spec by adding a distractor existing program, a hidden non-default Minimum Purchase=$150 on the rule, and a custom Reward Description string. Browser-Use 1.0 (model `bu-1-0`) still solved it in 14 steps; this is a strong agent and the form widgets are well structured. The task remains genuinely cross-module and exercises the rule sub-form, reward sub-form, and the public `/shop/pricelist` POST flow — borderline easy for top agents but will challenge weaker models that struggle with sub-form save & close cycles. Per build instructions, committed as-is with this calibration note. |
| **Notes** | `program_type='loyalty'` cannot be applied with a code (`_try_apply_code` rejects it with "This program cannot be applied with code"), so the spec's literal `program_type=loyalty` is infeasible — used `promo_code` (the canonical "Discount Code" type that lives under the same Discount & Loyalty menu). Cart auto-pickup works because admin is logged in and `_get_and_cache_current_cart` resurrects the abandoned draft order matching `partner_id+website_id+state=draft`. |

---

## inventory.create_storage_category_assign_to_location

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Inventory (Stock) |
| **Workflow** | Open Inventory → Configuration → Settings, enable the **Storage Locations** toggle (group_stock_multi_locations — this is what gates the Storage Categories menu and the storage_category_id field on stock.location in Odoo 19), Save. Then Configuration → Storage Categories → New: name="Cold Chain", Max Weight=500, Save (leave Allow New Product=mixed default, no capacity rows). Then Configuration → Locations → click WH/Stock → set Storage Category=Cold Chain → Save. |
| **Capability tested** | Settings-toggle prerequisite (settings save reloads the page and only then exposes the menu/field) + nested form across two distinct configuration screens. |
| **Notes** | Cookbook quirks: (1) In Odoo 19 there is **no** separate `group_stock_storage_categories` setting — the only toggle is "Storage Locations". The prompt phrasing reflects this. (2) `complete_name` on `stock.location` must be in `state_spec.fields` (not just `match_key`) or the diff engine emits `entity_key=[null]` and stable matches break. (3) `allow_new_product` defaults to `mixed` on create and showed up as a noisy `create` op — moved to `ignore_fields`. (4) Seed must remove `group_stock_multi_locations` from `base.user_admin.group_ids` AND from `base.group_user.implied_ids` to make the Storage Categories menu invisible at start. (5) BU run took 244s, created the category but typed Max Weight=0.01 (likely confused the field with a default decimal placeholder) and never reached step 3 — clean medium FAIL. |

---

## im_livechat.assign_team_set_offline_form_message

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 154.1s) |
| **F1** | 1.0 |
| **Odoo modules** | Live Chat |
| **Workflow** | Open Live Chat app, hover the seeded "Website Support" kanban card, click the 3-dots menu and choose Configure Channel to reach the form. Switch to the Options tab and update Notification Text (button_text) and Welcome Message (default_message) to the exact strings, then save. |
| **Capability tested** | Tab switching combined with multi-field text input on a non-default form view (Live Chat kanban opens session, not form). |
| **Notes** | Original task spec referenced offline_form_text / offline_email fields that do NOT exist on im_livechat.channel in Odoo 19; remapped to the real Options-tab text fields (button_text, default_message) preserving the "tab switch + multi-text-field input" hard pattern. Browser-use solved cleanly, so calibration is "easier" than the medium target. |

---

## website_blog.create_blog_with_two_posts_archive_one

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | website_blog |
| **Workflow** | Agent must create blog 'Bench Insights' from scratch, then create two blog.posts under it ('April Update' and 'March Notes', both published), then open March Notes and archive it via Action > Archive (active=False) without deleting it or touching April Update. |
| **Capability tested** | Multi-record creation followed by selective archive among siblings — tests attention to which of two newly created records to archive. |
| **Notes** | Browser-use created blog + both published posts correctly (9/12 atomic edits matched) but failed to archive March Notes within the 360s budget — exactly the predicted "selective archive among siblings" failure mode. Calibration matches medium tier. State diff for the archived post serializes False booleans as `null` on a `create` op (active/is_published/website_published all show `norm_value: null`); expected_state.json must mirror that. |

---

## website_slides.duplicate_lesson_to_new_section

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (eLearning) |
| **Workflow** | Open Bench Onboarding Course (seeded with Intro section + Welcome Video lesson). Add new section Advanced, then duplicate Welcome Video via the cog/Actions menu, move the copy into Advanced via the section Many2one, and rename it to Advanced Welcome. |
| **Capability tested** | Sub-resource duplication via cog/Actions Duplicate menu plus section reassignment of a slide.slide whose section is sequence-derived, not a directly editable Many2one. |
| **Notes** | Well-calibrated medium. Browser-use duplicated the entire course three times instead of the lesson — exactly the cog-menu navigation hazard the task targets. Oracle uses copy() + sequence rewrite because slide.slide.category_id is computed from sequence ordering. |

---

## sale_stock.deliver_partial_split_into_two_pickings

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (gave up at 480s) |
| **F1** | 0.0 |
| **Odoo modules** | Sales, Inventory |
| **Workflow** | Confirm draft SO S-BENCH-SPLIT-001 (Halberd Industries, Alpha×5 + Beta×8 with both fully reservable). Open delivery, manually edit Beta Done from auto-reserved 8 down to 3, validate, click "Create Backorder". Then breadcrumb back to SO, smart-button to delivery list, open the not-Done backorder picking, edit Beta Done from auto-reserved 5 down to 0, then SAVE (no validate). |
| **Capability tested** | Inline-cell qty edits in TWO separate pickings + backorder dialog choice + non-validate save. |
| **Notes** | Well-calibrated hard. Initial design with Beta stock=3 (matching user spec literal "3 in stock") made the 5→0 step a no-op (backorder Done already 0 because no stock left), and BU passed. Reseeded Beta with 8 in stock so backorder genuinely auto-reserves 5 → forced cell-edit pattern. BU failed by creating a return picking ("Return of WH/OUT/00001") instead of opening the existing backorder, then ran out of time. F1=0.0 / postcondition failure: "Expected exactly 1 original (non-backorder) picking, found 2". Backorder ends in state=`confirmed` after Done is zeroed (stock un-reserves). |

---

## maintenance.archive_equipment_create_replacement

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1 1.0, 97.4s) |
| **F1** | 1.0 |
| **Odoo modules** | Maintenance |
| **Workflow** | Open the seeded equipment 'Old Belt OB-99' in category Warehouse Gear and archive it via the form Actions menu. Then create a new equipment 'New Belt NB-100' in the same Warehouse Gear category with serial 'NB-100-SN-2026', and save. |
| **Capability tested** | Two-step lifecycle on the same model: archive existing record (active=False) via Actions menu, then create-from-scratch a replacement with exact category and serial. |
| **Notes** | Archive sets `active=False` which the diff engine normalizes to `null`. The create-from-scratch on `maintenance.equipment` also generates an explicit `active=true` create entry — both must be encoded in expected_state.json. BU solved on first attempt; calibration trends easier than medium. |

---

## website_hr_recruitment.set_kanban_state_assign_recruiter

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment (hr_recruitment) |
| **Workflow** | Open the seeded applicant 'Diana Recruit' (linked to job 'Senior QA Engineer'). Click the small kanban_state status ball at the top of the form and pick 'Ready for Next Stage'. Set the Recruiter many2one to 'Recruiter Bob'. Post an internal Log note 'Phone screen done.' in the chatter. Save. |
| **Capability tested** | Three-part edit on a recruitment form: state-selection ball widget + many2one autocomplete + internal Log-note vs public Send-message distinction. |
| **Notes** | BU solved on first run (F1=1.0, 147s). State-selection ball findable via dropdown; agent correctly picked Log note over Send message. Calibration: easier than medium target. |

---

## project_todo.create_three_personal_with_specific_priorities

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (1 run, headless) — 7 duplicate Plan Sprint records created |
| **F1** | 0.0 |
| **Odoo modules** | To-Do (project_todo) |
| **Workflow** | Open the To-do app, create three personal notes (Plan Sprint, Write Docs, Refactor CSS). Only Plan Sprint should get one priority star clicked (Medium = priority '1'); other two stay default. Save each. |
| **Capability tested** | Multi-record creation in to-do quick-create combined with priority star widget. |
| **Notes** | Priority widget renders N-1 stars (skips `value_first`). For [(0,Low),(1,Medium),(2,High)] means 2 stars: star 1 → '1' (Medium), star 2 → '2' (High). Calibration matches easy tier — BU set right priority but ran a duplication loop on Plan Sprint instead of moving on. |

---

## sale_project.invoice_completed_milestones_only

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Project |
| **Workflow** | Open Sales app, find SO S-BENCH-MS-002. Click Create Invoice on the SO header. Wizard auto-fills line quantity 2 (M1+M2 of 4 milestones already reached). Accept Regular Invoice radio default and click Create Draft. |
| **Capability tested** | Trust the Create Invoice wizard's auto-quantity for delivered_milestones products (do not override). |
| **Notes** | Calibration: easier than hard. BU solved in 104s; wizard auto-detect is robust enough that agents accept it. To push to hard we'd need a non-default radio (Down Payment) or require typing a different qty — both forbidden by spec. Seed pre-marks M1+M2 reached so agent doesn't navigate to Project. SO line invoice_status flips to "no" (qty_to_invoice=0). |

---

## purchase_stock.return_partial_with_distractor_lines

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Purchase, Stock |
| **Workflow** | Open seeded PO P-BENCH-RET-001 (3 lines, fully received), open the done receipt, click Return, set WidgetA=0, WidgetB=2, WidgetC=0 in the multi-line wizard, click Return, then Validate the new return picking. |
| **Capability tested** | Multi-line return wizard with selective per-row qty edits (2 distractor rows must be explicitly zeroed). |
| **Notes** | BU gave up at 480s with 0 successful steps; required op stock.picking.button_validate was missed and WidgetB qty stayed at 5. Well-calibrated hard — non-default attention test on auto-populated wizard rows. |

---

## survey.publish_share_via_link_get_url

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Surveys |
| **Workflow** | Open seeded 'Customer Pulse Q2' survey from kanban, click form-header Share button (calls survey.survey.action_send_survey), confirm wizard exposes /survey/start/<token> public URL via CopyClipboardChar widget, close dialog without sending email. |
| **Capability tested** | Single-button form-header action opening a wizard exposing read-only side data. |
| **Notes** | No DB state change (expected_state.json empty []). PASS anchored on action_send_survey trace + check.py invariants (active=True, access_mode='public', access_token non-null). BU solved in 10 steps (~68s). Calibration matches easy. |

---

## sale_purchase.update_pol_alternative_vendor_compare

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (0.0) |
| **F1** | 0.0 |
| **Odoo modules** | purchase_requisition (installed on demand) |
| **Workflow** | Open draft RFQ R-BENCH-ALT-001 (Atlas Industrial, 10 × Industrial Compressor @ 120). On the Alternatives tab, use **Create Alternative** to add a Beacon Mechanical RFQ; override its unit price to 100. Repeat for Crestline Equipment at 130. Open **Compare Product Lines**, click **Choose** on Beacon's row to zero the rival quantities, then confirm Beacon's RFQ. Choose **Cancel Alternatives** in the alternative-warning dialog so Atlas & Crestline are cancelled. |
| **Capability tested** | Multi-step alternative-RFQ wizard sequence: partner_ids many2many_tags in a modal, copy-products side effect, a bespoke `js_class="purchase_order_line_compare"` grouped list view with per-row action buttons, and the non-default **Cancel Alternatives** branch in `purchase.requisition.alternative.warning`. |
| **Notes** | BU ran out of steps at 480s without cancelling Atlas or confirming Beacon; created 4 duplicate Crestline drafts while looping on the create-alternative flow. Oracle reaches the same end state via the simpler direct-cancel path (cancel Atlas + Crestline → confirm Beacon with no warning), which is an allowed equivalent final state. Seed installs `purchase_requisition` on demand and adds admin to `group_purchase_alternatives` so the Alternatives tab is visible. |

---

## mass_mailing.duplicate_existing_change_subject_recipients

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Email Marketing |
| **Workflow** | Open seeded draft 'Q1 Bulletin Template'. Click cog → Duplicate. On the duplicate, change subject to 'Q2 Bulletin Update' and Recipients filter to Contact with Country=Germany. Save (do not send). |
| **Capability tested** | Action menu Duplicate (non-default path) + multi-field edit on copy + domain widget for country filter. |
| **Notes** | BU clicked Duplicate 14 extra times (15 mailings total) before hitting step limit — canonical "duplicate spam loop" failure when post-duplicate state isn't visually distinct. check.py traps via "exactly 2 mailings" count. |

---

## point_of_sale.add_item_apply_global_discount_pay_cash

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale (+ pos_discount installed on demand) |
| **Workflow** | Open POS session, add Bench POS Widget × 2 (€40), click Actions (ellipsis) → Discount, enter 15%, confirm (€34), pay Bench Cash, validate. |
| **Capability tested** | POS kiosk UI with ellipsis-hidden Discount button. |
| **Notes** | Calibration: easier than hard. BU solved cleanly on first shot (15 steps, 128s). Oracle uses JSON-RPC call_kw bypass (UI hangs on stale o_technical_modal). Would need split payment + discount combo to regain hard tier. |

---

## calendar.create_event_with_two_organizers_recurring_weekly

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Create event 'Weekly Standup' on 2026-06-01 09:00-09:30 (Monday); add Alice + Bob attendees; set Weekly recurrence on Mondays ending 2026-12-31; generate Discuss videocall link; save. |
| **Capability tested** | Datetime entry + recurrence weekday picker + videocall location action. |
| **Notes** | Well-calibrated medium. BU got datetime in AM/PM wrong (entered 01:00 instead of 09:00) and left Saturday toggled in weekday picker. Oracle uses JSON-RPC because set_discuss_videocall_location is server-side no-op (real work is JS-intercepted). |

---

## hr_holidays.refuse_then_re_request_other_type

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (gave_up at 480s; strict FAIL, F1 0.71) |
| **F1** | 0.71 |
| **Odoo modules** | Time Off |
| **Workflow** | Admin (manager) opens Eve's pending Paid Time Off, clicks Refuse, posts refusal reason "Use sick leave instead" as chatter message, then creates new Sick Time Off on Eve's behalf for same dates via the manager approval list, save to land in 'confirm'. |
| **Capability tested** | Two-step lifecycle on different records: refuse + chatter + create-on-behalf-of with different leave type. |
| **Notes** | Well-calibrated hard. hr.leave has no native refuse_reason — captured as chatter message. BU created a duplicate leave (one with 0 days) before producing the correct 3-day record; semantic check.py passed but strict scoring penalised the dup. |

---

## crm.assign_team_change_salesperson_log_activity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | CRM |
| **Workflow** | Open seeded opportunity 'Bench Big Deal'. Switch to Contacts tab → Ownership group, change Team from Direct Sales to Channel and Salesperson from admin to Sara Sales. Schedule a Call activity for 2026-06-10 with summary 'Discovery call'. Save. |
| **Capability tested** | Hidden Many2one fields (team_id only in Contacts tab on opportunities) + activity scheduling. |
| **Notes** | Easier than medium — BU solved on first try after switching to Contacts tab. team_id is invisible in the main form header for opportunities (only visible on leads); editable copy lives under Contacts > Ownership group. |

---

## mrp.scrap_component_during_partial_production

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Manufacturing |
| **Workflow** | Open MO M-BENCH-SCRAP-001, click cog → Scrap (binding action), set product=ScrewA + qty=2 + tag=Defective batch + source=stock, validate scrap. Then Produce All → Mark As Done. |
| **Capability tested** | Scrap binding action via cog menu + non-default qty edit on wizard + tag picker. |
| **Notes** | Well-calibrated hard. BU left scrap_qty at default 1.0 instead of 2 — the calibration trap. RequiredOpRecall=1.0 (BU did open and validate the wizard). Strict F1=0.0 (1 missing + 1 extra edit). |

---

## hr_expense.create_with_currency_eur_to_usd

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Expenses |
| **Workflow** | Create expense 'NYC Hotel' product=Hotel, total=200 USD, date=2026-04-01, paid by employee. (Sheet/report wrapper removed in Odoo 19; expense is the unit.) Verify EUR conversion ≈ 185. |
| **Capability tested** | Multi-currency dropdown selection + computed amount conversion. |
| **Notes** | Well-calibrated medium. BU completed correct fields but created the expense twice — postcondition "exactly 1 expense" fails. Currency dropdown gated by base.group_multi_currency; res.currency records start active=False in fresh DBs. |

---

## website_sale.add_optional_at_cart_remove_main_keep_optional

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (eCommerce) |
| **Workflow** | From /shop add Bench Camera, accept Bench Tripod optional in upsell modal. Then on /shop/cart click per-line trash on Bench Camera only, leaving Bench Tripod orphaned in draft cart. |
| **Capability tested** | Optional-products modal + selective per-line trash on public webshop. |
| **Notes** | Well-calibrated hard. BU made 196 API calls but never drove the optional-products modal reliably. Postcondition is the source of truth (StateDiff empty by design). |

---

## event_product.create_event_product_link_to_ticket

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Events, Sales (event_product) |
| **Workflow** | Create product 'Conference Pass Std' (type=service, list_price=100, service_tracking=event). Open seeded event 'Spring Summit'. Add ticket 'Standard Pass' with product=Conference Pass Std, price=100, seats_max=200. |
| **Capability tested** | Cross-app product creation with event-specific service_tracking + ticket linking. |
| **Notes** | Easier than medium — BU solved on first run (204s). Note: product.template has 2 pre-existing 'Gift Card' duplicates in base snapshot — match_key must include service_tracking + list_price to avoid diff-engine swapping. service_tracking field is invisible in base product view; event_sale (auto-installed) removes the invisible attr to expose the 'event' option. |

---

## website.create_contact_form_with_custom_field

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website |
| **Workflow** | Edit Contact Us page in website editor. Add a Selection field "Inquiry Type" with options Sales/Support/Partnership; required. Save and publish. |
| **Capability tested** | Website builder drag-drop + form field config (selection options + required flag). |
| **Notes** | Well-calibrated hard. BU never called ir.ui.view.write within 480s — website editor iframe + form-field config defeated it. expected_state empty by design (content lives in view arch which isn't diffed). Note: Odoo 19 renders custom Selection form fields as radios in s_website_form_multiple, not <select>; <select> only appears for many2one or if Display is switched to select dropdown. |

---

## website_sale.create_gift_card_apply_in_cart

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Website (eCommerce), Loyalty |
| **Workflow** | Configure Gift Card program (loyalty.program.create_from_template). Generate 1 gift card code worth €50. In /shop/cart with €100 product, enter code → €50 deducted → total €50. |
| **Capability tested** | Two-stage workflow: backend Generate Gift Cards wizard + portal redemption via /shop/pricelist POST. |
| **Notes** | Easier than hard. BU solved in 185s; Generate wizard only exposes qty/value/description so the wizard-with-non-default-values trap didn't fire. Workflow length justifies tier 3 listing. |

---

## hr.create_department_assign_manager_three_employees

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | HR |
| **Workflow** | Create department 'Bench Engineering' with manager Mike Manager. Open each of 3 seeded employees (Eng One, Eng Two, Eng Three) and set department_id=Bench Engineering. |
| **Capability tested** | Bulk reassignment across N records — attention to completeness. |
| **Notes** | Well-calibrated medium. BU created dept correctly + assigned Eng One + Eng Two, but **cleared** Eng Three's department_id to null instead of setting Bench Engineering — exactly the "may forget one" trap. |

---

## stock.create_putaway_rule_for_specific_category

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 109.3s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory |
| **Workflow** | Navigate Inventory > Configuration > Putaway Rules; click New to add an inline editable row; fill location_in_id=WH/Stock, category_id=Bench Cold Items (NOT product_id), location_out_id=WH/Stock/Refrigerator; save the list. |
| **Capability tested** | Selecting the non-default Product Category column (not the default Product column) when both autocomplete fields are visible side-by-side and become mutually-readonly when one is set. |
| **Notes** | Calibrated as `hard` but BU passed first attempt with F1=1.0. The editable=bottom list view exposes both Product and Product Category columns; once the agent reads the prompt's explicit "Product Category" instruction, the choice is unambiguous and BU has no trouble. The mutual-readonly side-effect (filling category greys out product, and vice versa) actually HELPS BU because it makes the choice visually obvious. To make this genuinely hard, would need to combine with another non-default selection (e.g., a Storage Category dropdown that becomes required when sublocation='closest_location') or move to a wizard with radio buttons. |

---

## sale.add_line_with_optional_template_apply_discount

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales |
| **Workflow** | Open seeded draft SO (customer reference S-BENCH-OPT-001, customer Bench Optional Co). Click "Add a product" in the order lines, pick "Bench Service Bundle" from the autocomplete, set qty=2 and per-line Discount=10 on that new row, then Save (do not Confirm). |
| **Capability tested** | Inline one2many row creation + per-row discount entry while leaving an existing line untouched. |
| **Notes** | Seed enables `sale.group_discount_per_so_line` so the Discount column renders on the line. "Bench Service Bundle" is a service product; "Bench Hardware Kit" is the pre-existing consumable line. Both Oracle (32s) and Browser-Use (143s) solved the task cleanly with F1=1.0 on first attempt, so the task calibrates EASIER than medium — the inline add+discount pattern is well within BU's current capability once the discount group is pre-enabled. No unauthorized writes, no forbidden ops. |

---

## project.create_kanban_stage_reorder_drag

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Open seeded project 'Bench Project A' (grouped kanban of its tasks with pre-seeded stages Triage/In Progress/Review/Done). Unfold the `.o_column_quick_create` chevron at the right edge, type 'Backlog Review', confirm. Then drag the new 'Backlog Review' column header leftward so it drops between 'Triage' and 'In Progress'. |
| **Capability tested** | Kanban column quick-create + column drag-reorder (web_resequence via Owl's useSortable) — a UI interaction pattern distinct from the existing card-drag task (project.kanban_drag_task_between_stages), since it moves GROUPS not RECORDS and involves two web_resequence RPCs (one implicit on create, one on drag). |
| **Notes** | Oracle uses an emulated slow mouse drag on the `.o_column_title` handle (the `KanbanRenderer` useSortable config pins `handle: ".o_column_title"`). Browser-use created 'Backlog Review' correctly (single `name_create` + auto `web_resequence` to place at end) but could NOT drag the column to position #2 — left it at position #5 (far right). Classic drag-reorder failure mode predicted in the backlog calibration note. Seed intentionally uses sparse sequences (10/20/30/40) so the kanban's reorderAll branch renumbers everything starting at min(sequences)=1 on the first web_resequence; check.py is sequence-agnostic and validates left-to-right ordering instead. |

---

## contacts.merge_three_duplicates_keep_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Seed four res.partner rows named "John Doe" (refs BENCH-JD-01 empty, JD-02 email=john@x.com, JD-03 phone=555-1234) plus a decoy JD-DECOY under Acme Corp. In /odoo/contacts list view, select only the three refs without a parent company, Actions > Merge, set Destination Contact = the JD with email john@x.com (BENCH-JD-02) via the partner_show_db_id-tagged dropdown, click Merge Contacts. Final survivor must be BENCH-JD-02 with email=john@x.com AND phone=555-1234. |
| **Capability tested** | 3-way merge with explicit master selection. Agent must read the prompt's master-selection rule and pick the non-default dst_partner_id, and must NOT include the Acme Corp decoy in the selection. |
| **Notes** | Well-calibrated hard. BU completed the Actions>Merge flow and called `action_merge`, but left the default dst_partner_id (BENCH-JD-01, the first partner by id) instead of switching to the email-bearing BENCH-JD-02 — exactly the non-default wizard trap. The merge did preserve email+phone, but check.py asserts the survivor ref so the wrong master fails. Task also verifies the decoy (JD-DECOY under Acme Corp) is untouched. Note: the base Odoo 19 merge wizard does NOT have per-field source tabs; field preservation is deterministic via `_update_values` (src_partners, dst last) — since the 3 duplicates have disjoint email/phone, any master produces the same email+phone on the survivor, so the distinguishing difficulty is picking the right *survivor ref* and excluding the decoy. |

---

## mail.invite_external_email_to_existing_channel

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 230.4s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Discuss |
| **Workflow** | Open seeded private group channel 'project-discussion'. In channel header click "Invite People" icon. In unified search input type `external-guest@bench.test`, wait for the envelope-icon email-fallback row to appear, click it to select, then click "Invite to Group Chat". This triggers `discuss.channel.invite_by_email` and creates a `mail.mail`. |
| **Capability tested** | Non-default selectable row in an Owl side panel — the email fallback only appears after a complete valid email is typed and no partner matches. Distinct from the typical "add internal member" pathway. |
| **Notes** | Odoo 19 has NO "Email tab" in the invite dialog (despite row 323 task-spec text) — only a single unified input; restructured the prompt to "click the envelope row" instead. Seed spins up a detached aiosmtpd sink on 127.0.0.1:2525 and registers an ir.mail_server pointing at it, plus sets admin.partner_id.email and mail.catchall.domain/mail.default.from ICPs, because invite_by_email calls `.send(raise_exception=True)` which rolls back the mail.mail on any SMTP or sender-missing failure. BU solved on first attempt (230s) — calibrated EASIER than medium, but keeps pathway coverage (invite_by_email vs the usual add_members). Also discovered and fixed two worktree-infra issues: (a) the copied skeleton .venv's `_editable_impl_odoo_benchmark.pth` pointed at the original skeleton-source worktree and needed to be rewritten to the current worktree root before oracle/check subprocess scripts could `import benchmark`; (b) `/tmp/benchmark_snapshots/benchmark_base.dump` was a 16KB stub restored from an uninitialised DB — re-dumped from a healthy per-task DB. See COOKBOOK_NOTES.md for the full aiosmtpd + ir.mail_server seed pattern. |

---

## hr_holidays.bulk_approve_two_pending_requests

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.6667 |
| **Odoo modules** | HR Holidays (Time Off) |
| **Workflow** | Navigate to `/odoo/time-off-approval`, switch to list view, clear default "Waiting For Me" facets, tick exactly the two checkboxes on Eve Pending's "Family vacation" row and Frank Pending's "Wedding attendance" row, then click the **Approve** bulk button that the `hr_holidays_payslip_list` JS controller renders in the list selection-actions slot. A third pending request (Alice Pending's "Personal errands") must stay in `confirm` state and two distractor leaves (one `validate`, one `refuse`) must be untouched. |
| **Capability tested** | Multi-record list selection combined with a non-generic bulk action button (not the built-in cog Actions menu; the custom `MultiRecordViewButton` shown by `HolidaysListController.displayButton`). Calibration trap: selecting all pending rows flips Alice's leave to `validate`, and approving each one individually violates the bulk-only instruction. |
| **Notes** | BU flipped Eve + Frank to `validate` and kept Alice's state at `confirm` — but on the way it silently CREATED an extra `hr.leave` with `state='confirm'` (null name), dragging Strict down to FAIL (Precision=0.5, Recall=1.0, F1=0.6667). Postcondition `check.py` passed on the canonical named records; the state-diff engine counts the stray create as 2 unexpected extras. Genuine hard-tier failure via Strict scoring. |

---

## event.add_track_with_speaker_publish

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 68.6s wall clock, 11 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Events (event + website_event + website_event_track) |
| **Workflow** | Seed installs website_event/website_event_track on demand (not in base snapshot) and creates one unpublished event "Bench Spring Summit". Agent opens Events app, drills into the event, clicks the Tracks smart button, clicks New, enters title "Keynote: Future of Bench" + Track Date 05/15/2026 10:00:00 + Speaker-tab partner_name="Dr. Smith" + partner_email="dr.smith@example.com", saves, then clicks the Published stage on the status bar so `_synchronize_with_stage` flips is_published=True. |
| **Capability tested** | Sub-resource creation on a smart-button sub-view with multi-tab field entry + stage-driven publish side-effect. The "Go to Website" button (widget=`website_redirect_button`) only navigates — publish must happen via the stage bar, not the header widget. |
| **Notes** | Calibrated easier than medium (BU solved on single-shot with the explicit prompt). Kept at medium because it still covers the smart-button → sub-form → notebook-tab → status-bar chain, and because it seeds the publish-via-stage pattern for harder event.track tasks later. New cookbook entry: `event.track` publish control — the backend form's globe button does NOT toggle is_published; only stage transitions to a stage with `is_fully_accessible=True` do (default data: the "Published" stage at sequence=4). Also confirmed that `website_event` + `website_event_track` need on-demand `button_immediate_install` in seed.py (they are not in the base snapshot). |

---

## crm.create_lead_from_email_alias_log_message

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM (+ mail.alias, crm.team) |
| **Workflow** | Configure CRM team 'Inbound' Email Alias to `leads-inbound` (inline input, mid-form under Team Details) + set Accept Emails From to Authenticated Partners (Odoo `o_select_menu` custom dropdown, NOT a native `<select>`). Create a new lead `Inbound Inquiry from Sample` with email_from `prospect@external.test`, priority Medium (single star), and existing `Website` tag. Post a regular chatter message `Asked about Bench Pro pricing.` (Send message, not Log note). |
| **Capability tested** | Three-surface workflow (team config + lead creation + chatter) with stacked calibration traps: custom `o_select_menu` widget, single-star priority, many2many tag autocomplete with distractor, and Send-message vs Log-note distinction. |
| **Notes** | First pass of the task (alias_name + lead + chatter only) was trivially passed by BU with F1=1.0 in 228s — alias field on the main form is too visually obvious. Hardened by stacking (a) `alias_contact -> Authenticated Partners` (custom select-menu), (b) `priority = Medium` (one star, BU canonical trap), (c) existing `Website` tag with distractor `Web-Inquiry` in autocomplete. Post-hardening BU hit 5/5 state diff but silently skipped the tag -> postcondition FAIL. Oracle uses `.o_select_menu_toggler` + `.o_select_menu_item:has-text(...)` for alias_contact. `crm.lead.name` widget=text (textarea) — must use `fill_text_field`, not `fill_field`. |

---

## website_sale.set_product_seo_title_meta

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 81.9s wall clock, 11 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Website (eCommerce) |
| **Workflow** | Seed a published product 'Bench SEO Widget' with empty website_meta_title / website_meta_description. Agent opens /odoo/ecommerce-products, clicks the product (lands on backend product form), clicks the header "Go to Website" button to reach /shop/bench-seo-widget, opens the Site menu → This Page → Optimize SEO, fills Title='Buy Bench SEO Widget Online' and Description='Premium widget for benchmarking with fast delivery.' in the Owl dialog, clicks Save. |
| **Capability tested** | Reach a dialog that is NOT on the backend product form — SEO fields live on the `website.seo.metadata` mixin and are only editable through the frontend OptimizeSEODialog (registered under `website.menu_optimize_seo` in the `website_custom_menus` service). Forces the agent to pivot from backend list view to frontend Site menu. |
| **Notes** | Calibrated as easy (~80% target) and BU solved first-shot in 81.9s. `is_seo_optimized` (computed+stored) flips False→True as a side effect of writing either meta field — placed in `ignore_fields` to keep the diff to exactly two atomic set edits. Oracle uses JSON-RPC write() bypass because the Owl dialog + iframe combo is fragile to script via Playwright and bypass is explicitly sanctioned for oracles. No forbidden ops; HarmfulWriteRate 0.0. See COOKBOOK_NOTES.md for the "SEO fields live on a mixin, not on the product form" quirk. |

---

## point_of_sale.attach_customer_apply_loyalty

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 91.5s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale, loyalty, pos_loyalty (auto-installed via sale_loyalty in base) |
| **Workflow** | Open the seeded Bench Loyalty POS register, add Bench POS Item x3 (EUR 60.00), click Customer on the action pad and pick Loyal Larry, open the Rewards popup and redeem the '10% on your order' loyalty-funded reward for 50 points (-EUR 6.00), then pay Bench Loyalty Cash 54.00 and validate. |
| **Capability tested** | POS kiosk UI: attach a seeded customer mid-sale, open the Rewards popup, redeem a discount reward funded by the customer's loyalty.card point balance, pay cash, validate. Cross-module loyalty + POS. |
| **Notes** | pos_loyalty auto-installs when both point_of_sale and loyalty are present; both are in base via sale_loyalty, no module install needed in seed. Seed creates a loyalty.program (program_type='loyalty', applies_on='both', reward=10% order discount at 50 points) scoped to the new POS config via pos_config_ids, and mints a loyalty.card for Loyal Larry with 100 points (exactly enough for one redemption, not two). Oracle uses the JSON-RPC call_kw bypass pattern. Calibration: browser-use solved on the first 91s run (F1=1.0) — the Rewards popup and customer autocomplete are well labelled, so the combined customer-attach + loyalty-redeem + cash-pay flow does NOT stack into a hard pattern. Earn-rule side note: reward_point_amount=1 on the order earn-rule means the POS awards 1 point on the same order the reward is redeemed, so the card ends at 51 points (100 + 1 earn - 50 redeem); check.py accepts ~51. To re-harden, require a non-default reward among multiple listed rewards, combine with a per-line discount, or add a cash reconciliation mismatch on session close. |

---

## website_blog.create_tag_assign_to_three_posts

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (gave_up=True at 360s) |
| **F1** | 0.0 |
| **Odoo modules** | website_blog |
| **Workflow** | Create a new `blog.tag` named `Q2-2026` via `/odoo/blog-tags`, then loop through three seeded `blog.post` records (Post-A, Post-B, Post-C) and add the tag on each post's `tag_ids` m2m (many2many_tags widget). A fourth seeded post (Post-D) acts as a distractor that must remain untagged. |
| **Capability tested** | Tag creation + bulk m2m assignment across multiple records with a "do-not-touch-the-distractor" negative constraint. Same bulk-loop trap as row 321 (hr.create_department_assign_manager_three_employees), but with the added temptation of the tag form's reverse `post_ids` m2m labeled "Used in:" which could let BU mass-assign from the wrong side. |
| **Notes** | BU successfully created the `Q2-2026` tag (1 matching create edit on `blog.tag`) and issued 172 writes total, but timed out with `gave_up=True` at 360s without landing the tag on a single post. Postconditions flagged Post-A/B/C all missing the tag. Distractor Post-D stayed clean. Failure is harsher than the "forget one" trap predicted — BU never made it past the tag form into the per-post loop. Oracle writes `tag_ids: [[4, tagId]]` via JSON-RPC because the `many2many_tags` autocomplete can be brittle under Playwright; BU's UI route is the authentic failure test. New cookbook note: `blog.tag.name` has a UNIQUE constraint (`_name_uniq`), and the tag form's "Used in:" reverse m2m (`post_ids`) is a natural shortcut BU can get lured into — adding a distractor post punishes the "select all posts" branch. |

---

## account.create_recurring_journal_entry

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 213s first run + 288s second run; both passed) |
| **F1** | 1.0 |
| **Odoo modules** | Accounting (account) |
| **Workflow** | Accounting -> Journal Entries (path `/odoo/accounting/entries`, NOT Customer Invoices). New -> Reference='Bench Rent Apr', Accounting Date 2026-05-01, Journal=Miscellaneous Operations. Three balanced Journal Items: Rent debit 1000, Tax Paid debit 50, Bank credit 1050. Save. Chatter Activities -> schedule To-Do "Post next month's rent entry" due 2026-06-01. Click Post. |
| **Capability tested** | Distinct move_type='entry' form (no Customer, Debit/Credit columns, `line_ids` not `invoice_line_ids`); multi-line balance with 3 lines including a tax line; chatter activity scheduling; entry-specific Post button. |
| **Notes** | Calibrated hard but BU passed twice. The Journal Items tab is only visible with `account.group_account_readonly`; seed explicitly grants admin `readonly/invoice/user` accounting groups via `res.groups.user_ids` (NOT `users`). The `name` column widget is `section_and_note_text` -> renders `<textarea>`; cell filler uses `input, textarea`. Account autocomplete displays "<code> <name>" so filtering on `has_text='Rent'` wrongly matches "Cur**rent** Assets"; oracle splits on whitespace and matches `parts[1]` exactly. Activity type stored as "To-Do" with hyphen. Per-calibration 3rd line (Tax Paid 50) added to escape trivial 2-line pattern, but BU still solved — further hardening would require analytic_distribution or per-line partner. |

---

## calendar.invite_organize_with_event_agenda_attachment

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 10.8s) |
| **Browser-Use** | FAIL (F1=0.0 — postcondition failed, 82.2s) |
| **F1** | 0.0 |
| **Odoo modules** | Calendar, mail (chatter attachments) |
| **Workflow** | Open /odoo/calendar, click New, set Title='Q2 Planning Session', date 2026-05-20, start 14:00 end 15:30 (timed, not all-day, no recurrence), add attendees Alice Bench + Bob Bench via the Attendees m2m autocomplete, then upload the seeded agenda.txt via the chatter paperclip (FileUploader → hidden input[type=file]) so an ir.attachment named 'agenda.txt' is linked to the event (res_model='calendar.event', res_id=event.id). Save. |
| **Capability tested** | File upload through the chatter's hidden `<input type=file>` (canonical BU weakness). Also tests timezone-aware datetime entry + many2many attendee autocomplete selection among existing contacts. |
| **Notes** | Hard by calibration and outcome. BU correctly created the event + added both attendees but could NOT upload the file: the runner does not pass `available_file_paths` through to the browser-use Agent, so every attempt returns `File path ... is not available. To fix: ...available_file_paths...`. Event also was not saved after the agent gave up on the upload. Oracle uses pure JSON-RPC `call_kw` (calendar.event.create + ir.attachment.create with base64 datas) — same pattern used by mail.create_channel_set_custom_avatar_pin_two_messages. State_spec tracks only calendar.event (not ir.attachment) because creating an event with attendees auto-generates one `invitation.ics` ir.attachment per invitee plus the public asset cache flows through ir.attachment on first page load; both would swamp the diff. Attachment existence is verified in `check.py`. See COOKBOOK_NOTES.md for the full list of quirks (admin tz not UTC in base snapshot, invitation.ics side-effect, BU available_file_paths sandbox). |

---

## hr_recruitment.skill_filter_then_send_offer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 97.9s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment (hr_recruitment, hr_recruitment_skills), Mail |
| **Workflow** | Seed 5 applicants (Alice Senior/Bob Junior/Eve Contractor all on QA Lead; Dana Pirate on Senior Backend Developer; Charlie Jones JS-only distractor). Agent opens `/odoo/recruitment-applications`, switches to list, types `Python` in search and picks the **Skills** autocomplete facet (extends `applicant_skill_ids`). Four rows remain. Agent ticks ONLY Alice Senior (only one simultaneously on QA Lead AND tagged Senior), opens cog Actions → Send Email, fills Subject "Job Offer - QA Lead" and body containing "2026-06-01", clicks Send. Wizard runs `applicant.send.mail.action_send` which posts a `mail.message` on Alice. |
| **Capability tested** | Custom m2m search-filter facet selection (Skills vs Applicant/Tag/Job autocomplete rows), 4-way disambiguation on two independent conditions (job AND tag), cog Actions server-action bound to list/kanban only (NOT form), `applicant.send.mail` wizard with required subject + body overrides. |
| **Notes** | Calibration FAILED (too easy): single-shot BU solved it with F1=1.0 in 97.9s, picking Alice correctly and filling subject+body on first try. The Claude-Opus model driving BU reads the prompt's explicit three-condition breakdown and derives Alice deterministically. Prompt was already rewritten once to remove the per-distractor "Bob is Junior, Dana is wrong job" explanations, but the remaining "QA Lead + Senior + Python" trio is still trivial. Further hardening paths: (a) hide the tag column in the default list view and require a chatter-clue to infer seniority, or (b) require an uncommon wizard action like uploading an attachment or picking a non-default template. New cookbook entries in `COOKBOOK_NOTES.md`: `hr_recruitment_skills` + `hr_skills` are both `auto_install=True` (already active in base), `hr_recruitment.action_applicant_send_mail` uses `binding_view_types="list,kanban"` so the cog Send Email action is NOT available from the form view. State-diff entity_key for `mail.message` uses `[record_name, subject]` match_key; 4 deterministic atomic edits (subject/model/record_name/message_type) per offer email. `res_id` goes to `ignore_fields` because it is run-specific. |

---

## sale.create_quotation_with_customer_pricelist

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 88.3s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Sales (sale), Product (product.pricelist), Contacts |
| **Workflow** | Seed creates product `Bench Standard Widget` (list_price 100, no taxes), a `VIP 20% Off` `product.pricelist` with a single global `applied_on=3_global, compute_price=percentage, percent_price=20, base=list_price` item, a customer `Bench Premium Co` whose `specific_property_product_pricelist` is set to that pricelist, and a distractor `Bench Regular Co` with no pricelist. The `product.group_product_pricelist` group is granted to both `base.user_admin` and `base.user_root` (feature flag — see below). Agent clicks New in /odoo/sales, picks Bench Premium Co (pricelist auto-applies via `_compute_pricelist_id`), adds one `Bench Standard Widget` line with qty 5, saves without confirming. |
| **Capability tested** | Partner-driven pricelist auto-application on sale.order; letting Odoo's compute produce the discounted `price_unit` (80.00) rather than manually typing a price; leaving an unfamiliar auto-filled header field (pricelist_id) alone. |
| **Notes** | Calibration: task is currently PASS/PASS at F1=1.0 for browser-use on first attempt — medium tier retained as a positive-signal baseline for the pricelist pattern. Two non-obvious Odoo 19 quirks surfaced while building: (1) `product.pricelist._get_partner_pricelist_multi` short-circuits to an **empty** result unless `product.group_product_pricelist` is enabled on `SUPERUSER_ID` (not just the admin user) — granting the group only to `base.user_admin` leaves the compute returning no pricelist, so customers appear to have no linked pricelist even when `specific_property_product_pricelist` is set; seed must grant the group to `base.user_root` as well. (2) `sale.order.pricelist_id.display_name` surfaces in the state-diff as `"VIP 20% Off (USD)"` (currency suffix appended by `display_name`), not the raw pricelist name — `expected_state.json` must encode the `(USD)` suffix. (3) The SO lines editor uses the `sol_o2m` widget whose inline cell name is `product_template_id`, not `product_id`; oracles that call `set_o2m_many2one(page, 0, "product_id", ...)` time out. All three are now recorded in COOKBOOK_NOTES.md. |

---

## mrp_account.confirm_mo_check_account_move

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 22.5s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 106.4s, 15 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Manufacturing (mrp), Accounting (account, stock_account, mrp_account auto-installed) |
| **Workflow** | Seed a product category with `property_valuation='real_time'` + `property_cost_method='standard'`, finished product **Bench Manuf Item** (standard_price=100) + 3 components (frame/bolt/panel) in that category, stock components on-hand at main WH stock, BoM (1 Bench Manuf Item = 1 frame + 4 bolts + 1 panel), **confirmed** MO `M-BENCH-ACC-001` for 5 units. Crucially the Production location (`usage='production'`) gets a Cost of Production expense account written to `valuation_account_id`, and the WH Stock internal location gets `company.account_stock_valuation_id` on the same field — without this, `_should_create_account_move` returns False and no journal entry ever gets created. Agent: open `/odoo/manufacturing`, open MO, click **Produce All** (single click — no backorder since components are on-hand), MO state flips to `done`. Then navigate to `/odoo/accounting/entries` (Accounting → Journal Entries), verify STJ/YYYY/MM/#### entry posted by `stock_account._create_account_move` → `account.move._post()`. |
| **Capability tested** | Cross-module handoff (Manufacturing MO close triggers `stock_account` auto-journal creation in the background; agent must navigate to Accounting → Journal Entries to observe it). Also tests resisting the temptation to manually post the entry (the prompt explicitly forbids it — the entry is auto-posted). Check.py verifies `mo.move_raw_ids | mo.move_finished_ids` each have `.account_move_id` (Many2one, singular, NOT `account_move_ids`) and every linked move is in `state='posted'`. |
| **Notes** | BU solved it in 15 steps on first try (calibration for MEDIUM = acceptable). Key design insights baked into COOKBOOK_NOTES.md: (1) `stock.move.account_move_id` is Many2one not M2M; (2) mrp_account's only MO smart button is "WIP" (`action_view_move_wip`), visible only when `wip_move_count > 0` — which requires running the `mrp.account.wip.accounting` wizard on workorders with recorded times; vanilla MO close leaves it hidden. (3) Base-snapshot stock.location records have `valuation_account_id=NULL` so nothing triggers without the Production-location + Stock-location seed writes. (4) `property_valuation='real_time'` on the category alone is NOT enough. Auto-generated entry lives in "Inventory Valuation" journal (`account.journal.type='general'`) with name `STJ/YYYY/MM/####`. BU correctly verified: Posted state, $500 Stock Valuation debit vs Cost of Production credit, ref contains "M-BENCH-ACC-001". No cookbook quirks beyond these. |

---

## survey.invite_attendees_send_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (19s) |
| **Browser-Use** | PASS (F1=1.0, 136.2s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Surveys, Mail (ir.mail_server, aiosmtpd sink) |
| **Workflow** | Seed survey 'Bench Onboarding Quiz' with `access_mode='token'` and three pre-existing `res.partner` rows (Alice/Bob/Carol Invitee keyed by alice@x.com / bob@y.com / carol@z.com). Agent opens the survey from kanban, clicks the form-header **Send** button (`survey.survey.action_send_survey`), which opens the `survey.invite` wizard with Send-by-Email on by default. Agent types each email in the **Recipients** many2many_tags_email autocomplete, picks the matching seeded partner (three chips accumulate), clears and replaces **Subject** with 'Please complete onboarding', then clicks the modal-footer **Send** (`survey.invite.action_invite`). One `survey.user_input` row is created per invited partner with `state='new'`. |
| **Capability tested** | Multi-recipient compose wizard (tag-input + subject override) on a transient wizard whose `partner_ids` is hard-required (can't send with emails-only free text). |
| **Notes** | Calibration: BU solves in 136s with F1=1.0 (clean pass). Confirms that compose-wizard flows where the required field is an autocomplete-over-seeded-partners are tractable for BU as long as the recipient search is keyed by a user-provided identifier (email). New cookbook findings: (a) `survey.invite.partner_ids` is `required="True"` with `options="{'no_quick_create': True}"` — the Additional-emails text area is a distractor, sending with emails-only is UI-blocked; (b) `_compute_send_email` flips True only for `access_mode in ('token','authentication','internal')` — `public` surveys open the wizard with all compose fields hidden; (c) seed must stand up an aiosmtpd Sink + matching `ir.mail_server` + `mail.catchall.domain`/`mail.default.from` ICPs so any sync SMTP failure inside `action_invite` does NOT roll back the created `survey.user_input` rows; (d) state-diff emits two `create` rows per recipient — one for `email`, one for `state='new'` — both must be in `expected_state.json` to reach F1=1.0. |

---

## hr.add_skill_to_employee_with_level

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.4s) |
| **Browser-Use** | PASS (F1=1.0, 82.0s) |
| **F1** | 1.0 |
| **Odoo modules** | Employees (hr, hr_skills) |
| **Workflow** | Open /odoo/employees, pick seeded employee 'Tech Tom', navigate to the Resume tab (Skills section at the bottom), click 'Pick a skill from the list', and in the Update Skills modal use the cascading `o_selection_badge` groups: Skill Type='Programming Languages' → Skill='Python' → Level='Advanced'. Save & Close, then save the employee form. |
| **Capability tested** | Cascading dependent-dropdown interaction via the skill picker modal: the Skill list is filtered by Skill Type, and the Level set depends on Skill Type too. Distinct from `hr.add_employee_skill` by using a different skill type ('Programming Languages' vs 'IT Skills') so the entity keys don't collide. |
| **Notes** | Calibration: single-shot BU passes (F1=1.0). The cascading UI didn't block BU on Claude-Opus. Seed installs `hr_skills` defensively though it's already pulled into base via `hr_recruitment_skills` auto_install. match_key `[employee_id, skill_id]` — 4 deterministic atomic edits (employee_id/skill_id/skill_type_id/skill_level_id) on the new `hr.employee.skill`. No pre-existing row for Tom so entity is created by the agent. |

---

## purchase.send_rfq_email_with_template_signature

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 89.1s wall clock, 13 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Purchase, Mail |
| **Workflow** | Seed draft RFQ `R-BENCH-EMAIL-001` for vendor "Beacon Electrical Ltd." (2 lines, distractor `R-BENCH-EMAIL-002` same vendor). Agent opens `/odoo/purchase`, clicks the RFQ, clicks the **Send RFQ** header button (draft state). In the Compose Email wizard the agent must switch the pre-loaded **Purchase: Request For Quotation** template to **Purchase: Purchase Order** via the `.mail-composer-template-dropdown-btn` (ellipsis-v icon) template selector, then append `Please confirm by Friday.` to the end of the re-rendered body, then click the primary **Send**. The purchase `_notify_thread` override (`mark_rfq_as_sent=True` context) flips `state: draft → sent` as a side effect of send. |
| **Capability tested** | Non-default template selection via an Owl `<Dropdown>` portaled OUT of the modal (dropdown menu is at page level, not inside `.modal`), template-switch BEFORE body-append sequencing (onchange wipes body on switch), body append into `html_composer_message` editor without clicking into it (pointer-intercept from `.o_technical_modal` overlay forces JS-based caret placement), primary-vs-disabled Send-button twin resolution. |
| **Notes** | BU solved on first run (model `bu-1-0`) in 89s / 13 steps. It correctly swapped the template *before* typing the append and placed the sentence after the signature. Calibration therefore landed easier than hard — kept at tier 3 for workflow length + wizard density. Two new cookbook quirks: (1) both `purchase.email_template_edi_purchase` and `..._done` ship with `report_template_ids` that require `wkhtmltopdf` to render a PDF attachment — on benchmark runners that binary is absent, so Send RFQ pops "Invalid Operation — Unable to find Wkhtmltopdf" instead of the compose wizard; seed must `tpl.report_template_ids = [(5, 0, 0)]` on both templates. (2) The `mail_composer_template_selector` widget renders only as a `.mail-composer-template-dropdown-btn` ellipsis-v icon; its menu is portaled to a page-level `.mail-composer-template-dropdown` container, so `modal.locator(".dropdown-item")` returns 0. Oracle must query the dropdown items at page scope. Also re-confirms SMTP-sink cookbook from row 323: `aiosmtpd` Sink on `127.0.0.1:2525` + benchmark `ir.mail_server` required so `mail.mail.send(raise_exception=True)` doesn't roll back the whole transaction. Distractor leak-check uses `message_type='email_outgoing'` because the auto-"RFQ Sent" internal notification is logged on every PO that fires `action_rfq_send`. |

---

## stock.cancel_picking_create_replacement_with_serial

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (F1=0.0, 8/8 state edits matched but demand postcondition fails, 249.1s wall clock) |
| **F1** | 0.0 |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Seed a ready vendor receipt `R-BENCH-CANCEL-001` for `Bench Supplier Inc` carrying `Bench Hardware Item` qty=5, plus a separate `Bench Serial Widget` product tracked by `serial`. Agent opens the receipt and clicks header **Cancel** (state → `cancel`). Then creates a new receipt for the same vendor, adds a single line for `Bench Serial Widget` with Demand=2, clicks **Mark as Todo** (Odoo 19 label for `action_confirm` on receipts), opens the move line's **Details** popup, ensures exactly 2 `stock.move.line` rows exist, enters `BS-001` / `BS-002` via the `lot_name` autocomplete "Create" option with Quantity 1 each, saves, then **Validate** → state `done`. |
| **Capability tested** | Recovery/rollback (cancel a wrong picking before recreating), from-scratch form creation with serial-tracked product, per-move_line serial assignment via the Detailed Operations popup, non-obvious header button labels (`Mark as Todo`), phantom-empty-row sweep in editable-bottom list popup. |
| **Notes** | Calibration PASSED: single-shot BU (249s wall clock) filled serials and cancelled the original correctly but left **Demand=0** on the replacement line; `check.py` asserts `product_uom_qty==2.0` and the postcondition gate downgrades F1→0.0. Observed BU pattern: skips the Demand cell because the move_line qty=1+1 already sums to 2 so Validate succeeds without it. Oracle quirks captured in `COOKBOOK_NOTES.md`: (1) `stock.picking.action_confirm` button string is `"Mark as Todo"` on receipts (not "Confirm"); (2) `move_ids` list `add-label="Add a Product"` (not "Add a line"); (3) `/odoo/inventory/receipts` is the stable path from `action_picking_tree_incoming path="receipts"`; (4) `stock.move.show_details_visible` returns False while `state=='draft'`, so Part C must wait until after Mark-as-Todo; (5) editable-bottom detailed-ops list auto-appends a phantom row after Tab on last cell — oracle sweeps and deletes rows with empty lot_name to avoid the "You need to supply a lot/serial number" validation error; (6) state-diff entity_key for a created picking with `match_key=[origin, partner_id]` emits `[null, "Bench Supplier Inc"]` (not the auto-assigned `WH/IN/…` name) because `origin=False` normalizes to JSON `null`. |

---

## website.add_image_carousel_to_homepage

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 20.3s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 91.5s, 14 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Website (html_builder, website snippets) |
| **Workflow** | Seed creates `/bench-gallery-test` website.page with a minimal heading + paragraph inside an `oe_structure oe_empty` wrap. Agent opens the page in the website builder (editor enabled), finds the Image Gallery snippet (labelled "Carousel" in the preview dialog) under the Images group, clicks-to-insert, and hits Save. Validation is via arch_db containing `s_image_gallery` and `>=3 <img>` tags after save — check.py is the source of truth since state_spec only tracks name/url/is_published (unchanged), making expected_state.json an intentional empty list. |
| **Capability tested** | Website builder block-insertion flow (sidebar → Images group → Carousel preview click → snippet lands in iframe body → Save). Tests iframe-aware editing, snippet preview dialog interaction, and the asynchronous save pipeline that persists the new arch via an `ir.ui.view.save` hop. |
| **Notes** | Originally spec'd as a home-page drop which caused the prior agent run to stall at 600s — pivoted per spec to a seed-provided `/page/bench-test` variant (here `/bench-gallery-test`) with `oe_structure oe_empty` body so the dropzone is obvious. BU solved it in 14 steps by using the click-to-insert flow (no drag required): the Carousel preview is an accessible tile inside the "Insert a block" dialog. Interesting calibration note: despite the backlog labelling this as "hard" and a "BU weakness", BU 1.0 passed first try at 91s wall clock because it opted for the click-based dialog path rather than the drag path. Oracle takes the documented JSON-RPC shortcut (`ir.ui.view.write({'arch': ...})`) since scripting the iframe drag from Playwright is notoriously fragile and the oracle is allowed to bypass per ODOO19_PATTERNS.md. Two quirks recorded in COOKBOOK_NOTES.md: (1) `oe_structure oe_empty` on the wrap div is the canonical marker that tells the builder "this page accepts block drops" — without it the dropzone arrows don't render; (2) The snippet in `website/views/snippets/snippets.xml` is declared as `<t t-snippet="website.s_image_gallery" string="Image Gallery" label="Carousel">`, so the sidebar heading says "Image Gallery" but the tile aria-label says "Carousel" — both strings need to appear in prompt.md for agent search robustness. |

---

## crm_sms.send_sms_to_opportunity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.4s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 78.6s) |
| **F1** | 1.0 |
| **Odoo modules** | CRM (crm), SMS (sms), CRM-SMS bridge (crm_sms) |
| **Workflow** | Seed installs `sms` + `crm_sms` (neither in base snapshot), creates partner `Bench Hot Prospect` with `country_id=base.us` and `phone='+16175551234'`, creates opportunity `Bench Hot Lead` linked to that partner. Agent opens `/odoo/crm`, clicks the `Bench Hot Lead` kanban card, opens the cog **Actions** menu, clicks **Send SMS**, types `Following up on your inquiry. - Bench team` into the Message textarea, clicks **Send** in the dialog footer. |
| **Capability tested** | Cog Actions menu discovery (the Send SMS binding is `binding_view_types='form'` on `crm.lead` → only visible via `.o_cp_action_menus` cog, NOT a header button); multi-field wizard on `sms.composer` in `composition_mode='comment'` with `comment_single_recipient=True`; `sms_widget` textarea fill; dialog footer Send button gated by `recipient_single_valid` (requires a validly sanitizable E.164 number). |
| **Notes** | Medium by calibration and outcome: BU solved it in 79s on first attempt (acceptable for MEDIUM coverage). New COOKBOOK entries: (1) seed must `button_immediate_install` both `sms` and `crm_sms` since neither is in `benchmark/base_modules.txt`. (2) Seed's phone MUST be a valid sanitizable E.164 (I used `+16175551234` instead of the task-spec's too-short `+15551234`) — otherwise `_phone_format` returns False, `recipient_single_valid=False`, and the wizard's Send button stays `disabled`. Partner needs `country_id=base.us` for the sanitizer to resolve. (3) `sms.sms` is persisted BEFORE `.send()` runs — so even though IAP fails with no credits and flips `state='error'`, the record still has `body`/`number`/`mail_message_id` filled correctly. check.py verifies persistence + linkage to mail.message; state_spec puts `state` in `ignore_fields` to suppress the environment-dependent outgoing→error transition. (4) `sms_widget` on `body` renders as a plain `<textarea>` inside `.o_field_widget[name='body']`; no rich editor, no iframe. (5) In trace_spec, include `sms.composer.action_send_sms` in optional_ops, not required, because browser-use posts via `web_save` + form button rather than calling the method directly. |

---

## website_event.publish_event_register_via_portal

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 23.1s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 85.1s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Events (event + website_event installed on demand) |
| **Workflow** | Seed installs website_event (not in base snapshot) and creates one unpublished event `Bench Public Day`. Phase 1: agent opens `/odoo/events`, opens the event, flips it to Published. Phase 2: navigates to `/event`, clicks the event card, clicks Register on the event page (opens `#modal_ticket_registration` Bootstrap modal), leaves the default single-ticket counter at 1, clicks the inner Register submit (JSON-RPC POST to `/event/<slug>/registration/new` inserts a second modal `#modal_attendees_registration` into body), fills Name=`Priya Patel` / Email=`priya.patel@example.com` / Phone=`+1 555 0142`, clicks Confirm Registration (POST to `/registration/confirm` → redirects to success page). |
| **Capability tested** | Closed-loop cross-module back-office → public portal round-trip + dual-modal chained portal registration form. Attendee inputs are named `{registration_index}-{question_type}-{question_id}` — must be matched by `name*='-name-'` substring, not `name$='-name'` suffix (the suffix is the numeric question id). |
| **Notes** | Calibration FAILED (intended hard tier, BU solved first-shot F1=1.0 in 85s). BU handled the dual-modal chain without trouble and the default ticket counter of 1 removed the `+` click hurdle. Kept at tier 3 (primary_track=false) to preserve the closed-loop back-office → portal pattern. New cookbook entries in COOKBOOK_NOTES.md: (1) `event.event.is_published` widget is `website_redirect_button` (navigation-only, NOT a toggle); "Publish" inline button is hidden by default since `website_visibility='public'` is the default. Canonical publish path: JSON-RPC `website_publish_button()` or the Owl systray toggle on the website preview. No stage-bar publish like `event.track` has. (2) The attendees-details modal is dynamically inserted into `document.body` after a JSON-RPC POST to `/registration/new` — it is NOT part of the initial event page DOM. (3) `event.registration.create` is called via `sudo()` inside the `/registration/confirm` controller AND the route carries the event slug (`custom:/event/<slug>/registration/confirm`), so neither the ORM op nor a clean route match shows up in `trace_spec.required_ops`. Rely on state diff + `check.py` only. (4) Default event questions (Name/Email/Phone with `is_default=True`) auto-attach to a fresh `event.event` via `_compute_question_ids` fallback — no seed work needed for the portal form to render. |

---

## appointment.public_booking_reschedule_cancel_portal

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Appointments (enterprise-only), Website/Portal |
| **Workflow** | Seed `appointment.type` 'Bench Intro Call' with a 30-min slot + 1 seeded user resource. Phase 1 (back-office): agent verifies config. Phase 2 (public portal): navigate to `/appointment/<slug>`, pick a slot next week, submit form (name=Bench Visitor, email=visitor@bench.test). Phase 3: open returned confirmation URL, click Reschedule to next-week+1, then Cancel. |
| **Capability tested** | Multi-phase public-portal workflow with reschedule + cancel (two separate portal actions post-booking). Tests backend-to-portal handoff + two distinct portal actions on a single booking record. |
| **Notes** | Blocked — `ir.module.module` reports `state='uninstallable'` for `appointment` on the current `odoo_benchmark` branch (Odoo Community Edition checkout does not ship the `appointment` addon source; no manifest found under `addons/`). Seed would need `button_immediate_install`, but that raises UserError on an uninstallable record. Calendar's `/calendar/meeting/view` portal only exposes Accept/Decline, not Reschedule/Cancel, so the workflow cannot be cleanly re-scoped onto `calendar.event`. Task skeleton (seed/check/oracle) is committed with clear BLOCKED guards that short-circuit with a diagnostic error instead of silently passing. Re-enable once enterprise `appointment` (+ `website_appointment` + `appointment_account_payment`) addons are vendored into the repo. Matches the precedent set by the earlier sibling task `appointment.portal_reschedule_and_cancel_booking` (also removed for the same reason). |

---

## helpdesk.team_sla_assign_escalate_close

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Helpdesk (Enterprise-only) |
| **Workflow** | Seed `helpdesk.team` 'Bench Support', create `helpdesk.sla` policy 'Bench 1hr Response' targeting High priority with time=1h on stage='In Progress'. Create a High-priority ticket 'Critical bug', assign to team user, move to In Progress (SLA timer starts), then move to Solved stage and mark Closed. |
| **Capability tested** | Multi-step configuration (team + SLA policy) + record lifecycle across stages with SLA status tracking. |
| **Notes** | Removed because the `helpdesk` addon is not present in this checkout (Odoo 19 Community — `helpdesk` is an Enterprise-only module). Verified: no `helpdesk`, `helpdesk_*`, `ticket`, or `support` directories under `addons/`; `benchmark/base_modules.txt` contains no `helpdesk` reference; follows same precedent as `helpdesk.create_ticket_tag_schedule_activity_resolve` (also Removed for module unavailability). Task cannot be implemented or validated on branch `odoo_benchmark` in the current environment. |

---

## marketing_automation.tag_trigger_drip_campaign

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Marketing Automation (Enterprise-only) |
| **Workflow** | Seed `res.partner.category` 'Bench Leads'. Create `marketing.automation` 'Welcome Drip' targeting model=`res.partner`, filter=category contains 'Bench Leads'. Add Activity 1: send `mailing.mailing` 'Welcome Day 1' (trigger=immediate, `trigger_type='begin'`). Add Activity 2: send 'Day 3 Follow-up' (trigger=3 days after Activity 1 opened, `trigger_type='mail_open'` + `interval_number=3` + `interval_type='days'`). |
| **Capability tested** | Multi-activity marketing automation builder with parent-child trigger chaining (begin → mail_open delay). |
| **Notes** | Removed because the `marketing_automation` addon is not present in this checkout (Odoo 19 Community — `marketing_automation` is an Enterprise-only module; see `skills/expand-benchmark-coverage.md` which explicitly lists it under Enterprise-only alongside `appointment` and `helpdesk`). Verified: no `marketing_automation` directory under `addons/` (only `marketing_card` exists); no module declares `_name = 'marketing.automation'` or `'marketing.activity'`; `benchmark/base_modules.txt` contains no `marketing_automation` reference. Follows the same precedent as `helpdesk.create_ticket_tag_schedule_activity_resolve`, `helpdesk.team_sla_assign_escalate_close`, and `appointment.portal_reschedule_and_cancel_booking` (all Removed for module unavailability). Task cannot be implemented or validated on branch `odoo_benchmark` in the current environment. |

---

## event_product.sell_event_product_fill_attendee_details

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 40.5s) |
| **Browser-Use** | FAIL (strict, gave_up=True at 360s wall-clock; StateDiffF1=1.0, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Events (event_product / event_sale auto-installed bridge) |
| **Workflow** | Seed creates customer `Bench Attendee Co`, a service product `Bench Summit Ticket` with `service_tracking='event'` / `list_price=100` / `invoice_policy='order'`, and event `Bench Summit` with one paid ticket `Standard Pass` linked to that product (price=100) plus the auto-default `Registration for Bench Summit` placeholder (backed by the built-in `EVENT_REG` product). Agent opens `/odoo/sales`, creates a new quotation for Bench Attendee Co, adds `Bench Summit Ticket` to Order Lines — the `event_configurator` wizard fires (because `product.event_ok=True`) — picks `Bench Summit` + `Standard Pass` and clicks Ok. Confirms the SO, which opens the `registration.editor` wizard pre-filled from the buyer's name/email; overwrites Name=`Alice Attendee` / Email=`alice@bench.test` and clicks Create/Update registrations. |
| **Capability tested** | Chain of two modal wizards triggered by SO actions (configurator on product pick, registration editor on confirm) + overriding pre-filled o2m row fields before submitting the second wizard. |
| **Notes** | Oracle deterministic PASS. Browser-use reached the correct final state (all 9 atomic edits match, postcondition check passes) but used the full 360s budget chaining the two wizards, so `gave_up=True` flipped strict to FAIL. Medium calibration matches the expected behaviour: the attendee tab must be filled, not just saved. New cookbook notes: (1) `product.event_ok` triggers the `event_configurator` wizard on SO line product pick (no explicit UI action needed). (2) `registration.editor` is a one2many wizard pre-filled from partner email/name — clicking the primary footer button without editing the row saves with buyer defaults, which is the intended calibration trap. (3) Seed-scoping: only `event.registration` + `sale.order` in state_spec avoids the base snapshot's Gift Card product.template duplicate-key nondeterminism and keeps the diff narrowly on what the agent mutates. (4) Pre-seeding both `Standard Pass` and `Registration for Bench Summit` tickets on `event.event.event_ticket_ids` via `(0, 0, …)` stops the auto-default ticket from polluting the diff. |

---

## sale_loyalty.buy_x_get_y_reward_in_cart

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 47.2s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 139.8s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Loyalty (sale_loyalty + website_sale_loyalty) |
| **Workflow** | Back-office `/odoo/discount-loyalty`, create program `Buy 2 Widgets Get 1 Gadget` with `program_type='promotion'`, `trigger='auto'`. Open the default rule and set Minimum Quantity=2 + Among-products=`Bench Widget`. Open the default reward and switch Reward type selection from the default "discount" to "Free Product" (the "Among" group then appears), pick `Bench Gadget`, set Quantity rewarded=1, Description="Free Bench Gadget". Save. Portal phase: navigate `/shop/cart` — the seeded cart has 2 Bench Widgets; `website_sale_loyalty.Cart.cart` auto-fires `_update_programs_and_rewards()` + `_auto_apply_rewards()`, attaching a free Bench Gadget reward line (discount=100%, price_subtotal=0). |
| **Capability tested** | Buy-X-Get-Y promotion configuration using cascading loyalty-rule + loyalty-reward dialogs (reward-type dropdown flips the visible field group), plus implicit auto-apply side effect on /shop/cart via website_sale_loyalty controller. |
| **Notes** | Calibration FAILED: BU solved it first-shot F1=1.0 in 139.8s (16 steps) — it handled both cascading dropdowns (rule editor + reward editor with reward_type switch) without getting stuck. Kept at tier 3 anyway since the reward-type switch is a genuine cascade test that fails intermittently on other runs. New cookbook entries added to ODOO19_PATTERNS.md: (1) Free-product reward lines have `price_unit=list_price` and `discount=100`, NOT `price_unit=0` — check.py must assert `price_subtotal`/`discount==100`. (2) `website_sale_loyalty.Cart.cart` auto-invokes `_update_programs_and_rewards` + `_auto_apply_rewards` on every /shop/cart GET — a single-reward `trigger='auto'` promotion with a satisfied rule attaches the reward line just by visiting /shop/cart. (3) JSON-RPC `reward_product_id` must be a `product.product` (variant) id, not `product.template` — resolve via `product.template.product_variant_id`. |

---

## website_blog.create_post_with_cta_seo_schedule

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website Blog |
| **Workflow** | In the Blog kanban pick `Bench News`. Create a new post titled `Bench Releases Q2 Features`. In the body, insert a CTA button block with label `Learn More` whose href is `/shop`. Open the **Optimize SEO** dialog (cog Actions > Optimize SEO) and set Meta Title = `Q2 Releases - Bench` and Meta Description = `Read about our Q2 release highlights and what it means for customers.`. Set the Publishing date to `05/20/2026 09:00:00` (future). Save; leave the post unpublished (scheduled). |
| **Capability tested** | Three unrelated surfaces stacked into one medium task: drag/insert a CTA button snippet in the HTML editor, fill the Optimize SEO modal, and set a future Publishing date without toggling Publish. |
| **Notes** | BU calibration: StateDiff matches 6/6 create-edits (name, blog_id, both SEO fields, and is_published/website_published=null for the scheduled state), but the `check.py` regex catches that BU never manages to insert the `<a href='/shop'>Learn More</a>` anchor in the body — BU's content stays empty (`<p></p>`) after 360 s of wall clock. Postcondition fail → strict FAIL, F1=0.0 via postcondition override. Cookbook: `blog.post.content` (not `arch_db`); `is_published`/`website_published` diff as `null` (not `false`) on create-and-schedule flows; Optimize SEO dialog is available on the blog.post backend form (unlike website_sale products where it's frontend-only). |

---

## sale_purchase.mto_so_generate_po_change_vendor_confirm

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Purchase, Stock (MTO + Buy via sale_purchase_stock bridge) |
| **Workflow** | Seed creates a confirmed SO for a storable product wired with MTO + Buy routes and two vendors (Acme 50.00 / Brook 40.00). Confirming the SO auto-generates a draft RFQ for Acme (first vendor by sequence). Agent opens the SO, clicks the Purchase smart button, changes `partner_id` to Brook Trading Ltd so `_compute_price_unit_and_date_planned_and_name` recomputes the line to 40.00, saves, and clicks Confirm Order. |
| **Capability tested** | Closed-loop cross-module navigation (Sales → Purchase via smart button) + edit-the-generated-RFQ vs create-a-new-PO + vendor-driven price recompute. |
| **Notes** | Calibrated under target — both oracle (24s) and browser-use (169s) pass F1=1.0. Could be escalated by hiding the smart-button hint or seeding distractor RFQs. Seed had to flip MTO.active, buy_route.product_selectable, warehouse.buy_to_resupply + re-run `_create_or_update_route()`, and force `procure_method='make_to_order'` on MTO rules — otherwise `action_confirm` silently produces no RFQ. MTO+Buy (non-dropship) PO lines do NOT carry `sale_line_id`; the SO↔PO link runs through `stock.reference.purchase_ids` (sale_purchase_stock override). check.py uses `purchase.order.origin == SO.name`. Vendor-swap on a partner_id match_key surfaces in the diff as `delete(old_partner) + create(new_partner)`, NOT as a single `set` edit. |

---

## event_sale.multi_ticket_checkout_two_attendees

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 30.3s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 69.5s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Events + Sales + Website (event, sale, event_sale, website_event, website_event_sale, payment_custom) |
| **Workflow** | Seed installs `website_event`, `website_event_sale` and `payment_custom` (none in base snapshot), enables the `payment.payment_provider_transfer` (Wire Transfer) provider while disabling every other provider, sets ICP `sale.async_emails=True`, populates a full US billing address on admin's partner (so `/shop/checkout?try_skip_step=true` forwards straight to `/shop/payment`), and creates published event `Bench Expo 2026` with two paid tickets: Standard €50 and VIP €150. Agent flow: `/event` → event card → event detail → Register button opens `#modal_ticket_registration` with two counter rows → bump both Standard and VIP counters to 1 → click Register (`.a-submit`) → JSON-RPC POST to `/event/<slug>/registration/new` inserts `#modal_attendees_registration` with TWO attendee sections (`<h5>Ticket #1 - Standard</h5>` + `<h5>Ticket #2 - VIP</h5>`) → fill Alice/Standard + Bob/VIP → click **Go to Payment** (label is paid-event-specific: `website_event_sale` inherits `registration_attendee_details` and swaps from `Confirm Registration` to `Go to Payment`) → redirects via `/shop/checkout?try_skip_step=true` → lands on `/shop/payment` → pick **Wire Transfer** radio (the only enabled provider) → click **Pay now** → `/payment/status/poll` triggers `_post_process` which flips tx to `pending` and SO to `state='sent'` via `action_quotation_sent()`. |
| **Capability tested** | Multi-ticket portal registration (2 ticket rows in modal, 2 attendee rows below), non-default Wire Transfer payment option (not the default radio), closed-loop back-office seeding → public portal purchase → payment submission round-trip. |
| **Notes** | Calibration FAILED (intended hard tier, BU solved first-shot F1=1.0 in 69.5s). Pattern similar to row 342: BU is surprisingly good at the dual-modal + multi-attendee portal flow when labels are plain. Kept at tier 3 (primary_track=true) as a representative hard event_sale round-trip. Key findings: (1) **Paid-event attendee modal label swap**: `website_event_sale` replaces `Confirm Registration` with `Go to Payment` — oracle / check must account for either. (2) **Wire Transfer ends SO in `state='sent'`, not `'sale'`** — `_apply_updates` sets tx to `pending` and `action_quotation_sent()` (NOT `action_confirm`) runs. Registrations stay in `state='draft'` (sale_status=`to_pay`). check.py accepts `sent`/`sale`/`done` so post-confirm runs don't regress. (3) **`sale.async_emails=True` is MANDATORY** for Wire Transfer to work in an ephemeral test DB: without it, the synchronous `_send_payment_succeeded_for_order_mail` inside `_post_process` raises (no SMTP), the cursor is rolled back in `/payment/status/poll`, `is_post_processed` stays False, and the SO is stuck in `draft`. (4) **Admin address must be fully populated** (name/email/phone/street/city/state_id/zip/country_id for US) in seed — missing any field redirects the agent to `/shop/address` before payment. (5) **Payment providers default to `state='disabled'`**; seed must explicitly `write({'state': 'enabled'})` on the target provider AND disable every other provider to keep the radio deterministic. (6) **Multi-ticket modal counter input name** is `nb_register-<ticket_id>` and attendee section heading is `Ticket #N - <ticket_name>` (space-dash-space). (7) The Sale-on-pending path is documented in new ODOO19_PATTERNS.md section "event_sale / website_event_sale — multi-ticket portal checkout". |

---

## purchase_stock.receive_partial_scrap_damaged_units

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Purchase, Inventory (stock) |
| **Workflow** | Open confirmed PO P-BENCH-DMG-001 (Bench Parts Vendor, Bench Parts qty=20). Click Receipt smart button. On the generated ready receipt, lower Done from 20 to 15 inline. Open cog Actions > Scrap, fill product=Bench Parts, scrap_qty=5 (not default 1), scrap_location_id=WH/Lost (not default Virtual Locations/Scrap), click Scrap Products. Back on picking click Validate, then Create Backorder in the dialog. |
| **Capability tested** | Three-trap stack: inline Done-cell edit on an auto-reserved partial receipt + stock.scrap wizard with two non-default fields (qty and scrap_location) + backorder confirmation dialog. |
| **Notes** | Solid hard calibration — BU hit the scrap_qty trap exactly as predicted (set scrap_qty=0.01 instead of 5; state diff 8/9 matched but postcondition gated F1 to 0.0). New cookbook quirks documented: `stock.picking.origin` on PO receipts inherits `purchase.order.name` (not `origin`); validate-with-backorder rewrites the original move's `product_uom_qty` down from full demand to Done qty; scrap-from-picking creates a `stock.move` with `scrap_id` set so check.py must filter `not m.scrap_id`; `scrap_location_id` + `location_id` require `stock.group_stock_multi_locations` on admin; custom WH/Lost inventory location must be seeded (`usage='inventory'` + parent=warehouse.view_location_id). |

---

## hr_expense.split_submitted_report_resubmit

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 44.0s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 143.4s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Expenses |
| **Workflow** | Seed 3 submitted `hr.expense` records for employee `Lee Bench` sharing the trip identifier R-BENCH-SPLIT-001: Meal (40, Bench Meals), Gadget (500, Bench Office Supplies, non-compliant), Taxi (25, Bench Travel). Admin is granted the three expense-approver groups (team_approver + manager + user) so the approve/refuse buttons are visible. Agent opens the approver list (`/odoo/action-hr_expense.hr_expense_actions_my_all` or the Expenses app), clicks the Gadget expense, hits **Refuse** in the statusbar, fills the wizard reason `Not compliant`, confirms. Back to the list, opens Meal, clicks **Approve**. Opens Taxi, clicks **Approve**. End state: Meal + Taxi in `approved`, Gadget in `refused`, `Not compliant` snippet recorded in Gadget chatter. |
| **Capability tested** | Per-line triage of a multi-expense submitted batch — agent must refuse one specific line (with a filled wizard reason) AND approve the other two, NOT blanket-approve or blanket-refuse. Tests loop-over-batch, correct line selection, refuse-reason modal handling, and re-opening siblings for separate approval. |
| **Notes** | Original spec assumed legacy `hr.expense.sheet` per-line refuse + automatic split sheet for the refused line. That model is **removed in Odoo 19** — the approval workflow lives directly on `hr.expense` with `approval_state ∈ {submitted, approved, refused}`. Pivoted to "per-expense triage of 3 submitted records sharing a trip id". BU calibration **FAILED** (task easier than intended): browser-use solved it single-shot in 143.4s with F1=1.0 and zero postcondition failures — the 3-record loop + refuse-reason modal did not trip it. Kept at hard tier anyway since per-line triage of batches remains a relevant pattern. New cookbook entries: (1) `hr.expense` per-line refuse opens `hr.expense.refuse.wizard` (required `reason` Char); `_do_refuse` posts the `hr_expense.hr_expense_template_refuse_reason` mail template. (2) Admin needs team_approver + manager + user groups together to see approve/refuse on another employee's expense. (3) Manager list action xmlid: `hr_expense.hr_expense_actions_my_all`. |

---

## im_livechat.configure_channel_then_handle_widget_chat

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 69.5s, 9 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Live Chat, Discuss, Mail |
| **Workflow** | Seed pre-creates the `im_livechat.channel` 'Bench Support' (admin as operator) with a URL rule, a `mail.canned.response` shortcut `hello` -> `Hi, thanks for reaching out!`, and a `discuss.channel` (channel_type='livechat') named 'Visitor #BENCH-359' with admin + anonymous visitor as members plus one waiting `mail.message` from the visitor body 'Hi there'. Agent opens `/odoo/discuss`, clicks the livechat session in the 'Bench Support' sidebar category, types `::hello` in the composer, picks the `hello` option from the suggestion popover (which substitutes the shortcut with the full text), and sends with Enter/Send. |
| **Capability tested** | Triggering the Odoo 19 Discuss canned-response suggestion popover via the `::` delimiter and selecting the substitution (not sending the literal shortcut text); plus sidebar navigation into a livechat session inside the auto-collapsing `im_livechat.channel` sidebar category. Multi-tab widget flow calibrated down to single-tab per backlog guidance (Playwright multi-tab is fragile). |
| **Notes** | Canned responses in Odoo 19 are triggered by **double-colon `::`**, NOT single-colon (single colon triggers the emoji picker); backlog spec said `:hello` and was corrected to `::hello`. Cookbook quirk discovered & documented in ODOO19_PATTERNS.md: `mail.canned.response` visibility in the `/mail/data` webclient endpoint is gated by `create_uid = env.user.id OR group_ids in user.all_group_ids.ids`. Odoo shell runs as `__system__` (id=1), NOT admin (id=2), so a naive `env["mail.canned.response"].create({...})` yields a record admin cannot see. Seed MUST `with_user(admin).create({..., "group_ids": [(6, 0, [base.group_user.id])]})`. Browser-use solved the task on the first try (9 steps, 69.5s) — calibration slots this as "easier" than hard tier. |

---

## project_todo.bulk_move_tasks_between_projects

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Seed creates two projects `Bench Proj A` (4 tasks: Alpha/Bravo/Charlie/Delta) and `Bench Proj B` (empty). Agent opens each of Alpha/Bravo/Charlie in the task form, changes the `Project` many2one from Proj A to Proj B, and Saves — three times. Delta must remain in Proj A as a distractor. Final: Proj A has 1 task (Delta), Proj B has 3 (Alpha/Bravo/Charlie). |
| **Capability tested** | Repeated form-edit of a many2one field across 3 similar records without touching the 4th distractor. Originally scoped as "multi-select + bulk 'Move to Project' action" but **no such action exists in Odoo 19 Community** — `project.task` has no move-to-project wizard, and the `project_id` column in `project_task_view_tree_main_base` is declared `readonly="1"`, so list inline edit is blocked too. Canonical path is per-task form edit. |
| **Notes** | Calibration pivot: bulk wizard / list inline-edit pattern was unavailable; fell back to per-task form edit of project_id × 3. Oracle uses JSON-RPC `web_save` for determinism. Browser-use moved only **Alpha** (1/3) then hallucinated an access-rights error and gave up despite the admin user clearly having write permission — classic BU misfire on repeated form-hop workflows where the `o-autocomplete--input` combobox loses its dropdown-detectable shape after the first save. Genuine hard-tier FAIL: state_diff F1=0.0 (engine binarises on Recall<1 for small expected sets), 4 postcondition failures. BU wall-clock 161 s before abort, well inside the 480 s budget. |

---

## website_hr_recruitment.edit_job_form_publish_preview

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 45.3s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 111.1s single-shot, 14 steps) |
| **F1** | 1.0 |
| **Odoo modules** | website_hr_recruitment (depends on hr, hr_recruitment, website) |
| **Workflow** | Seed creates unpublished `hr.job` "Bench QA Engineer" in Administration dept with empty backend `description` and a pre-populated `website_description` containing a "Requirements" section (Python, Playwright, 2+ yrs) that the agent must leave alone. Agent flow: `/odoo/recruitment` → click **Configure** on the Bench QA Engineer kanban card → full job form → **Summary** notebook tab → type exact phrase "Write automated tests for Bench Products." into the HTML editor → switch back to Details tab → click the `website_published` **Published** `boolean_toggle` (its onchange mirrors to `is_published`) → **Save** → click the **Go to Website** / **Job Page** smart button (widget `website_redirect_button` on `is_published`) which navigates to `/jobs/<slug>` on the public website where the seeded Requirements section renders. |
| **Capability tested** | Backend-form HTML-editor edit + boolean_toggle publish + smart-button navigation to the public portal preview. Multi-notebook-tab navigation (Details ↔ Summary) with partial state persisted across tabs before Save. |
| **Notes** | Calibration OVERESTIMATED (BU solved first-shot F1=1.0 in 14 steps). The seeded `website_description` avoids the fragile website-editor iframe entirely, keeping this solidly at medium tier. Kept primary_track=true as a clean medium reference. Key findings: (1) **`website_description` is frontend-only** — it renders via `<div t-field="job.website_description"/>` on `/jobs/detail/<slug>` and is NOT exposed in the backend hr.job form; tasks that need its content asserted should pre-seed the HTML and tell the agent not to touch it. (2) **`website_published` boolean_toggle onchange flips `is_published`** in the same user action — expect BOTH fields in the state diff. (3) **Backend `description` Html field** is on the Summary notebook tab (`page name="job_description_page"`); both `description` and `website_description` must be in state_spec.yaml `ignore_fields` because the HTML diff is noisy — validate via `html2plaintext` in check.py. (4) **`is_published` in the button box uses widget `website_redirect_button`** — same semantics as `event.event` / `event.track` documented in ODOO19_PATTERNS.md: navigation only, NOT a publish toggle. (5) BU correctly identified the "Job Page" button label (name `open_website_url`) as the Go-to-Website action even though the prompt called it "Go to Website". |

---

## website_sale.apply_product_filter_clear_facets

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 92.3s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 89.0s / 14 steps single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Website Sale |
| **Workflow** | Seed two `product.public.category` records (`Gadgets`, `Widgets`) plus five published products (Bench Gadget Mini/Plus/Pro at 30/80/150; Bench Widget Tiny/Max at 20/120). From `/shop` the agent: clicks the **Gadgets** category in the sidebar (URL becomes `/shop/category/<slug-id>`), applies a **max-price=100** filter via the right-hand multirange counter input (URL gets `?max_price=100`), clicks **All Products** to drop the `/category/...` path segment while keeping the `max_price=100` query param, then opens the **Bench Widget Tiny** product page and clicks **Add to cart**. |
| **Capability tested** | Chained `/shop` filter manipulation that mixes a URL **path** filter (category) with a URL **query** filter (price). Non-trivial because the "remove category facet" action is actually an "All Products" link (no `x` chip exists), and the price slider is a dual-handle multirange that the agent has to interact with via the hidden counter `<input type='number'>` rather than drag. Final add-to-cart proves the agent saw the Widget Tiny product that only appears after category removal. |
| **Notes** | BU first-shot PASS (F1=1.0, 89.0s, 14 steps). It did bounce briefly on the price counter ("clicked $150 span → type 100 → Enter") but recovered. Task kept at tier 2 because the capability chain (category=path, price=query, clear-one-preserve-other, then final commit) is a legitimate medium test even if current BU model solves it. Postcondition NOTE: because `/shop` is `auth='public'`, cart ownership depends on whether BU bothers logging in — check.py MUST search carts by line content (product name), NOT by `partner_id=admin`, or a non-logged-in BU run will silently fail the assertion. New cookbook entries in ODOO19_PATTERNS.md: (a) category filter is a URL path, not a facet chip; (b) price slider has hidden `<input type='number'>` counters that can be toggled by clicking the `$<value>` span; (c) `/shop/cart/add` is `auth='public'` jsonrpc; (d) correct model name is `product.public.category`. |

---

## fleet.log_service_cost_add_odometer_close

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 41.2s, 8/8 edits) |
| **Browser-Use** | FAIL (F1=0.0, 3 postcondition failures, 270.7s single-shot) |
| **F1** | 0.0 |
| **Odoo modules** | Fleet |
| **Workflow** | Seed creates vehicle `BENCH-TRUCK-01` (Benchmark Auto / Benchmark Truck, admin as driver) + vendor `Bench Garage` + service type `Oil Change`, flips `env.company.currency_id` to EUR (activating the currency record if needed) so the Cost monetary widget renders with the prompted EUR symbol. Agent must open the vehicle, click the **Services** smart button, **New** → fill `Service Type=Oil Change`, `Date=04/15/2026`, `Cost=120.00`, `Vendor=Bench Garage`, `Odometer Value=25000` (entering 25000 with NO thousands separator), leave description/notes empty, **Save**, then click **Done** on the clickable-statusbar `state` field. Filling the `odometer` field on the service form auto-materialises one `fleet.vehicle.odometer` row via the inverse `_set_odometer`. |
| **Capability tested** | Three-trap stack: (1) odometer field location/skip — the field is in the RIGHT column of the service form, easy to miss; (2) decimal-separator parsing — typing `25,000` yields `value=0.0025` in Owl's numeric parser; (3) clickable-statusbar state transition — agents often stop after Save and forget to advance the stage. Plus an implicit quad-count check on `fleet.vehicle.log.services` and `fleet.vehicle.odometer` to catch the "create, then create again" spiral. |
| **Notes** | BU spiralled exactly as predicted: created 4 service records (3 without vendor) + 6 odometer rows (3 phantom at 0.0025 from the `25,000` → `0.0025` parse, plus 3 legit 25000.0 on successive retries). F1=0.0, 3 postcondition failures. New cookbook entries added to ODOO19_PATTERNS.md § Fleet: (a) `fleet.vehicle.log.services.odometer` is a computed Float with `_set_odometer` inverse that creates an `fleet.vehicle.odometer` row — no separate navigation needed; `create()` drops `odometer=0` so zero-value fills silently no-op. (b) `state` uses `widget="statusbar"` with `clickable=1` (values `new/running/done/cancelled`) — click target `.o_statusbar_status button.o_arrow_button:has-text('Done')`, no confirmation dialog. (c) `currency_id` is `related='company_id.currency_id'` (readonly); seed must flip `env.company.currency_id` to EUR and activate the currency (inactive by default in base snapshot). (d) **Comma-as-decimal trap**: typing `25,000` into a Float widget yields 0.0025 — BU retries 3+ times, spawning phantom odometer rows; tasks should use bare-numeric prompts and enforce row-count in check.py. |

---

## maintenance.create_equipment_schedule_preventive_plan

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 23.2s) |
| **Browser-Use** | FAIL (F1=0.0, 1 postcondition failure, 290.4s single-shot) |
| **F1** | 0.0 |
| **Odoo modules** | Maintenance |
| **Workflow** | Open Maintenance → Equipments, click New. Fill Name='Bench Press 01', create the Machinery category on-the-fly (it is intentionally not seeded), pick Technician 'Bench Tech' (user pre-seeded). Open the **Maintenance** tab and set **Expected Mean Time Between Failure** = `30` days (writable `expected_mtbf`, NOT the readonly computed `mtbf`). Save. Reopen the saved equipment, go to **Product Information** tab, set **Effective Date** = `06/01/2026`. Save. |
| **Capability tested** | (1) On-the-fly category creation via autocomplete "Create" shortcut. (2) Correct target-field disambiguation — `expected_mtbf` (writable) vs `mtbf` (readonly computed). (3) Two-phase save: reopening a saved record to edit one more field instead of creating a duplicate. |
| **Notes** | Single-shot BU result: FAIL. Agent created **two** `Bench Press 01` equipment records (and two `Machinery` categories). The first record was saved complete with `effective_date=2026-06-01`; on the reopen step the agent instead created a **new** equipment at /odoo/equipments/new, repeating the same name/technician/mtbf, leaving `effective_date` at default (today, 2026-04-19). `check.py` caught via "Expected exactly 1 equipment named 'Bench Press 01', found 2". State diff saw 10 edits vs 5 expected → precision=recall=0. Cookbook additions: (a) `maintenance.equipment` has no `next_action_date` field in Odoo 19 — writable date fields are `effective_date`, `warranty_date`, `assign_date`, `scrap_date`. The task pivoted from the row-373 original `next_action_date` to `effective_date` (semantically equivalent for preventive-plan start date / MTBF anchor). (b) Two-phase-save is a reliable medium-tier BU trap that doesn't require any wizard. (c) `maintenance.equipment.category._unlink_except_contains_maintenance_requests` guards category deletion — seed must delete equipment first, then guard-unlink. |

---

## calendar.configure_meeting_with_location_and_reminder

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 27.9s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 88.9s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Seed creates two internal users `Alice Attendee` (login `alice.attendee`) and `Bob Attendee` (login `bob.attendee`). Agent opens `/odoo/calendar`, clicks **New**, fills name `Quarterly Review`, start `06/10/2026 02:00:00 PM`, end `04:00 PM` (2h later), location `Conference Room B, Floor 3`, adds Alice + Bob via the attendees (`partner_ids`) many2many_tags autocomplete, switches to the **Options** notebook tab, picks the pre-existing `Notification - 1 Hours` calendar.alarm from the **Reminders** (`alarm_ids`) many2many_tags, and saves. |
| **Capability tested** | Multi-field calendar event create + notebook-tab switch + two distinct many2many_tags pickers (attendees and alarms) + location Char on header. Uses the canonical `float_time` duration trick in the oracle to avoid the flaky `.o_daterange_end` popover pattern documented in ODOO19_PATTERNS.md. |
| **Notes** | Calibration CORRECT (medium): BU single-shot PASS in 88.9s matches the expected medium-tier behavior — straightforward form fields + tab nav + existing-tag pickers. `alarm_ids` has `no_quick_create=True`, so agents must pick an existing calendar.alarm record from autocomplete; the pre-seeded `Notification - 1 Hours` (from `calendar/data/calendar_data.xml`) is the canonical "1 hour before" answer. check.py asserts `duration_minutes == 60` rather than a specific alarm name/xmlid so any equivalent alarm passes. trace_spec.yaml forbids `calendar.alarm.create`/`unlink` to pin to seeded data. Cookbook quirk: writing `duration` = `02:00` into the visible `float_time` input is the reliable way to set `stop` in an oracle — fill into `.o_daterange_end` -> `.o_time_picker_input[1]` is flaky whenever the default stop (start + 1h) has already auto-populated (silently drops the fill). The 1h-duration oracles in other calendar tasks don't hit this because they happen to match the default. |

---

## product_expiry.receive_lot_set_expiry_date

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 37.3s) |
| **Browser-Use** | PASS (F1=1.0, 181.3s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (stock), product_expiry |
| **Workflow** | Seed installs `product_expiry` on demand (not in base snapshot), creates a lot-tracked perishable product `Bench Perishable` with `use_expiration_date=True` + `expiration_time=30` (days), sets Receipts picking type `use_create_lots=True` + `use_existing_lots=True`, builds a confirmed-ready receipt `BENCH-PERISH-RCV-01` for qty=10 with `move_line.quantity` pre-filled. Agent opens the receipt, clicks **Details** on the move line, types `BP-LOT-001` in the lot_id cell and picks `Create "BP-LOT-001"` from autocomplete, clicks the internal-link arrow on the lot to open the stock.lot NESTED dialog, sets **Expiration** = today+60 and **Removal Date** = today+55, Save the lot dialog, Save the popup, Validate the receipt. |
| **Capability tested** | Multi-dialog navigation (picking form → Detailed Operations modal → stock.lot nested-dialog via m2o internal-link) combined with Odoo 19 DateTimeField widget interaction (button → input flip pattern) on two separate datetime fields while respecting the `_compute_dates` ordering (expiration_date first, then removal_date, otherwise the compute clobbers removal). |
| **Notes** | BU solved single-shot in 181s (F1=1.0, 0 postcondition failures) — task is medium-calibrated: non-trivial (3x oracle wall clock, multi-modal + datetime widget) but not a reliable failure trap. New cookbook entries in ODOO19_PATTERNS.md: (1) `DateTimeField` renders as `<button>` not `<input>` whenever the field has a value and isn't the active picker — oracle must click button first to flip it. (2) `product_expiry` install-on-demand recipe (depends only on `stock`). (3) Receipts picking type must have BOTH `use_create_lots` and `use_existing_lots` True to expose the `lot_id` m2o with Create autocomplete + internal-link. (4) m2o internal-link inside a dialog opens a NESTED modal via `openRecord('dialog')` when `env.inDialog=True`; walk visible modals and pick the one with the stock.lot fingerprint (`expiration_date` field) rather than `.last`. (5) `stock.lot._compute_dates` recomputes `use_date`/`removal_date`/`alert_date` on every `expiration_date` write — set expiration_date first, removal_date second. |

---

## mrp.bom_with_kit_component_confirm_mo

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.8s, 3/3 create edits) |
| **Browser-Use** | FAIL (F1=0.0, 1 postcondition failure, 90.5s single-shot) |
| **F1** | 0.0 |
| **Odoo modules** | mrp |
| **Workflow** | Seed creates five products: `Bench Sub-A`, `Bench Sub-B`, `Bench Frame` (atomic storable components), `Bench Kit` with a **phantom** (kit) `mrp.bom` listing `1x Sub-A + 2x Sub-B`, and `Bench Assembly` with a **normal** `mrp.bom` listing `1x Bench Kit + 1x Bench Frame`. Agent must create a draft MO with `name='M-BENCH-KIT-001'`, product=Bench Assembly, qty=1, bom_id=the Bench Assembly normal BoM, then click Confirm. On confirm `mrp.production._get_moves_raw_values` calls `bom.explode()` which auto-drills the phantom kit → `move_raw_ids` becomes 3 rows (Sub-A=1, Sub-B=2, Frame=1), NOT 2 rows (Kit=1, Frame=1). |
| **Capability tested** | Two combined traps: (1) **phantom/kit BoM auto-expansion** — the agent must trust that Confirm alone expands the kit, not manually edit the Components tab; prompt explicitly says to NOT touch the Components tab. (2) **MO Reference vs Source/origin UI ambiguity** — the Odoo 19 `mrp.production` form does NOT render an editable "Reference" input in the header; the auto-generated `name` (`WH/MO/00001`) is only editable by clicking the breadcrumb text in the top bar. The Miscellaneous tab has a `origin` (Source) Char that looks like a reference, so BU types the requested `M-BENCH-KIT-001` into Source instead. |
| **Notes** | BU single-shot FAIL exactly as predicted: BU typed `M-BENCH-KIT-001` into the **Source** field in the Miscellaneous tab, not into the MO name — actual DB name stayed at the auto-generated `WH/MO/00001`. Check.py catches this via `env["mrp.production"].search([("name", "=", "M-BENCH-KIT-001")])` returning empty. BU even hallucinated success in its final report ("Reference: M-BENCH-KIT-001") despite the divergent DB state. Phantom BoM expansion DID work correctly — 3 raw moves appeared on the confirmed MO — so the kit-expansion trap was not the source of failure; the calibrated trap was the Reference/Source UI confusion. Oracle uses JSON-RPC `create({'name': ..., ...}) + action_confirm` for determinism. New cookbook entries added to ODOO19_PATTERNS.md § mrp: (a) `mrp.production.name` has no editable Reference input on the draft form — only the breadcrumb text can override it; the Miscellaneous `origin` Char is a UI trap that looks like a reference. (b) `bom.explode()` recursively drills phantom child BoMs on MO confirm; `_get_moves_raw_values` skips lines whose `child_bom_id.type == 'phantom'`. (c) For a confirmed-but-not-produced MO, assert on `move.product_uom_qty` (demand) not `move.quantity` (actual, which is 0 until produce). (d) BoM Type dropdown label "Kit" = selection key `'phantom'` (not `'kit'`). |

---

## website_sale_slides.assign_attendees_publish_course

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (eLearning), Mail |
| **Workflow** | Seed creates two slide.channel rows — `Bench Onboarding` (draft, visibility=public) and `Bench 101` (published, visibility=members, enroll=invite) — plus two res.partner rows (Alice Attendee / Bob Attendee) and a fake SMTP sink. Agent flips `Bench Onboarding` visibility to Course Attendees on the Options tab (auto-coerces enroll → On Invitation via `_compute_enroll`), publishes via the frontend Owl systray toggle after clicking Go to Website, returns to the backend form and adds `Bench 101` in the Prerequisites many2many_tags field, then uses the Add Attendees header button to enroll Alice + Bob via the Enroll Attendees email wizard. |
| **Capability tested** | Domain-dependent m2m autocomplete (prereq dropdown only lists `Bench 101` once BOTH visibility='members' AND is_published=True are applied on the form), backend-form-vs-frontend publish split (`widget="website_redirect_button"` is navigation-only; the real toggle is the Owl `publish_website_systray_item`), and an email-forced invite wizard (`send_email` is hidden by `invisible="enroll_mode or channel_visibility != 'public'"` so SMTP must be wired). Oracle uses JSON-RPC `slide.channel.partner.create` because `_action_add_members` is private (underscore-prefixed) and not callable via `call_kw`. |
| **Notes** | Browser-use completed visibility + publish + attendee wizard correctly but typed `Bench 101` into the prereq autocomplete without clicking the dropdown option — so `prerequisite_channel_ids` stayed empty. 10/10 atomic edits matched on state diff (visibility/enroll/is_published/website_published + 2 attendee creates × 3 fields), but check.py's "exactly ['Bench 101']" postcondition fires → F1 forced to 0. Calibration lands as designed: the domain-filtered m2m_tags field with a seeded candidate that ONLY appears after two distinct form-state changes is the explicit trap. |

---

## mrp_subcontracting.receive_subcontracted_product_with_components

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 32.4s, 9/9 edits) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 116.3s / 17 steps single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Manufacturing, MRP Subcontracting, Purchase |
| **Workflow** | Seed installs `mrp_subcontracting` + `mrp_subcontracting_purchase`, disables **Resupply Subcontractors** on every warehouse (default True would otherwise auto-create a secondary WH/RES/… picking on PO confirm), creates subcontractor `Bench Subcontractor Inc` (`supplier_rank=1`), three products — serial-tracked `Bench Sub Assembly` (finished, `tracking='serial'`) + untracked `Bench Sub Part-A` / `Bench Sub Part-B` — a subcontract-type BoM with the subcontractor on `subcontractor_ids` (1 of each component per finished unit), `+2` `stock.quant` for each component at the subcontractor's subcontracting location, and a confirmed `purchase.order` `P-BENCH-SUB-001` for qty=2 of the finished product. Confirming the PO auto-generates the incoming Receipt (state=assigned) AND an auto-created subcontract `mrp.production` (state=confirmed) linked via `move_orig_ids`. Agent must open the receipt, click the move-row **Details** button (opens the subcontracting move form dialog), ensure 2 move_line rows, enter `BSA-2026-01` / `BSA-2026-02` (qty 1 each) via the autocomplete Create option, save the popup, then Validate the receipt. On validate, `_sync_subcontracting_productions._split_productions` splits the single MO into two lot-specific MOs (one per serial), both become done, and raw components are back-flushed from the subcontracting location (−2 Part-A, −2 Part-B). |
| **Capability tested** | Four-trap stack: (1) serial entry via the Detailed Operations popup on a subcontract move — agent must open the popup rather than inline-edit; (2) autocomplete `Create "<serial>"` option for on-the-fly `stock.lot` creation; (3) exactly 2 distinct move_line rows with qty=1 each (vs single-row qty=2 shortcut); (4) full subcontracting auto-chain: receipt → subcontract MO → raw-move backflush, verified not just on `stock.picking.state='done'` but on subcontract `mrp.production.state='done'` (all MO splits) AND the subcontracting-location `stock.quant` decrease. |
| **Notes** | Single-shot BU result: **PASS**. BU fumbled a few retries inside the Detailed Operations popup (typed serial without clicking Create, briefly assigned BSA-2026-01 to the wrong row) but ultimately recovered and validated in 17 agent steps / 116s. Task is capability-legitimate but solvable — keeping at tier 3 because the seed/oracle/check chain is genuinely complex and the MO-splitting state-diff pattern is non-obvious. New cookbook section `ODOO19_PATTERNS.md § mrp_subcontracting`: (a) `mrp_subcontracting` + `mrp_subcontracting_purchase` are NOT in the base snapshot; seed must `button_immediate_install`. (b) Confirming a subcontracting PO auto-generates TWO pickings sharing `origin` — the Receipt AND a `Resupply Subcontractor` internal picking (`subcontracting_to_resupply=True` by default on every warehouse); when the task pre-stocks components at the subcontracting location directly, seed MUST `warehouses.write({"subcontracting_to_resupply": False})` to suppress the phantom resupply picking (otherwise oracle `click_list_row(PO_NAME)` opens the wrong picking). (c) With `tracking='serial'` on the finished product + qty>1, validating the receipt causes `_sync_subcontracting_productions._split_productions` to split the single subcontract MO into one MO per lot — `expected_state.json` must encode the extras with `#dup1`/`#dup2` entity-key suffixes + `op=create`. (d) Incoming picking type needs `use_create_lots=True` AND `use_existing_lots=True` for the Detailed Operations popup `lot_id` autocomplete to expose a `Create "<serial>"` option. |

---

## hr_recruitment_survey.attach_survey_require_applicant_submit

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 25.3s, 1/1 edits) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 179.7s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment, Survey, Recruitment/Survey bridge |
| **Workflow** | Seed installs `hr_recruitment_survey` on demand (not in base snapshot), creates survey `Bench Screening` with `survey_type='recruitment'` + 1 page + 2 questions (text_box + numerical_box), creates job `Bench Recruit Lead` with NO survey attached, and applicant `Alice Candidate` in `Initial Qualification`. Agent must flip `/odoo/recruitment` kanban → list view, click `Bench Recruit Lead` row → job form, open the Recruitment notebook tab (XML string "Details", page name `recruitment_page`), pick `Bench Screening` from the **Interview Form** m2o autocomplete, and save. Optional verification step: open Alice Candidate's applicant form and confirm the `Send Interview` header button (`invisible="not active or not survey_id"`) is now rendered because `hr.applicant.survey_id` is `related='job_id.survey_id'`. |
| **Capability tested** | Non-default recruitment-app navigation (kanban card click on a job opens Applications, not the job form — agent must use viewswitcher or the 3-dots Configuration menu), domain-filtered m2o autocomplete (`survey_type='recruitment'` required), and a bridge field that surfaces in a notebook tab added by an inheriting module. The `hr.job.survey_id` edit is the only persisted state change; the Send Interview button visibility is a visual signal, not a separate write. |
| **Notes** | Single-shot BU result: **PASS** (F1=1.0). BU took the viewswitcher → list → row → notebook tab → m2o autocomplete → save path cleanly in steps 6–9 of 37; the remaining 28 steps were spent flailing for the Applications smart button / Alice's applicant form (decorative div clicks, loop-detection nudges) but the DB write was already persisted. Task design produces a clean 1-edit diff and self-verifies via the visible Send Interview button; considered tier 2 / medium calibration-legitimate. New cookbook section `ODOO19_PATTERNS.md § hr_recruitment_survey`: (a) `hr_recruitment_survey` is NOT in the base snapshot — seed must `button_immediate_install()`. (b) Interview Form m2o on hr.job has `domain=[('survey_type','=','recruitment')]`; surveys with default `survey_type='custom'` are filtered out silently. (c) hr.applicant.survey_id is `related` from job — no applicant-level write needed to surface the Send Interview button. (d) hr.job kanban exposes a hidden `action_new_survey` ("Interview Form") menu item that auto-creates a blank survey when `!record.survey_id.raw_value` — forbid in trace_spec to prevent a cheap pass. (e) `/odoo/recruitment` kanban card click opens `action_hr_job_applications`, NOT the job form; viewswitcher → list is the natural path. |

---

## pos_restaurant.open_table_order_mark_ready

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale, pos_restaurant (installed on demand — not in base snapshot) |
| **Workflow** | Open Point of Sale, open the seeded `Bench Restaurant` register, click table `T1` on the `Main Floor` floor plan, add `Starter Salad` (€15) x1, click the `Course` action-pad button to wrap Starter Salad into Course 1 + create an empty Course 2, add `Main Steak` (€20) x1 (lands in Course 2), click the primary Send/Order button on the action pad to fire Course 1 to the kitchen (`restaurant.order.course.fired=True`). No payment step. |
| **Capability tested** | Restaurant POS kiosk UI: floor-plan table click, course split (Course button), action-pad Send vs Pay distinction, kitchen-fire ("mark ready") state via `fired=True` flag on `restaurant.order.course`. Cross-module install: `pos_restaurant` is not in the base snapshot and must be installed on demand by the seed. |
| **Notes** | `pos_restaurant` is NOT in `benchmark/base_modules.txt`, so seed runs `button_immediate_install()` on demand. `pos.config.module_pos_restaurant=True` auto-spawns a default floor + T1 table via `_setup_default_floor` — seed detaches and replaces those with a deterministic `Main Floor` / T1 (table_number=1) pair to stabilise the floor-plan display name `Main Floor, 1` used as the state-diff `match_key`. The Odoo 19 "kitchen ready / mark ready" concept is implemented as `restaurant.order.course.fired` (Boolean, with matching `fired_date`). In the UI, clicking the primary action-pad button labelled with the category-count summary (class `.submit-order`, also referred to as the Send/Order button) fires the first non-fired course (`sendOrderInPreparationUpdateLastChange` in `pos_restaurant/pos_store.js` sets `firstCourse.fired=true`). Calibration: browser-use SOLVES this task in a single shot (wall clock 102.7s, 13 steps). BU successfully navigates the floor plan → order → Course split → Send flow. First state-diff match-key used (`pos_reference`) diverged between oracle (explicit string) and BU (auto-generated `<config>-<session>-<seq>`), so match-key switched to `table_id` for stable cross-run F1. POS kiosk is a clearly labeled Owl surface; harder failure modes would require non-default course choices, guests count, or a split-bill / transfer workflow. |

---

## website_customer.publish_customer_reference_on_public_page

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 23.8s) |
| **Browser-Use** | PASS (F1=1.0, 61.4s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Website (Customer References), Contacts |
| **Workflow** | Seed installs `website_customer` on demand (not in base snapshot; pulls `website_crm_partner_assign` + `website_partner`), creates `Bench Delivery Partner` (implementer company) and `Bench Happy Client` (company) with `country_id=US`, `website` URL, `assigned_partner_id=Bench Delivery Partner`, `website_published=False`. Agent opens /odoo/contacts, finds Bench Happy Client, clicks the **Go to Website** stat button (`website_redirect_button` — navigation-only) to land on `/partners/<slug>`, flips the Owl systray **Unpublished → Published** switch (`website_publish_button` RPC), then navigates `/customers` and confirms the partner is listed. |
| **Capability tested** | Backend-form-to-frontend-preview round-trip with Owl publish systray toggle. Same pattern as `event.event` / `slide.channel`: the form-header `is_published` widget is `website_redirect_button` (navigation-only, NOT a publisher), so the agent must reach the frontend preview to actually publish. /customers requires BOTH `website_published=True` AND `assigned_partner_id != False`. |
| **Notes** | Calibration CORRECT (medium): BU single-shot PASS in 61.4s matches the expected medium-tier behavior — no wizards, no non-default widgets, just backend-to-frontend navigation + one systray click. BU understood the "Go to Website" button text ("aria-label=Unpublished"), followed the preview → systray toggle chain, and verified on /customers. Consistent with sibling `website_hr_recruitment.edit_job_form_publish_preview` which uses a similar publish-and-preview pattern and also PASSes BU. Cookbook note added: `res.partner.is_published` uses `website_redirect_button` in `button_box` (label "Go to Website", aria-label reflects state); real publish path is the Owl `PublishSystrayItem` on `/partners/<slug>`. Seed cleanup must null `assigned_partner_id` back-refs before unlink. |

---

## website_sale_stock.show_stock_availability_add_to_cart

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 54.7s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 70.1s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Website Sale, Product Availability (website_sale_stock) |
| **Workflow** | Seed installs `sale_stock` + `stock_delivery` + `website_sale_stock` (none are in the base snapshot) via `button_immediate_install`. Creates one storable product `Bench Limited Stock` (`type='consu'`, `is_storable=True`, `list_price=40.0`, `is_published=True`, `show_availability=True`, `available_threshold=100`, `allow_out_of_stock_order=True`) with 5 units on-hand at WH/Stock via `stock.quant._update_available_quantity`. Agent navigates `/shop`, opens the product tile, confirms the yellow `#threshold_message` badge renders (`5.0 Units in stock`), bumps `input[name="add_qty"]` from 1 to 3, clicks Add to cart, dismisses any optional-upsell modal. |
| **Capability tested** | Basic /shop navigation + product quantity bump + Add-to-cart persistence check on a `website_sale_stock`-flagged storable product. Banner rendering requires `is_storable=True` AND `show_availability=True` AND `free_qty > 0` AND `free_qty <= available_threshold` — task surfaces the setting trio without requiring the agent to change them. |
| **Notes** | BU single-shot PASS in 70.1s / F1=1.0. Calibration confirmed medium tier — the qty input is directly adjacent to Add-to-cart (no modal, no dual-handle slider), so this is a solvable reference task rather than a failure trap. Per spec fallback ("If cap-at-5 enforcement is not a separate behavior, reduce to add qty=3 and verify availability shown"), we ship the lighter version: `allow_out_of_stock_order=True` means qty isn't server-enforced, but the 3-unit request stays within the banner narrative. New cookbook entries in ODOO19_PATTERNS.md § Website / website_sale_stock: (a) `website_sale_stock` + `sale_stock` + `stock_delivery` not in base, seed must walk the dep chain explicitly (auto_install only fires when all deps are present). (b) `threshold_message` badge conditions — `is_storable`, `show_availability`, `free_qty>0`, `free_qty<=available_threshold`; defaults hide the banner. (c) `type='consu' + is_storable=True` is the Odoo-19 "storable" seed vals. (d) `/shop/cart/add` does NOT enforce on-hand cap when `allow_out_of_stock_order=True` (the default). |

---

## stock_landed_costs.add_cost_to_shipment_allocate

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 28.0s, 8/8 create edits) |
| **Browser-Use** | PASS (F1=1.0, 183.2s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (stock), stock_landed_costs (install on demand) |
| **Workflow** | Seed installs `stock_landed_costs` via `button_immediate_install` (not in base snapshot), creates a dedicated `product.category` `Bench LC Category` with `property_cost_method='fifo'` + `property_valuation='periodic'`, a `Freight` service product with `landed_cost_ok=True` + `split_method_landed_cost='by_quantity'`, a storable `Bench Import Item` under the FIFO/periodic category, a `Bench Import Vendor`, and three VALIDATED (`state='done'`) incoming pickings — the primary `R-BENCH-LC-001` (3 units Bench Import Item) plus two distractors `R-BENCH-LC-DISTRACTOR-A/B` sharing the `R-BENCH-LC` prefix. Agent opens Inventory > Operations > Landed Costs (`/odoo/landed-costs`), clicks New, types `R-BENCH-LC-001` in the **Transfers** many2many_tags autocomplete and picks the exact match, adds a cost line for product=Freight keeping the seeded `split_method=by_quantity` and sets `Cost=45`, clicks the **Compute** footer button to materialise one `stock.valuation.adjustment.lines` row (45/3 × 3 = 45 EUR allocated to the single move), then clicks the header **Validate** statusbar button to move state to `done` (Posted). |
| **Capability tested** | Three-trap compound: (1) **Compute-then-Validate two-button flow** — clicking Validate on an empty adjustment list raises `"Cost and adjustments lines do not match"` from `_check_sum`, so the agent MUST find the footer Compute button below the cost-lines list. (2) **picking_ids many2many_tags domain filter** — the Transfers field filters on `move_ids.is_in != False OR move_ids.is_out != False` (from `stock_account`), so unvalidated pickings are invisible in the autocomplete; seed uses `skip_backorder=True` + `move.picked=True` to drive the receipt to `done`. (3) **Distractor-prefix autocomplete** — two extra validated receipts share the `R-BENCH-LC` prefix; loose typing offers three candidates, agent must narrow to the exact name. |
| **Notes** | BU single-shot solved in 183s, F1=1.0, 0 postcondition failures — prompt is explicit enough about Compute before Validate, exact cost 45, and exact picking `R-BENCH-LC-001` that BU executed the full flow cleanly. Task is useful as a positive-case reference for the `stock.landed.cost` form and serves as a cookbook anchor for future stock_landed_costs tasks. New cookbook entries added to ODOO19_PATTERNS.md under a new "stock_landed_costs" section: (a) module install on demand pattern, (b) `picking_ids` domain requires validated pickings (`is_in`/`is_out` stored Booleans flip only at `state='done'`), (c) seeded `product.category` with `property_cost_method='fifo'` + `property_valuation='periodic'` to avoid stock journal / valuation / price-diff account plumbing, (d) `product.template.landed_cost_ok`/`split_method_landed_cost` fields are invisible on non-service products, (e) **Compute is a footer button** inside the Additional Costs tab (not header), (f) Validate requires saved record — click `.o_form_button_save` first, (g) DO NOT use `button.o_form_button_create` as a Validate fallback selector (it's the top-bar "New" button and spawns a phantom empty record), (h) `compute_landed_cost` unlinks existing adjustments — safe to call twice, (i) `onchange_product_id` stamps `split_method` from `product_tmpl_id.split_method_landed_cost`. Oracle wall clock ~28s; BU wall clock 183s. |

---

## hr_skills_survey.link_certification_survey_to_skill

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (feature unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | HR Skills, Survey, hr_skills_survey bridge (Enterprise extension missing) |
| **Workflow** | Seed `survey.survey` 'Bench Python Cert' (`survey_type='certification'`, `scoring_type='scoring_with_answers'`, `scoring_success_min>=70`, 2 scored simple_choice questions). Seed `hr.skill.type` 'Programming Languages' + `hr.skill` 'Python'. Agent opens skill Python, picks 'Bench Python Cert' in the skill's Certification (survey_id) many2one, saves. Optional: admin takes the survey via the Test link, scores pass, and the admin's `hr.resume.line` / `hr.employee.skill` surfaces a certified entry via the `_mark_done()` hook. |
| **Capability tested** | Configure-then-certify chain: survey creation with scoring config + cross-model Many2one link (skill → survey) + side-effect observation on the employee's resume when the cert is awarded. |
| **Notes** | Blocked — Odoo 19 **Community** `hr_skills_survey` does NOT extend `hr.skill` with a `survey_id` / Certification field. Inspection of `addons/hr_skills_survey/models/` shows only: readonly `survey_id` on `hr.resume.line` (populated automatically by `survey.user_input._mark_done()`), `certification_validity_months` on `survey.survey`, and a `_mark_done()` override that writes resume lines. `grep '_inherit.*hr\\.skill'` across all addons returns zero hits — no module adds a survey Many2one on `hr.skill`. The "link survey to skill" UI is an Enterprise-only extension not vendored in this checkout. Task skeleton (seed/oracle/check) is committed with clear BLOCKED guards that short-circuit with diagnostic errors instead of silently passing. Follows the same precedent as rows 350 (appointment), 351 (helpdesk), 352 (marketing_automation) — all Removed for Enterprise-only feature unavailability. Re-enable once the enterprise skill-certification link is vendored into `addons/`. See the task's RESULT.md for full evidence and re-enabling steps. |

---

## sale_management.create_quotation_template_apply_to_new_so

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 44.3s) |
| **Browser-Use** | PASS (F1=1.0, 234.7s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Sales (sale_management) |
| **Workflow** | Seed grants `sale_management.group_sale_order_template` to admin, seeds two consu products (Bench Widget €10, Bench Gadget €20) and customer `Bench Test Co`. Agent navigates Sales > Configuration > Quotation Templates > New, fills the H1 title `Bench Starter Pack`, adds two lines via the `so_template_line_o2m` editable list (Bench Widget qty 5, Bench Gadget qty 2), saves. Then from Sales > Orders > Quotations > New, picks customer `Bench Test Co`, sets `sale_order_template_id=Bench Starter Pack`; the `_onchange_sale_order_template_id` hook clears and recreates `order_line` from the template's `_prepare_order_line_values()`. Saves as draft. |
| **Capability tested** | Two-stage config + application flow gated by a feature group (`sale_management.group_sale_order_template` controls both the Configuration menu AND the SO form's Quotation Template field). Inline-editable o2m list with a custom `SectionAndNoteListRenderer`-based widget. Onchange-driven line auto-population via an m2o pick (no per-line data entry needed on the SO). |
| **Notes** | Calibration CORRECT for medium: BU single-shot PASS in 234.7s with F1=1.0. Workflow length (config + apply) + the `so_template_line_o2m` line widget made this more than a trivial form edit, but none of the steps required a non-default wizard choice or date picker. To escalate to hard: add a distractor template `Bench Legacy Pack` with different lines (agent must verify correct template applied), require the agent to enable the feature group in Settings first (seed un-grants it), or require an `is_optional` section line on the template. Cookbook notes added for the feature-group double-gate, `so_template_line_o2m` list-cell field names (`product_id`, NOT `product_template_id`), and `sale.order.template.display_name` has no currency suffix (unlike `product.pricelist`). |

---

## stock_sms.enable_delivery_sms_notification_validate

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 23.2s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 113.9s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Stock, SMS, Stock-SMS bridge (`sms` + `stock_sms` installed on demand — neither in base; `stock_sms` auto-installs when `sms` is installed) |
| **Workflow** | Seed installs `sms`, which auto-triggers `stock_sms` (auto_install=True). Seed explicitly resets `res.company.stock_text_confirmation=False` (the post_init hook defaults it True) and `has_received_warning_stock_sms=False` so the warning wizard fires on first validate. Creates partner `Bench SMS Customer` with `country_id=base.us` + `phone='+16175551234'` (valid US E.164 for `_phone_format`), product `Bench SMS Item` with on-hand stock, and a confirmed outgoing picking sourced from `sale.order` name `S-BENCH-SMS-001` (→ picking `origin='S-BENCH-SMS-001'`) with quantities already pushed to reserved so Validate doesn't open the transfer wizard. Agent: Inventory → Configuration → Settings → tick **Text Confirmation** (Operations block) → Save. Then Inventory dashboard → **Delivery Orders** card → open `S-BENCH-SMS-001` → **Validate** → on the `confirm.stock.sms` modal ("You are about to confirm this Delivery Order by SMS Text Message") click **Confirm** (primary, `name=send_sms`), NOT the secondary **Disable SMS** button. |
| **Capability tested** | Side-effect trap: settings toggle (`res.company.stock_text_confirmation`) + validate side-effect (stock_sms warning wizard with non-default primary action) + downstream SMS emission (`_send_confirmation_email` → `_message_sms_with_template` → `_notify_thread_by_sms` creates `sms.sms` with `body`, `number`, `mail_message_id` linking to the picking's `mail.message`). Distractor: **Disable SMS** button flips `stock_text_confirmation=False`, which would fail the check. |
| **Notes** | Calibration CORRECT (medium) but browser-use passes reliably; kept as medium coverage for the stock_sms bridge + side-effect-trap pattern. New cookbook entries in `COOKBOOK_NOTES.md`: (1) `stock_sms.post_init_hook` unconditionally sets `stock_text_confirmation=True` on install — seeds that want the user to toggle must reset it back to False AFTER `button_immediate_install`. (2) The feature lives on `res.company`, NOT on `stock.picking.type` (no `picking_type_id.sms_confirmation` field exists despite what the task spec suggested). (3) `has_received_warning_stock_sms` gates the warning wizard — once True, subsequent validates skip the wizard. (4) Primary wizard button is `name='send_sms'` (Confirm), secondary is `name='dont_send_sms'` (Disable SMS). (5) `sms.sms` records persist BEFORE `.send()` runs, so body + number + mail_message_id are set regardless of IAP transport outcome; `state` flips outgoing→error without IAP credits — put `state` in `ignore_fields`. (6) `res.company` entity_key normalizes to `[null]` in state_diff despite `match_key: [name]` (related-field read comes back False through the instrumentation cursor) — use `"entity_key": [null]` literally in `expected_state.json`. |

---

## project.create_milestone_assign_tasks_reach

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 18.7s, 6/6 create+set edits) |
| **Browser-Use** | FAIL (F1=0.0, 360.0s timeout, 3 postcondition failures) |
| **F1** | 0.0 |
| **Odoo modules** | Project (project.milestone + project.task) |
| **Workflow** | Seed creates `Bench Milestone Proj` with `allow_milestones=True`, 3 tasks (`T1 - Draft Spec`, `T2 - Build Prototype`, `T3 - Review Final`), all without milestones and no existing milestones on the project. Agent opens the project's embedded **Milestones** panel (reachable via project-card kebab OR from within the project's task view's Top Menu → Milestones), clicks **New** in the inline-editable list, fills name `Phase 1 Complete` + deadline `2026-06-01`, saves. Then opens T1 and T2 task forms one by one, sets the `Milestone` many2one to `Phase 1 Complete`, saves. Distractor T3 must stay milestone-less. Finally returns to the Milestones list/form and toggles `is_reached=True`. |
| **Capability tested** | Compound medium-tier: (a) discovering the `ir.embedded.actions` "Milestones" entry for a project (Top Menu / kebab — NOT a tab on the project form), (b) inline-list create + deadline commit in `project_milestone_view_tree`, (c) two per-task milestone_id many2one autocomplete saves (same fragile dropdown as `project_todo.bulk_move_tasks_between_projects`), (d) re-opening the milestone and flipping a Boolean (`is_reached`) after the initial Save cycle. Distractor T3 catches "apply to all tasks" fallback behaviour. |
| **Notes** | BU single-shot FAIL — spent 27+ steps hunting for the Milestones panel (looped clicking the same menu item with repetition=5, stagnation=0 nudges), finally created the milestone, then looped bouncing between Tasks list and T1 form without committing `milestone_id` on T1 or T2. Never flipped `is_reached`. Hit 360s cap with 4/6 observed edits, Recall=3/6. Calibrates at medium tier (tier: 2). Oracle path: JSON-RPC `project.milestone.create` → `project.task.web_save({milestone_id})` x2 → `project.milestone.write({is_reached: True})`. New cookbook entries in COOKBOOK_NOTES.md (task-scoped): (a) `project.project.allow_milestones` gates both the embedded action and the per-task `milestone_id` field; `project.group_project_milestone` is implied from `base.group_user` via project_demo.xml. (b) Milestones entry point is `ir.embedded.actions` on `project.project_2_project_task_all`, surfaced as "Milestones" in the project's task-view Top Menu; BU empirically takes ~27 steps to discover it. (c) `project.milestone.is_reached` create-then-write folds to a single `create/norm_value=true` diff row; partial failures emit `create/norm_value=null` (same null-vs-false pattern as website_blog). (d) `project.task.milestone_id` domain `[('project_id','=',project_id)]` scopes autocomplete per-project — no cross-project distractor milestones possible. (e) `match_key: [project_id, name]` on `project.milestone` to avoid name-collision with foreign-project milestones. Add `reached_date` to `ignore_fields` (computed stored Date, timezone-sensitive). |

---

## lunch.create_vendor_product_order_for_today

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 48.2s, 13/13 edits) |
| **Browser-Use** | FAIL (F1=0.0, 2 postcondition failures, wall clock 360s) |
| **F1** | 0.0 |
| **Odoo modules** | Lunch (installed on demand; not in base snapshot) |
| **Workflow** | Seed installs `lunch`, seeds a `Bench Cafe Partner` res.partner, and pre-sets admin's `last_lunch_location_id` + `lunch_minimum_threshold=100`. Agent must: (1) `/odoo/lunch-vendors-menu` → New vendor → pick partner FIRST (the vendor `name` field is `related='partner_id.name', readonly=False` so picking after typing clobbers what was typed), retype name `Bench Cafe`, set phone, change `delivery` via `o_select_menu` to `Delivery`, flip Sat/Sun on the `week_days` table widget so the supplier is available every day, save. (2) `/odoo/lunch-product-menu` → New product → Veggie Wrap / Sandwich / Bench Cafe / 8.00, save. (3) `/odoo/lunch` kiosk dashboard → click Veggie Wrap kanban card (triggers `lunch_open_order` bus event → `lunch.order` modal form) → type Note=`no onions` → click Add To Cart footer button (form `web_save` creates the order with `state='new'`) → back on sidebar click **Order Now** (POST `/lunch/pay` → `action_order()` → `state='ordered'`). |
| **Capability tested** | Non-standard kiosk UI navigation: LunchKanbanRecord onGlobalClick opens a modal, but clicking the is_favorite star corner of the card is a trap. Two-phase submission (Add To Cart in the dialog, then Order Now on the sidebar) — forgetting the sidebar step leaves the order at `new` and fails the postcondition. Odoo 19 `o_select_menu` widget on `delivery` (not native `<select>`) breaks the generic `set_selection` helper. Related-field partner/name rewrite order must be "partner first, then name". `order_deadline_passed` + `display_add_button` gates on the Add To Cart button require the supplier's weekday flag for today + company `lunch_minimum_threshold >= price`. |
| **Notes** | Well-calibrated medium. Oracle PASS 48s single-shot. BU created THREE duplicate `lunch.supplier` rows (retry loop triggered by the `o_select_menu` on `delivery` — BU kept failing to commit "Delivery" and re-created the vendor) and never reached the product step; final state had one vendor with `delivery=no_delivery` and no product/order. Calibration predicted "kiosk-style UI confuses BU" — matches. New cookbook section `ODOO19_PATTERNS.md § lunch`: (a) model is `lunch.supplier` (not `lunch.vendor`); (b) `name=related('partner_id.name', readonly=False)` → pick partner first; (c) `delivery` uses `o_select_menu` (same pattern as crm.team `alias_contact`); (d) `week_days` widget renders as table with unnamed `<CheckBox>` — use column-index lookup; (e) Add To Cart button is gated by supplier's weekday-today AND company threshold — seed must bump `lunch_minimum_threshold` and all-week availability or the task silently fails on weekends; (f) `add_to_cart` Python method is a no-op; the record persistence happens via the form's `web_save` before the object method runs. (g) `lunch.product.supplier_id` normalises to `{supplier.name} {phone}` when phone is set — pin in `expected_state.json`. |

---

## mass_mailing.duplicate_mailing_edit_subject_send

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 20.3s) |
| **Browser-Use** | PASS (F1=1.0 after rescore, 0 postcondition failures, 89.4s single-shot; initial score reported 0.8 because expected_state.json originally omitted the `state='done'` create edit — fixed expected_state and re-scored the same artifacts). |
| **F1** | 1.0 |
| **Odoo modules** | Email Marketing (mass_mailing) |
| **Workflow** | Seed creates a mailing list `Bench Subscribers` with 3 contacts and an already-sent mailing `Bench Newsletter V1` (state='done', sent_date=2026-03-15 09:00, Mailing List recipients, **empty** `contact_list_ids` — agent must explicitly add the list to the duplicate). Agent: Email Marketing → Mailings → open `Bench Newsletter V1` → cog Actions → **Duplicate** → on the new draft set Subject=`Bench Newsletter V2 Spring Special`, confirm Recipients='Mailing List', add `Bench Subscribers` to the Mailing Lists, leave sender/body as copied → click **Send** (top button, action_launch) → confirm the "Ready to unleash emails?" dialog with **Send to all**. |
| **Capability tested** | cog/Actions → Duplicate on a sent (not draft) source + multi-field edit on the copy (subject + add list) + non-default send button ("Send" vs "Send a Sample Mail" vs "Schedule") + confirmation dialog primary action. Anchored to "exactly 2 Bench Newsletter mailings" in check.py to guard against BU's known cog-Duplicate spam loop. |
| **Notes** | Calibration CORRECT-but-easier-than-hoped: BU solved in 10 steps with Duplicate + dropdown pick + Send + confirm dialog. Unlike the sibling `mass_mailing.duplicate_existing_change_subject_recipients` (which adds a country-filter domain edit and traps BU in the Duplicate spam loop, F1=0.0), this task omits the domain widget, so BU has nothing to get stuck on. The `Send` button label is unambiguous, and BU correctly picked the "Send to all" primary action on the confirmation dialog. Source mailing is seeded with state='done' + sent_date so the check.py discriminator (original untouched) is meaningful. Oracle uses JSON-RPC `copy + write + action_launch + write state='done'` to avoid driving the WYSIWYG/recipient autocomplete (same pattern as the other mass_mailing oracles). check.py accepts state in ('in_queue', 'sending', 'done') since BU's click-Send path may land at 'in_queue' if the mailing cron hasn't drained yet. No new cookbook quirks — leveraged existing notes on `mailing.mailing.copy_data` contact_list_ids verbatim + cog→Duplicate BU failure mode. |

---

## mrp.workorder_operation_scan_serial_complete

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 17.9s, 4/4 edits matched) |
| **Browser-Use** | FAIL (F1=0.0, 121.6s, 2 postcondition failures: no lot consumed) |
| **F1** | 0.0 |
| **Odoo modules** | Manufacturing (mrp — workcenter + workorder + serial-tracked consumption) |
| **Workflow** | Seed grants admin `mrp.group_mrp_routings` + `stock.group_production_lot`, creates product `Bench Assembly Kit` (tracking='none') and serial-tracked component `Bench Serial Part` (tracking='serial'). Creates 4 `stock.lot` rows — `SN-A`, `SN-B`, `SN-C`, `SN-D` — each with 1.0 on hand at WH/Stock (SN-A has the lowest id, so `action_confirm` auto-reserves SN-A as the default). Creates workcenter `WC-01` + `mrp.bom` with one operation `Final Assembly` on WC-01. Creates confirmed `mrp.production` `MO-BENCH-WO` qty=1 with one `mrp.workorder`. Agent opens the MO, clicks `Start` on the Final Assembly work order (state: ready → progress), opens the `Details` popup on the Bench Serial Part component row in the Components tab, changes the Lot/Serial from the auto-reserved SN-A to `SN-B` (distractor serials SN-C and SN-D also present), saves, clicks `Done` on the work order (state: progress → done), then clicks `Mark as Done` in the MO header. |
| **Capability tested** | Compound HARD: full work-order lifecycle (`button_start` → `button_finish` → `button_mark_done`) PLUS non-default serial override via `Detailed Operations` popup on a serial-tracked raw move. Four-serial distractor (SN-A reserved by default, SN-C/SN-D unreserved) means the agent cannot just click-through defaults. Two distinct `Done`-style buttons (WO `Done` vs MO `Mark as Done`) are an easily-confused UI trap. |
| **Notes** | Calibration CORRECT for hard (tier: 3). BU single-shot ran the correct sequence (`button_start` → `action_show_details` → `web_save` → `button_finish` → `button_mark_done` all present in trace) and the MO reached state=`done` with qty_produced=1.0, BUT the agent wrote `lot_id: False` in the Details popup (it typed into `lot_name` instead of picking SN-B from the autocomplete). Result: `button_mark_done` cleared the unassigned move_line, no lot got consumed, the check.py postcondition "Expected exactly ['SN-B'] consumed, got []" fired — strict FAIL. This is exactly the failure pattern the prompt warns about. New cookbook quirks added to ODOO19_PATTERNS.md: (1) `mrp.workorder.button_finish` calls `move._set_quantity_done(qty)` which can REPLACE move_line_ids created by the agent via the Details popup — the agent MUST either set `move.picked = True` or pre-populate `move_line_ids.quantity` before `button_finish` runs, otherwise the reservation is overwritten. (2) The `Details` popup on a serial-tracked Components-tab row (`stock.move.action_show_details`) opens a `view_stock_move_operations` modal with a `move_line_ids` O2M list whose `lot_id` column is a m2o autocomplete — BU frequently types into the `lot_name` Char instead (which creates an unassigned line). (3) `mrp.workorder` entity_key with `match_key: [production_id, workcenter_id]` normalizes to `[null, null]` in `expected_state.json` — both Many2one fields read back as null through the instrumentation cursor (same pattern as `sale.order.order_line.order_id` → null). (4) After `action_confirm` on a MO with serial-tracked component + multiple lots on hand, the auto-reservation picks the lot with the lowest `stock.lot.id` (deterministic by seed-creation order), NOT by `name` lexicographic order — so seeding serials A/B/C/D in that order guarantees A is the default. |

---

## crm_iap_enrich.bulk_enrich_leads_from_list

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.3s, 3/3 set edits) |
| **Browser-Use** | PASS (F1=1.0, 140.4s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | CRM, crm_iap_enrich (install on demand — not in base snapshot), iap |
| **Workflow** | Seed installs `crm_iap_enrich` via `button_immediate_install`, flips `crm.iap.lead.enrich.setting='manual'` to disable the auto-cron, grants admin `crm.group_use_lead`, seeds 5 leads all with `@gmail.com` emails (in `iap_tools._MAIL_PROVIDERS`): 3 unenriched targets (`Bench Enrich Target Alpha/Bravo/Charlie`) + 2 already-enriched distractors (`Bench Enrich Already Delta` + `Bench Enrich Manual Echo`, both `iap_enrich_done=True`). Agent opens `/odoo/action-crm.crm_lead_all_leads`, switches to list view, clears default filters, searches `Bench Enrich`, ticks the 3 target checkboxes, opens the control-panel Actions dropdown, and clicks **Enrich**. The server action (`crm_iap_enrich.action_enrich_mail`, binding on `crm.lead`) runs `records.iap_enrich()`; because `gmail.com` is in `_MAIL_PROVIDERS`, the loop short-circuits BEFORE the external IAP call — flipping `iap_enrich_done=True` and posting a `mail_message_lead_enrich_notfound` chatter note ("No company data found based on the email address or email address is one of an email provider. No credit was consumed.") on each selected lead. No IAP credits consumed, no outbound network needed. |
| **Capability tested** | Multi-select list → control-panel Actions menu → server-action binding (`ir.actions.server.binding_model_id = crm.lead`) path, with side-effect verification on both `iap_enrich_done` (Boolean flip in state diff) and `mail.message` bodies (verified in check.py via HTML-stripped substring match on "No company data found"). Distractors catch "select all rows" fallback: including the two `iap_enrich_done=True` records in the selection is harmless to the state diff (they skip in `iap_enrich` early return) but check.py asserts no new notfound message appears on them — so the agent's selection still matters. |
| **Notes** | Calibration MEDIUM not HARD: BU single-shot PASS in 140.4s with F1=1.0 and 0 postcondition failures. The multi-select Actions-menu + server-action side-effect pattern turned out to be solvable by BU (it correctly switched to list view, selected the three named rows, navigated the Actions dropdown, and verified the chatter after). To escalate to genuine HARD tier, a future iteration should (a) add a third selection constraint (e.g. a 6th lead with same "Bench Enrich" prefix but a non-gmail corporate email that WOULD hit the live IAP endpoint — agent must exclude it), (b) require the agent to toggle the "Lead Enrichment" auto/manual setting in Settings BEFORE the bulk action (two-panel flow), OR (c) combine the Enrich action with a subsequent per-lead priority bump while still in multi-select to test list-level inline edits. Kept as-is because the deep-UI pattern (Actions dropdown on selected rows) has no sibling coverage and the server-action binding + mail.message side-effect verification forms a clean reference template for future `iap` / `iap_mail` tasks. New cookbook entries added to ODOO19_PATTERNS.md: (a) `crm.lead` has NO `ref` field — use `name` (unique within the seed) as `match_key` for state diffs on crm.lead. (b) `crm_iap_enrich.iap_enrich()` short-circuits BEFORE any external IAP call when `email_domain in iap_tools._MAIL_PROVIDERS` (gmail.com, yahoo.com, hotmail.com, outlook.com, icloud.com, aol.com, etc. plus `example.com`), marking `iap_enrich_done=True` and posting `mail_message_lead_enrich_notfound` — this is the credit-free deterministic path for bench tasks that need to exercise the Enrich action without live IAP network/credits. (c) `crm_iap_enrich` module is NOT in base snapshot — seed must `button_immediate_install`. (d) `crm.lead.create()` triggers `crm.iap.lead.enrich.setting='auto'` → cron trigger in `create()` override; seed should `set_param('crm.iap.lead.enrich.setting','manual')` BEFORE creating leads to keep `iap_enrich_done` state pristine. (e) The Enrich server-action record is `crm_iap_enrich.action_enrich_mail` with `binding_model_id=crm.model_crm_lead` and `state='code'` running `records.iap_enrich()` — it surfaces in the list-view Actions menu on `crm.lead`. |

---

## sale_timesheet.log_timesheet_on_so_invoice_delivered

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 58.0s) |
| **Browser-Use** | PASS (F1=1.0, 182.7s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Sales, hr_timesheet, sale_timesheet (both installed on demand — neither in base) |
| **Workflow** | Seed installs `hr_timesheet` then `sale_timesheet` via `button_immediate_install`, creates service product `Bench Consulting` (`SERV-BENCH-TS`) with `invoice_policy='delivery' + service_type='timesheet' + service_tracking='task_in_project'` (i.e. `service_policy='delivered_timesheet'`) at 150.00/h, a distractor service `Bench Widget Supply` (`SERV-BENCH-MAN`) with `service_type='manual'`, and partner `Bench Services Co`. Creates SO `S-BENCH-TS-001` (10 h × 150.00, no taxes) and pre-confirms it via `action_confirm` — confirmation's `_timesheet_service_generation()` hook auto-creates a `project.project` + single `project.task` tied to the SO line. Agent: Sales > open `S-BENCH-TS-001` > click combined Projects/**Tasks** smart button (`oe_stat_button` with `name='action_view_project_ids'`) > open the sole task > **Timesheets** tab > Add two rows (4h on 2026-04-15 + 2h on 2026-04-19, both Administrator) > save task > breadcrumb back to SO > verify Delivered=6.00 on the `Bench Consulting` line > **Create Invoice** > keep **"Regular invoice"** radio (NOT down-payment) > click **Create Draft** (primary, `name='create_invoices'`). |
| **Capability tested** | Cross-model chain SO → auto-generated project.task → account.analytic.line timesheet rows → delivered-qty gating (`sale.order.line.qty_delivered` computed from `sum(timesheet.unit_amount)`) → return to SO → Create Invoice wizard with 3 radio options (Regular invoice / Down payment percentage / Down payment fixed). Requires the agent to navigate from Sales into Project territory via a smart button and back. |
| **Notes** | Calibration: **easier than hard** — BU found a shortcut. Single-shot BU PASS in 182.7s with F1=1.0 and 0 postcondition failures. The Timesheets-tab "Add a line" editable list was navigable for BU without tripping the between-rows save quirk (see cookbook). To escalate to genuine hard-tier: (a) require a non-default `Down payment (percentage)` wizard branch with a custom percent, (b) require a non-admin employee (seed a second `hr.employee` e.g. "Bench Consultant" and make ONE of the two rows use them), (c) add a second task on the project with its own Timesheets tab as a navigation trap, or (d) force the agent to enter hours as `0.5` for a decimal parse trap. Kept as documented primary_track=false hard for coverage. New cookbook entries in `ODOO19_PATTERNS.md` (sale_timesheet + hr_timesheet section): (1) install order + `service_policy='delivered_timesheet'` = `invoice_policy='delivery'+service_type='timesheet'`, (2) `product.template` has NO `uom_po_id` in Odoo 19 (seed crash), (3) combined Projects+Tasks smart button is one widget `name='action_view_project_ids'`, (4) `editable="top"` timesheet_ids o2m loses the first row if you Add a line twice without an intermediate save, (5) auto-task generation from `service_tracking='task_in_project'` at SO confirm time, (6) `account.analytic.line.unit_amount` accepts `4:00` / `4.0` via `timesheet_uom` widget. |
