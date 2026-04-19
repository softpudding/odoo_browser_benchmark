# Benchmark Task Status

Tracks all benchmark tasks. Update when adding new tasks or running evaluations.

**Status values:** `WIP` — oracle or eval incomplete | `Done` — oracle passes, eval recorded

Last eval: 2026-04-19 | Oracle: 168/168 (100%) | Browser-Use: 59/168 (35.1%) | New WIP: 85 (44 medium + 23 easy + 18 hard)

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
| 155 | website.add_menu_item_reorder [medium] | Add a website menu item and reorder it within the navigation hierarchy | Done | PASS | FAIL/FAIL | 0.0 |
| 156 | website.create_contact_form_block [hard] | Edit a website page to add and configure a contact form block | Done | PASS | FAIL/PASS | 0.5 |
| 157 | stock.scrap_product_from_receipt [medium] | Open a stock receipt and scrap part of a received product from the operation flow | Done | PASS | PASS/PASS | 1.0 |
| 158 | stock.adjust_inventory_with_location_filter [medium] | Adjust inventory for a target product in one location while leaving other locations unchanged | Done | PASS | PASS/PASS | 1.0 |
| 159 | stock.receive_serial_tracked_product [hard] | Validate a receipt by assigning exact serial numbers to tracked units | Done | PASS | PASS/PASS | 1.0 |
| 160 | mrp.update_bom_component_quantity [medium] | Update one component quantity on an existing bill of materials and save it | Done (dup of 257) | — | — | — |
| 161 | mrp.create_mo_consume_produce_done [hard] | Create a manufacturing order, record component consumption, and mark production done | Done | PASS | PASS/PASS | 1.0 |
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
| 175 | mrp.scrap_component_during_production [hard] | Scrap one consumed component from a running MO via the component action menu | Done | PASS | PASS/PASS | 1.0 |
| 176 | mrp.convert_bom_to_kit_type [easy] | Change an existing BOM's type from Manufacture This Product to Kit | Done | PASS | PASS | 1.0 |
| 177 | mrp.create_variant_specific_bom [hard] | Create a BOM that applies only to a single product variant via attribute filter | Done | PASS | FAIL/FAIL | 0.0 |
| 178 | mrp.configure_mo_operation_time_finish [medium] | Open a work order on an MO, set expected duration, and mark it finished | Done | PASS | FAIL/PASS | 1.0 |
| 179 | point_of_sale.sell_two_products_apply_discount [medium] | Ring up two POS products, apply a 10% line discount, pay cash | Done | PASS | PASS/PASS | 1.0 |
| 180 | point_of_sale.refund_previous_order [hard] | Refund a prior POS order partially from the Orders menu | Done | PASS | FAIL/FAIL | 0.0 |
| 181 | point_of_sale.attach_customer_mid_sale [easy] | Open a POS session, add a product, attach existing customer, pay cash | Done | PASS | PASS/PASS | 1.0 |
| 182 | point_of_sale.close_session_reconcile_cash_diff [medium] | Close a POS session with a counted cash amount different from expected | Done | PASS | PASS/FAIL | 0.5 |
| 183 | website_sale.add_product_to_cart_checkout_portal [medium] | As a public user, add a product to cart and complete checkout with address | Done | PASS | FAIL/PASS | 0.5 |
| 184 | website_sale.apply_promo_code_at_checkout [medium] | Create a coupon program in backend then apply the code on the storefront | Done | PASS | PASS/PASS | 1.0 |
| 185 | website_sale.edit_product_image_gallery [easy] | Add an extra image to a published product via the shop editor | Done | PASS | PASS/PASS | 1.0 |
| 186 | website_sale.configure_delivery_method_weight [medium] | Create a delivery method with weight-based pricing rules | Done | PASS | FAIL/PASS | 0.5 |
| 187 | website.create_new_page_publish [medium] | Create a blank new website page, add a heading, and publish it | Done | PASS | FAIL/FAIL | 0.0 |
| 188 | website.set_page_seo_fields [easy] | Use the Promote dialog to set meta title, description, and keywords on a page | Done | PASS | FAIL/FAIL | 0.6667 |
| 189 | website.add_image_snippet_swap_source [medium] | Drag an Image snippet into a page and swap its source image | Done | PASS | FAIL/FAIL | 0.0 |
| 190 | website.duplicate_page_rename_unpublish [easy] | Duplicate an existing website page, rename the copy, and leave unpublished | Done | PASS | PASS/PASS | 1.0 |
| 191 | hr_holidays.approve_multiple_requests_bulk [hard] | Multi-select pending time-off requests in list view and bulk approve | Done | PASS | FAIL/FAIL | 0.67 |
| 192 | hr_holidays.request_leave_with_attachment [medium] | Request leave and attach a PDF justification via the chatter | Done | PASS | FAIL/FAIL | 0.0 |
| 193 | hr_expense.split_expense_analytic_distribution [hard] | Split one expense line 50/50 across two analytic accounts | Done | PASS | FAIL/PASS | 0.5 |
| 194 | hr_expense.refuse_report_with_reason_chatter [medium] | Refuse a submitted expense report and post the reason to chatter | Done | PASS | PASS/PASS | 1.0 |
| 195 | hr_expense.post_approved_expense_to_journal [medium] | Manager posts an approved expense report to its journal entry | Done | PASS | PASS/PASS | 1.0 |
| 196 | mail.star_and_reply_inbox_message [easy] | Star an inbox message and post a reply | Done | PASS | FAIL/FAIL | 0.0 |
| 197 | mail.mark_message_done_archive_notification [easy] | Mark Done on an inbox notification to remove it from Inbox | Done | PASS | FAIL/FAIL | 0.1667 |
| 198 | mail.create_group_channel_upload_attachment [medium] | Create a private channel, invite a member, and upload a file attachment | Done | PASS | FAIL/FAIL | 0.0 |
| 199 | im_livechat.add_canned_response_send_in_chat [medium] | Create a canned response shortcut and send it in an operator chat | Done | PASS | PASS/PASS | 1.0 |
| 200 | fleet.log_service_cost_record [easy] | Add a service cost record (oil change) to an existing vehicle | Done | PASS (32.1s) | FAIL (142.4s) | 0.00 |
| 201 | fleet.assign_vehicle_tags_category [easy] | Add two tags and set a category on a vehicle | Done | PASS | PASS | 1.0 |
| 202 | fleet.transfer_vehicle_new_driver [medium] | Change a vehicle's driver and set the new assignment date | Done | PASS | FAIL/FAIL | 0.0 |
| 203 | event.add_event_questions_to_registration [medium] | Add two custom questions to an existing event registration form | Done | PASS | PASS/PASS | 1.0 |
| 204 | event.create_event_tracks_session_schedule [hard] | Add two conference tracks with times to a published event | Done | PASS | FAIL/FAIL | 0.0 |
| 205 | event.set_ticket_seat_availability_limit [easy] | Set total seat limit and per-ticket max for an event | Done | PASS | FAIL | 0.4 |
| 206 | stock.create_internal_transfer_between_locations [medium] | Create an internal transfer between two locations, add a line, and validate | Done (dup of 258) | — | — | — |
| 207 | stock.create_putaway_rule_for_product [hard] | Configure a putaway rule routing a product to a specific sub-location | Done | PASS | PASS/PASS | 1.0 |
| 208 | stock.count_inventory_apply_with_date [medium] | Make an inventory adjustment with a specific counted date | Done | PASS | FAIL/FAIL | 0.0 |
| 209 | stock.set_storage_category_capacity [medium] | Define a storage category with capacity and assign it to a location | Done | PASS | FAIL/FAIL | 0.0 |
| 210 | account.create_manual_journal_entry_balanced [hard] | Create a misc journal entry with three balanced debit/credit lines and post | Done | PASS | PASS/PASS | 1.0 |
| 211 | account.reconcile_bank_statement_line_manual [hard] | Open a bank statement line and reconcile it against a suggested invoice | Done | PASS | FAIL/FAIL | 0.0 |
| 212 | account.create_recurring_entry_template [medium] | Save a journal entry as a recurring entry template | Done | PASS | PASS/PASS | 1.0 |
| 213 | account.lock_books_set_period_lock_date [medium] | Set the Non-Advisors Lock Date in accounting settings | Done | PASS | FAIL/FAIL | 0.0 |
| 214 | crm.set_lost_reason_reassign_salesperson [medium] | Mark opportunity Lost with specific reason then reassign salesperson | Done | PASS | — | — |
| 215 | crm.pivot_view_opportunities_by_stage_revenue [easy] | Switch CRM pipeline to Pivot view, group by stage, measure expected revenue | Done | PASS | PASS/PASS | 1.0 |
| 216 | project.kanban_drag_task_between_stages [easy] | Drag a task kanban card from one stage to another | Done | PASS | FAIL | 0.0 |
| 217 | project.create_project_from_template_duplicate [medium] | Duplicate an existing project keeping its tasks | Done | PASS | PASS/PASS | 1.0 |
| 218 | project.recurring_task_configure_frequency [medium] | Configure an existing task as recurring with weekly frequency | Done | PASS | PASS/PASS | 1.0 |
| 219 | contacts.add_bank_account_to_partner [easy] | Add an IBAN bank account to an existing partner via Invoicing tab | Done | PASS | — | — |
| 220 | contacts.archive_partner_then_unarchive_filter [easy] | Archive a contact then unarchive it via the Archived search filter | Done (dup of 232) | — | — | — |
| 221 | calendar.invite_external_attendee_by_email [easy] | Create a calendar event inviting an external email address not in partners | Done | PASS | PASS | 1.0 |
| 222 | survey.create_survey_one_page_publish_share [medium] | Create a 3-question survey, publish it, and copy the share link | Done | PASS | PASS/PASS | 1.0 |
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
| 345 | point_of_sale.cash_in_sell_cash_out_close_session [hard] | In POS, perform cash in, complete a sale, record cash out, then close the session | Removed | FAIL (spec) | — | — |
| 346 | delivery.country_rule_and_free_threshold_apply_to_so [medium] | Create a carrier with destination rules and free-shipping threshold, then apply it to a matching quotation | Done | PASS | PASS | 1.0 |
| 347 | inventory.cycle_count_two_locations_apply_selected_delta [medium] | Perform a cycle count across two locations and apply only the intended stock discrepancy | Done | PASS | FAIL | 0.0 |
| 348 | project_todo.create_note_set_color_deadline [easy] | Create a note, set a deadline, and apply a non-default kanban color | Done | PASS | FAIL | 0.0 |
| 349 | survey.create_certification_quiz_attempt_limit_publish [hard] | Build a certification quiz with passing score and attempt limit, then publish it | Removed | FAIL (oracle) | — | — |
| 350 | appointment.public_booking_reschedule_cancel_portal [hard] | Configure an appointment type, book it publicly, then reschedule and cancel it from the portal | Removed | FAIL (module unavailable) | — | — |
| 351 | helpdesk.team_sla_assign_escalate_close [hard] | Create a helpdesk team with SLA policy, process a ticket through assignment and escalation, then close it | Removed | FAIL (module unavailable) | — | — |
| 352 | marketing_automation.tag_trigger_drip_campaign [hard] | Build a tag-triggered marketing automation flow with delayed actions and a stop condition | Removed | FAIL (module unavailable) | — | — |
| 353 | event_product.sell_event_product_fill_attendee_details [medium] | Sell an event-linked product and complete attendee details for the generated registration | Done | PASS | FAIL | 1.0 |
| 354 | event_sale.multi_ticket_checkout_two_attendees [hard] | Configure two paid ticket types and complete one website checkout with separate attendee details | Done | PASS | PASS | 1.0 |
| 355 | sale_loyalty.buy_x_get_y_reward_in_cart [hard] | Configure a Buy X Get Y promotion and verify the free-product reward appears in the cart | Done | PASS | PASS | 1.0 |
| 356 | sale_purchase.mto_so_generate_po_change_vendor_confirm [hard] | Confirm an MTO sale order, inspect the generated PO, switch vendor, and continue the chain | Done | PASS | PASS | 1.0 |
| 357 | sale_stock.confirm_so_manual_reserve_validate_delivery [medium] | Confirm a sale order, manually reserve stock on its delivery, and validate the transfer | Done | PASS | PASS | 1.0 |
| 358 | website_blog.create_post_with_cta_seo_schedule [medium] | In the 'Bench News' blog, create a post with a CTA button block (Learn More, href='/shop'), fill Meta Title + Meta Description via the Optimize SEO dialog, and schedule publish for 2026-05-20 09:00 without publishing | Removed | FAIL (oracle) | — | — |
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
| 391 | project_sms.send_reminder_sms_to_task_followers [medium] | Open project Bench SMS Project's Tasks list, multi-select two seeded reviewer tasks, cog Actions > Send SMS in mass mode, body "Reminder: please review by EOD", Send now — emits one sms.sms per task (2 total, one per reviewer phone) | Done | PASS | FAIL | 0.5 |
| 392 | mrp.workorder_operation_scan_serial_complete [hard] | Start a work order, consume serial-tracked component via scan, mark operation done and finish MO | Done | PASS | FAIL | 0.0 |
| 393 | crm_iap_enrich.bulk_enrich_leads_from_list [hard] | From CRM Leads list view, multi-select 3 unenriched leads (skip 2 distractors) and run the Actions > Enrich server action | Done | PASS | PASS | 1.0 |
| 394 | website_forum.post_question_accept_answer [medium] | Post a question on the website forum, answer it, accept the answer | Done | PASS | FAIL | 0.0 |
| 395 | stock.transfer_reserved_to_ready_partial_backorder [hard] | Reserve qty on a delivery, validate only part of it, create backorder | Done | PASS | FAIL | 0.0 |
| 396 | website_sale_wishlist.add_product_share_to_email [medium] | Add a seeded product to the admin wishlist from /shop (share-by-email feature absent in Odoo 19 Community — re-scoped to wishlist persistence) | Done | PASS | PASS | 1.0 |
| 397 | purchase.create_rfq_receive_invoice_3way_match [hard] | Create RFQ (Bench Supply Co + Bench PO Item A qty=10 + Bench PO Item B qty=5), Confirm Order, open Receipt smart button, set Done=7 on Item A (leave B=5), Validate with Create Backorder, navigate to Purchase Orders list, select the PO checkbox, click Create Bills, set Bill Reference `BSC-BILL-3WM`, Confirm (post). Enforces full 3-way match: PO state=purchase, original picking done, backorder pending, account.move posted with BSC-BILL-3WM ref linked to the PO. | Done | PASS | FAIL | 0.0 |
| 398 | hr_attendance.clock_in_out_kiosk_mode [medium] | From Attendance kiosk, an employee clocks in and then clocks out | Done | PASS | PASS | 1.0 |
| 399 | account.credit_note_partial_refund_post [hard] | On posted invoice `INV/BENCH/001` (Bench Item A qty=4@100 + Bench Item B qty=2@50 = 500.00), open the Reverse wizard (header "Credit Note"), set reason "Wrong qty", click **Reverse** (primary `refund_moves`, NOT "Reverse and Create Invoice"), on the draft credit note change Item A qty 4→2 AND delete Item B line, Confirm-post. Source invoice stays posted; credit note `out_refund` total=200, `reversed_entry_id`=source. | Done | PASS | FAIL | 0.0 |
| 400 | website.submit_contact_form_create_crm_lead [medium] | Submit the frontend /contactus form and verify a CRM lead is created | Done | PASS | PASS | 1.0 |
| 401 | stock_barcode.receive_via_barcode_scan_validate [hard] | Use Barcode app to receive a picking by scanning product codes | Removed | FAIL (module unavailable) | — | — |
| 402 | hr_holidays.request_allocation_approve_self_book_day_off [hard] | Allocate time off, approve, then book a day off against it | Done | PASS | PASS | 1.0 |
| 403 | hr_recruitment.create_applicant_kanban_move_to_offer [medium] | Create an applicant via kanban, move through stages to Contract Proposal | Done | PASS | PASS | 1.0 |
| 404 | account_followup.send_reminder_level_two_customers [hard] | Configure a follow-up level, trigger reminder on overdue invoices, send | Removed | FAIL (module unavailable) | — | — |
| 405 | stock.adjust_inventory_count_apply_moves [medium] | Open Physical Inventory, edit counted qty, apply adjustments | Done | PASS | FAIL | 0.0 |
| 406 | event.create_event_add_question_publish [hard] | Create event, add registration question with required answer, publish | Done | PASS | PASS | 1.0 |
| 407 | hr_expense.scan_submit_expense_from_mobile_portal [medium] | From My Expenses portal, create a simple expense and submit | Done | PASS | PASS | 1.0 |
| 408 | mail.send_email_with_attachment_log_as_note [medium] | On a partner form, send an email with attachment via chatter Send Message | Done | PASS | FAIL | 0.0 |
| 409 | project.create_task_with_deadline_tags_assignees [medium] | Create a project task with deadline, 2 tags, and 2 assignees | Done | PASS | PASS | 1.0 |
| 410 | website_sale.checkout_portal_apply_coupon_complete [hard] | Add product to cart, apply coupon code at checkout, complete order | Done | PASS | PASS | 1.0 |
| 411 | documents.upload_document_tag_assign_to_folder [medium] | Upload a document to a folder, tag it, assign owner | Removed | FAIL (module unavailable) | — | — |
| 412 | stock.create_scrap_order_for_damaged_qty [medium] | Create a scrap order for 3 damaged units from WH/Stock | Done | PASS | PASS | 1.0 |
| 413 | calendar.create_recurring_meeting_weekly_pattern [medium] | Create a recurring meeting with weekly pattern, 4 occurrences | Done | PASS | FAIL | 0.0 |
| 414 | crm.duplicate_lead_convert_to_opportunity [medium] | Duplicate a lead, convert the copy to an opportunity | Done | PASS | FAIL | 0.0 |
| 415 | mrp.scrap_consumed_component_during_production [hard] | During MO production, scrap 1 of 3 consumed units, validate MO | Done | PASS | PASS | 1.0 |
| 416 | account.reconcile_customer_payment_against_invoice [hard] | Register a customer payment and reconcile against an open invoice | Done | PASS | PASS | 1.0 |
| 417 | product.configure_variant_attribute_two_values [medium] | Configure a product with a Size attribute + 3 values, generates variants | Done | PASS | PASS | 1.0 |
| 418 | sale.configure_pricelist_apply_to_order_line [hard] | Create pricelist with rule, apply to SO, verify discount | Done | PASS | PASS | 1.0 |
| 419 | mrp.unbuild_product_back_to_components [hard] | Unbuild 2 finished products and return components to stock | Done | PASS | PASS | 1.0 |
| 420 | point_of_sale.apply_fixed_discount_before_payment [hard] | In POS, add 2 products, apply fixed 5 EUR discount, pay cash | Done | PASS | PASS | 1.0 |
| 421 | mrp_account.mo_consume_and_close_check_valuation [hard] | Confirm MO with tracked cost components, close, verify stock.valuation.layer | Done | PASS | PASS | 1.0 |
| 422 | mail.create_alias_route_to_record [hard] | Create a mail alias pointing to a crm.team, incoming email creates a lead | Done | PASS | PASS | 1.0 |
| 423 | account.reverse_journal_entry_from_general_ledger [hard] | From GL, find posted entry, reverse it, verify reverse entry posted | Done | PASS | PASS | 1.0 |
| 424 | website_slides.duplicate_course_edit_add_slide [medium] | Duplicate an existing course, rename, add a new slide | Done | PASS | PASS | 1.0 |
| 425 | hr.generate_employee_card_set_badge_id [medium] | Set Badge ID (barcode) on an employee, optionally trigger Print Badge | Done | PASS | PASS | 1.0 |
| 426 | sale.duplicate_quotation_edit_delivery_date_confirm [medium] | Duplicate a draft quotation, change delivery date, confirm | Done | PASS | PASS | 1.0 |
| 427 | stock.create_physical_inventory_adjust_two_products [medium] | From Inventory Adjustment menu, add 2 products with counted qty, Apply | Done | PASS | PASS | 1.0 |
| 428 | mail.schedule_activity_on_partner_with_note [medium] | Schedule a 'To Do' activity on a partner with note and deadline | Done | PASS | PASS | 1.0 |
| 429 | hr_timesheet.log_time_for_2_days_approve_via_manager [hard] | Log timesheets for 2 days, submit, approve via manager | Removed | FAIL (module unavailable) | — | — |
| 430 | website_blog.change_author_republish_post [medium] | Change a published blog post's author to a different user | Done | PASS | PASS | 1.0 |
| 431 | event.create_event_add_ticket_publish [medium] | Create an event with a specific date, add a paid ticket type, and set it to published | Done | PASS | PASS | 1.0 |
| 432 | fleet.add_vehicle_log_odometer [easy] | Create a new vehicle record, then log an odometer reading via the dedicated odometer action | Done | PASS | PASS/FAIL | 0.5 |
| 433 | mrp.create_bom_with_components [medium] | Create a Bill of Materials for a product with three specific components and quantities | Done | PASS | FAIL | 0.0 |
| 434 | website_sale.publish_product_shop [easy] | Find an unpublished product in the backend, set its sales price and publish it to the shop | Done | PASS | PASS | 1.0 |
| 435 | account.register_partial_payment_reconcile_invoice [hard] | Register partial payment on posted customer invoice, verify reconciliation state | Done | PASS | PASS | 1.0 |
| 436 | stock.delivery_transfer_validate_partial_backorder_no [medium] | Validate delivery picking with partial qty, decline backorder creation | Done | PASS | FAIL | 0.0 |
| 437 | purchase.confirm_rfq_receive_full_three_way_match [medium] | Confirm RFQ, mark PO received, verify 3-way match ready | Done | PASS | PASS | 1.0 |
| 438 | hr.create_department_assign_manager_two_employees [medium] | Create HR department, assign manager, add 2 employees | Done | PASS | FAIL | 0.0 |
| 439 | project.set_task_priority_urgent_assign_tag [easy] | Set first priority star (priority '1') and add existing 'Bug' tag on seeded task | Done | PASS | PASS | 1.0 |
| 440 | sale.add_section_note_line_to_quotation [medium] | Add section header + note line to draft quotation | Done | PASS | PASS | 1.0 |
| 441 | website.publish_draft_page_set_menu_visibility [hard] | Publish a draft website page and add it to main menu in position 2 | Done | PASS | FAIL | 0.0 |
| 442 | crm.assign_lead_salesperson_change_stage_won [medium] | Assign salesperson, move stage, mark Won | Done | PASS | PASS | 1.0 |
| 443 | mass_mailing.create_mailing_select_list_schedule_send [hard] | Create mass mailing, pick list, schedule future send | Done | PASS | FAIL | 0.0 |
| 444 | fleet.assign_vehicle_create_contract_active [medium] | Create vehicle contract, link to existing vehicle, activate | Done | PASS | FAIL | 0.0 |
| 445 | sale.apply_discount_percent_on_sale_order_line [medium] | Apply percent discount on sale order line | Done | PASS | PASS | 1.0 |
| 446 | account.post_draft_invoice_send_to_customer [medium] | Post draft invoice then send by email | Done | PASS | PASS | 1.0 |
| 447 | stock.receipt_full_quantity_validate_no_backorder [easy] | Validate incoming shipment at full qty, no backorder | Done | PASS | PASS | 1.0 |
| 448 | project.close_task_change_state_to_done [easy] | Mark a project task as Done via state widget | Done | PASS | PASS | 1.0 |
| 449 | mrp.confirm_mo_produce_partial_keep_backorder [hard] | Confirm MO, produce partial qty, create production backorder | Done | PASS | PASS | 1.0 |
| 450 | purchase.set_vendor_product_code_on_po_line [medium] | Edit PO line description field | Done | PASS | PASS | 1.0 |
| 451 | hr_holidays.request_sick_leave_approve_self [hard] | Request sick leave and approve as manager | Done | PASS | FAIL | 0.0 |
| 452 | website_event.add_sponsor_to_event_publish [medium] | Add sponsor to event and publish | Done | PASS | PASS | 1.0 |
| 453 | crm.lead_set_contact_name_email_phone_save [easy] | Fill contact name/email/phone on existing lead | Done | PASS | PASS | 1.0 |
| 454 | stock.adjust_product_reorder_rule_min_max [medium] | Set reordering rule min/max on product | Done | PASS | PASS | 1.0 |
| 455 | account.reconcile_bank_statement_line_to_invoice [hard] | Reconcile a bank statement line against a posted invoice | Removed | FAIL (module unavailable) | — | — |
| 456 | sale.create_sale_quotation_from_opportunity_smart_button [medium] | Create quotation from CRM opportunity smart button | Done | PASS | PASS | 1.0 |
| 457 | stock.archive_old_product_set_inactive [easy] | Archive a product via cog Actions | Done | PASS | PASS | 1.0 |
| 458 | purchase.add_product_to_rfq_with_taxes [medium] | Add new product line to RFQ with taxes | Done | PASS | PASS | 1.0 |
| 459 | hr.create_public_holiday_calendar_entry [medium] | Add a public holiday entry for a specific date | Done | PASS | PASS | 1.0 |
| 460 | mrp.create_bom_kit_type_for_product [hard] | Create a BoM of type Kit with 2 components | Done | PASS | FAIL | 0.0 |
| 461 | website_blog.schedule_post_future_date_unpublish [hard] | Unpublish a blog post and reschedule for future | Done | PASS | FAIL | 0.0 |
| 462 | sale.cancel_confirmed_order_restore_draft [medium] | Cancel confirmed SO then set back to draft | Done | PASS | PASS | 1.0 |
| 463 | product.set_product_category_change [easy] | Change a product's category | Done | PASS | PASS | 1.0 |
| 464 | calendar.create_meeting_invite_attendees_send [medium] | Create calendar meeting with 2 attendees | Done | PASS | FAIL | 0.0 |
| 465 | hr.request_reimbursement_expense_report [hard] | Submit hr.expense + approve + post | Done | PASS | PASS | 1.0 |
| 466 | stock.set_putaway_rule_default_location [medium] | Create a putaway rule for a product | Done | PASS | PASS | 1.0 |
| 467 | account.create_vendor_bill_from_scratch_pay [hard] | Create vendor bill from scratch, confirm, then Pay in full via Register Payment wizard | Done | PASS | FAIL | 0.0 |
| 468 | sale.edit_existing_quotation_add_optional_product [medium] | Add a new product line to draft SO | Done | PASS | PASS | 1.0 |
| 469 | stock.transfer_create_internal_transfer_validate [medium] | Create + validate internal transfer | Done | PASS | PASS | 1.0 |
| 470 | crm.bulk_archive_lost_leads [medium] | Filter Lost leads + bulk archive | Done | PASS | PASS | 1.0 |
| 471 | hr_holidays.request_time_off_with_attachment [hard] | Request leave and attach justification | Done | PASS | FAIL | 0.0 |
| 472 | product.configure_stock_route_for_product [medium] | Enable MTO route on product | Done | PASS | PASS | 1.0 |
| 473 | account.post_customer_invoice_with_tax_groups [medium] | Create customer invoice with tax, post | Done | PASS | FAIL | 0.0 |
| 474 | sale.duplicate_confirmed_order_edit_customer [medium] | Duplicate confirmed SO, change customer | Done | PASS | PASS | 1.0 |
| 475 | mrp.unreserve_raw_material_on_mo [medium] | Unreserve components on confirmed MO | Done | PASS | PASS | 1.0 |
| 476 | hr.promote_employee_set_new_job_title_save [easy] | Update employee job title | Done | PASS | PASS | 1.0 |
| 477 | website_forum.upvote_question_mark_as_answer [medium] | Upvote forum question + accept answer | Done | PASS | PASS | 1.0 |
| 478 | account.refund_customer_invoice_cash_basis [hard] | Partial credit note via Reverse wizard + price_unit override on single-line invoice | Done | PASS | PASS | 1.0 |
| 479 | im_livechat.send_message_to_operator [medium] | Open live chat widget and send a message | Done | PASS | FAIL | 0.0 |
| 480 | crm.log_opportunity_note_internal [easy] | Log internal note on opportunity chatter | Done | PASS | PASS | 1.0 |
| 481 | stock.cancel_picking_abandoned [medium] | Cancel assigned picking with dialog | Done | PASS | PASS | 1.0 |
| 482 | website_blog.delete_comment_moderate [hard] | Delete a blog post comment via moderation | Done | PASS | PASS | 1.0 |
| 483 | hr_recruitment.hire_candidate_refuse_another [hard] | Hire one applicant (Contract Signed → Create Employee → set Job Title → Save), refuse another with the 'Not a fit' reason among near-duplicate distractors | Done | PASS | PASS | 1.0 |
| 484 | account.modify_account_move_line_label [medium] | Reset to draft, edit line label, repost | Done | PASS | FAIL | 0.0 |
| 485 | website_sale.add_product_review_publish [medium] | Submit a product review on storefront | Done | PASS | PASS | 1.0 |
| 486 | sale.convert_quotation_to_order_verify_invoice_status [easy] | Confirm a draft quotation to SO | Done | PASS | PASS | 1.0 |
| 487 | project.assign_task_to_user_change_deadline [medium] | Assign existing user to a task + set the deadline | Done | PASS | PASS | 1.0 |
| 488 | stock.receive_serial_tracked_product_two_serials [hard] | Receive serial-tracked product with 2 serials | Done | PASS | PASS | 1.0 |
| 489 | website_sale.configure_free_shipping_threshold [medium] | Configure delivery carrier free shipping threshold | Done | PASS | PASS | 1.0 |
| 490 | account.import_opening_balance_set_initial_equity [hard] | Post opening balance journal entry | Done | PASS | PASS | 1.0 |

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

## hr_attendance.clock_in_out_kiosk_mode

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Attendances |
| **Workflow** | Seed `Bench Worker` (PIN=1234, barcode=ATT001) and set the company to kiosk mode `manual` with PIN identification. From `/odoo/attendances`, click the sidebar **Kiosk Mode** menu (logs the admin out and redirects to the public `/hr_attendance/<token>` kiosk). In the tablet-style manual grid, click the employee card, enter `1234` on the numpad, press **OK** to check in. Return to the grid, click the employee again, enter the PIN, press **OK** to check out. |
| **Capability tested** | Public kiosk tablet UI: non-backend Owl app, employee-card selection, PIN numpad entry, two-phase clock-in/clock-out with greeting-screen auto-return in between. |
| **Notes** | `attendance_kiosk_mode` selection values in Odoo 19 are `barcode`, `barcode_manual`, `manual` — the "Manual Selection" label in Settings maps to the raw value `manual`. Barcode must be alphanumeric ≤18 chars with no hyphens (`hr.employee._verify_barcode`). The kiosk menu item issues an HTTP redirect via a server action that logs the admin session out; subsequent automated access requires navigating the public token URL directly. |

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

## point_of_sale.cash_in_sell_cash_out_close_session

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (spec) |
| **Browser-Use** | — |
| **F1** | — |
| **Notes** | Removed during oracle recheck because the current task wiring is not deterministic against the live POS UI. The seeded `opening_control` session is graded by `check.py`, but the browser UI entry points can open and close a different session for the same config, leaving the seeded session in `opening_control`. In repeated Playwright runs the UI closed a session successfully, yet `check.py` still saw the stale opening-control session with no cash-move lines. Re-enable only after the seed/check pair pins the exact session the UI operates on. |
| **Odoo modules** | Point of Sale |
| **Workflow** | Open the register `Benchmark Cash Desk`, perform Cash In `20.00`, sell one `Bench Snack Crate`, pay with `Bench Cash`, perform Cash Out `5.00`, and close the register with counted cash `27.00`. |
| **Capability tested** | Full POS kiosk cycle combining burger-menu cash moves, payment flow, and session close / cash-count reconciliation. |

---

## survey.create_certification_quiz_attempt_limit_publish

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (oracle) |
| **Browser-Use** | — |
| **F1** | — |
| **Notes** | Removed during oracle recheck because the task no longer had a verified browser-faithful oracle after JSON-RPC shortcuts were disallowed. The remaining implementation depends on the Survey question/section builder's nested one2many editing dialogs, and no passing pure-UI oracle was completed in the current environment. Re-enable once a Playwright-only oracle is validated end-to-end. |
| **Odoo modules** | Survey |
| **Workflow** | Create certification survey `Forklift Safety Certification`, configure one-page-per-section, invited-only access, scoring/certification, 80% passing score, 2-attempt limit, and add the exact two sections plus four multiple-choice questions and answers. |
| **Capability tested** | Survey builder composition across the main form, Options notebook, and nested question/answer editors. |

---

## website_blog.create_post_with_cta_seo_schedule

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (oracle) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Website Blog |
| **Workflow** | In the Blog kanban pick `Bench News`. Create a new post titled `Bench Releases Q2 Features`. In the body, insert a CTA button block with label `Learn More` whose href is `/shop`. Open the **Optimize SEO** dialog (cog Actions > Optimize SEO) and set Meta Title = `Q2 Releases - Bench` and Meta Description = `Read about our Q2 release highlights and what it means for customers.`. Set the Publishing date to `05/20/2026 09:00:00` (future). Save; leave the post unpublished (scheduled). |
| **Capability tested** | Three unrelated surfaces stacked into one medium task: drag/insert a CTA button snippet in the HTML editor, fill the Optimize SEO modal, and set a future Publishing date without toggling Publish. |
| **Notes** | Removed during oracle recheck because the old oracle still relied on JSON-RPC shortcuts and no passing pure-UI replacement was completed in the current environment. The unresolved piece is the combined backend-form + website-editor CTA insertion flow. Re-enable once a Playwright-only oracle is validated end-to-end. |

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

---

## website_forum.post_question_accept_answer

| | |
|---|---|
| **Row** | 394 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 11.5s, 7/7 edits) |
| **Browser-Use** | FAIL (F1=0.0, 1 postcondition failure, 360s timeout, 0 gave-up step) |
| **F1** | 0.0 |
| **Odoo modules** | `website_forum` (installed on demand; not in base snapshot) |
| **Workflow** | Seed installs `website_forum`, creates a public forum `Bench Q&A` (mode=`discussions`, multi-answer), a portal user `benchbot` with karma 5000, and a seeded question `How to configure Bench module?` by benchbot plus two candidate answers by benchbot (one canonical — content mentions `button_immediate_install` — and one decoy — suggests editing `odoo.conf`). Agent opens `/forum`, enters Bench Q&A, opens the question, posts their own answer in the Your Answer textarea (≥50 chars required), then clicks the circle-check Accept icon on benchbot's canonical answer. |
| **Capability tested** | Frontend forum UI (not backend form). Small SVG Accept checkmark on the left of the answer vote column (`.o_wforum_validate_toggler > i.fa-check-circle-o`) is the failure locus. Parent/child `forum.post` hierarchy (question has `parent_id=False`, answers have `parent_id=question.id`). Own-post acceptance guard: `/forum/.../toggle_correct` rejects `request.env.uid == post.create_uid.id` → the accepted answer MUST be authored by a different user than admin, hence the benchbot pre-seed. |
| **Notes** | Single-shot BU FAIL (expected). BU successfully (a) navigated `/forum` → Bench Q&A, (b) logged in, (c) posted the admin answer via Your Answer form (state-diff picked up all 6 `create` edits on the new `forum.post`), then spent ≈50 loop-detected steps hunting for the Accept checkmark on the canonical benchbot answer: tried `a[data-href*='mark_as_best']`, `.fa-check-circle`, `.o_wforum_validate`, opened the More dropdown, opened About/Help, and eventually tried to log out as admin and log back in as benchbot — none of which hit the real selector `.o_wforum_validate_toggler`. Loop-detection nudges started firing at step 15 and never recovered. Karma was NOT a blocker (admin has `is_admin()` True, bypassing all `karma_answer_accept_*` thresholds in `forum.post._compute_post_karma_rights`). BU even recognized "Mitchell Admin is not the question author" and incorrectly concluded that was the reason (it isn't; `karma_answer_accept_all` handles that). New cookbook entries for `ODOO19_PATTERNS.md § website_forum`: (1) `website_forum` NOT in base snapshot — `button_immediate_install` required in seed; (2) frontend `toggle_correct` controller blocks self-accept unconditionally (karma-independent), so any "agent posts answer + accepts" task must seed a non-admin user to author the answer to be accepted; (3) answer `content` textarea has `minlength="50"` — prompts must supply ≥50-char answer string or HTML; (4) admin is `is_admin()` in forum karma compute — no need to grant `karma_ask / karma_answer / karma_answer_accept_*` explicitly; (5) state-diff match_key for `forum.post` must include `name + parent_id + create_uid`, and seeded peer answers need DISTINCT `name` values to be individually addressable (backend `forum.post.name` on answers is normally `Re: <question title>` but the frontend only shows content, so we pin per-answer names like `Bench Bot canonical answer` / `Bench Bot decoy answer` without affecting the UX); (6) `forum.post` creation on admin-posted answers emits 6 `create` edits (name, parent_id, forum_id, is_correct=null, state=active, create_uid) — the `is_correct=null` (not `false`) is the same null-vs-false quirk already documented for `blog.post` booleans. |

---

## website_sale_wishlist.add_product_share_to_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 48.7s, 2/2 create edits matched) |
| **Browser-Use** | PASS (F1=1.0, 82.1s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Website eCommerce (`website_sale`) + Wishlist (`website_sale_wishlist`) |
| **Workflow** | Seed creates one consumable product `Bench Wishlist Item` (list_price 25.00, is_published=True, no taxes, no variants). Agent logs in as admin, navigates `/shop`, clicks the product tile to land on `/shop/bench-wishlist-item-<id>`, clicks the **heart** button (labelled *Add to wishlist*) rendered by `website_sale_wishlist.product_add_to_wishlist` inside `#product_option_block` — selector `a.o_add_wishlist_dyn`. The JS handler (`AddProductToWishlistButton.addProduct`) POSTs `/shop/wishlist/add` which calls `ProductWishlist._add_to_wishlist` and persists a `product.wishlist` row with `partner_id=admin.partner_id.id` (because the user is authenticated) + `website_id=current.id`. Agent finally navigates `/shop/wishlist` to render the wishlist page and confirm the product card is listed. |
| **Capability tested** | Frontend heart-icon click + /shop → product detail → /shop/wishlist navigation + login-driven ownership (wishlist row lands with `partner_id` set because admin is logged in; a public session would leave `partner_id=False` and the row would be orphaned to `request.session['wishlist_ids']`). check.py asserts exactly one admin-owned wishlist row referencing the seeded product, guards against partner_id=False (public-session heart click), and rejects extra admin wishlist rows (agent scatter-hearting unrelated products). |
| **Notes** | **DEVIATION from original backlog description.** The backlog row called for a "Share via email" dialog on `/shop/wishlist` emitting a `mail.mail` with recipient=`recipient@bench.test`. Pre-flight grep (`grep -rn "share" addons/website_sale_wishlist/`) returned NO hits — the module in Odoo 19 Community ships no share controller (no `/shop/wishlist/share` route), no share template in `website_sale_wishlist_template.xml`, no share JS in `static/src/interactions/`. Per instructions the task was re-scoped to wishlist-persistence verification (product.wishlist row with `partner_id` set), which IS observable at the DB level and still exercises the heart-icon frontend click + header wishlist link navigation. Calibration: EASY-leaning medium (BU PASS single-shot in 82s, F1=1.0) — the heart button has a clear text label ("Add to wishlist"), only one product is published so no disambiguation is needed, and the JS handler updates `.fa-heart-o` → `.fa-heart` + badge counter for unambiguous visual feedback. A harder version would (a) seed 3 products and require the agent to heart the *right* one while ignoring distractors, (b) require an unpublished/archived product that the agent must republish first before the heart shows up, or (c) re-target the task on `website_sale_comparison` (compare list) where the add-to-compare button is adjacent. Kept as medium/tier:2 per spec. New cookbook quirks added to ODOO19_PATTERNS.md below. |

---

## stock.transfer_reserved_to_ready_partial_backorder

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 42.2s) |
| **Browser-Use** | FAIL (F1=0.0, 189.9s single-shot; BU opened picking → Check Availability → opened Detailed Ops popup → typed `7` into the Quantity cell + clicked Save on the popup, BUT the cell edit did not persist server-side. When BU clicked Validate afterward the picking committed the full reserved qty=10 and went state=done WITHOUT raising the Create Backorder dialog, so no backorder picking was created and move.quantity stayed 10.0). |
| **F1** | 0.0 |
| **Odoo modules** | Inventory (stock) |
| **Workflow** | Seed creates customer `Bench Partial Cust`, storable product `Bench Partial Item` with 10 units on-hand at WH/Stock, and a confirmed (NOT yet reserved) outgoing picking `D-BENCH-PARTIAL-001` for 10 units. Agent: Inventory → Delivery Orders list → open `D-BENCH-PARTIAL-001` → header **Check Availability** (state → assigned, Quantity reserved 10) → click the **Details** (`action_show_details`) icon on the single move line → in the Detailed Operations popup, change the **Quantity** cell from 10 to 7 → click **Save** in the popup footer → on the picking form, click **Validate** → on the "Create Backorder?" dialog, click **Create Backorder** (primary, left). Original picking ends state=done, move.quantity=7; a backorder picking is auto-created with product_uom_qty=3 and state=assigned. |
| **Capability tested** | Hard composite: (a) header **Check Availability** is required before the cell-edit (skipping it forces an Immediate Transfer wizard, not the Create Backorder dialog); (b) **Detailed Operations popup** — the `action_show_details` button opens a secondary `stock.move` form dialog with an inline-editable move_line_ids list where the `quantity` cell must be edited, tab-committed, AND the popup Save button clicked for the change to persist; (c) **Create Backorder** (primary) vs **No Backorder** (secondary) radio-style dialog on Validate. |
| **Notes** | Calibration HIT. BU thought it did everything right ("I edited the quantity to 7.00 in the Detailed Operations popup and saved it") but the persistence step failed and Validate promoted the full qty=10 to Done, silently bypassing the backorder dialog. This matches the ODOO19_PATTERNS note: "`stock.picking` line editing: Done qty is an inline-cell edit — notoriously hard to persist via browser UI (cell doesn't always save on blur)". Key seed detail: must grant admin `stock.group_stock_multi_locations` so `show_details_visible` is True on the single move line (otherwise the Details button is hidden when there is exactly one move_line). Seed must also NOT call `action_assign()` (nor allow at_confirm auto-reservation), otherwise the agent skips Check Availability and the task collapses to a plain partial-validate. Oracle's popup-Save locator required Escape as a fallback — the technical modal's footer Save button (`.modal-footer button:has-text('Save & Close')` or `.o_form_button_save` inside the dialog) intercepts pointer events on the outer form's save button, so the oracle keys the popup-close via footer button OR Escape. expected_state.json captures state confirmed→done on original + create-row for the backorder (entity_key tuple uses pinned picking.name `D-BENCH-PARTIAL-001` so `backorder_id` normalizes deterministically to that display-name). |

---

## stock_barcode.receive_via_barcode_scan_validate

| Field | Value |
|---|---|
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Barcode (Enterprise `stock_barcode`) + Inventory |
| **Workflow** | Open `/odoo/barcode` → Operations → Receipts → open receipt `R-BENCH-BC-001` → scan `BENCH-A-001` three times (or tap `+`), scan `BENCH-B-002` three times, click Validate. Final state: picking state=done, both moves quantity=3, no backorder. |
| **Capability tested** | Barcode tablet UI + scan input (or click-add fallback) + Validate tile. Hard pattern: unique client-action UI, not the standard list/form backend. |
| **Notes** | Blocked — the `stock_barcode` addon is **Enterprise-only** and not vendored in this Odoo 19 Community checkout. Verified: `ls addons/stock_barcode` returns "No such file or directory"; `grep -rn "stock_barcode" addons/` returns only i18n po strings and one `module_stock_barcode = fields.Boolean("Barcode Scanner")` upgrade_boolean on `addons/stock/models/res_config_settings.py:29` (ticking it in the UI would ask Odoo to install the absent module). No `/odoo/barcode` controller, no `stock_barcode_action_main_menu` client action, no `BarcodePickingModel` / `BarcodeMainMenu` JS classes. Task skeleton (seed/oracle/check) is committed with clear BLOCKED guards that short-circuit with diagnostic errors instead of silently passing. Follows the same precedent as `barcodes.receive_product_via_scan_validate` (removed for identical reason), rows 350 (appointment), 351 (helpdesk), 352 (marketing_automation), and 387 (hr_skills_survey) — all Removed for Enterprise-only feature unavailability. Re-enable once enterprise `stock_barcode` is vendored into `addons/`. See the task's RESULT.md for full evidence and re-enabling steps. |

---

## account.credit_note_partial_refund_post

| | |
|---|---|
| **Row** | 399 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 34.5s, 6/6 edits) |
| **Browser-Use** | FAIL (F1=0.0, 1 postcondition failure, 110.1s, single-shot) |
| **F1** | 0.0 |
| **Odoo modules** | `account` (customer invoices + `account.move.reversal` wizard) |
| **Workflow** | Seed posts `INV/BENCH/001` for partner `Bench AR Co`: Bench Item A qty=4 @100 = 400.00, Bench Item B qty=2 @50 = 100.00, total 500.00 (both products `consu`, taxes cleared with `[(5, 0, 0)]`). Agent opens Accounting → Customers → Invoices, clicks `INV/BENCH/001`, clicks the statusbar **Credit Note** button (which opens the `account.move.reversal` wizard), fills `reason="Wrong qty"`, leaves the Reversal date at today's default, then clicks **Reverse** (primary `btn-primary[name='refund_moves']` in the wizard footer — NOT the secondary **Reverse and Create Invoice** which is `name='modify_moves'`). This creates a draft `out_refund` credit note prefilled with both source lines. The agent must then (a) change Bench Item A `quantity` 4→2 on the draft and (b) delete the Bench Item B row via the row trash icon (`.o_list_record_remove`), then header-post via **Confirm**. Postconditions: source invoice `state='posted'` untouched; credit note `move_type='out_refund'`, `state='posted'`, `reversed_entry_id=source.id`, exactly 1 product line (Item A, qty=2, price_unit=100), `amount_total=200.0`, `ref` contains `"Wrong qty"` (wizard-built `"Reversal of: INV/2026/00001, Wrong qty"`). |
| **Capability tested** | Header-button wizard opening on a posted invoice + **post-wizard line trimming** on the generated draft (both qty edit on one row AND full-row deletion on another) BEFORE the header Confirm. The reversal wizard footer has two buttons — `refund_moves` (Reverse) and `modify_moves` (Reverse and Create Invoice) — the agent MUST choose the first; `modify_moves` creates a new draft invoice (not a credit note to post) and is forbidden in trace_spec. |
| **Notes** | Single-shot BU FAIL as expected for hard tier. BU successfully: logged in, found the invoice via Sales (lucky — the seed ref `INV/BENCH/001` is the Char `ref` field, while the auto-generated `name` is `INV/2026/00001`; BU matched on partner + total 500.00), opened the Credit Note wizard, typed `Wrong qty`, clicked the correct `refund_moves` **Reverse** button, then on the draft clicked Item A qty 4.00 cell — `[BrowserSession] ⚠️ Text field clearing failed, typing may append to existing text` fired on every attempt (3 retries, each typed "2" which appended as "42" or wrote into a phantom placeholder line). BU then deleted Item B correctly on the FIRST try (Delete row button). Final outcome: credit note posted with `amount_total=200` visible in UI (BU reported "total is $200.00, status Posted"), BUT check.py saw `2` product lines via `filtered(display_type=='product')` — the phantom placeholder row that BU's failed qty edits created persisted through the post, and `display_type='product'` applies to ALL editable rows including the blank one it typed into. State-diff on `account.move` scored 6/6 matches (all refund_moves create edits and source.payment_state='partial' set edit) but `strict_success=False` → `state_diff_f1=0.0` because of the one postcondition failure. Calibration: hard-tier genuine FAIL pattern (phantom line caused by BU's broken clear-then-type behavior). F1 estimate: **~20-30% BU pass rate** (most runs will hit the same clear-fail loop; some runs may succeed if BU's first qty type lands cleanly on 2.00). New cookbook entries appended to `ODOO19_PATTERNS.md § account.move.reversal wizard`: (1) the `account.move.reversal` wizard in Odoo 19 has **NO `refund_method` radio** (that 3-option radio from Odoo ≤16 was removed in 17+) — footer has exactly 2 buttons, `refund_moves` (Reverse, primary) and `modify_moves` (Reverse and Create Invoice, secondary); prompts must NOT refer to a radio. (2) The reversal wizard button is labeled **"Credit Note"** on the invoice statusbar (`button[name='action_reverse']`), NOT "Reverse" — the footer button inside the wizard is labeled "Reverse". (3) `account.move.reversal._prepare_default_reversal` builds the credit note ref as `"Reversal of: <source.name>, <reason>"` using the source's auto-generated `name` (e.g., `INV/2026/00001`), so expected_state.json entity_keys must use that exact string — NOT the seed's `ref` Char. (4) The reversal date defaults to today via `fields.Date.context_today`; if set in the **future**, `auto_post='at_date'` and the header Confirm button is hidden — tasks leaving the default avoid this trap but MUST NOT prompt for future dates. (5) `display_type='product'` on `account.move.line` includes **phantom/placeholder rows** that BU's broken clear-then-type loop creates (qty=0, price_unit=0, product_id unset but `display_type='product'` inherited from the kanban list context). check.py must either filter by `product_id` truthiness or use `len(product_lines)==1` as a trap to catch phantom lines — here we rely on the count trap. (6) `account.move.line.unlink` happens via the row trash icon (`td.o_list_record_remove button`) — BU handles this correctly. |

---

## website.submit_contact_form_create_crm_lead

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 6.1s, 6/6 create edits matched) |
| **Browser-Use** | PASS (F1=1.0, 36.8s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Website (`website`) + CRM (`crm`) + auto-installed `website_crm` |
| **Workflow** | Seed creates a published page `/contactus-bench` whose `<form>` snippet carries `data-model_name="crm.lead"` and `s_website_form_no_recaptcha`, with six `<input>` / `<textarea>` children wired by `name=` attribute to the crm.lead fields whitelisted by `website_crm/data/ir_model_data.xml` (`contact_name`, `phone`, `email_from`, `partner_name`, `name`, `description`). Agent opens `/contactus-bench` as a frontend visitor (no login required — form is public), fills each field with the exact seeded values, clicks Submit, and waits for the `/contactus-thank-you` redirect. The `website.controllers.form.WebsiteForm._handle_website_form` hook + the `website_crm` override inject `company_id`, `lang_id`, and reformat the phone via `phone_validation`, then `insert_record` creates the `crm.lead` row. |
| **Capability tested** | End-to-end frontend-form → backend-record pipeline: Owl `Interaction` class on `.s_website_form` intercepts `.s_website_form_send` clicks, POSTs a FormData bundle to `/website/form/crm.lead`, the server deserializes inputs via model whitelist, and a crm.lead is persisted. Unlike `website.create_contact_form_with_custom_field` (which drives the website *builder* inside an iframe to ADD a Selection field), this task exercises the public-visitor form submission flow. |
| **Notes** | **Calibrated easier than anticipated.** BU passed single-shot in 36.8s; the frontend form has clear label text for each input and Submit button is unambiguous. The website_crm routing caused the created lead to land with `type='opportunity'` (the crm.lead default) rather than `type='lead'` — expected_state.json reflects that. Note: the seeded page ships with class `s_website_form_no_recaptcha` on the `<form>`, which the public `Form.willStart()` hook checks to skip `recaptcha.loadLibs()` — this was added because in base snapshots where `ir.config_parameter.recaptcha_*_key` is set, the loader would block form submission with a token error. expected_state.json uses `op: "create"` for each tracked field (contact_name, email_from, partner_name, name, phone, type) with `entity_key = [email_from, contact_name]` as the composite match key. A harder variant would (a) leave the default /contactus page intact and require the agent to switch the form to "Create an Opportunity" in the website builder first, (b) seed a dropdown "Inquiry Type" the agent must select before Submit, or (c) require two submissions routing to different sales teams. Kept as medium/tier:2. New cookbook quirks added to ODOO19_PATTERNS.md below. |

---

## account_followup.send_reminder_level_two_customers

| Field | Value |
|---|---|
| **Row** | 404 |
| **Difficulty** | hard |
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Accounting Follow-up (Enterprise-only `account_followup`) |
| **Workflow** | Seed 3 posted customer invoices `OV/BENCH/001..003` for partner `Bench Overdue Co` with `invoice_date_due = today - 45d`. Agent: Accounting → Customers → **Follow-up Reports** (or Customer Statement), opens `Bench Overdue Co`'s follow-up card, clicks header **Send Email** (default level-2 reminder template). Verify ≥1 `mail.mail` / `mail.message` logged on the partner referencing the three invoice names. Final state: all three invoices remain `state='posted'` and `payment_state='not_paid'`; partner's `followup_status` advances; at least one chatter message cites all three invoice names. |
| **Capability tested** | Enterprise Follow-up Reports tablet UI: (a) per-partner aggregation of overdue `account.move` rows by `invoice_date_due`, (b) per-level email template + default text customization on `account_followup.followup.line`, (c) header `Send Email` action that renders and queues a `mail.mail` with invoice PDF attachments, (d) chatter audit trail on `res.partner` capturing the sent reminder. Hard pattern: cross-module closed loop (account → account_followup → mail) with level-escalation side-effects. |
| **Notes** | Blocked — `account_followup` is **Enterprise-only** and NOT vendored in this Odoo 19 Community checkout. Verified: `ls addons/account_followup/` → "No such file or directory"; `grep -rn "account_followup" addons/` → **zero** matches (no model, view, controller, or even i18n stub). The only adjacent Community artefact is the `send_invoices_followups` upgrade_boolean on Accounting Settings at `addons/account/views/res_config_settings_views.xml:115`, which installs the orthogonal `snailmail_account` module (physical-mail invoicing), not the follow-up reminder workflow. No `/odoo/action-account_followup.*` routes, no `account_followup.followup.report` client action, no `account_followup.followup.line` levels, no `res.partner.followup_status` / `followup_line_id` / `followup_next_action_date` fields. Task skeleton (seed/oracle/check/cleanup) ships with BLOCKED guards that short-circuit with diagnostic errors instead of silently passing. Follows the same precedent as rows 350 (appointment), 351 (helpdesk), 352 (marketing_automation), 387 (hr_skills_survey), 401 (stock_barcode), and `barcodes.receive_product_via_scan_validate` — all Removed for Enterprise-only feature unavailability. Re-enable once enterprise `account_followup` is vendored into `addons/`. See the task's RESULT.md for full evidence and re-enabling steps. |

---

## hr_holidays.request_allocation_approve_self_book_day_off

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 12.5s, 6/6 create edits matched) |
| **Browser-Use** | PASS (F1=1.0, 196.3s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | HR Holidays (Time Off) |
| **Workflow** | Two-phase cross-flow on `/odoo/time-off-approval`. Seed creates (a) a `Bench Bonus Days` leave type with `requires_allocation='yes'` + `allocation_validation_type='hr'` + `leave_validation_type='hr'` + `request_unit='day'`, and (b) a `Bench Worker` employee whose `parent_id` points to `admin.employee_id` and whose `leave_manager_id` is admin. Phase 1: Management → Allocations → New, employee=Bench Worker, type=Bench Bonus Days, number_of_days=5, desc=`Q2 bonus`, Save → Approve so the allocation moves to `state='validate'`. Phase 2: Management → Time Off (or New Request) → New, same employee + type, desc=`Bench day off`, request_date_from=request_date_to=`2026-05-15`, Save → Approve so the leave moves to `state='validate'`. Server-side constraint: `hr.leave`'s virtual-remaining check refuses to validate if the matching allocation is not in `validate` — ordering is load-bearing. |
| **Capability tested** | Sequential two-record creation workflow with an ordering constraint. Each record requires its own Save-then-Approve (no shortcut). BU must not (a) skip the allocation entirely and start with the leave (which fails validate with "number of remaining time off is not sufficient"), nor (b) forget the second Approve click on either record and leave one in `confirm`. No wizard, no modal radio — the difficulty is pure ordering + two discrete state transitions. |
| **Notes** | **Calibrated easier than intended — BU passed single-shot in 196s with F1=1.0, all 6 create edits matched, both required ops (`hr.leave.action_approve` + `hr.leave.allocation.action_approve`) hit, 0 forbidden writes.** Task spec asked for `allocation_validation_type='officer'` but that value does not exist on `hr.leave.type.allocation_validation_type` in Odoo 19 (valid selection: `no_validation` / `manager` / `both` / `hr`); used `'hr'` which preserves the Confirm → Approve lifecycle described in the prompt. `requires_allocation` is a Selection (`'yes'`/`'no'`) NOT a Boolean in Odoo 19 — seeding with `True` raises. Suggestions to harden into a genuine tier-3: (1) add a distractor allocation already in `validate` for an unrelated employee that must stay untouched; (2) require the leave to use `request_unit='half_day'` so the agent must pick a non-default half-day radio in the form; (3) chain a refuse-then-approve trap where the first allocation attempt must be refused for wrong quantity and a replacement created. Cookbook note appended to `ODOO19_PATTERNS.md § hr.leave.type / hr.leave.allocation — Odoo 19 allocation validation lifecycle`. |

---

## hr_holidays.request_sick_leave_approve_self

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 14.9s, 4/4 create edits matched, RequiredOpRecall=1.0) |
| **Browser-Use** | FAIL (F1=0.0, 420s timeout, 3 postcondition failures, RequiredOpRecall=0.0) |
| **F1** | 0.0 |
| **Odoo modules** | HR Holidays (Time Off) |
| **Workflow** | Seed creates a `Sick Leave` leave type with `requires_allocation=False` + `leave_validation_type='hr'` + `time_type='leave'` + `request_unit='day'`, and a `Bench Sick Employee` user + employee reporting to admin (`parent_id=admin_emp.id`, `leave_manager_id=admin.id`). Admin is granted `hr_holidays.group_hr_holidays_user/manager/responsible`. Agent starts on `/odoo/time-off`, clicks New Request / New, fills Time Off Type=Sick Leave, Employee=Bench Sick Employee, start=2026-05-11 (Mon) → end=2026-05-12 (Tue), description=`Sick leave benchmark`, saves — landing in `state='confirm'` (To Approve). Agent then navigates to `/odoo/time-off-approval` (Management / Approvals), locates the pending record, and clicks Approve — flipping the record to `state='validate'` with `number_of_days=2.0`. |
| **Capability tested** | Two-step role lifecycle — employee-side submit then manager-side approve — spanning two distinct Time Off views, combined with datetime widget entry for date_from/date_to. There is NO `action_confirm` on `hr.leave` in Odoo 19 (state defaults to `'confirm'` on create) so the oracle and the agent both go straight from create to `action_approve`. `leave_validation_type='hr'` forces an explicit Approve click from an HR-group user; admin has the group, so there is no validate1 intermediate. |
| **Notes** | **Calibrated as intended — BU cleanly failed single-shot (F1=0.0, 420s timeout, RequiredOpRecall=0.0).** BU exhausted the full 420s time limit stuck on the new-request form, never advancing past the today-date default (2026-04-19) in the start/end fields and never reaching the Approvals dashboard. Final state stayed `state='confirm'` with `number_of_days=0.0` (defaulted to today-to-today). Gotchas: (1) In this Odoo 19 build `hr.leave.type.requires_allocation` is declared `fields.Boolean` (`hr_holidays/models/hr_leave_type.py:88`), contradicting the `"yes"/"no"` Selection note in `hr_holidays.request_allocation_approve_self_book_day_off`'s cookbook — seed with `False`/`True`. (2) `number_of_days` is working-day based, so a Sun→Mon range yields 1 day; we use Mon→Tue (2026-05-11 → 2026-05-12) for a clean 2-day assert. (3) `state_spec.yaml` matches `hr.leave` by `[employee_id, holiday_status_id]` (both Many2one display names) rather than by `name` — the agent's description is not load-bearing. (4) New-record diff ops are all `op: "create"`; never mix `set`. |

---

## hr_holidays.request_time_off_with_attachment

| Field | Value |
|---|---|
| **Row** | 471 |
| **Difficulty** | hard |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 28.0s, 4/4 create edits matched, RequiredOpRecall=1.0, WritePrecision=1.0, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 355.1s single-shot, 5 postcondition failures, 3 Paid Leave records created instead of 1, wrong dates 2026-07-10/11, no ir.attachment linked to any leave, 1 forbidden `hr.leave.action_refuse` fired) |
| **F1** | 0.0 |
| **Odoo modules** | HR Holidays (Time Off) + mail chatter file upload (`ir.attachment` via the chatter paperclip, hidden `<input type=file>`) |
| **Workflow** | Seed creates a `Paid Leave` hr.leave.type (`requires_allocation=False`, `leave_validation_type='hr'`, `request_unit='day'`, `time_type='leave'`), grants admin the HR Holidays groups, ensures admin has an hr.employee, wipes prior `Medical appointment` leaves + BENCH-JUST.pdf attachments on hr.leave, and writes a minimal valid PDF (322 bytes) to `seed_artifacts/BENCH-JUST.pdf`. Agent on `/odoo/time-off` clicks New Request / New, fills Time Off Type=`Paid Leave`, dates `2026-07-01` (Wed) → `2026-07-02` (Thu) via the date widget, description=`Medical appointment`, Save so the leave lands in `state='confirm'` (To Approve). Agent then opens the saved form's chatter paperclip and uploads `BENCH-JUST.pdf` — resulting in an `ir.attachment(name='BENCH-JUST.pdf', res_model='hr.leave', res_id=<leave_id>)` with non-empty bytes. Oracle bypasses the UI with RPC to guarantee deterministic PASS. |
| **Capability tested** | File upload via the chatter paperclip on an `hr.leave` form (hidden `<input type=file>` behind `button[aria-label='Attach files']`) combined with two Odoo 19 date-widget entries (start + end) and a non-default Time Off Type selection (`Paid Leave` must be chosen explicitly, not the auto-selected first type in the dropdown). The paperclip pattern is a known-hard anchor — the benchmark runner does NOT pass `available_file_paths` to browser-use, so any attempt to call `set_input_files` through BU's file-upload bridge is blocked; BU also cannot drive a native OS file-picker dialog. The leave must stay in `confirm` (prompt explicitly forbids Approve), so agents that click Approve after saving corrupt the state. |
| **Notes** | **Calibrated as intended — BU single-shot FAIL (F1=0.0, 5 postcondition failures: wrong dates, 3 leaves created instead of 1, no ir.attachment linked).** BU got confused by repeated save/refuse cycles: (a) it created 3 `Paid Leave` records (one refused, one current, one spurious — triggered our `forbidden_ops: hr.leave.action_refuse` gate), (b) it picked dates `2026-07-10`/`2026-07-11` instead of `2026-07-01`/`2026-07-02` despite the exact dates in the prompt, (c) the `number_of_days` on the surviving leaves ended up 1.0 instead of 2.0, (d) **no chatter attachment ever appeared on any of the three leaves** — confirming the hidden-input-file barrier. Distinct from row 402 (`request_allocation_approve_self_book_day_off`, which tests sequential allocation→leave without file upload) and row 451 (`request_sick_leave_approve_self`, which tests a two-role submit+approve lifecycle without attachment). Shares the file-upload anchor with `hr_holidays.request_leave_with_attachment` (medium variant using `Annual Leave` + allocation + different dates/filename) but bumps to tier 3 by (1) seeding a type with `requires_allocation=False` so agents can't blame an allocation lookup, (2) requiring the exact filename `BENCH-JUST.pdf` (non-obvious — differs from the medium sibling's `leave_justification.pdf`), (3) a different description (`Medical appointment`) and different dates (`2026-07-01`/`2026-07-02`). Gotchas mirror row 451: `requires_allocation` is a `fields.Boolean` (not Selection), `hr.leave` has no `action_confirm` (state defaults to `confirm` on create), `number_of_days` is working-day based (Wed+Thu = 2 working days), and the state-diff ops on the newly-created leave are all `op: "create"` (never mix `set`). `expected_state.json` matches on `[employee_id, holiday_status_id]` = `["Mitchell Admin", "Paid Leave"]` (admin's display name in the base snapshot is `Mitchell Admin`). |

---

## stock.adjust_inventory_count_apply_moves

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.3s, 8/8 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | FAIL (F1=0.0, 360.0s single-shot wall-clock cap hit, gave_up=True, 4 postcondition failures) |
| **F1** | 0.0 |
| **Odoo modules** | Inventory (`stock`) — Physical Inventory list view + `stock.quant.action_apply_all` + `stock.quant.action_apply_inventory` + follow-up `Inventory Adjustment Reference` dialog |
| **Workflow** | Seed creates 2 storable products (`Bench Prod A` with on-hand 20, `Bench Prod B` with on-hand 15) at `WH/Stock` via `env["stock.quant"]._update_available_quantity`. Agent opens **Inventory → Operations → Physical Inventory**, clicks the Counted Quantity cell on the Bench Prod A row and types `18`, presses Tab to commit, does the same on Bench Prod B with `16`, then clicks **Apply All** in the list header. A `Apply / Update Quantities` confirmation dialog appears (single-row "Inventory Adjustment Reference" Char prompt); agent clicks the primary Apply button. Odoo posts the adjustments: `stock.quant.quantity` on the two WH/Stock rows becomes 18 and 16, and two `stock.move` records with `is_inventory=True, state=done` are created (delta -2 for A, +1 for B), which generate mirror `stock.quant` rows at the virtual `Inventory adjustment` location. |
| **Capability tested** | Inline editable tree-cell commit on the Physical Inventory list (field `inventory_quantity`) for 2 specific rows, followed by a modal-dialog confirmation and a sanity check that `stock.quant.quantity` and `stock.move.is_inventory` have both been written. BU typically (a) opens the form view of a single quant instead of editing the list cell, (b) types into the cell but never commits (no Tab / Enter / blur), (c) edits On Hand instead of Counted Quantity, or (d) fills both cells correctly but clicks Save without ever clicking Apply — leaving `inventory_quantity_set=True` but `quantity` unchanged. |
| **Notes** | Clean single-shot FAIL. BU exhausted the 360s cap (`gave_up=True`), never wrote the Counted Quantity cells. Check.py gates on BOTH `stock.quant.quantity` matching the target AND a done `stock.move` with `is_inventory=True` whose net signed delta equals the expected adjustment (so a BU run that updates quantity directly via `stock.quant.write` without going through Apply would fail the second gate). expected_state.json tracks 8 atomic edits: 2 `set` on the WH/Stock quants (18, 16) + 6 `create` edits on the mirror `Inventory adjustment` quants (3 per product: product_id, location_id, quantity — `+2` for A since WH/Stock lost 2 to the virtual location, `-1` for B since WH/Stock gained 1 from it). state_spec.yaml uses `match_key=[product_id, location_id]` on `stock.quant`, which normalizes to composite display names (e.g. `["Bench Prod A", "WH/Stock"]` and `["Bench Prod A", "Inventory adjustment"]`). Sibling task `stock.adjust_inventory_quantities` (row 315 / hard) targets 3 products with distractor rows; this task is the simpler 2-product medium variant and adds the stock.move / is_inventory postcondition gate that the hard variant lacks. |

---

## hr_recruitment.create_applicant_kanban_move_to_offer

| Field | Value |
|---|---|
| **Row** | 403 |
| **Difficulty** | medium |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 36.1s, 6/6 create edits matched) |
| **Browser-Use** | PASS (F1=1.0, 76.6s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment (`hr_recruitment`) |
| **Workflow** | Seed creates an `hr.job` named `Bench Senior Dev` (department `Bench Engineering`) plus four job-scoped `hr.recruitment.stage` records named **Initial Qualification / Qualified / Contract Proposal / Contract Signed** (sequences 10/20/30/40) — the canonical Odoo 19 demo stages are `New / Qualification / First Interview / Second Interview / Contract Proposal / Contract Signed`, so these are custom names pinned via `hr.recruitment.stage.job_ids`. No applicants are pre-created. Agent opens `/odoo/recruitment`, clicks the **Bench Senior Dev** kanban card (job action, not the 3-dots menu), lands on the Applications kanban grouped by `stage_id`, clicks the `+` on the **Initial Qualification** column, types `Alice Applicant`, confirms the quick-create, then reopens the new card's full form to set `email_from=alice@bench.test` + `partner_phone=+15555555555`, saves, and advances the form status bar twice (`Initial Qualification → Qualified → Contract Proposal`). |
| **Capability tested** | Per-column kanban quick-create (`button.o_kanban_quick_add` inside `.o_kanban_header`, then the `hr_recruitment.quick_create_applicant_form` with only `partner_name`+`job_id`), reopening the newly-created card to reach the full applicant form (since the quick-create lacks `email_from` / `partner_phone`), exact-string field fills on `email_from` + `partner_phone`, and form status-bar stage advancement via the `rotting_statusbar_duration` widget with `clickable:'1'`. Tests the "create-from-scratch-then-advance-state" pattern without requiring drag-and-drop. |
| **Notes** | **Calibrated easier.** BU passed single-shot in 76.6s with F1=1.0, all 6 create edits matched (partner_name, email_from, partner_phone, stage_id→Contract Proposal, job_id→Bench Senior Dev, active). Oracle ran in 36.1s. Task sits on the easy side of the medium band — linear 3-step flow (quick-create, open form, status-bar-click×2) with no wizard modal and no radio-disambiguation. To harden into a genuine tier-3 drag-and-drop task, either (a) force kanban drag by hiding the status bar via a custom view, (b) require a `Send Email` wizard on arrival at Contract Proposal that must carry an exact subject/body, or (c) add distractor applicants in adjacent stages so the agent must drag the correct card. Seed quirks: canonical stage names collide with two demo records (`Contract Proposal`, `Contract Signed`) — pinning via `job_ids` disambiguates. `hr.recruitment.stage.job_ids=[]` means "global/shared" which would surface extra columns in the Applications kanban, so the seed uses `[(6, 0, [job.id])]`. Cookbook quirks added to `ODOO19_PATTERNS.md § hr_recruitment — Applications kanban entry + quick-create fields`. |

---

## event.create_event_add_question_publish

| | |
|---|---|
| **Row** | 406 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 17.5s, 11/11 edits matched via JSON-RPC bypass) |
| **Browser-Use** | PASS (F1=1.0, 141.8s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | `event` + on-demand `website_event` |
| **Workflow** | Seed cleans up prior runs and installs `website_event` (not in base snapshot). Agent: Events → **New** → fill `Event Name = Bench 2026 Conference`, date start `07/15/2026 09:00:00`, date end `07/16/2026 17:00:00`. Opens the **Questions** tab (the notebook page below the event header fields). Clicks **Add a line** on the `question_ids` m2m list, which opens a `SelectCreate` dialog. Clicks **New** inside that dialog to open the `event.question` form (primary-mode `event_question_view_list_add` inherits from `event_question_view_list`, but **New** surfaces `event_question_view_form`). Fills Q1 = `Company` / `question_type='text_box'` (radio "Text Input") / `is_mandatory_answer=True` / `once_per_order` left unchecked. Clicks **Save & New** to chain to Q2. Fills Q2 = `Experience Level` / `question_type='simple_choice'` (radio "Selection") / `is_mandatory_answer=True` / `once_per_order` unchecked, then the **Answers** nested notebook tab surfaces (visible because `question_type == 'simple_choice'`) where three answer rows `Beginner`/`Intermediate`/`Expert` are added via the inline-editable one2many. Clicks **Save & Close**. Saves the event. Publishes via the frontend preview: clicks the **Unpublished** `website_redirect_button` indicator (navigates to `/event/<slug>`), then flips the Owl systray **Unpublished → Published** toggle. |
| **Capability tested** | Create-from-scratch event + Questions tab `question_ids` m2m-with-create dialog + nested simple_choice `answer_ids` one2many + systray publish via Owl iframe. Three proven-hard patterns composed. |
| **Notes** | **Calibration MISS — BU passed single-shot cleanly** (19 steps, 141.8s, F1=1.0, 0 postcondition failures). BU navigated the Questions tab, clicked Add a line → New, used **Save & New** to chain-create the two questions, added 3 nested answer rows on Q2 via **Add a line** inside the simple_choice notebook, saved, then correctly clicked the website_redirect_button → Owl systray toggle to publish. The task *does* exercise the documented-hard UI patterns (`SelectCreate` dialog, nested o2m within a o2m-create-dialog, Owl iframe systray publish), but the Odoo 19 event form is clean enough that BU's LLM navigates it with the form-label text alone. Oracle uses JSON-RPC bypass for determinism (same pattern as `website_event.publish_event_register_via_portal`): creates both questions + answers via `event.question.create`, creates the event, appends the new questions via `write({question_ids:[[4,id]]})`, and calls `event.event.website_publish_button()` + defensive `write({is_published:true})`. expected_state.json captures 11 atomic create edits: 3 on event.event (name, is_published, website_published) + 4 per question (title, question_type, is_mandatory_answer, **once_per_order=null** — the False boolean normalizes to null in the diff engine, required to get F1=1.0). A harder variant would (a) mix general_question_ids (once_per_order=True) with specific_question_ids (once_per_order=False) requiring two separate visits to the tab, (b) require seat_limit + seats_max on the event so `_check_seats_availability` fires on save, or (c) chain an event.type preset that wipes default questions so the agent must re-add them. **Primary_track=false** given the BU pass. Task kept as hard/tier:3 because the composite UI flow is still non-trivial; it joins the collection of hard-tier tasks BU happens to solve on its first try (like `website_event.publish_event_register_via_portal` row 354). |

---

## hr_expense.scan_submit_expense_from_mobile_portal

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 30.3s) |
| **Browser-Use** | PASS (F1=1.0, 69.4s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Expenses |
| **Workflow** | Seed creates/updates a `product.template` called `Travel - Taxi` (type=service, can_be_expensed=True, list_price=25.00, **standard_price=0.0**) and ensures admin has the three expense groups + an `hr.employee` record. Agent: Expenses → My Expenses → **New**, picks product `Travel - Taxi`, fills description `Airport taxi`, types `45.00` into the Total input (which is `total_amount_currency` since `product_has_cost=False`), sets date to `2026-04-19`, Saves, then clicks the statusbar **Create Report** / **Submit to Manager** so the expense leaves `draft`. End state: single `hr.expense` with `name='Airport taxi'`, `total_amount=45.0`, `product_id=Travel - Taxi`, `state='approved'` (admin is both owner and approver so it auto-validates through the team_approver group). |
| **Capability tested** | "Log an expense from scratch and submit" — from-scratch record creation with an exact text description, exact monetary override, and a statusbar button sequence that in Odoo 19 compresses the legacy Save → Submit-to-Manager flow into a single Create Report action. |
| **Notes** | **Cookbook quirk (NEW): hr.expense `total_amount_currency` is READONLY whenever `product_has_cost == True`.** `product_has_cost = not company_currency.is_zero(product.standard_price)`. When `standard_price > 0`, the form switches to the "product-priced" layout where Total is computed from `quantity * price_unit` — the user cannot type a number directly into Total. Initial seed used `standard_price=25.00` which produced a `total_amount=25` value the oracle could not override (verified in two runs: `web_save` payload carried `total_amount: 25, total_amount_currency: 25` regardless of selector tried). Fix: seed `standard_price=0.0` (keep `list_price=25.00` as the visible reference), which flips `product_has_cost=False` and exposes the editable `total_amount_currency` input. Prompt updated to drop the "override default 25.00" phrasing since there is no live default. BU solved it single-shot in 69.4s — calibration slots as easy-medium (appropriate for tier 2). |

---

## mail.send_email_with_attachment_log_as_note

| Field | Value |
|---|---|
| **Row** | 408 |
| **Difficulty** | medium |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 18.2s, 0 atomic edits / 0 postcondition failures) |
| **Browser-Use** | FAIL (F1=0.0, 88.4s single-shot, 1 postcondition failure — file upload blocked by BU `available_file_paths` sandbox) |
| **F1** | 0.0 |
| **Odoo modules** | Mail (chatter composer + `mail.message.subtype_id` mt_comment vs mt_note) + Contacts (`res.partner`) |
| **Workflow** | Seed creates partner `Bench Chatter Co` (email `info@benchchatter.test`, is_company=True) and drops a `seed_artifacts/welcome_kit.txt` file on disk. Agent opens /odoo/contacts, clicks the partner row, scrolls to the chatter, clicks the **Send message** tab (NOT the default Log note tab), types `Attached our welcome kit` in the composer, clicks the paperclip (aria-label "Attach files") which triggers a hidden `<input type="file" class="o_input_file d-none">`, selects `welcome_kit.txt`, waits for the attachment chip, and clicks **Send**. Oracle short-circuits the UI by directly calling `res.partner.message_post` via call_kw with `body='Attached our welcome kit'`, `message_type='comment'`, `subtype_xmlid='mail.mt_comment'`, `attachment_ids=[<id>]` where the attachment was first created as `ir.attachment(res_model='mail.compose.message', res_id=0)` and then migrated onto the post by `_process_attachments_for_post`. |
| **Capability tested** | Two orthogonal BU failure modes: (1) the chatter opens on **Log note** by default, so agents writing the body without first clicking **Send message** produce `subtype_id=mail.mt_note`, which check.py explicitly rejects; (2) the paperclip triggers a hidden `<input type=file>` — BU cannot drive native file dialogs, AND the benchmark runner does not pass `available_file_paths` to the `Agent(...)` kwargs, so BU's `input_text/upload_file` actions fail with `File path ... is not available. To fix: The user must add this file path to the available_file_paths parameter`. check.py gates on `subtype_id == env.ref('mail.mt_comment')` (rejects mt_note) AND `attachment_ids` non-empty AND ≥1 attachment named `welcome_kit.txt` with non-empty bytes. |
| **Notes** | Single-shot BU FAIL as expected for the file-upload family. BU successfully (a) navigated to /odoo/contacts/10, (b) switched to the Send message tab, (c) typed the required body, but (d) hit the `available_file_paths` sandbox 6 times in a row on file-upload retries, then gave up without clicking Send — so check.py saw zero messages (`Messages present: []`) rather than an mt_note miscategorisation. Steps=0 in the agent_result.json because the runner counts only completed actions, not retries. Second calibration note: partner_ids on the posted message is legitimately EMPTY even on a correct oracle post — res.partner does not auto-follow itself in Odoo 19's benchmark base, so `_message_get_auto_subscribe_followers` returns empty and the Send-message subtype resolves to 0 notified partners. Initial check gated on `partner.id in msg.partner_ids.ids` and REJECTED the oracle; the corrected check pins Send-vs-Log discrimination on `subtype_id` alone. Cookbook quirks added to this task's COOKBOOK_NOTES.md and to ODOO19_PATTERNS.md § mail.message subtype_id — chatter Send message vs Log note. F1 estimate: ~0% BU pass rate until the benchmark runner is updated to pass `available_file_paths=[...]` to BU's Agent constructor. |

---

## documents.upload_document_tag_assign_to_folder

| Field | Value |
|---|---|
| **Row** | 411 |
| **Difficulty** | medium |
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | Documents (Enterprise-only `documents`) |
| **Workflow** | Seed would create a `documents.folder` named `Bench Folder`, a `documents.facet` named `Type` scoped to that folder, a `documents.tag` named `invoice` on that facet, and a deterministic `/tmp/bench_documents_sample.pdf` on disk. Agent: Documents → click `Bench Folder` in the Workspaces tree → click the header **Upload** button → Playwright `expect_file_chooser()` supplies the PDF → wait for the uploaded card in the Kanban → click the card to open the right-hand inspector panel → pick `invoice` in the `tag_ids` m2m and `Administrator` in `owner_id` → click outside to blur-save. Final state: one `documents.document` with `folder_id=Bench Folder`, `tag_ids` includes `invoice`, `owner_id=admin`, and a linked `ir.attachment` whose `name` matches the uploaded file. |
| **Capability tested** | Enterprise Documents workflow: (a) Workspaces tree navigation, (b) header Upload button that triggers a hidden `<input type='file'>` (Playwright `expect_file_chooser` pattern), (c) Kanban-card → inspector side-panel transition, (d) m2m tag autocomplete + m2o owner autocomplete on the inspector with implicit blur-save. Medium pattern: new-record creation via file upload + 2 field writes, no wizard, no status bar. |
| **Notes** | Blocked — `documents` is **Enterprise-only** and NOT vendored in this Odoo 19 Community checkout. Verified: `ls addons/documents/` → "No such file or directory"; `grep -rn "documents.document" addons/` returns only 5 files, all soft references that gate on `env.get("documents.document")` (the canonical optional-Enterprise-integration pattern) — `spreadsheet/static/tests/helpers/data.js` (mock JS factory), `cloud_storage/models/ir_attachment.py`, `cloud_storage_migration/models/ir_attachment.py`, `account/tests/test_audit_trail.py`, and `account/models/ir_attachment.py`. None register the real model. No `documents.folder` / `documents.tag` / `documents.facet` models; no `/odoo/documents` client action; no `documents_kanban` view; no `documents_inspector` Owl component. `ls addons/ \| grep -i document` returns only `l10n_latam_invoice_document` (unrelated LATAM invoice type). Task skeleton (seed/oracle/check/cleanup) ships with BLOCKED guards that short-circuit with diagnostic errors instead of silently passing. Follows the same precedent as rows 350 (appointment), 351 (helpdesk), 352 (marketing_automation), 387 (hr_skills_survey), 401 (stock_barcode), 404 (account_followup), and `barcodes.receive_product_via_scan_validate` — all Removed for Enterprise-only feature unavailability. Re-enable once enterprise `documents` is vendored into `addons/`. See the task's RESULT.md for full evidence and re-enabling steps. |
---

## project.create_task_with_deadline_tags_assignees

| Field | Value |
|---|---|
| **Row** | 409 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 33.4s, 2/2 atomic edits matched via Playwright UI) |
| **Browser-Use** | PASS (F1=1.0, 94.0s single-shot, 0 postcondition failures, 12 steps) |
| **F1** | 1.0 |
| **Odoo modules** | `project` |
| **Workflow** | Seed creates project `Bench Tag Proj` (empty), two `project.tags` rows (`urgent`, `backend`), and a second internal user `Bench Dev 2` (login `bench_dev_2`, groups = `base.group_user` + `project.group_project_user`). Agent: Projects → click `Bench Tag Proj` card → control-panel **New** → inline quick-create form opens with `Task Title...` textarea focused. Fills `Fix login bug`, then on the Deadline field types `06/30/2026` + Tab (closes the datepicker popover), then picks existing `urgent` + `backend` options from the `tag_ids` many2many autocomplete (avoiding the `Create "xxx"` quick-create item), then picks `Mitchell Admin` + `Bench Dev 2` from the `user_ids` autocomplete. Save via cloud icon. |
| **Capability tested** | project.task form create with date_deadline datetime + tag_ids many2many_tags existing-pick + user_ids many2many existing-pick (two assignees). Intended calibration risks: datepicker popover stealing the next click, picking `Create "urgent"` instead of existing, forgetting second assignee. |
| **Notes** | **Calibration MISS — BU passed single-shot cleanly.** BU correctly pressed Tab after typing the deadline, used the `role=option` autocomplete items for both tags (distinct id `tag_ids_0_0_0` per render) and both assignees, and clicked the Save button. Medium-tier task that BU solves on first try — similar to `project.create_task_assign_tags_deadline` (row 14-series). Retained as-is for deadline + dual-tag + dual-assignee coverage; date_deadline is a `fields.Datetime` in Odoo 19 (`project_task.py:183`) so typed `06/30/2026` stores as `2026-06-29 16:00:00 UTC` for the America/Los_Angeles admin TZ and check.py converts UTC → admin-local date before comparing. state_spec tracks only `name` + `active` on project.task (match_key=name); all other fields (date_deadline, tag_ids, user_ids, project_id) are asserted in check.py — a freshly-created task emits both `name` and `active=True` as `op=create` edits, so expected_state.json must include both for F1=1.0. trace_spec forbids `project.tags.create` and `res.users.create` to catch agents that quick-create rather than pick existing. |

---

## website_sale.checkout_portal_apply_coupon_complete

| Field | Value |
|---|---|
| **Row** | 410 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, ~70s) |
| **Browser-Use** | PASS (F1=1.0, ~66s, 12 steps single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | `website_sale` + `website_sale_loyalty` + `sale_loyalty` + `loyalty` + `payment_custom` |
| **Workflow** | Seed: published `Bench Coupon Item` (list_price 100, taxes cleared); `loyalty.program` `BENCH10` with `program_type='coupons'`, `trigger='with_code'`, reward `discount=10` `discount_mode='percent'` on order; ONE pre-generated `loyalty.card` with `code='BENCH10CODE'`; only `payment.payment_provider_transfer` enabled (all others disabled for radio determinism); `sale.async_emails=True` ICP; admin partner's billing address fully filled. Agent: `/shop` → click `Bench Coupon Item` tile → Add to cart → `/shop/cart` → type `BENCH10CODE` in the `<input name='promo'>` field of `<form name='coupon_code'>` → click Apply (POSTs to `/shop/pricelist?r=/shop/cart`, dispatches to `sale.order._try_apply_code` → `loyalty.card` branch → reward line at -$10) → click `name='website_sale_main_button'` ("Checkout") → `/shop/address` Confirm → `/shop/payment` select Wire Transfer radio → Pay now → `/shop/confirmation`. End state: SO in `state='sent'`, `amount_total=90.0`, product line + `loyalty.reward` discount line + auto-attached delivery line (is_delivery=True, price 0); `payment.transaction` on the Wire Transfer provider in `pending`. |
| **Capability tested** | Closed-loop public checkout crossing website_sale + loyalty + payment_custom. Coupon-code flow through the `coupon_form` template (distinct from `promo_code` `program_type` which puts the code on the rule). Wire-Transfer `state='sent'` acceptance. Auto-attached shipping line filtering in check.py. |
| **Notes** | **Not a BU-trap**: BU passed single-shot in 12 steps with clean navigation (login → tile click → Add to cart → View cart → type code + Apply → Checkout → Confirm address → Pay now → confirmation). Kept as hard/tier:3 for its coverage value: this is one of the few tier-3 tasks that covers the full public-portal checkout with a non-trivial pre-generated discount mechanism and an atypical payment path. **Calibration quirks fixed during iteration**: (a) oracle v1 used the HTML `a#add_to_cart` button which flakes on the optional-products modal; switched to `/shop/cart/add` JSON-RPC; (b) state_spec `match_key=[partner_id, amount_total]` resolves to `(null, 90.0)` for a newly-created SO (no pre-task order), so `expected_state.json` must mirror `[null, 90.0]` with `op='create'` — using a name-based key gave F1=0 on a passing run; (c) delivery line (`is_delivery=True`) auto-attaches at /shop/payment and must be filtered out of the "no extra products" assertion — without this filter the postcondition false-fails on a perfectly-completed checkout; (d) Wire Transfer transition leaves SO in `state='sent'`, NOT `'sale'` — check.py accepts `sent|sale|done`. |

---

## stock.create_scrap_order_for_damaged_qty

| Field | Value |
|---|---|
| **Row** | 412 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 26.8s, 3/3 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 88.2s single-shot, 0 postcondition failures, 18 non-forbidden writes) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (`stock`) — `stock.scrap` form + `stock.scrap.action_validate` + `stock.quant._update_available_quantity` + `stock.group_stock_multi_locations` gating |
| **Workflow** | Seed creates storable product `Bench Scrap Item` (type='consu', is_storable=True, tracking='none') and drops 10 on-hand units at `WH/Stock` via `env["stock.quant"]._update_available_quantity(product, stock_location, 10.0)`. Seed also grants the admin `stock.group_stock_multi_locations` so the Source Location + Scrap Location fields are visible on the scrap form (they default-bind silently without the group). Agent navigates to Inventory → **Operations → Scrap** (action `stock.action_stock_scrap`, list view of Scrap Orders), clicks **New**, picks product `Bench Scrap Item` in the `product_id` m2o, overwrites the default `scrap_qty=1.00` with `3`, leaves Source Location at the default `WH/Stock` and Scrap Location at the default `Virtual Locations/Scrap`, saves the form, then clicks the **Validate** button in the header (`button[name='action_validate']`). End state: one `stock.scrap` with `product_id=Bench Scrap Item`, `scrap_qty=3`, `state='done'`; one linked `stock.move` with `scrap_id` set, `product_uom_qty=3`, `state='done'`, source=`WH/Stock`, dest=inventory-usage `Virtual Locations/Scrap`; `WH/Stock` on-hand drops from 10 → 7. |
| **Capability tested** | "Create-from-scratch scrap order with explicit quantity override and header Validate" — tests three failure modes the medium tier targets: (a) forgetting to override `scrap_qty` from the default 1.00 (check.py gates on 3.0), (b) saving the draft but not clicking Validate so state stays `draft` (check.py gates on `state='done'`), (c) using the product-form Scrap button (which opens a pre-bound wizard from product context) vs the Operations > Scrap list (which opens a blank form). expected_state.json tracks the 3 create edits: product_id, scrap_qty, state. trace_spec.yaml requires `stock.scrap.action_validate` (the distinguishing non-default gesture). |
| **Notes** | **Calibration MISS — BU passed single-shot cleanly** (88.2s, F1=1.0, 3/3 atomic edits matched, 0 postcondition failures, RequiredOpRecall=1.0, WritePrecision=1.0, HarmfulWriteRate=0.0, StrictClean=True). The Operations > Scrap menu is discoverable, the form is a single-screen wizard with obvious `product_id` and `Quantity` fields, and the Validate button is in a standard statusbar — all patterns BU handles well. Appropriate for tier 2 (medium); confirms `stock.adjust_inventory_quantities` + `inventory.scrap_product` easy-tier behaviour that BU reliably completes direct `stock.scrap` form flows when the quantity is an explicit prompt value. To harden into a tier-3 (hard) variant: (a) require a specific scrap reason tag on `scrap_reason_tag_ids` (m2m that Odoo ships empty — seed must pre-create + prompt "add tag Damaged"), (b) require changing Scrap Location away from the default to a custom `WH/Lost` seeded sub-location (forces the multi-locations autocomplete), or (c) launch the scrap from a picking context (`stock.picking` cog Actions → Scrap) so the wizard pre-binds a picking_id and auto-creates a `stock.move` with `scrap_id` on the parent picking. Cookbook bits already in ODOO19_PATTERNS.md § `mrp / stock.scrap quirks` — this task reinforces the "default scrap_qty=1.0 must be overridden" trap and documents the clean-path end-to-end timings. |

---

## mrp.scrap_consumed_component_during_production

| Field | Value |
|---|---|
| **Row** | 415 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 36.7s, 0 steps) |
| **Browser-Use** | PASS (F1=1.0, 212.8s single-shot, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | `mrp` + `stock` |
| **Workflow** | Seed: product `Bench Assembly Kit` (consu/is_storable, tracking='none') + component `Bench Screw` (consu/is_storable, tracking='none'); normal BoM with 1 line `3 Bench Screw` per kit, `consumption='flexible'`, no routing (no work orders); `10` Bench Screw on-hand at WH/Stock (covers 3 consume + 1 scrap + buffer, also avoids the `stock.warn.insufficient.qty.scrap` secondary wizard); confirmed+assigned MO `MO-BENCH-SCRAP` for 1 kit. Agent: Manufacturing → MOs → open `MO-BENCH-SCRAP` → open the control-panel cog / 3-dots Actions menu → click **Scrap** (`mrp.action_production_order_scrap` `ir.actions.server` with `binding_view_types='form'`) → wizard `stock.scrap` with defaults Product=Bench Screw+Qty=1+Source=WH/Stock → click **Scrap Products** → wizard calls `stock.scrap.action_validate` → returned to MO form → click header **Produce All** / **Mark as Done** (`mrp.production.button_mark_done`) → consumption-warning / MO auto-consumes the remaining 2 screws. End state: `mrp.production.state='done'`, `qty_produced=1.0`, `qty_producing=1.0`; exactly 1 `stock.scrap` linked via `production_id` with `scrap_qty=1`, `product_id=Bench Screw`, `state='done'`. |
| **Capability tested** | Non-default access path (cog Actions menu / 3-dots), scrap wizard with trivial defaults, MO finish after a mid-run scrap. Scrap mechanism = scrap-from-MO pipeline, NOT scrap-from-stock. Sub-variant of `mrp.scrap_component_during_partial_production` (which uses reason-tag + qty=2); this one keeps scrap_qty at the wizard default 1.0 and has a single-component BoM. |
| **Notes** | **Calibration MISS — BU passed single-shot in 212.8s (F1=1.0, 0 postcondition failures).** BU correctly navigated the cog Actions menu, picked Bench Screw + qty=1 in the scrap wizard, validated, then hit Mark as Done. With `scrap_qty` default=1 and only one component in the BoM, the wizard requires almost no deviation from defaults — which is the opposite failure pattern from `mrp.scrap_component_during_partial_production` (ScrewA qty=2 out of {ScrewA, ScrewB}). Retained as-is for the `scrap-from-MO at scrap_qty=1` coverage slot; this is the "easy calibration" of the scrap-during-production workflow and is useful as a BU-passable baseline alongside the harder variants. **Design quirks confirmed on this task**: (a) `stock.scrap` `match_key=[production_id]` normalizes to the MO display name `MO-BENCH-SCRAP`, emitting a `{field: production_id, op: create, norm_value: 'MO-BENCH-SCRAP'}` diff row on top of product/scrap_qty/state creates — must all six (mrp.production state+qty_produced + stock.scrap production_id+product_id+scrap_qty+state) be enumerated in `expected_state.json` for F1=1.0; (b) `action_production_order_scrap` is an `ir.actions.server` (`binding_model_id=mrp.production`, `binding_view_types='form'`) reachable via the cog menu, NOT a header button; (c) seed seeds `10` screws on-hand to cover both the consumption and the scrap so the secondary `stock.warn.insufficient.qty.scrap` wizard does not open. No F1 drop during iteration — oracle+BU both PASS first try. |

---

## account.reconcile_customer_payment_against_invoice

| Field | Value |
|---|---|
| **Row** | 416 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.0s, 10/10 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 70.3s single-shot, 0 postcondition failures, 17 non-forbidden writes) |
| **F1** | 1.0 |
| **Odoo modules** | Accounting (`account`) — `account.move` customer invoice + `account.payment.register` wizard + `account.payment` + auto-reconciliation of the receivable journal items |
| **Workflow** | Seed creates partner `Bench Recon Co` + service product `Bench Recon Service` + a posted customer invoice with `ref='INV/BENCH/RECON'`, `amount_total=500.00`, `state='posted'`, `payment_state='not_paid'` (taxes cleared via `tax_ids=[(5,0,0)]`). Agent: Accounting → Customers → Invoices → open `INV/BENCH/RECON` → click the **Pay** button in the statusbar (`account.move.action_register_payment`) to open the `account.payment.register` wizard modal → leave defaults (Journal=Bank, Payment Method=Manual, Amount=500.00, Date=today, Memo=invoice name) → click primary footer button **Create Payment** (`button[name='action_create_payments']`). Wizard calls `_create_payments()` → creates `account.payment` (`payment_type='inbound'`, `amount=500.0`, `partner_id=Bench Recon Co`) → posts its underlying `account.move` (`move_type='entry'`) → reconciles the payment's counterpart line against the invoice's receivable line. End state: invoice `payment_state='paid'`; exactly one `account.payment` with `state='paid'` (reconciled posted payment), `amount=500`, `payment_type='inbound'`, on a Bank journal; plus the payment's auto-generated journal entry move (`move_type='entry'`) which we track explicitly in `expected_state.json`. |
| **Capability tested** | Accept-defaults Register Payment wizard — open the payment registration dialog on a posted invoice, verify the amount/journal/method/date defaults are already correct for a full payment, click the single primary footer button. Tracks the downstream reconciliation via `payment_state='paid'` and the creation of the payment's internal `account.move` journal entry. |
| **Notes** | **Calibration MISS — BU passed single-shot** (70.3s, F1=1.0, all atomic edits matched, 0 postcondition failures). This fits the "Accept-defaults wizards" category in `TASK_CREATION_GUIDE.md` under "patterns that do NOT fail browser-use" — Odoo's Register Payment wizard pre-fills amount=invoice-total, journal=first-bank, method=Manual, date=today, so the agent only needs to click "Create Payment". Retained at hard/tier 3 per the pre-allocated STATUS slot + spec, but functionally this is equivalent to `account.register_payment_defaults` (easy). **Calibration quirks fixed during iteration**: (a) the invoice header button is labeled **Pay** in Odoo 19 (not "Register Payment" — the wizard's title is "Register Payment" but the statusbar button is string="Pay"); (b) `account.payment.state` reports `'paid'` (not `'posted'`) once auto-reconciled on an otherwise-clean journal item — check.py accepts `posted|paid|in_process` and `expected_state.json` uses `'paid'`; (c) `account.move.payment_state` goes directly to `'paid'` (not `'in_payment'`) because the Bank journal has no `outstanding_account` configured in the base snapshot, so the payment posts straight to the receivable account; (d) the payment's backing `account.move` (`move_type='entry'`) shows up in state tracking with its auto-assigned name `INV/2026/00001` — these 5 create edits are baked into `expected_state.json`; (e) cleanup must `remove_move_reconcile()` + `action_draft()` + `action_cancel()` on prior payments before `unlink()` or the next seed fails with "You can't delete a posted entry". **To harden into a real trap**: (i) partial payment (change Amount 500 → 300, expect `payment_state='partial'`), (ii) non-default Journal (seed two bank journals, require picking the non-first one), or (iii) add a Memo override + Payment Date back-date — follow `account.pay_invoice_with_memo` (row elsewhere) which BU reliably fails. |

---

## calendar.create_recurring_meeting_weekly_pattern

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 35.7s wall clock, 0 postcondition failures) |
| **Browser-Use** | FAIL (F1=0.0, 360.0s timed out, 2 postcondition failures, 14 events created) |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Agent: Calendar → control-panel **New** → fills `name=Bench Weekly Standup`, `start=05/04/2026 10:00:00 AM`, `duration=00:30` → switches to **Options** tab → toggles `recurrency` boolean_toggle ON → verifies `rrule_type_ui=Weekly` via SelectMenu → clears every other weekday on the `calendar_week_days` widget so only Monday (index 1 in US locale) is active → sets `end_type=Number of repetitions` via SelectMenu → fills `count=4` → saves via breadcrumb. Recurrence expands to 4 Monday occurrences 5/4, 5/11, 5/18, 5/25. |
| **Capability tested** | Count-based weekly recurrence configuration with the weekday-row widget and the two SelectMenu fields (`rrule_type_ui`, `end_type`). Calibration risk: agents often leave the today-of-week pre-selected alongside Monday, or pick the `End date` default end_type and type a date instead of flipping to `Number of repetitions`. |
| **Notes** | Oracle types `05/04/2026 10:00:00 AM` which stores as `2026-05-04 02:00:00 UTC` on this harness (admin.tz=UTC from seed but the Odoo web datetime widget interprets typed strings in the BROWSER's local tz — Asia/Singapore / UTC+8 — not the admin's Odoo tz). Check.py is tz-aware via `pytz` on `admin.tz` and compares admin-local date only (not hour-of-day), matching the `calendar.configure_meeting_with_location_and_reminder` pattern. Critical oracle quirk: the `recurrency` `boolean_toggle` lives on the **Options** tab (`addons/calendar/views/calendar_views.xml:250-252`), NOT on the main form body — forgetting `click_tab(page, "Options")` before `set_boolean(page, "recurrency", True)` produces a 60s Playwright timeout on the hidden checkbox locator (first oracle draft hit this). Browser-use FAILed at the 360s time_limit, creating 14 stray `calendar.event` rows (multiple base events on 5/4, plus events on 5/5, 5/6, 5/7, 5/12 — i.e. the today-of-week weekday bleed). No forbidden unlinks recorded. Genuine medium-tier failure via the "did not deselect pre-selected weekday + did not flip end_type to count" calibration trap. |

---

## crm.duplicate_lead_convert_to_opportunity

| Field | Value |
|---|---|
| **Row** | 414 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 32.2s wall clock) |
| **Browser-Use** | FAIL (F1=0.0, 246.8s, 1 postcondition failure: 2 records named 'Bench Cloned Opp') |
| **F1** | 0.0 |
| **Odoo modules** | `crm` |
| **Workflow** | Seed: admin granted `crm.group_use_lead` so Leads submenu + Convert-to-Opportunity header button are exposed; one `crm.lead` `Bench Template Lead` (type='lead', contact_name='Template Contact', email_from='template.bench@example.com', expected_revenue=1500). Agent: CRM → Leads → open `Bench Template Lead` form → cog (Actions) → **Duplicate** → on the copy edit the title textarea to `Bench Cloned Opp` and Save → click header **Convert to Opportunity** → in the `crm.lead2opportunity.partner` wizard, explicitly pick the **Convert to opportunity** radio (field `name` — wizard auto-computes to `merge` because the copy inherits `email_from` from the template, so `_get_lead_duplicates` finds ≥2 matches), then flip the **Related Customer** radio (field `action`) to **Link to an existing customer** (default was `create` because no matching partner), type `Bench Cloned Customer` into the Customer autocomplete, and pick the `Create "Bench Cloned Customer"` quick-create option → click **Create Opportunity** (`action_apply`). End state: original `Bench Template Lead` unchanged (type='lead'); new `crm.lead` `Bench Cloned Opp` with type='opportunity' and partner_id → new `res.partner('Bench Cloned Customer')`. |
| **Capability tested** | cog/Actions **Duplicate** discovery on a form toolbar + convert-to-opportunity wizard with TWO non-default radio selections (`name='convert'` overriding an auto-merge default, and `action='exist'` instead of auto-`create`) + m2o quick-create `name_create` path inside a modal. |
| **Notes** | Well-calibrated medium. BU created **two** records named `Bench Cloned Opp` — likely duplicated once, then either created-from-scratch or re-clicked Duplicate. The `enforce exactly 1` check in check.py plus the entity_key `[Bench Cloned Opp]` detects the duplication. **Seed quirk**: email_from is copied by `copy()`, which makes `_compute_name` flip the wizard to `merge` by default because the copy now duplicates the template by email — oracle must click the `Convert to opportunity` radio explicitly; prompt.md warns humans about this too. **Radio widget**: Odoo 19 renders `widget="radio"` as `<input class="o_radio_input" data-value="<key>">` inside `.form-check.o_radio_item`; click with `force=True` on the input (label only drives the click when hover works). **partner_id visibility on leads**: `crm.lead.partner_id` is invisible on the lead form (not is_partner_visible) unless the record is an opportunity or already has a partner — this is why the partner must be set INSIDE the convert wizard via the `action='exist'` branch, not on the lead form directly. |

---

## purchase.create_rfq_receive_invoice_3way_match

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 61.2s, 12/12 create edits matched) |
| **Browser-Use** | FAIL (F1=0.0 single-shot, 480s wall clock, 12 postcondition failures — swapped Item A/B lines on the PO, never validated the receipt, never clicked Create Bills) |
| **F1** | 0.0 |
| **Odoo modules** | Purchase (`purchase`) + Stock (`purchase_stock`) + Accounting (`account`) |
| **Workflow** | Closed-loop cross-module 3-way match. Seed creates vendor `Bench Supply Co`, 2 storable products `Bench PO Item A` ($20) and `Bench PO Item B` ($40) with `purchase_method="receive"` + `invoice_policy="delivery"`, and a distractor draft RFQ from `Bench Filler Vendor` (different vendor). Agent flow: Purchase → New RFQ → vendor=Bench Supply Co → add 2 lines (A qty=10@20, B qty=5@40) → Confirm Order → Receipt smart button → set Done=7 on Item A (leave B=5) → Validate → **Create Backorder** (primary) dialog → navigate to Purchase Orders list → checkbox the PO → Create Bills (list header) → bill form opens with lines pre-filled at qty_received (7, 5) → set Bill Reference `BSC-BILL-3WM` → Confirm (action_post). |
| **Capability tested** | Long multi-step flow across 3 apps: create-from-scratch PO with exact field values (phantom-line trap), inline Done-qty edit on a receipt (partial receive), Create Backorder radio dialog, cross-module round-trip Purchase → Inventory → Purchase → Accounting, and posting a vendor bill with a Bill Reference. Check.py enforces: PO state=purchase, 2 lines with correct product order / qty / price_unit / qty_received (7, 5); original receipt state=done with matching Done qty on each move; backorder pending with 3 remaining Item A units; exactly one posted `account.move` (move_type=in_invoice) with `ref='BSC-BILL-3WM'` linked to the PO via `invoice_line_ids.purchase_line_id`; distractor RFQ untouched (state=draft). |
| **Notes** | **Calibration: confirmed hard.** BU single-shot: 480s timeout, swapped line products on PO creation, never validated, never clicked Create Bills. 12 postcondition failures. **Key cookbook quirk discovered:** in Odoo 19, `purchase.order` form has **no "Create Bill" status-bar button** — only `action_create_invoice` via `purchase.order.view.list` header ("Create Bills", plural). Prompt + oracle must direct agent through `/odoo/purchase-orders` → checkbox row → Create Bills. A second quirk: opening a freshly-created vendor bill through `action_view_invoice`'s redirect (URL `/odoo/purchase-orders/bills/<id>`) leaves the Owl form in a non-edit state where `fill_field("ref")` alone does NOT dirty the form (Save button stays disabled, `action_post` silently no-ops). Oracle workaround: set `invoice_date` via `set_date()` FIRST (the date picker click kicks the form into edit mode), then `fill_field("ref", ...)` persists. Distractor vendor RFQ ensures BU cannot pick the wrong PO to Create Bills from. |

---

## product.configure_variant_attribute_two_values

| Field | Value |
|---|---|
| **Row** | 417 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.6s, 9/9 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 269.7s single-shot, 0 postcondition failures, 36 non-forbidden writes) |
| **F1** | 1.0 |
| **Odoo modules** | `product` — `product.template` + `product.attribute` + `product.attribute.value` + `product.template.attribute.line` + auto-generated `product.product` variants via `_create_variants` |
| **Workflow** | Seed creates a clean `Bench Variant Shirt` `product.template` (`type='consu'`, `list_price=39.0`, `sale_ok=True`) with **zero** attribute lines and exactly 1 base `product.product` variant. Drops any pre-existing `Size` attribute (via `product.template.attribute.line.unlink()` on every referencing template, then `value_ids.unlink()` + `attribute.unlink()`) so the agent must create it inline. Agent: Sales/Inventory → Products → open `Bench Variant Shirt` → switch to the **Attributes & Variants** notebook tab → click "Add a line" inside the `attribute_line_ids` nested o2m → in the inline row, set Attribute=`Size` (tapping "Create" in the m2o dropdown if it doesn't exist) → fill the Values tags field with `Small`, `Medium`, `Large` one at a time (each creates a `product.attribute.value` inline via the "Create" dropdown action) → Save the form. Save fires the `product.template` write with `attribute_line_ids=[(0,0,{attribute_id, value_ids:[(6,0,[…])]})]`, which triggers `_create_variants` → 3 `product.product` rows auto-appear (one per size). End state: `product.attribute` `Size` exists with `create_variant='always'` (default) and 3 values; `product.template.attribute.line` count=1 on the template with those 3 `value_ids`; `product.product` count=3 for the template. |
| **Capability tested** | Nested o2m configuration in the Attributes & Variants tab with **inline creation** of a many2one target (`product.attribute`) **and** a many2many tag field of value records (`product.attribute.value`) within a single new attribute_line row — plus implicit reliance on the template save → `_create_variants` side effect to generate the 3 variants (agent never touches `product.product` directly). |
| **Notes** | **Calibration MISS — BU passed single-shot in 269.7s** (F1=1.0, 0 postcondition failures, 36 non-forbidden writes, 0 forbidden). BU correctly opened the Attributes & Variants tab, added a new line, created the `Size` attribute inline via the m2o "Create" action, added Small/Medium/Large as tag values (each creating a `product.attribute.value`), and saved — variants auto-generated. The notebook-tab + inline-create flow that the spec flagged as calibration risk (nested o2m with inline creation of both the attribute and its values) did NOT trap BU. Sits in the "Deep UI interaction" category of `TASK_CREATION_GUIDE.md` but practically is an "accept-defaults after configuring values" pattern — the critical value `create_variant='always'` is the default on `product.attribute`, and the values tag field accepts "Quick Create" on any typed text. **Design quirks solidified during iteration**: (a) `_create_variants` fires on template save after `attribute_line_ids` write — do NOT pre-seed variants, let the agent's save trigger them; (b) `state_spec` must key `product.attribute.value` on `[attribute_id, name]` because value names like "Small" can collide across attributes (e.g., seed has pre-existing size values) — the 9-edit diff splits into `attribute.create×2 (name+create_variant)` + `attribute.value.create×6 (name+attribute_id for each)` + `product.template.attribute_line_ids set`; (c) seed's prior-run cleanup MUST unlink `product.template.attribute.line` rows referencing the attribute on all templates before unlinking the attribute or PSQL FK raises; (d) start_url `/odoo/inventory/products` works (Inventory → Products menu) — Sales → Products also works but BU prefers Inventory in the base menu layout. **To harden into a real trap**: (i) non-default `create_variant='dynamic'` (requires agent to change the attribute's Variant Creation setting before saving — buried one tab deep on the attribute sub-form), (ii) mixed-attribute configuration (Size + Color with unequal value counts, check variant cross-product = 3×2=6), (iii) require specific `default_value`/`html_color` on each value, or (iv) require archiving one of the three auto-generated variants after save. |

---

## mrp.unbuild_product_back_to_components

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.9s wall clock, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 132.8s wall clock, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Manufacturing, Inventory |
| **Workflow** | Agent: Manufacturing app → action URL `/odoo/action-mrp.mrp_unbuild` (or Products → Unbuild Orders menu) → New → product=`Bench Assembly` (BoM auto-fills via `_onchange_product_id`) → quantity=`2` → leave Manufacturing Order blank + Source/Destination Location = `WH/Stock` defaults → click statusbar **Unbuild** (`action_validate`). Stock deltas at WH/Stock: -2 Bench Assembly, +6 Bench Screw, +2 Bench Housing. |
| **Capability tested** | Product-driven (`mo_id=False`) unbuild without an originating Manufacturing Order — different flow from the MO-linked unbuild in `mrp.unbuild_finished_goods_to_recover_components`. BoM auto-selection onchange + single-button validate. |
| **Notes** | Calibrated as **hard** but BU PASSED first attempt F1=1.0 in 132.8s — the spec flagged this ("Calibration risk: Unbuild form auto-sets BoM on product selection; single Validate button; clean form flow") and it played out exactly. The form is too linear: product picker → auto-BoM → qty=2 → one Unbuild button. No wizards, no radio dialogs, no cross-module navigation. Unbuild form exposes `product_id`, `bom_id`, `mo_id`, `product_qty`, `location_id`, `location_dest_id` as flat fields and all but `product_id` + `product_qty` carry sensible defaults from the BoM/warehouse. BU's final message: "Successfully unbuilt 2 units of Bench Assembly. The unbuild order UB/00002 is now in the 'Done' state." To escalate to genuine BU-failing hard tier, would need one of: (a) multi-BoM picker ambiguity (two BoMs on same product → force BU to pick the right one), (b) tracking='serial' on finished product + a specific lot to select in an unbuild-wizard lot picker, or (c) non-default Source/Destination Location (e.g. recover to a sub-location `WH/Stock/QC`) which requires `stock.group_stock_multi_locations`. |

---

## sale.configure_pricelist_apply_to_order_line

| Field | Value |
|---|---|
| **Task ID** | `sale.configure_pricelist_apply_to_order_line` |
| **Row** | 418 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 56.0s, 5/5 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 325.9s single-shot, 44 steps, 0 postcondition failures, 50 non-forbidden writes) |
| **F1** | 1.0 |
| **Odoo modules** | Sales (`sale`) + Product (`product`) — `product.pricelist` + `product.pricelist.item` (rule with `compute_price='formula'`, `applied_on='3_global'`, `price_discount=10`, `base='list_price'`) + `sale.order` with `pricelist_id` + `sale.order.line._compute_price_unit` (pricelist-driven unit price recompute). |
| **Workflow** | Seed enables `product.group_product_pricelist` on admin + user_root (so both the Sales > Products > Pricelists menu and the SO form's `pricelist_id` field are visible), then creates a consumable product `Bench Price Item` (`list_price=200.00`, `taxes_id=[(5,0,0)]` for clean math), a customer `Bench Price Co` (no pre-assigned pricelist so the agent must pick it themselves). Agent stage 1: Sales > Products > Pricelists > **New** -> type `Bench 10% Off` in the H1 name, click **Add a line** in the Sales Prices tab which opens a `product.pricelist.item` form dialog; in that dialog keep Apply To = Product (default) with the product field empty (onchange resolves `applied_on='3_global'`), switch the **Price Type** radio from the default "Fixed Price" to **Formula** (unhides the `pricelist_rule_base` group), leave Based price on Sales Price, enter `10` into the **Discount** (`price_discount`) field, click **Save & Close** -> click the main form save. Agent stage 2: Sales > Orders > Quotations > **New** -> Customer = `Bench Price Co`, Pricelist = `Bench 10% Off`, click **Add a product**, select `Bench Price Item` (qty defaults to 1). The SO line's `_compute_price_unit` triggers via the pricelist onchange and computes `price_unit = 200 * (1 - 10/100) = 180.00`. Save (do NOT confirm). End state: 1 `product.pricelist` with 1 matching rule, 1 draft `sale.order` for `Bench Price Co` with `pricelist_id=Bench 10% Off`, 1 `sale.order.line` (`Bench Price Item`, qty=1, `price_unit=180.00`), `state='draft'`. |
| **Capability tested** | Nested modal configuration on a pricelist rule (`product.pricelist.item`) where the correct "10%" sub-field depends on which radio the agent picks for `compute_price` — "Discount" (percentage) vs "Formula" (with its own `price_discount` sub-section under `pricelist_rule_base`) vs "Fixed Price". Also tests letting an onchange-driven compute (`sale.order.line._compute_price_unit`) populate `price_unit` via the SO's `pricelist_id` instead of the agent typing the value. |
| **Notes** | **Calibration MISS at tier 3** — browser-use passed single-shot (325.9s, 44 steps, F1=1.0, all 5 atomic edits matched, `strict_success=True`, 0 postcondition failures) despite repeatedly hitting "Oops! Something went wrong" dialogs while trying to save `price_discount=10` in the rule modal (~steps 11-22). The agent recovered by navigating back to Pricelists, re-opening the half-saved rule, and re-entering `10` until the value stuck. The agent did initially click the **Formula** radio but `price_discount` failed to persist on the first several Save & Close attempts (field is in a hidden group until the radio onchange fires — the input may not be focused before the save). Recovery loop ate ~8 steps of wall-clock but BU eventually got to PASS. **Cookbook quirks discovered**: (a) the Pricelists menu lives under **Sales > Products > Pricelists** (not Configuration) and only shows when `product.group_product_pricelist` is enabled on admin AND user_root — seeding only admin breaks the onchange pricelist computation when root-triggered background writes run; (b) the `item_ids` one2many in the pricelist form is rendered as a non-inline list (no `editable=bottom`) so clicking **Add a line** opens a full-form modal for `product.pricelist.item`, NOT inline editing — our oracle uses the modal's "Save & Close" button (`.modal-footer button.o_form_button_save`); (c) the rule form has TWO discount-looking fields: a top `percent_price` under Price Type = "Discount" (percentage) and a nested `price_discount` under Price Type = "Formula" / base="Sales Price" — agents and humans both frequently pick the wrong one, so the prompt explicitly calls out "Formula" and "Discount field inside the formula sub-section"; (d) `display_applied_on='1_product'` with an empty `product_tmpl_id` is what triggers `applied_on='3_global'` via `_onchange_display_applied_on` — no need to touch "All Products" directly; (e) on the SO form, `pricelist_id` is read-only until `product.group_product_pricelist` is in the user's groups at login time — the seed handles this so the form field is visible to the agent. **To harden into a real trap** (future iteration): (i) seed a distractor pricelist named `Bench 20% Off` so the agent must pick the correct one; (ii) require a second rule with `min_quantity=10` for a volume-discount tier; (iii) require base='pricelist' (chained pricelist) so the agent must set a nested `base_pricelist_id` — all three would push the failure rate higher. Retained at hard/tier 3 per the pre-allocated STATUS slot. |

---

## point_of_sale.apply_fixed_discount_before_payment

| Field | Value |
|---|---|
| **Row** | 420 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 19.2s wall clock) |
| **Browser-Use** | PASS (F1=1.0, 111.3s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | `point_of_sale`, `pos_discount` (installed on demand) |
| **Workflow** | Seed: installs `pos_discount` via `button_immediate_install()`, creates POS config `Bench POS` with `module_pos_discount=True`, `discount_pc=14.29` (popup default), `discount_product_id` → the `pos_discount.product_product_consumable` data record, and a single **Bench Cash** payment method. Two tax-free products: `Bench POS Item A` list_price=20.00 and `Bench POS Item B` list_price=15.00 (both `available_in_pos=True`, `taxes_id=[(5,0,0)]`). Opens a `pos.session` in `opening_control`. Agent: POS → open `Bench POS` register → click Bench POS Item A → click Bench POS Item B → open the ellipsis/Actions popup → click **Discount** → popup pre-fills `14.29` → accept default → a discount line with ~-5.00 EUR appears → click **Payment** → **Bench Cash** tile → type `30` → **Validate** to reach the receipt screen. End state: `pos.order` with 2 product lines (A qty=1 price_unit=20.00, B qty=1 price_unit=15.00) + 1 global-discount line (price_subtotal≈-5.00), `amount_total≈30.00`, `state='paid'`, single cash payment of ~30.00, POS session stays open. |
| **Capability tested** | Driving the POS kiosk UI to apply the *global* discount (`pos_discount` Discount control button that lives inside the ellipsis/Actions popup in Odoo 19), accepting a pre-filled non-default percentage (14.29), and completing a multi-line cash payment. |
| **Notes** | **Calibration: easier than hard.** Browser-use solved the task first try in 111s, F1=1.0. Similar outcome as `point_of_sale.add_item_apply_global_discount_pay_cash` (BU also passed that). POS global-discount-at-default-percent is **not** a hard pattern on modern BU; the ellipsis/Actions popup discovery is no longer a blocker. **Math**: 14.29% × 35.00 = 5.0015 → rounded to 2dp ≈ 5.00. Check uses a 0.2 tolerance on `amount_total` (30.0 ± 0.2) and 0.5 on the discount line subtotal (-5.0 ± 0.5) to absorb rounding. **Oracle pattern**: JSON-RPC `call_kw` bypass (same as `split_payment_email_receipt` / `add_item_apply_global_discount_pay_cash`) — Playwright-driven POS oracles are flaky because `o_technical_modal` sometimes intercepts pointer events. Oracle creates the order with all 3 lines (2 product + 1 discount at price_unit=-5.00), then `pos.make.payment.create` + `.check` closes the order. **Seed quirks**: `pos_discount` is NOT in the benchmark_base snapshot; seed must `button_immediate_install()` on demand (like `survey`/`stock_dropshipping`). The `pos.config` requires `module_pos_discount=True`, `iface_discount=True`, `discount_pc=<float>`, and `discount_product_id=<id>`; omitting any of these raises `UserError` on `open_ui()`. Tax-free products need `taxes_id=[(5,0,0)]` on **both** `product.product` and `product.product_tmpl_id` because `available_in_pos` on product.product pulls company default taxes from the template otherwise. **Escalation ideas**: split payment across Cash + Bank tiles with the same global discount, or a non-default discount percentage distinct from `discount_pc`, or a mid-order customer change combined with the discount so the price recomputes. |

---

## sale.duplicate_quotation_edit_delivery_date_confirm

| Field | Value |
|---|---|
| **Row** | 426 |
| **Task ID** | `sale.duplicate_quotation_edit_delivery_date_confirm` |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 24.3s wall clock, 3/3 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 81.5s wall clock single-shot, 27 non-forbidden writes, 0 forbidden, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | Sales (`sale`) — cog/Actions `Duplicate` on `sale.order` form + `commitment_date` Datetime field rendered as "Delivery Date" on the Other Info tab + `action_confirm` statusbar button. |
| **Workflow** | Seed creates partner `Bench Copy Co`, two tax-free consu products `Bench SO Item A` (list_price=50) and `Bench SO Item B` (list_price=30), and a draft `sale.order` with `name='S-BENCH-COPY-001'` and `client_order_ref='S-BENCH-COPY-001'` for Bench Copy Co (`user_id=admin`) carrying two lines (A qty=2, B qty=3, `tax_ids` cleared). Agent: Sales → Quotations → open `S-BENCH-COPY-001` → control-panel cog / Actions menu → **Duplicate** (Odoo navigates to the new draft copy) → on the duplicate open the **Other Info** notebook tab → set **Delivery Date** (`commitment_date`) to `08/15/2026` → Save → click **Confirm** in the statusbar. End state: exactly two `sale.order` rows for `Bench Copy Co` — the original `S-BENCH-COPY-001` still draft with its two seeded lines and `commitment_date=False`, plus the duplicate (auto-sequenced name, `client_order_ref=False`) in state `'sale'` with the same two lines and `commitment_date` whose date part is `2026-08-15` (check tolerates admin-tz drift of up to ±24h on the datetime → date conversion). |
| **Capability tested** | Cog/Actions `Duplicate` on `sale.order` (distinct from the crm.lead / website_slides / mass_mailing Duplicate flows already covered), followed by a notebook-tab switch (`Other Info`) to reach a Datetime widget (`commitment_date`), editing that datetime field via the DateTimeField button↔input dual-rendering path (see `ODOO19_PATTERNS.md § DateTimeField widget: button vs input dual rendering`), saving, and finally triggering `sale.order.action_confirm` via the statusbar — all while leaving the original untouched. |
| **Notes** | **Calibration: soft medium.** BU PASS on first shot (81.5s single-shot, F1=1.0, 0 postcondition failures) — the sale.order cog `Duplicate` + Other Info tab + Delivery Date + statusbar Confirm is a well-signposted flow and not a reliable BU trap on its own. Useful as deterministic coverage of the `commitment_date` datetime widget + Other-Info-tab discovery combo. **Match-key design**: both original and duplicate share `partner_id='Bench Copy Co'`, and `sale.order.name` has `copy=False` so the duplicate gets a fresh sequence name. The `client_order_ref` field is also `copy=False` — seeding the source with `client_order_ref='S-BENCH-COPY-001'` gives us a distinct entity_key (source = `["S-BENCH-COPY-001"]`, duplicate = `[null]`) so `expected_state.json` can anchor three edits on `[null]`: `client_order_ref=null`, `partner_id='Bench Copy Co'`, `state='sale'`. Same `copy=False`-as-match-key trick that other Sale duplicate tasks use when the agent never types a new reference. **commitment_date tz**: the ORM stores the datetime in UTC; admin tz on the benchmark_base snapshot is effectively UTC so typing `08/15/2026 00:00:00` lands as `2026-08-15 00:00:00` and the naive `.date()` compare matches. `check.py` defensively sweeps ±24 hours of offsets in case a future snapshot ships a non-UTC admin tz (same pattern as `purchase.duplicate_rfq_change_vendor_confirm` where `date_order` is compared as date with a `+8h` shift for the demo Asia/Singapore seed tz). **Oracle tactic**: the `/odoo/sales` list action defaults to `search_default_my_quotation=1` and can render kanban first, which makes `click_list_row` flaky at 60s timeouts. Oracle resolves the SO id via a single JSON-RPC `search_read` then navigates to `/odoo/sales/<id>` directly — the Duplicate/Save/Confirm flow is still driven through the UI, only the initial record lookup is shortcut. **Escalation ideas** to harden: (i) seed a second SO for the same partner so the agent must disambiguate before clicking Duplicate, (ii) require the agent to re-enter the two order lines from scratch on the copy instead of keeping the auto-copied ones, (iii) add a `commitment_date` validity constraint via a Delivery wizard (e.g., enable `sale_stock` + MTO so the datetime change actually reschedules a pending picking), or (iv) combine with a client_order_ref rename on the copy (distinct from `sale.duplicate_quotation_change_customer` which changes customer instead). |

---

## sale.duplicate_confirmed_order_edit_customer

| Field | Value |
|---|---|
| **Row** | 474 |
| **Task ID** | `sale.duplicate_confirmed_order_edit_customer` |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 30.6s wall clock, 3/3 atomic edits matched, 0 postcondition failures, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 83.6s wall clock single-shot, 17 non-forbidden writes, 0 forbidden, 0 postcondition failures, StrictClean=True) |
| **F1** | 1.0 |
| **Odoo modules** | Sales (`sale`) — cog/Actions `Duplicate` on a CONFIRMED `sale.order` form + `partner_id` many2one edit on the resulting draft copy (no statusbar button click, unlike row 426). |
| **Workflow** | Seed creates two partners (`Bench Orig Co` owner of the source SO, plus the pre-existing target partner `Bench Clone Co`), two tax-free consu products `Bench SO Dup Item A` (list_price=40) and `Bench SO Dup Item B` (list_price=25), and a **CONFIRMED** `sale.order` with `client_order_ref='BENCH-DUP'` / `partner_id=Bench Orig Co` / `user_id=admin` / two lines (A qty=2, B qty=3, `tax_ids` cleared) / `state='sale'` (via `action_confirm()` after seed). Agent: Sales → Quotations or Orders → open `BENCH-DUP` → control-panel cog / Actions → **Duplicate** (Odoo lands on the new draft copy, which inherits `partner_id=Bench Orig Co` and the two order lines) → change the **Customer** m2o on the copy from `Bench Orig Co` to `Bench Clone Co` via the autocomplete dropdown → **Save** (do NOT click Confirm). End state: exactly 2 `sale.order` rows — original (`client_order_ref='BENCH-DUP'`, `partner_id=Bench Orig Co`, `state='sale'`, two seeded lines intact) and new draft copy (`client_order_ref=False` because the field has `copy=False`, `partner_id=Bench Clone Co`, `state='draft'`, same two copied lines). |
| **Capability tested** | Cog/Actions `Duplicate` on a CONFIRMED `sale.order` (distinct from row 426's DRAFT-quotation duplicate), followed by a `partner_id` many2one edit on the resulting draft copy (no delivery-date tab, no statusbar click). The trap is NOT confirming the copy — all other `sale.*` duplicate tasks in the suite confirm after editing, so the default BU "Duplicate → edit → Confirm" policy would violate `state='draft'` on the copy. `trace_spec.forbidden_ops` lists `sale.order.action_confirm` + `sale.order.action_cancel` + `sale.order.action_draft` + `sale.order.unlink` to catch those deviations. |
| **Notes** | **Calibration: soft medium.** BU PASS on first shot (83.6s single-shot, F1=1.0, 0 postcondition failures, 0 forbidden writes) — BU correctly inferred "do NOT confirm" from the prompt and stopped after saving the partner change. The contrast-with-row-426 phrasing at the top of the prompt appears to have been enough. Useful as deterministic coverage of the "Duplicate on a confirmed record produces a DRAFT copy" + partner_id edit pattern without any Confirm step. **Match-key design**: same copy=False trick as rows 426 / 423 — `sale.order.client_order_ref` is `copy=False`, so seeding the source with `client_order_ref='BENCH-DUP'` keeps the original's entity_key stable while the duplicate's is `[null]`. `expected_state.json` anchors 3 atomic edits on the `[null]` key: `client_order_ref=null`, `partner_id='Bench Clone Co'`, `state='draft'`. **Forbidden ops**: since the task explicitly forbids confirming the copy, `sale.order.action_confirm` is in `forbidden_ops` — this also catches the failure mode where an agent clicks Confirm on the copy (the most likely default-policy mistake given every other `sale.duplicate_*` task in the suite confirms). `required_ops` is empty because `copy()` + `partner_id` write + `web_save` are all in optional_ops (BU typically uses `web_save` rather than a distinct `write`). **Oracle tactic**: JSON-RPC `search_read` on `[('client_order_ref','=','BENCH-DUP')]` to resolve the source id, then `/odoo/sales/<id>` direct-navigate — same pattern as row 426, avoids default `search_default_my_quotation=1` filter edge cases. Autocomplete-dropdown selection uses a page-level locator (portal) and filters out `Create "<value>"` quick-create entries to prefer the seeded existing partner. **Escalation ideas** to harden: (i) seed multiple partners containing the string "Bench Clone" so the autocomplete requires typing enough characters to disambiguate, (ii) require a `client_order_ref` rename on the copy in addition to the partner change, (iii) combine with a line-qty edit on the copy (currently lines are asserted unchanged), (iv) seed the source SO with an in-progress delivery or invoice to make the confirmed-→-duplicate path non-trivial (currently the confirmed SO has no downstream docs, so `copy()` is unblocked), or (v) use a name-similarity trap (`Bench Orig Company` vs `Bench Orig Co`) to force exact-match partner selection. |

---

## hr.generate_employee_card_set_badge_id

| Field | Value |
|---|---|
| **Row** | 425 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.3s wall clock, 1/1 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 86.4s wall clock, 23 non-forbidden writes, 0 forbidden, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | HR (`hr`) — `hr.employee.barcode` (view label "Badge ID"). |
| **Workflow** | Seed creates employee `Bench Worker Badge` with `barcode=False` and a best-effort `job_id` (first hr.job matching "developer"). Agent: Employees app → open `Bench Worker Badge` → click the **Settings** notebook tab (the tab with `name='hr_settings'`, `string='Settings'`, holding User / Approvers / Application Settings / Attendance-Point of Sale groups) → in the Attendance/Point of Sale group, type `EMPBENCH001` into the **Badge ID** field → Save. Optionally click the **Print Badge** button if it rendered (appears only after save because it is `invisible="not barcode"`) — best effort, not required for the check. |
| **Capability tested** | Tab switching on a form view + single-field alphanumeric text entry where the field carries a regex validator (`[A-Za-z0-9]{1,18}`). Verifies agents can navigate to a specific named notebook tab rather than the default first tab. |
| **Notes** | **Pre-flight pivot**: user request said `badge_id` but Odoo 19 `hr.employee` has **no `badge_id` field** — `addons/hr/models/hr_employee.py:206` defines it as `barcode = fields.Char(string="Badge ID", ...)` with a `_verify_barcode` constraint (`:1287-1291`) enforcing `re.match(r'^[A-Za-z0-9]+$', val) and len(val) <= 18`. Pivoted per pre-flight guidance, chose `EMPBENCH001` (11 chars, alphanumeric) to satisfy the validator — the same `hr_attendance` cookbook rule that makes `ATT-001` / `BADGE_42` invalid. **Calibration: small medium.** BU passed single-shot in 86s (F1=1.0), so this is a soft medium — primarily valuable for deterministic coverage of the hr_settings tab and the barcode validator. The "Print Badge" button is `invisible="not barcode"` so oracles/agents must save the form first before the button appears; prompt explicitly marks the click as optional. To harden to genuine hard tier would need (a) a wizard-mediated badge issuance flow (none in community), (b) multiple distractor employees with similar names (forces name disambiguation), or (c) a prefix rule the agent must derive from the prompt (e.g. "use the first 3 letters of department + random 5 digits") — that crosses into tier 3. Retained `primary_track=true`. |

---

## website_slides.duplicate_course_edit_add_slide

| Field | Value |
|---|---|
| **Task ID** | `website_slides.duplicate_course_edit_add_slide` |
| **Row** | 424 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 12.0s, 7/7 atomic edits matched, 0 postcondition failures, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 107.4s single-shot, 0 postcondition failures, 24 non-forbidden writes, StrictClean=True) |
| **F1** | 1.0 |
| **Odoo modules** | eLearning (`website_slides`) — `slide.channel` + `slide.slide` with cog/Actions `Duplicate` on the course form + `slide_category='article'` content row on the Content tab. |
| **Workflow** | Seed creates one published training `slide.channel` (`Bench Course Original`, `channel_type='training'`, `visibility='public'`, `enroll='public'`, `is_published=True`, `user_id=admin.id`) with exactly one existing published video `slide.slide` (`Bench Intro Video`, `slide_category='video'`, YouTube URL). Seed explicitly wipes auto-created `slide.channel.partner` rows so the attendee count stays clean. Agent: open eLearning → open `Bench Course Original` course form → cog/Actions → **Duplicate** → rename the copy to `Bench Course Spring` → save → open the **Content** tab → **Add Slide** → set Title=`Welcome slide`, Category=Article (or Document), short description body → save. End state: exactly two `Bench Course*` `slide.channel` rows; `Bench Course Spring` has exactly one non-category `slide.slide` named `Welcome slide` with `slide_category in ('article','document')`; `Bench Course Original` is unchanged (still has its single `Bench Intro Video` slide and its original name). |
| **Capability tested** | Cog/Actions `Duplicate` on a `slide.channel` (distinct from the cog on an individual `slide.slide`); post-duplicate rename on the correct record (the copy, not the original); then a second distinct UI flow (Content tab → Add Slide) where the agent must pick `slide_category` from the Article/Document dropdown and complete a second save. |
| **Notes** | **Calibration: easier than medium.** Browser-use solved single-shot in 107s with F1=1.0 and 0 postcondition failures — the course-level cog `Duplicate` is easy to find, and the Add Slide flow on the Content tab is unambiguous once the agent is on the right course. The "BU conflates course Duplicate with slide Duplicate" failure documented in `ODOO19_PATTERNS.md § website_slides` only bites when the prompt asks to duplicate a *lesson* (see row 386 `duplicate_lesson_to_new_section`), not a whole channel. **Oracle pattern**: JSON-RPC `slide.channel.copy([id])` → `write({'name': 'Bench Course Spring'})` → `slide.slide.unlink()` on the slides that `copy_data` brought along with the channel → `slide.slide.create({'slide_category': 'article', ...})`. Without the intermediate unlink of copied slides, `copy_data` leaves `Bench Intro Video` on the Spring copy and check.py rightly fails (spring_slides != ['Welcome slide']). **State-spec quirk**: `slide.channel.website_published` on a fresh `copy()` diffs as `op: "create"`, `norm_value: null` (not `true`), same as the `website_blog.create_post_with_cta_seo_schedule` null-vs-false quirk — `expected_state.json` encodes `null` to match the diff engine's observed output. **Escalation ideas** to harden into a real medium trap: (i) seed a distractor channel named `Bench Course Winter` so the agent must duplicate the correct one; (ii) require the new slide be `slide_category='quiz'` with one correct-answer question instead of an article (nested notebook editing); (iii) additionally move the duplicated copy into a new "Section" row on the Content tab, combining the section-is-a-slide quirk with the duplicate flow. |

---

## mrp_account.mo_consume_and_close_check_valuation

| Field | Value |
|---|---|
| **Row** | 421 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.6s wall clock, 0 steps) |
| **Browser-Use** | PASS (F1=1.0, 58.8s wall clock, ~9 BU steps) |
| **F1** | 1.0 |
| **Odoo modules** | Manufacturing (`mrp`), `stock_account`, `mrp_account` (auto-installed when `mrp` + `stock_account` are present) |
| **Workflow** | Seed a product category `Bench Val Real Time` with `property_valuation='real_time'` + `property_cost_method='average'`, a finished product `Bench Assembly` (`standard_price=0` by design — value must come from the component rollup), and two components `Bench Component 1` / `Bench Component 2` each at `standard_price=10` with 5×MO_QTY on-hand at the main WH stock location. BoM: 1 `Bench Assembly` = 1 × Component 1 + 1 × Component 2 (`consumption='flexible'`, `type='normal'`). Confirmed MO `MO-BENCH-VAL` for 1 unit. Stock valuation accounts pre-wired: `company.account_stock_valuation_id` → `140000 Stock Valuation`, `company.account_stock_journal_id` → general journal, `stock.location` of `usage='production'` → `500100 Cost of Production`, WH internal Stock location → Stock Valuation. Agent: open `/odoo/manufacturing`, open MO, click **Produce All** (single click — `qty_producing=1=product_qty`, components on-hand, no backorder wizard). MO state → `done`. `_action_done` on each `stock.move` runs `_set_value()` and (via `mrp_account`) `_cal_price()` to push `price_unit` on the finished move = sum of consumed component values; for `cost_method='average'` the finished move then values via `_get_value_from_production` → `quantity × price_unit`, giving `move.value == 20.0`. Each raw move gets `is_out=True` with `value == 10.0` (component standard price × qty). |
| **Capability tested** | Single-click MO close that exercises Odoo 19's renamed stock-valuation primitives (`stock.move.value` / `is_in` / `is_out` / `is_valued` + `product.value` history model instead of the pre-19 `stock.valuation.layer`), combined with the `mrp_account._cal_price` cost-rollup path that only fires when the finished product's `cost_method` is `fifo` or `average`. Check.py filters via `stock.move.production_id` (finished good, exactly 1 match, `is_in=True`, `value>0`) and `stock.move.raw_material_production_id` (raw moves, exactly 2, `is_out=True`, each `value≈10.0`) and asserts the finished value equals the sum of raw values (≈20.0). |
| **Notes** | **Odoo 19 model rename — critical design pivot**: the prompt/backlog asks to verify `stock.valuation.layer`, but that model was removed in Odoo 19 and replaced by `stock.move.value` (Monetary) + `stock.move.is_in` / `is_out` / `is_valued` (Boolean) + a new `product.value` history model. Check.py must use those fields directly; `env['stock.valuation.layer']` raises KeyError. **Cost-method trap**: `_cal_price` only rolls component values into `finished_move.price_unit` when `cost_method in ('fifo','average')`. Under `cost_method='standard'` the hard-coded branch `finished_move.price_unit = finished_move.product_id.standard_price` fires, so seeding the finished product at `standard_price=0` (per task spec) gives `value=0` and a postcondition failure. The seed uses `cost_method='average'` on the category so the rollup kicks in. **Location valuation accounts**: same invariant as `mrp_account.confirm_mo_check_account_move` — without `stock.location.valuation_account_id` wired to both the Production location (Cost of Production) and the WH Stock internal location (Stock Valuation), `_should_create_account_move` returns False on the finished move and the account.move side crashes; the seed defensively wires both even though this task only asserts the stock.move.value side. **Calibration: BU PASS on first shot** (~9 steps, 58.8s) — single-click Produce All with pre-reserved on-hand components is a low-friction pattern. Target for hard-tier was <40% pass; this is a calibration miss. To harden: (a) require a matching qty≠1 that forces a Produce/Done partial flow, (b) add a distractor MO in `Ready` state the agent might open by mistake, (c) use `consumption='strict'` so component-qty mismatch pops a modal, (d) require lot-tracked components so each component consumption needs a lot selection. Retained at hard/tier 3 per the pre-allocated STATUS slot. |

---

## account.reverse_journal_entry_from_general_ledger

| Field | Value |
|---|---|
| **Task ID** | `account.reverse_journal_entry_from_general_ledger` |
| **Row** | 423 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.1s wall clock, 3/3 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 390.3s single-shot, 0 postcondition failures, 44 non-forbidden writes, 0 forbidden). BU reported `success=False` in its own narrative loop but state/API trace scoring said PASS. |
| **F1** | 1.0 |
| **Odoo modules** | Accounting (`account`) — `account.move` (`move_type='entry'`), `account.move.line` (grouped misc journal-items report), `account.journal` (type=`general`, Miscellaneous Operations), `account.move.reversal` wizard (`refund_moves`). |
| **Workflow** | Seed: ensures a `Rent` expense account (code 6120) + `Bank` liquidity account (from the bank journal's `default_account_id`) + a `Miscellaneous Operations` general journal, grants admin the accountant groups so the Misc Journal Items report and the `Reverse Entry` header button render, then creates + posts a single balanced `account.move` with `move_type='entry'`, `journal_id=Misc`, `ref='BENCH-GL-REV'`, `date='2026-04-15'`, two lines (Rent debit 100.00, Bank credit 100.00). Agent intended path: Accounting → Accounting → Miscellaneous (grouped misc journal items report, `action_account_moves_journal_misc`) → expand the `BENCH-GL-REV` group header → click the move reference anchor to open the `account.move` form → click the **Reverse Entry** header statusbar button → in the `Reverse Journal Entry` wizard, leave Journal (Misc) and Reversal Date (today) at defaults → click the primary **Reverse** (`refund_moves`). End state: the source entry stays `state='posted'`, and a new `account.move` with `move_type='entry'`, `reversed_entry_id=source.id`, `state='posted'` (auto-posted by the wizard), `journal_id=Misc`, two lines with debit/credit swapped (Rent credit 100, Bank debit 100). |
| **Capability tested** | Drilling from a grouped report view (`account.move.line` grouped by `move_id`) into the underlying `account.move` form, then locating and using the move-type-specific header button `Reverse Entry` (visible only for `move_type='entry' and state='posted' and payment_state != 'reversed'`) rather than the `Credit Note` button used for customer/vendor invoices. Also exercises the wizard's `refund_moves` primary action with all defaults accepted (the wizard has a very small surface when `move_type='entry'` — `reason` is invisible, `Reverse and Create Invoice` is hidden, only Journal + Reversal Date + primary Reverse button). |
| **Notes** | **Calibration MISS at tier 3** — browser-use PASSED single-shot (F1=1.0, 390.3s, 0 postcondition failures, 44 non-forbidden writes). BU took the simpler **Accounting → Accounting → Journal Entries** list path (not the Miscellaneous Journal Items grouped report the prompt names), found the entry directly, clicked the header **Reverse Entry** button, and accepted wizard defaults. The prompt's "drill from the grouped misc report" trap did not force the agent off the easier path because the regular Journal Entries list also contains BENCH-GL-REV and the header `Reverse Entry` button is equally reachable from either form-view load. **Cookbook quirks discovered**: (a) In Odoo 19 Community there is **no** `account_reports` addon / no real "General Ledger" report — the closest equivalent is `action_account_moves_journal_misc` ("Miscellaneous"), an `account.move.line` list with `search_default_group_by_move=1` + `search_default_misc_filter=1`. The task's "from General Ledger" wording had to be recast as "from the Miscellaneous Journal Items report" to stay faithful to Community UI. (b) The `Reverse Entry` button is a **header statusbar button** with `name="%(action_view_account_move_reversal)d"`, `invisible="move_type != 'entry' or state != 'posted' or payment_state == 'reversed'"`. It is **NOT** the `Credit Note` button (`action_reverse`, visible only on `out_invoice`/`in_invoice` posted) and **NOT** in the cog Actions menu for form view — `action_view_account_move_reversal` has `binding_view_types="list,kanban"` so it only appears as a cog Actions entry when records are multi-selected on an `account.move` list/kanban, not on a form. (c) The `account.move.reversal` wizard form hides `reason` when `move_type == 'entry'` and hides `Reverse and Create Invoice` — so the only primary button is `refund_moves` (labeled "Reverse"). (d) `refund_moves` auto-posts the new entry (no separate Confirm click); the reversal's `state='posted'` appears directly in the state diff as a single `create`. (e) The reversal's generated `ref` follows the pattern `"Reversal of: <source.name>"` (no reason suffix when `reason` is empty/hidden for entries), e.g. `"Reversal of: MISC/2026/04/0001"` — use that as the entity_key for the reversal in `expected_state.json`. (f) Seed grants `account.group_account_readonly` / `group_account_invoice` / `group_account_user` to admin so the Misc Journal Items menu item and the `Reverse Entry` statusbar button render (`Reverse Entry` has `groups="account.group_account_invoice"`). **To harden into a real trap** (future iteration): (i) add several distractor misc entries (BENCH-GL-REV-A, BENCH-GL-REV-B, BENCH-GL-REV-TARGET) so BU must pick the right one by a specific date or reference, (ii) force a non-default **Reversal date** (e.g. last month's date) that BU must type into the date widget — a known hard pattern from `account.create_credit_note_and_reconcile`, (iii) force a non-default **Journal** (e.g. a second general journal named "Bench Audit Journal") requiring agent to change the journal many2one in the wizard, or (iv) seed the same source ref on two different journals and require the one whose journal is Miscellaneous. Retained at hard/tier 3 per the pre-allocated STATUS slot even though BU passed single-shot; record the calibration miss here for next iteration. |

---

## mail.create_alias_route_to_record

| Field | Value |
|---|---|
| **Task ID** | `mail.create_alias_route_to_record` |
| **Row** | 422 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 43.1s wall clock, 2/2 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 176.6s single-shot, 50 non-forbidden writes, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | `mail` (`mail.alias`, `mail.alias.domain`) + `crm` (`crm.team`, `crm.lead` as alias target model) + Settings form (`res_config_dev_tool` widget) + admin granted `base.group_no_one` so developer mode unlocks the Technical menu. |
| **Workflow** | Seed creates the `Bench Alias Team` `crm.team` with `use_leads=True`, ensures a default `mail.alias.domain` exists, releases any stale `mail.alias` with `alias_name='benchalias'` from prior runs, and explicitly adds `base.group_no_one` to admin (Technical Features group — only effective when `request.session.debug` is truthy, which seed cannot set). Agent: starts at `/odoo/settings`, scrolls to the **Developer Tools** panel at the bottom of the General Settings form and clicks **Activate the developer mode**. This calls `router.pushState({debug:1}, {reload:true})` — the page reloads with `?debug=1` and the **Technical** submenu now appears in the Settings navbar. Agent navigates Settings → Technical → Email → Aliases (or action URL `/odoo/action-mail.mail_alias_action`), clicks **New**, fills `alias_name='benchalias'`, sets `alias_model_id` by typing `crm.lead` and picking the autocomplete row labelled **Lead** (skipping the `o_m2o_dropdown_option` Create variants), fills `alias_defaults` textarea with the literal `{'team_id': <seeded-id>}`, sets `alias_contact='Everyone'` via the native `<select>`, saves. |
| **Capability tested** | (a) Recognising that the Technical → Email → Aliases menu is absent because developer mode is off (the seed intentionally leaves the session `debug` flag unset — `res.users.has_group('base.group_no_one')` is gated on `session.debug`, see `odoo/addons/base/models/res_users.py:1081`). (b) Locating the "Activate the developer mode" link in the Developer Tools widget rendered via `<widget name='res_config_dev_tool'/>` near the bottom of the base Settings form. (c) Surviving the hard page reload. (d) Filling a Python dict literal (`alias_defaults`) that must parse via `ast.literal_eval` and include the right `team_id`. (e) Disambiguating the `alias_model_id` many2one between the real `crm.lead` ir.model row (label **Lead**) and the quick-create variants that would silently spawn a new `x_crm.lead` custom model. |
| **Notes** | **Calibration MISS — BU passed single-shot in 176.6s.** BU correctly recognised the developer-mode gate, clicked Activate the developer mode, waited out the reload, navigated to Settings → Technical → Email → Aliases, created the alias with the right model/defaults/contact, and saved — F1=1.0, 50 non-forbidden writes, 0 postcondition failures. **Cookbook quirks solidified**: (1) `ir.model._description` for `crm.lead` is literally `"Lead"`, NOT "Lead/Opportunity" — searching the many2one for "Lead/Opportunity" returns zero real hits and only the quick-create variants, and clicking one triggers `ir.model.name_create(...)` spawning a new custom `x_crm.lead` model (characteristic failure signature: postcondition reports `alias_model_id is 'x_crm.lead', expected 'crm.lead'`). Use the technical name **`crm.lead`** for a unique hit via `_rec_names_search = ['name', 'model']`. (2) The autocomplete dropdown's Create / Search-More entries carry an extra class `o_m2o_dropdown_option` on the same `<li>` (see `addons/web/static/src/views/fields/relational_utils.js:489`). Playwright's `has_not=page.locator(...)` filters by descendants, NOT by a class on the element itself — the reliable filter is the CSS pseudo-class on the same element, i.e. `li.o-autocomplete--dropdown-item:not(.o_m2o_dropdown_option)`. (3) `base.group_no_one` on admin is only *effective* when `request.session.debug` is truthy — seeding the group is a necessary but not sufficient precondition; the UI toggle is still required. The widget calls `router.pushState({debug:1}, {reload:true})` causing a full hard reload — Playwright must `wait_for_url("**debug=1**")` + re-wait for `.o_action_manager` after the reload. (4) There are three variants of the Activate link ("Activate the developer mode", "… with assets", "… with tests assets") — use `.filter(has_not_text='assets').filter(has_not_text='tests')`. (5) The generic `mail.alias` form renders `alias_contact` as a native `<select>` (unlike `crm.team.alias_contact` which uses the custom `o_select_menu` widget) — `select.first.select_option(label='Everyone')` works here. (6) `alias_defaults` is a plain Text field rendered as a `<textarea>`; after interacting with the m2o above, a leftover autocomplete dropdown / tooltip frequently covers the textarea and Playwright reports `subtree intercepts pointer events` — dismiss via JS (`document.querySelectorAll('.o-autocomplete--dropdown-menu,.o-tooltip').forEach(el => el.remove())`) then `click(force=True)`. (7) `mail.alias.alias_name` is UNIQUE per `alias_domain_id`; seed must release any stale alias with the target name or the agent's Save hits `UniqueViolation`. **To escalate to real BU-failing hard tier** (future iteration): (i) require a multi-key `alias_defaults` dict (`{'team_id': N, 'user_id': M, 'tag_ids': [(6,0,[K])]}`) so the agent must compose a nontrivial Python literal with relational commands, (ii) require `alias_contact='followers'` AND adding a specific follower to the alias parent record, (iii) add a distractor `mail.alias` pre-seeded with alias_name `benchalias_old` pointing at `crm.team` (wrong model) so the agent must create a NEW row rather than editing the distractor, or (iv) require setting `alias_force_thread_id` to a specific lead id so incoming mail updates an existing record rather than creating one (adds a m2o-reference + integer pair to hunt for). |
---

## stock.create_physical_inventory_adjust_two_products

| Field | Value |
|---|---|
| **Row** | 427 |
| **Difficulty** | medium |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 30.8s, 8/8 atomic edits matched, 0 postcondition failures) |
| **Browser-Use** | PASS (F1=1.0, 97.4s single-shot, 15 steps, 0 postcondition failures, 25 non-forbidden writes) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (`stock`) — Physical Inventory list view (`action_view_quants` with `inventory_mode=True`) + `stock.quant.action_apply_all` + `stock.quant.action_apply_inventory` + follow-up `Inventory Adjustment Reference` dialog. Admin granted `stock.group_stock_multi_locations`. |
| **Workflow** | Seed creates 2 storable products (`Bench Prod X` with on-hand 15, `Bench Prod Y` with on-hand 25) at `WH/Stock` via `env["stock.quant"]._update_available_quantity`, and grants admin `stock.group_stock_multi_locations` so the virtual `Inventory adjustment` location is reachable and the Physical Inventory list surfaces the full location column. Agent opens **Inventory → Operations → Physical Inventory**, clicks the Counted Quantity cell on the Bench Prod X row and types `12`, presses Tab to commit, does the same on Bench Prod Y with `27`, then clicks **Apply All** in the list header. A `Apply / Update Quantities` confirmation dialog appears (single-row "Inventory Adjustment Reference" Char prompt); agent clicks the primary Apply button. Odoo posts the adjustments: `stock.quant.quantity` on the two WH/Stock rows becomes 12 and 27, and two `stock.move` records with `is_inventory=True, state='done'` are created (delta -3 for X, +2 for Y), which generate mirror `stock.quant` rows at the virtual `Inventory adjustment` location (+3 for X since WH/Stock lost 3 to the virtual bucket, -2 for Y since WH/Stock gained 2 from it). |
| **Capability tested** | Inline editable tree-cell commit on the Physical Inventory list (field `inventory_quantity`) for 2 specific rows, followed by a modal-dialog confirmation and a sanity check that `stock.quant.quantity` and `stock.move.is_inventory` have both been written. Same capability pattern as sibling row 405 (`stock.adjust_inventory_count_apply_moves`), but with a larger delta magnitude (-3 / +2 vs -2 / +1) and symmetric up/down adjustments. BU typically (a) opens the form view of a single quant instead of editing the list cell, (b) types into the cell but never commits (no Tab / Enter / blur), (c) edits On Hand instead of Counted Quantity, or (d) fills both cells correctly but clicks Save without ever clicking Apply — leaving `inventory_quantity_set=True` but `quantity` unchanged. |
| **Notes** | **Calibration MISS at tier 2** — browser-use PASSED single-shot (F1=1.0, 97.4s, 15 steps, 0 postcondition failures), unlike its sibling row 405 which failed on the same pattern. BU recovered from two mid-flow errors: (1) clicking the Counted Quantity cell first accidentally triggered a blank new-row creation (likely from pressing Enter/Tab in an inline list with create-in-place), producing a "Missing required fields" error on first Apply All — BU clicked **Discard** to kill the phantom row. (2) Clear-text failed silently (`"Text field clearing failed, typing may append to existing text"` warning from the harness) but typing still worked because Odoo's inline numeric widget selects-all on focus. The second Apply All surfaced the `Inventory Adjustment Reference` dialog and BU clicked `Update Quantities` (recognized the `button[name='action_apply']` label variant). Takeaways: (a) despite the same mechanics as row 405, this task's prompt is slightly clearer on commit (*"Press Tab (or click outside)"*) which may have helped BU avoid the stuck-editor bug; (b) the `Discard` button on phantom new rows is a reliable recovery path when inline-list Tab creates a blank entry — worth documenting for other editable-list tasks; (c) the task remains valid medium-tier but does NOT produce a reliable BU FAIL — to harden: add a 3rd distractor product `Bench Prod Z` whose Counted Quantity should NOT be changed, so the agent must filter/search rather than Apply All after blindly opening the list. **Cookbook quirks (confirmed from row 405)**: Counted Quantity cell binds to `stock.quant.inventory_quantity`, NOT `quantity` (which is stored-computed, writable only via `_update_available_quantity` or the Apply flow). Apply All opens a modal with primary `button[name='action_apply']` (label "Update Quantities" or "Apply" depending on localization). Downward adjustment produces `+qty` mirror quant at `Inventory adjustment`; upward adjustment produces `-qty`. Check.py gates on BOTH `stock.quant.quantity` matching the target AND a done `stock.move` with `is_inventory=True, state='done'` whose net signed delta equals the expected adjustment (so a BU run that updates quantity directly via `stock.quant.write` without going through Apply would fail the second gate). expected_state.json tracks 8 atomic edits: 2 `set` on the WH/Stock quants (12, 27) + 6 `create` edits on the mirror `Inventory adjustment` quants (3 per product: product_id, location_id, quantity — +3 for X, -2 for Y). state_spec.yaml uses `match_key=[product_id, location_id]` on `stock.quant`, which normalizes to composite display names (e.g. `["Bench Prod X", "WH/Stock"]` and `["Bench Prod X", "Inventory adjustment"]`). |
---

## mail.schedule_activity_on_partner_with_note

| Field | Value |
|---|---|
| **Task ID** | `mail.schedule_activity_on_partner_with_note` |
| **Row** | 428 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 22.4s wall clock, 0 atomic edits / 0 postcondition failures). Oracle calls `res.partner.activity_schedule(activity_type_id=<To-Do>, summary, note, date_deadline)` via call_kw, which is exactly what `mail.activity.schedule._action_schedule_activities` delegates to on the wizard Save. |
| **Browser-Use** | PASS (F1=1.0, 74.6s single-shot, 0 postcondition failures). BU clicked the **Activity** chatter button, typed summary, opened the date_deadline datepicker, typed `05/15/2026`, typed `Discuss Q2 plan` into the note editor, and clicked Save. BU's own `done` narrative correctly reported success; the runner's `agent_result.success=False` is from BU's internal loop bookkeeping, not from the state/trace scoring. |
| **F1** | 1.0 |
| **Odoo modules** | `mail` — `mail.activity`, `mail.activity.type` (default `To-Do`), `mail.activity.schedule` wizard, chatter Activity button. Also `res.partner` as the target mixin. |
| **Workflow** | Seed creates a fresh `res.partner` named `Bench Activity Partner` (is_company=True, email `hello@benchactivity.test`, company_type='company', street+phone filled) after idempotently unlinking any prior copies plus their chatter messages, activities, and attachments. Agent path: Contacts → click `Bench Activity Partner` row → form opens → chatter header `Activity` button → `mail.activity.schedule` wizard modal opens with `activity_type_id='To-Do'` preselected by default → fill `summary='Follow up call'` in the short Char field → click the `date_deadline` button (renders as "Apr 24" by default under today's TZ), which flips to an input, then type `05/15/2026` and Tab out → click into the `note` rich-text editor and type `Discuss Q2 plan` → click the footer **Schedule** primary button (`name="action_schedule_activities"`). End state: exactly one `mail.activity` row with `res_model='res.partner'`, `res_id=partner.id`, `activity_type_id.name='To-Do'`, `summary='Follow up call'`, `date_deadline=date(2026,5,15)`, `note` HTML containing `Q2 plan`. |
| **Capability tested** | Chatter Schedule-Activity wizard with four heterogeneous fields filled in one modal: (1) many2one with a default preselected (agents that re-pick `To-Do` still succeed, but agents that mistype into activity_type autocomplete can mis-select `Call`/`Meeting`/`Upload Document` instead — check.py gates on `activity_type_id.name=='To-Do'`), (2) short Char summary, (3) `date_deadline` button-to-input widget typed as US-locale `MM/DD/YYYY` (the deadline renders as a read-only button like "Apr 24" before first click, so the agent must click it once to get the input), (4) a `note` Html field rendered as an Owl rich-text editor (NOT a `<textarea>` — a generic `input.fill(...)` into the first visible field will target the summary, not the note). check.py also rejects agents that create **two** activities (e.g. one from the wizard and a second via `Mark as Done & Schedule Next`). |
| **Notes** | **Calibration MISS — BU passed single-shot in 8 steps.** BU found the chatter Activity button, correctly identified that `To-Do` was the default type, correctly typed into summary vs. note (didn't swap), and navigated the date_deadline button → input transition on the first try. The task was designed with two latent traps (note-vs-summary field swap, date format) but neither tripped BU on this run. Retained as medium/tier:2 for coverage: this is the only task in the suite that exercises the `mail.activity.schedule` wizard fully (summary + HTML note + typed date), so it complements `purchase.set_order_deadline_schedule_call_confirm` (schedules a Call activity with only summary+date, no note) and `crm.edit_opportunity_schedule_call` / `crm.create_opportunity_tag_schedule_call`. **Cookbook quirks confirmed during build**: (a) `mail.activity.type` for "To Do" is stored as **"To-Do"** (with hyphen), not "To Do" — matches the prior ODOO19_PATTERNS entry at line 1385. (b) `mail.activity.schedule._action_schedule_activities` calls `self._get_applied_on_records().activity_schedule(activity_type_id, summary, note, date_deadline, user_id)` — so posting to `res.partner.activity_schedule(...)` via call_kw is a faithful oracle shortcut that produces the same `mail.activity` row the UI would. (c) `res.partner` inherits `mail.thread` + `mail.activity.mixin`, so `activity_schedule` is available directly on partners (no dedicated subclass needed). (d) The wizard's `date_deadline` `_compute_date_deadline` defaults to today + the activity type's `delay_count`/`delay_unit` (`To-Do` defaults to 5 days from today), so the pre-fill is `today+5d`, NOT today — prompt must specify `05/15/2026` explicitly to override. (e) Check.py strips `<p>` / `<br>` HTML tags from `activity.note` before substring-matching `"Q2 plan"` because the Owl wysiwyg wraps typed text as `<p>Discuss Q2 plan</p>`. |

---

## website_blog.change_author_republish_post

| Field | Value |
|---|---|
| **Task ID** | `website_blog.change_author_republish_post` |
| **Row** | 430 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 19.0s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 11 non-forbidden writes, 0 forbidden) |
| **Browser-Use** | PASS (F1=1.0, 79.6s single-shot, 0 postcondition failures, 37 non-forbidden writes, 0 forbidden) |
| **F1** | 1.0 |
| **Odoo modules** | Website Blog (`website_blog`) — `blog.blog` (`Bench News`), `blog.post` (`Bench Blog Post`, `author_id` m2o to `res.partner`, `is_published`/`website_published=True`), `res.users` + `res.partner` (seeded internal user `Bench Editor`, login `bench_editor`, `group_ids` contains `base.group_user`). |
| **Workflow** | Seed: upserts the `Bench News` blog (reused across other `website_blog` tasks), creates/refreshes the `bench_editor` internal user (group `base.group_user`, partner auto-linked), then creates a published `blog.post` named `Bench Blog Post` with `author_id=admin.partner_id`, short `content` body, and `is_published=website_published=True`. Agent: Website → Blogs (Site > Blog Posts, `/odoo/blog-post-pages`) → open `Bench Blog Post` form → change the **Author** many2one in the Publishing Options group from `Mitchell Admin` to `Bench Editor` via autocomplete → Save. Must NOT flip the Published toggle off. End state: `blog.post.author_id` = Bench Editor's `res.partner` id; `is_published` and `website_published` remain True; name, blog, subtitle, content, post_date unchanged. |
| **Capability tested** | (a) Locating a top-level many2one field (Author) on a standard form layout — the Publishing Options group is a fixed right-hand column, not behind a tab or cog dialog. (b) Using the autocomplete dropdown to pick an existing partner without triggering the `o_m2o_dropdown_option` quick-create variants (`Create "Bench Editor"` / `Create and Edit…`). (c) Preserving the published state while saving — the form's Publish pill is a separate Owl toggle that must be left alone. `blog.post.author_id` is m2o to **`res.partner`**, not `res.users`; the agent must pick the partner auto-created from the `bench_editor` user rather than typing the login. |
| **Notes** | **Calibration as designed** — BU passed single-shot at 79.6s with F1=1.0 and 0 postcondition failures, exactly matching the tier-2 medium target for a clean "open form, swap a m2o, save" exercise. This is the paired easy-end calibration datapoint against the sibling task `website_blog.edit_post_change_author_add_tags_schedule` (which keeps the same author-swap surface but adds two tag chips + a scheduled Publishing date — that combination pushes BU into FAIL territory). Cookbook quirks reused from prior `website_blog` tasks: (a) `blog.post.author_id` is m2o to **`res.partner`** (default `self.env.user.partner_id`), so check.py must compare against `editor_user.partner_id.id`, not `editor_user.id`. (b) Writing `author_id` alone does NOT emit null-vs-false diffs on `is_published`/`website_published` because the published flags do not change (pre=post=True) — only the `author_id` edit surfaces in the state diff, giving a clean single-edit `expected_state.json`. (c) The `Bench News` blog is deliberately shared with other `website_blog` tasks (e.g. `create_post_with_cta_seo_schedule`); seed is idempotent (search-or-create + reactivate), cleanup does NOT unlink the blog. (d) `bench_editor` user + partner are left in place across runs to avoid orphan partners, same pattern as the alice/bob seed in `edit_post_change_author_add_tags_schedule`. **Escalation levers if this is ever promoted to hard** (future): (i) add a distractor second user `Bench Reviewer` with a similar name so the autocomplete row requires disambiguation, (ii) combine with a Publishing-date change (date picker, a known BU-fail pattern), or (iii) force the agent through the frontend Edit-via-Website route which exposes the Author field only in a sidebar Properties panel. |
---

## project_sms.send_reminder_sms_to_task_followers

| Field | Value |
|---|---|
| **Task ID** | `project_sms.send_reminder_sms_to_task_followers` |
| **Row** | 391 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 28.9s wall clock, 0 steps, 4/4 atomic edits matched, 0 postcondition failures, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.5, 360s timeout, `gave_up=True`, postconditions PASS, precision=0.333, recall=1.0). BU sent the same body to both recipients correctly but kept clicking Send Now / reopening the composer after success, so the diff observed 12 `sms.sms` create edits vs the 4 expected — duplicate-send penalty on precision. |
| **F1** | 0.5 |
| **Odoo modules** | `sms` (not in base_modules.txt) + auto-installed bridge `project_sms` (`auto_install=True`, `depends=['project','sms']`). Seed calls `button_immediate_install('sms')` which pulls `project_sms` in transitively. |
| **Workflow** | Seed creates project `Bench SMS Project` (`allow_recurring_tasks=False`), a project-scoped stage `Review` (required — without a stage the tasks fall into a collapsed `None` kanban group and disappear from the default list view), two US partners `Bench Reviewer A` / `Bench Reviewer B` with phones `+16175551200` / `+16175551201` and `country_id=base.us`, and two tasks `Urgent Review Request — Reviewer A` / `Urgent Review Request — Reviewer B` pinned to the stage, each with `partner_id` set to its reviewer. `message_subscribe` adds both reviewers as followers on both tasks (cosmetic only — mass-mode SMS does NOT use followers). Agent: open `/odoo/project` → click `Bench SMS Project` kanban card → switch to list view → tick both reviewer row checkboxes → cog Actions → **Send SMS** → type `Reminder: please review by EOD` → **Send now** (mass-mode secondary button `name=action_send_sms_mass_now`). Produces one `sms.sms` per selected task (2 total) with `number` = each reviewer's sanitized E.164 phone and `body` = the reminder text, linked via `mail_message_id` to a `mail.message` on `project.task` with `message_type='sms'`. |
| **Capability tested** | Multi-record selection on a project's task list, cog/Actions menu-driven `sms.composer` binding in `mass` mode, mass-mode secondary `Send now` button (vs the primary `Put in queue` that persists to queue without sending). Also exercises the `project_sms` auto-install bridge whose binding view supplies `{'default_composition_mode':'mass','default_mass_keep_log':True,'default_res_ids': active_ids}`. |
| **Notes** | **Design pivot from original spec** — the user spec said *"open task, chatter, click Send SMS, composer opens with recipients=followers"*. That framing is incorrect for `project_sms`: the bridge binds `sms.composer` via `binding_model_id=project.task` with `composition_mode='mass'`. Mass mode sends ONE sms per selected record using `_sms_get_recipients_info` → `_mail_get_partners` → `partner_id.phone`; followers are NOT recipients. The chatter itself exposes no Send SMS button — the only entry point is the cog Actions menu (`binding_view_types=list,kanban,form`). To satisfy the "≥2 sms.sms" check, the task seeds two tasks with distinct `partner_id`s and asks the agent to multi-select both from the project's tasks list. Followers are still added via `message_subscribe` so the "reviewer" framing remains coherent if a human tester expands followers. **Stage seeding is mandatory** — without `stage_id` the tasks default to a collapsed `None` group in the project tasks kanban (via `project.task.type.group_expand`) and the list view also hides them until the agent expands the group; a seeded `Review` stage pinned to the project keeps both tasks visible on first render. **sms.sms persistence invariant** (re-confirmed from `crm_sms` / `stock_sms` cookbooks): `sms.sms` rows are created inside `_action_send_sms_mass` with `body`, `number`, `mail_message_id` populated BEFORE `.send()` is called; `.send()` only flips `state` from `outgoing` to `error` when IAP has no credits. check.py asserts persistence + number + body + linkage and ignores `state`/`failure_type` (both in `state_spec.ignore_fields`). **Phone sanitization** — US E.164 phones `+16175551200/01` with `country_id=base.us` on the partner ensure `_phone_format` sanitizes to the input verbatim; a missing country or a truncated number would leave `sanitized=False` and route the sms into `state='canceled'` with `failure_type='sms_number_missing'`, still producing a row but breaking human-readable flow. **BU failure mode** — BU sent both SMSs on the first Send Now click (F1 postconditions PASS) but the agent kept re-opening the cog menu and clicking Send Now, producing 4 extra `sms.sms` creates and dragging precision to 0.333. This is a natural "wizard completion detection" failure for mass-send flows where Odoo's modal auto-closes on success but leaves the control panel selection intact, tempting the agent to retry. **Oracle selectors**: `button[name='action_send_sms_mass_now']` in the modal footer is the canonical Send Now button; falling back to `button:has-text('Send now')` is safe because the other footer buttons are `Put in queue` and `Discard`. |

---

## hr_timesheet.log_time_for_2_days_approve_via_manager

| Field | Value |
|---|---|
| **Task ID** | `hr_timesheet.log_time_for_2_days_approve_via_manager` |
| **Row** | 429 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | `hr_timesheet` (Community, **not in `base_modules.txt`** → not installed in `benchmark_base`) + `hr_timesheet_sheet` / `timesheet.sheet` (**Enterprise-only**, source absent from `addons/`). |
| **Workflow** | Intended: Seed project `Bench Approve Proj` + task `Development` + employee `Bench Dev` (internal user with `hr_timesheet.group_hr_timesheet_user` and `hr.group_hr_user`) whose parent = admin's employee. Agent switches to Bench Dev, creates 2 `account.analytic.line` rows on different dates (2026-04-15 / 2026-04-16, `unit_amount=8.0`) against that task, opens the containing weekly `timesheet.sheet` and clicks **Submit to Manager** (`draft → confirm`). Admin switches back in, opens the pending sheet from `Timesheets → To Approve`, clicks **Approve** (`confirm → done`). |
| **Capability tested** | Multi-day timesheet logging + submit-to-manager + manager-approve lifecycle crossing two user roles — targets the `timesheet.sheet` state machine (`draft → confirm → done`) plus two analytic lines pinned to one sheet. |
| **Notes** | **Blocked on two stacked gaps**: (1) `hr_timesheet_sheet` (a.k.a. `timesheet.sheet`, which supplies `Submit to Manager` + `Approve` on weekly sheets and the `state`/`sheet_id` fields on `account.analytic.line`) is an **Odoo Enterprise-only** addon. Its source is not vendored under `addons/` in this Community checkout — no `hr_timesheet_sheet/` directory exists and `ir.module.module` would report it as uninstallable. (2) Even the base `hr_timesheet` addon (whose source *is* present) is **not listed in `benchmark/base_modules.txt`**, so the `benchmark_base` snapshot does not install it: `/odoo/timesheets` menu and the Timesheets tab on `project.task` are absent in the stock DB. The suggested fallback from the task brief ("manager marks analytic lines as validated via cog Actions / write `validated=True`") does **not** work: Community `hr_timesheet` has no `validated`, `state`, or `sheet_id` field on `account.analytic.line` (verified by grepping the hr_timesheet models + views). Without an Enterprise submit/approve mechanism there is no semantically meaningful approval signal to assert in `check.py`. Task skeleton is committed with BLOCKED guards that short-circuit `seed`, `check`, `oracle`, and `cleanup` with diagnostic errors (same precedent as rows 350/351/352/387). To re-enable: (a) add `hr_timesheet` to `benchmark/base_modules.txt` and rebuild `benchmark_base`, AND (b) vendor the Enterprise `hr_timesheet_sheet` addon (or replace it with an equivalent submit/approve mechanism — e.g. an `approvals`-based wrapper around `account.analytic.line`). |
---

## purchase.confirm_rfq_receive_full_three_way_match

| Field | Value |
|---|---|
| **Task ID** | `purchase.confirm_rfq_receive_full_three_way_match` |
| **Row** | 437 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.9s wall clock, 2/2 atomic edits matched, 0 postcondition failures, StrictClean=True, 25 non-forbidden writes, 0 forbidden) |
| **Browser-Use** | PASS (F1=1.0, 74.0s single-shot, 2/2 atomic edits matched, 0 postcondition failures, StrictClean=True, 30 non-forbidden writes, 0 forbidden). BU reported `success=False` / `steps=0` in its own narrative loop (agent framework bookkeeping quirk), but state/API-trace scoring both said PASS. |
| **F1** | 1.0 |
| **Odoo modules** | Purchase (`purchase`) — `purchase.order`, `purchase.order.line`, `product.product` + `product.template` (storable `type='consu'` + `is_storable=True`, `purchase_method='receive'`, `invoice_policy='delivery'`), `res.partner` (`supplier_rank=1`), `stock.picking` (auto-generated by `purchase.order._create_picking`). |
| **Workflow** | Seed creates vendor `Bench Supplier Inc` (email `orders@benchsupplier.example.com`, `supplier_rank=1`), two storable products `Bench 3WM Bracket` (25.00) and `Bench 3WM Fastener Kit` (5.00) both with `purchase_method='receive'` for 3-way match semantics, and a draft RFQ `BENCH-RFQ-3WAY-2` (partner_ref + origin both pinned) with two lines qty=8 / qty=12 and taxes cleared `(5,0,0)`. Agent: `/odoo/purchase` → open RFQ row with Vendor Reference `BENCH-RFQ-3WAY-2` → click **Confirm Order** statusbar button → click **Receive Products** smart button (`action_view_picking`, redirects to the single auto-generated `stock.picking`) → click **Validate** on the receipt statusbar. End state: `purchase.order.state='purchase'`, `purchase.order.invoice_status='to invoice'` (3-way match READY — received but not billed), `stock.picking.state='done'`, both `purchase.order.line.qty_received` = ordered demand. No vendor bill created. |
| **Capability tested** | (a) Navigation from list-view to form via the Vendor Reference column (partner_ref pinned for deterministic row identification), (b) statusbar `button_confirm` invocation, (c) smart-button redirect pattern (PO → sole picking via `action_view_picking`), (d) `stock.picking.button_validate` on an auto-filled receipt (no cell edit, no backorder dialog expected for full demand). |
| **Notes** | **Calibration anchor as designed** — medium tier, ~60% projected pass rate, anchor for the "clean confirm + smart-button + validate" baseline. BU passed single-shot at 74s with F1=1.0, confirming this is a calibration floor for the purchase receipt family. **Distinct from sibling tasks**: (i) `purchase.create_rfq_receive_invoice_3way_match` (row 397, hard) does the FULL 3-way including bill creation — this task stops at receipt validation and explicitly forbids vendor bills. (ii) `purchase_stock.confirm_rfq_receive_full` uses a different vendor (Pioneer Industrial Supply) and does NOT assert `invoice_status='to invoice'` — this task's check.py validates that field specifically. (iii) Inventory-level partials (e.g. `purchase_stock.receive_partial_scrap_damaged_units`) force backorder dialogs and cell edits; this task has neither. **State-diff design**: `state_spec.purchase.order.match_key=[partner_ref]` gives a deterministic entity_key `['BENCH-RFQ-3WAY-2']`, and the two tracked fields `state` (draft→purchase) + `invoice_status` (no→to invoice) generate exactly 2 atomic edits — oracle and BU both produce the same clean diff. **Cookbook quirks surfaced**: (a) `purchase.order.invoice_status` transitions `'no' → 'to invoice'` via `_compute_qty_received` chain when `stock.picking.button_validate` flips move `state` to `'done'` and `_compute_qty_received` populates `purchase.order.line.qty_received`; this chain is the canonical 3-way-match READY signal and is cleanly observable in the state diff. (b) Products with `purchase_method='receive'` ensure that `purchase.order.line.qty_to_invoice` computes off `qty_received` rather than `product_qty`, which is what makes invoice_status flip to `to invoice` at receipt validation rather than at PO confirmation. (c) The `Receive Products` smart button (`action_view_picking`) label is stable across Odoo 19 Community/Enterprise; when exactly one picking exists, the action redirects straight to the form view — no intermediate list. (d) Clearing `tax_ids` via `[(5,0,0)]` in seed keeps `amount_total` deterministic across company tax configs even though this task doesn't assert totals (defensive). **Calibration risk (for future medium-hard promotion)**: add (i) a distractor RFQ for the same vendor so `click_list_row` by partner_ref is disambiguation-sensitive, (ii) flip one line's `purchase_method` to `'purchase'` to create mixed 3-way / 2-way semantics, or (iii) add a date-pinned `date_planned` mismatch so validation forces a wizard — the clean smart-button → Validate shape of this baseline task is trivially BU-solvable. |
---

## hr.create_department_assign_manager_two_employees

| Field | Value |
|---|---|
| **Task ID** | `hr.create_department_assign_manager_two_employees` |
| **Row** | 438 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 42.7s wall clock, 4/4 atomic edits matched, 0 postcondition failures, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 177.4s wall clock, `gave_up=False`, 4/4 matching + 2 EXTRA edits, 1 postcondition failure). BU created the department with the correct manager AND successfully set both workers' departments to a `Bench Ops` — but it created **two** separate `hr.department` rows both named `Bench Ops`: the first with manager=Bench Dept Manager and Worker 1 attached, the second with `manager_id=False` and Worker 2 attached. The count check (`members_in_new_dept != 2`) caught the split. |
| **F1** | 0.0 |
| **Odoo modules** | HR (in base) |
| **Workflow** | Seed 3 `hr.employee` rows — `Bench Dept Manager`, `Bench Dept Worker 1`, `Bench Dept Worker 2`, all with `department_id=False`. Agent: `/odoo/employees` → left sidebar **Departments** → **New** → Name=`Bench Ops`, Manager=`Bench Dept Manager` → Save → back to Employees list → open `Bench Dept Worker 1` → Department=`Bench Ops` → Save → open `Bench Dept Worker 2` → Department=`Bench Ops` → Save. End state: one `hr.department` row named `Bench Ops` with `manager_id=Bench Dept Manager`, and exactly 2 `hr.employee` rows (Worker 1 and Worker 2) with `department_id` pointing to that department. |
| **Capability tested** | Create-parent-then-edit-2-separate-children multi-step nav without UI shortcut (the agent must leave the department form, return to the main Employees list, and open two distinct employee forms). Mirrors the row 321 three-employee variant but with only 2 workers and distinct entity names (`Bench Dept *` vs `Eng *`, `Bench Ops` vs `Bench Engineering`, `Bench Dept Manager` vs `Mike Manager`) so that both tasks can run back-to-back in the same DB without seed collisions. |
| **Notes** | **Distinct-from row 321** via complete rename of all seeded entities and by dropping the seeded "Operations" pre-department (this variant starts with `department_id=False` on all 3 employees so the agent SETS rather than REASSIGNS). **BU failure mode** — classic create-from-name-with-autocomplete trap: when BU typed "Bench Ops" into Worker 2's Department m2o field, the autocomplete's "Create 'Bench Ops'" quick-create item was clicked instead of the pre-existing department row. Result: two identically-named `hr.department` rows — id=2 with the manager and Worker 1 attached, id=3 with `manager_id=False` and Worker 2 attached. `check.py`'s `search([("name","=","Bench Ops")], limit=1)` picks the lower-id row (the one WITH the manager) and `search_count([("department_id","=",dept.id)])` returns 1, flagging the split. The diff engine handles name-dup entity keys with `#dup1` suffix, so the second Bench Ops surfaces as 2 extra atomic edits (`name=Bench Ops` + `manager_id=None`), driving F1 to 0.0 despite all 4 expected edits matching. **Calibration** — well-calibrated medium (~60% expected pass): BU completes the navigation sequence but trips on the duplicate-create trap, exactly the kind of attention-to-detail failure this multi-step task targets. The alternate "from the department's Members tab" path (adding members via the department form's reverse o2m) also works and is the path the calibration-risk note flagged, but BU here chose the canonical per-employee path and still failed. **check.py structure** mirrors row 321 with an additional `search_count(department_id=dept.id)==2` invariant (needed because BU's duplicate-department bug would otherwise leave the primary dept with correct manager and only 1 member, silently passing if we only asserted "workers have department named Bench Ops"). Manager is explicitly excluded from the new department (`mgr.department_id.name != NEW_DEPT_NAME`) per prompt rule "Bench Dept Manager stays without a department". |
---

## project.set_task_priority_urgent_assign_tag

| Field | Value |
|---|---|
| **Task ID** | `project.set_task_priority_urgent_assign_tag` |
| **Row** | 439 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 23.1s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 25 non-forbidden writes, 0 forbidden). Oracle toggled the first `.o_priority_star` via Playwright `.click()` and added the existing `Bug` tag through the m2m autocomplete (skipping any `Create` quick-create row). |
| **Browser-Use** | PASS (F1=1.0, 72.9s single-shot, 0 postcondition failures, 28 non-forbidden writes, 0 forbidden). BU found the task card in the seeded `To Do` stage, opened the form, clicked the star widget a single time (priority '0' → '1'), opened the Tags autocomplete, picked the existing `Bug` tag, and saved. |
| **F1** | 1.0 |
| **Odoo modules** | `project` — `project.project` (`Bench Prio Project`), `project.task` (`Fix critical bug`, `priority` Selection `0..3`, `tag_ids` m2m to `project.tags`), `project.task.type` (shared default stages `To Do`/`In Progress`/`Done` pinned to the project), `project.tags` (`Bug`). |
| **Workflow** | Seed: idempotently unlinks any prior task named `Fix critical bug`, drops the old `Bench Prio Project` (cascading residual tasks), and removes any seeded `Bug` tag. Re-creates the project, ensures the three default stages (`To Do`/`In Progress`/`Done`) are pinned to the project via `type_ids` (each `project.task.type` search-or-create-then-link), creates one `project.tags` named `Bug`, and inserts one `project.task` with `stage_id=To Do`, `priority='0'`, `tag_ids=[(5,0,0)]`, plus a descriptive body. Agent path: Project (`/odoo/project`) → click `Bench Prio Project` kanban card → task kanban grouped by stage → click `Fix critical bug` card → form opens → click the **first** star in the `.o_field_widget[name='priority']` widget (toggles priority '0' → '1') → Tags m2m input → type `Bug` → pick the existing `Bug` autocomplete row (NOT `Create "Bug"`) → Save (cloud icon / Ctrl+S). End state: one `project.task` named `Fix critical bug` on `Bench Prio Project` with `priority='1'`, `tag_ids` containing exactly one tag (`Bug`), exactly one `project.tags` named `Bug` in the DB, and exactly one task on the project. |
| **Capability tested** | Easy-tier calibration anchor: (a) single priority-star click in the Odoo priority widget (4-level `0..3` Selection rendered as 3 clickable stars — clicking the N-th star sets priority=N, so a greedy agent clicking all three lands on priority='3' = Urgent and fails check.py), (b) many2many_tags autocomplete picking an EXISTING tag over a dangling `Create "Bug"` quick-create row (`project.tags.create` is in `forbidden_ops` so quick-creating surfaces as a HarmfulWrite). Both sub-capabilities appear individually in the suite (`project.update_task_priority`, `project.create_task_assign_tags_deadline`) but this is the easy-tier smoke that combines them on a single existing record without any date/user fields. |
| **Notes** | **Calibration as designed** — BU passed single-shot at 72.9s with F1=1.0 and 0 postcondition failures, matching the easy/tier-1 target (<60s best case; 72.9s well under the 300s limit). **Prompt precision mattered**: first draft ("set to High/Urgent, priority='1'") was ambiguous because Odoo's `project.task.priority` Selection labels `'1'`=`Medium priority`, `'2'`=`High priority`, `'3'`=`Urgent` (see `addons/project/models/project_task.py:154`). BU's first run interpreted "High/Urgent" as priority `'2'` and clicked two stars; check.py correctly rejected `priority='2'`. Revised prompt says **"click ONLY the first star"** and **"exactly one filled star"** with explicit "do NOT click a second or third star" — this maps uniquely to the task spec's `priority='1'`. **Stage seeding is mandatory** (same cookbook lesson as `project_sms.send_reminder_sms_to_task_followers`): without a seeded stage the task falls into a collapsed `None` group in the default kanban view (via `project.task.type.group_expand`) and the card isn't clickable from the project drill-down. Pinning `To Do`/`In Progress`/`Done` to the project via `type_ids` / `project_ids` (linking existing default types when present) keeps the kanban grouping stable. **Priority widget selector**: `.o_field_widget[name='priority'] .o_priority_star` returns three anchor nodes — `.first.click()` sets priority='1' deterministically. Fallback evaluate-JS path sets the hidden `<input>` to `'1'` and dispatches `input`/`change` for the edge case where the stars aren't hydrated yet. **expected_state.json** is a single `op=set` entry on `priority`; `active` and `name` are unchanged (task already exists), so no `op=create` entries appear unlike the sibling `project.create_task_with_deadline_tags_assignees`. `tag_ids` is a m2m and is deliberately validated only via check.py (not in expected_state) because the diff engine's m2m entity-key format is brittle across runs; check.py asserts the `Bug` tag presence by case-insensitive name plus duplicate-tag detection. **Environment quirk observed during build**: the worktree `.venv` was pre-warmed only with `playwright` + `pyyaml`; Odoo's startup demands `babel`, `browser-use`, and the full `requirements.txt` stack. Running `uv pip install -r requirements.txt && uv pip install browser-use` once re-hydrated the venv and unblocked both oracle and BU runs. |
---

## stock.delivery_transfer_validate_partial_backorder_no

| Field | Value |
|---|---|
| **Task ID** | `stock.delivery_transfer_validate_partial_backorder_no` |
| **Row** | 436 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 35.0s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 49 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 360.0s wall clock `gave_up=True`, 3 postcondition failures, 206 API calls, 92 non-forbidden writes, 0 forbidden). BU's inline "Quantity" cell edit never persisted — `Text field clearing failed, typing may append to existing text` warning fired on every retry, BU clicked Validate anyway, the Create Backorder dialog appeared, BU clicked the **primary/default 'Create Backorder'** button (THE TRAP), creating a backorder `WH/OUT/00002` for 2 units AND leaving Quantity (Done) at 5 instead of 3. BU then tried to recover by cancelling + creating new receipts / deliveries (observed `WH/IN/00001`, `WH/IN/00002`, `WH/OUT/00001`, `WH/OUT/00002` extras), never reached the target state, timed out at 360s. |
| **F1** | 0.0 |
| **Odoo modules** | Inventory (`stock`) — `stock.picking` (outgoing) + `stock.move` + `stock.move.line` + `stock.backorder.confirmation` wizard (Create Backorder / No Backorder dialog). |
| **Workflow** | Seed creates customer `Bench Ship Co`, storable product `Bench Pick Item` (`type='consu', is_storable=True, tracking='none'`) with 5 units on-hand at `WH/Stock` via `env["stock.quant"]._update_available_quantity`, and a Ready/reserved outgoing delivery picking pinned to `name='WH/OUT/BENCH-BACKORDER-NO'` for 5 units to the customer. The picking is `action_confirm` + `action_assign`'d so `state='assigned'` and the single move line is fully reserved (quantity=5). Agent: Inventory → Delivery Orders → open `WH/OUT/BENCH-BACKORDER-NO` → click the inline Quantity cell on the single `Bench Pick Item` move row, change 5 → 3, Tab-commit → click **Validate** in the header → on the **Create Backorder?** dialog, click the **secondary 'No Backorder'** button (NOT the primary/default 'Create Backorder'). End state: picking `state='done'`, move.quantity=3, NO backorder `stock.picking` with `backorder_id=original.id`, on-hand at WH/Stock dropped from 5 to 2. |
| **Capability tested** | Hard-pattern wizard dialog with a **non-default secondary button** — the canonical "backorder decline" counterpart to row 395 (`stock.transfer_reserved_to_ready_partial_backorder`, which requires the *primary* Create Backorder button). Per `ODOO19_PATTERNS.md §Stock`: *"Backorder dialog: 'Create Backorder' is the default/primary button in Odoo 19"* — an agent that reflexively clicks the highlighted/left button creates an unwanted backorder. Also exercises the Odoo 19 inline cell-edit quirk on `stock.move.quantity` (cell doesn't always commit on blur — BU's clear-text failure loop on this exact cell is the same pattern that fails row 395). This is a medium/tier-2 because the picking is pre-reserved (no Check Availability step, no Detailed Operations popup required) — just inline-cell + dialog secondary button. |
| **Notes** | **Calibration HIT as designed** — clean single-shot BU FAIL at 0.0 F1 with 3 distinct postcondition failures (qty_done wrong, extra picking exists, on-hand unchanged). BU exhibited two compounding failures: (a) the inline quantity cell edit loop hit Odoo 19's persistence quirk — harness warning *"Text field clearing failed, typing may append to existing text"* fired 3+ times — and BU never confirmed the cell committed before hitting Validate; (b) when the Create Backorder dialog appeared, BU defaulted to clicking the **primary** button label it recognized ("Create Backorder"), which is EXACTLY the trap the task was designed for. The seed is deliberately minimalist (single customer, single product, single move line, pre-reserved, on-hand=demand) so there is only ONE way the task can fail that way — no ambiguity on which picking or which row to touch. **Task distinction from row 395**: row 395 requires Check Availability → Detailed Operations popup → Save → Validate → **'Create Backorder' (PRIMARY)**; row 436 skips straight to inline-edit → Validate → **'No Backorder' (SECONDARY)**. Together they provide orthogonal calibration of the backorder dialog's two paths. **Cookbook quirks confirmed**: (a) `stock.backorder.confirmation` wizard footer has `name='process'` (primary, Create Backorder) + `name='process_cancel_backorder'` (secondary, No Backorder) — the latter is the required_op in `trace_spec.yaml`; forbidden_ops lists `stock.backorder.confirmation.process` to catch the default-click trap at the trace layer. (b) `state_spec.yaml` `match_key: [name, partner_id, backorder_id]` produces entity_key `["WH/OUT/BENCH-BACKORDER-NO", "Bench Ship Co", null]` on the original picking — `backorder_id=False` normalizes to JSON `null`, and since NO backorder is expected, no second entity appears in expected_state.json (clean single-edit `state: set confirmed→done`). (c) Seed pins `picking.name='WH/OUT/BENCH-BACKORDER-NO'` directly (rather than relying on Odoo's auto `WH/OUT/00001` sequence) so the prompt can refer to the exact reference string the UI shows, and so check.py can locate the picking by name unambiguously even after retries create sibling `WH/OUT/00002` rows. (d) `action_assign()` on seed means the picking arrives in state `assigned` with a single move_line reserved for the full 5 — the agent does NOT need Check Availability (prompt explicitly says so), removing that step isolates the trap to the inline-edit + dialog choice. (e) check.py's on-hand sanity check (5 → 2) catches the case where the agent somehow finishes with state=done but qty_done=5 (full shipment) OR state=done but quants untouched (cancelled without shipping). |
---

## mass_mailing.create_mailing_select_list_schedule_send

| Field | Value |
|---|---|
| **Task ID** | `mass_mailing.create_mailing_select_list_schedule_send` |
| **Row** | 443 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 17.1s wall clock, 4/4 atomic edits matched, 0 postcondition failures, 35 API calls, 14 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle uses JSON-RPC `mailing.mailing.create` + `mailing.mailing.schedule.date.create` + `action_schedule_date` to bypass the WYSIWYG iframe body editor + datetime widget (both proven fragile under Playwright per ODOO19_PATTERNS §DateTime and §Mass Mailing). |
| **Browser-Use** | FAIL (F1=0.0, 211.8s wall clock, `gave_up=False`, 4/4 matching atomic edits + 0 extra, StrictClean=True, 67 API calls, 32 non-forbidden writes). BU successfully created the mailing (subject=`Spring Promo`, mailing_model_name=`mailing.list`, state=`in_queue`, schedule_type=`scheduled`, Mailing List attached) — all 4 expected diff edits matched. **Single postcondition failure**: `schedule_date = 2026-05-20 02:00:00 UTC` instead of the expected `2026-05-20 10:00:00` (in admin's tz, which is UTC in the benchmark base). BU's final self-report claimed the Scheduled Date was `05/20/2026 10:00:00`, but the datetime widget silently committed `02:00` — classic datetime-widget drift (ODOO19_PATTERNS §DateTime button-vs-input dual render). Postcondition failure forces F1=0.0 per the eval engine's postcondition-priority rule (eval.py L503-506). |
| **F1** | 0.0 |
| **Odoo modules** | `mass_mailing` — `mailing.mailing` (create from scratch), `mailing.list` + `mailing.contact` (seeded audience), `mailing.mailing.schedule.date` wizard (datetime widget + `action_schedule_date` footer button). |
| **Workflow** | Seed: cleanup any prior run, create `mailing.list` named `Bench Newsletter Subs` and 3 `mailing.contact` rows subscribed to it (`spring1/2/3@bench.test`). Agent path: `/odoo/email-marketing` → **New** button → fill Subject=`Spring Promo` → keep default Recipients=`Mailing List` (do NOT change) → in the `Mailing Lists` autocomplete, pick the seeded `Bench Newsletter Subs` row (NOT the quick-create `Create "..."` entry) → click into the iframe WYSIWYG body editor and type `Save 20%` (clear placeholder text first) → click **Schedule** in the top control panel (NOT Send, NOT Send a Sample Mail) → a small `mailing.mailing.schedule.date` dialog opens titled "When do you want to send your mailing?" with a single `Send on` datetime field → clear the pre-filled value, type `05/20/2026 10:00:00` → click the primary **Schedule** button in the dialog footer to confirm. End state: `mailing.mailing.state='in_queue'`, `schedule_type='scheduled'`, `schedule_date` is May 20 2026 10:00 in admin's tz (UTC in the benchmark base), `mailing_model_name='mailing.list'`, `contact_list_ids` includes `Bench Newsletter Subs`, `body_html` contains `Save 20%`. |
| **Capability tested** | **Hard triad**: (a) create-from-scratch mailing.mailing with DB-required `email_from` and paired `mailing_model_id`/`mailing_model_name` fields (Odoo 19 DB constraint per ODOO19_PATTERNS L49-50); (b) WYSIWYG iframe body editor (not a plain `<textarea>` — agent must click INTO the iframe editable region to type, a known Odoo-mail quirk); (c) the `mailing.mailing.schedule.date` wizard's datetime widget (the datetime field uses the button-vs-input dual render pattern from ODOO19_PATTERNS §DateTime + formatter-aware tz conversion). The combination of three fragile widgets in one flow produces the "agent-believes-it-succeeded-but-didn't" failure mode where BU's final message claims `10:00` but the DB stores `02:00 UTC`. Distinct from row 389 (`mass_mailing.duplicate_mailing_edit_subject_send`) which tests Duplicate→edit→Send (no Schedule wizard). Distinct from row 438 (`mass_mailing.build_campaign_send_test_schedule`) which is medium-tier with a simpler pre-seeded audience and tests the Schedule wizard only (no iframe body requirement + wider datetime acceptance). |
| **Notes** | **Calibration HIT as designed** — hard tier target ≤40% pass, achieved 0.0 F1 on single-shot BU with a clean trace. **Three-widget compound failure** isolates the datetime widget as the anchor (BU got iframe body, Mailing List autocomplete, and Schedule button right; only the datetime slipped). **Oracle uses JSON-RPC** for three fragile paths: (a) `mailing.mailing.create` with `body_html='<div><p>Save 20%</p></div>'` (iframe bypass), (b) `mailing.mailing.schedule.date.create({schedule_date: '2026-05-20 10:00:00'})` + `action_schedule_date` (datetime bypass — same pattern as row 438 oracle which also JSON-RPCs the schedule wizard). (c) `email_from` pulled from `res.users.admin.email` with fallback to `admin@example.com` to satisfy the DB NOT NULL constraint. **check.py tz handling**: accepts both `schedule_date == 2026-05-20 10:00 UTC` (bench base tz) AND the user-TZ-adjusted equivalent (`sd_utc.astimezone(user_tz) == expected_local`) so the task is portable to non-UTC admin accounts. The BU failure surface is the postcondition message which quotes both the UTC storage value AND the user-TZ view for easier debugging. **state_spec ignore_fields** excludes `schedule_date` (noisy tz diff), `sent_date`, `contact_list_ids` (m2m noise per ODOO19_PATTERNS §state_spec gotchas), `body_html`/`body_arch`/`email_from` — these are validated in check.py instead. **expected_state.json** has 4 `op=create` entries (subject, state, schedule_type, mailing_model_name) — the Spring Promo subject is the entity_key match field. **trace_spec forbidden_ops** includes `mailing.mailing.action_launch` + `action_send_mail` + `mailing.mailing.test.send_mail_test` to catch agents that click Send / Send Sample instead of Schedule (the canonical calibration trap besides the datetime). **Cookbook quirks confirmed**: (i) `mailing.mailing.schedule.date` wizard fires the same `state='in_queue'` + `schedule_type='scheduled'` writes the UI "Schedule" button does (no separate `action_schedule` method — the wizard IS the schedule flow); (ii) `contact_list_ids` is copied verbatim by `mailing.mailing.copy()` so a create-from-scratch task must explicitly pass the list even when the source (here, no source) would have it; (iii) iframe body editor: the oracle JSON-RPC writes both `body_html` AND `body_arch` because each is the source-of-truth in different render paths (`body_arch` is the web-editor version; `body_html` is the sent-mail version — Odoo's `_inline_field_body` hook copies arch→html on save, but a fresh RPC create skips that). |
| **Quirks for future tasks** | The `mailing.mailing.schedule.date` wizard's datetime field is the HARDEST anchor in any mass-mailing scheduling task — BU reliably misreads the value it types into the Odoo datetime button-input widget (hour slipped from 10 → 02 in this run, and ODOO19_PATTERNS notes similar drift on `stock.lot.expiration_date`). For future "schedule X at time Y" tasks, prefer short, unambiguous times like `12:00` (noon) over tz-sensitive times, or relax check.py to accept ±30 min if tz handling isn't the point. For this row we kept strict equality because "agent believes 10:00 stored 02:00" IS the calibration signal. |

---

## crm.assign_lead_salesperson_change_stage_won

| Field | Value |
|---|---|
| **Task ID** | `crm.assign_lead_salesperson_change_stage_won` |
| **Row** | 442 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.6s wall clock, 3/3 atomic edits matched, 50 API calls, 24 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 91.4s wall clock, 3/3 atomic edits matched, 60 API calls, 28 non-forbidden writes, 0 forbidden, StrictClean=True). BU solved single-shot — assigned Bench Rep via Salesperson autocomplete and clicked the Won status-bar button cleanly. |
| **F1** | 1.0 |
| **Odoo modules** | CRM (`crm.lead`, `crm.stage`, `res.users`) |
| **Workflow** | Seed creates internal user `Bench Rep` (login `bench.rep`, `base.group_user` + `sales_team.group_sale_salesman`), partner `Bench Buyer Co`, and an **unassigned** `crm.lead` `Bench Big Deal` (`type='opportunity'`, `user_id=False`, `expected_revenue=50000`, `probability=10`) in the default first non-won `crm.stage` (sequence asc). Agent: CRM → open `Bench Big Deal` kanban card → set **Salesperson** Many2one to `Bench Rep` via autocomplete → Save → click the **Won** button on the form header `o_statusbar_buttons` (fires `action_set_won_rainbowman`). End state: `user_id.name='Bench Rep'`, `stage_id.name='Won'` (`is_won=True`), `probability=100`, `active=True`. |
| **Capability tested** | Two-action combo: Many2one assignment on `user_id` (near-top-of-form avatar widget) + header status-bar "Won" action. The pair exercises autocomplete picking AND the statusbar button the agent must not confuse with the inline stage buttons (which would only move the stage without triggering the rainbowman/probability logic). |
| **Notes** | **Calibration MISS** — medium tier target ~60% pass, BU single-shot PASSED (F1=1.0). Likely too easy: both actions are labelled clearly ("Salesperson" field, "Won" status-bar button) and there are no distractors / non-default choices / wizards. Similar to row 314 (`crm.assign_team_change_salesperson_log_activity`) which also passed BU despite adding a Contacts-tab hidden Many2one and an activity wizard. This confirms a pattern: CRM pipeline tasks that combine only "assign Many2one + click statusbar" are not hard enough for calibration — agents reliably find the avatar field and the Won header button. Leaving as Done with honest PASS metrics; future CRM medium tasks should add a wizard (e.g. the Won rainbow-man dismisses cleanly, so try adding a compose email or activity scheduling after Won) or a non-default dialog choice to raise difficulty. **Cookbook quirks confirmed**: (a) `crm.lead` has `user_id` visible on the opportunity form header (avatar widget) — the opportunity variant exposes it, unlike `team_id` which only shows under Contacts tab (see row 314 notes). (b) Won status-bar button calls `action_set_won_rainbowman` (primary) or `action_set_won` — oracle uses a disjunction selector `button[name='action_set_won_rainbowman'], button[name='action_set_won'], .o_statusbar_buttons button:has-text('Won')` to handle both code paths; `trace_spec.yaml` lists `action_set_won_rainbowman` as required_op and `action_set_won` as optional. (c) `crm.stage.is_won` flag is the semantic check (name=='Won' is necessary but not sufficient — check.py asserts both). (d) Seed uses `stage_id=first non-won stage sequence asc`: on the base snapshot this is "New", keeping the kanban default unchanged. (e) `expected_state.json` captures 3 edits: `user_id set→Bench Rep`, `stage_id set→Won`, `probability set→100.0`; `active` is unchanged so omitted. |

---
## fleet.assign_vehicle_create_contract_active

| Field | Value |
|---|---|
| **Task ID** | `fleet.assign_vehicle_create_contract_active` |
| **Row** | 444 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 41.7s wall clock, 7/7 atomic edits matched, 0 postcondition failures, 42 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 123.6s wall clock single-shot, 1 postcondition failure `"Contract vendor (insurer_id) is not set"`, 60 API calls, 28 non-forbidden writes, 0 forbidden). Agent reported success in its final message ("Successfully created a new leasing contract ... with vendor Bench Lease Co ... status set to Running") but the `insurer_id` field was never actually written — state_diff shows `insurer_id: null` as an extra edit and `insurer_id: Bench Lease Co` as the missing expected edit. Classic "claim done, skip a field" failure. |
| **F1** | 0.0 |
| **Odoo modules** | Fleet — `fleet.vehicle`, `fleet.vehicle.log.contract`, `fleet.service.type` (`category='contract'`), `res.partner` (vendor). |
| **Workflow** | Seed creates vehicle `BENCH-VAN-01` (Bench Mobility / Bench Van) with a non-admin driver partner `Bench Driver Partner`, a vendor partner `Bench Lease Co` (`supplier_rank=1, company_type='company'`), and ensures the `Leasing` contract type exists (`fleet.service.type` with `category='contract'`). Agent: Fleet → open vehicle `BENCH-VAN-01` → click the **Contracts** smart button (`contract_count` statinfo) → **New** on the contract list → fill `Type=Leasing` (cost_subtype_id), `Vendor=Bench Lease Co` (insurer_id), `Contract Start Date=04/20/2026`, `Recurring Cost=200.00` (cost_generated, frequency stays default `monthly`) → **Save** → confirm the clickable statusbar shows **Running** (state='open'); if not, click Running to activate. |
| **Capability tested** | Smart-button navigation to a sub-form, exact-field create-from-scratch with an autocomplete-vendor pick, plus a statusbar confirm/activate step. Medium trap is the "claim-success but forget a field" pattern on the Vendor field — the Leasing `cost_subtype_id` has no implied vendor link, so an agent distracted by populating Type/Start/Cost/Frequency can easily skip the Vendor m2o and still perceive the form as "complete" (all visible tabs filled). Postcondition catches the omission via `check.py`. |
| **Notes** | **Calibration landed on-target for medium** — BU completed the create + save + statusbar steps cleanly (filled Type, Start Date, Recurring Cost, Frequency, and transitioned state to `open`) but silently skipped the `insurer_id` field entirely despite the prompt's explicit "Vendor: `Bench Lease Co`" line. 6/7 atomic edits matched, 1 missing edit + 1 extra edit (insurer_id null), score zeroed by postcondition_failures per `eval.py` logic. **Odoo 19 quirk discovered & cookbooked**: (a) `fleet.vehicle.log.contract` form header has **NO "Activate Contract" button** — the original task spec's reference was wrong for Odoo 19 Community. The only way to flip state is the clickable `<field name="state" widget="statusbar" options="{'clickable': '1'}"/>` in the form header. (b) State values are `futur / open / expired / closed` displayed as `New / Running / Expired / Cancelled` — default is `open`, NOT `futur`, so a freshly-created contract lands in Running directly from UI create (the `write()` override that flips `state='futur'` when `start_date > today` runs only on subsequent `write()` calls, not on the initial `create()`). Consequence for oracle: the "Running" statusbar button renders as `disabled aria-current="step" data-value="open"` on fresh-save — clicking it throws a Playwright TimeoutError. Oracle pattern: check `aria-current == 'step'` on the `button[data-value='open']` element and skip the click if already current. (c) Prompt re-phrased to "confirm state is Running, click Running step only if it isn't already" — keeps the task coherent for humans + aligns with Odoo 19's actual UI behavior. (d) `cost_subtype_id` field is labeled "Type" with a domain `[('category', '=', 'contract')]` — the same `fleet.service.type` table as service costs but filtered by category; seed must create with `category='contract'` or the autocomplete returns nothing. (e) `insurer_id` is labeled "Vendor" on the form (not "Insurer Vendor"), and uses `widget="many2one_avatar"` — set_many2one helper handles it fine. (f) Seed uses `Vehicle.create(...)` (not write) to avoid the extra `fleet.vehicle.assignation.log` that `write({driver_id: ...})` would auto-append (documented in ODOO19_PATTERNS.md §Fleet). |

## sale.add_section_note_line_to_quotation

| Field | Value |
|---|---|
| **Task ID** | `sale.add_section_note_line_to_quotation` |
| **Row** | 440 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 24.7s wall clock, 6/6 atomic edits matched, 0 postcondition failures, 48 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 96.1s wall clock, 6/6 atomic edits matched, 0 postcondition failures, 48 API calls, 20 non-forbidden writes, 0 forbidden, StrictClean=True; `success=False` from the harness but the end state is correct — BU reported in stdout "I added a section named 'Phase 1' and a note 'Delivery by end of month' to the Order Lines tab"). |
| **F1** | 1.0 |
| **Odoo modules** | Sales (`sale`) — `sale.order` / `sale.order.line` with `display_type` Selection `[line_section, line_subsection, line_note]`. Uses the `sol_o2m` widget's footer `<control>` with three `<create>` buttons (Add a product / Add a section / Add a note), backed by `SectionAndNoteListRenderer` from `addons/account`. |
| **Workflow** | Seed creates customer `Bench Struct Co`, two tax-cleared consu products (`Bench Struct Item A` @ 40.0, `Bench Struct Item B` @ 25.0), and a draft `sale.order` pinned to `name='SO-BENCH-STRUCT'` and `client_order_ref='SO-BENCH-STRUCT'` with two product lines (A qty=1, B qty=2). Agent: Sales → Quotations → open `SO-BENCH-STRUCT` → Order Lines tab → in the list footer (next to the default "Add a product") click **Add a section**, name `Phase 1`, Tab-commit → click **Add a note**, type `Delivery by end of month`, Tab-commit → Save (do NOT confirm). End state: exactly 4 `sale.order.line` rows (2 seeded products unchanged + 1 `display_type='line_section'` named `Phase 1` + 1 `display_type='line_note'` named `Delivery by end of month`), quotation stays `state='draft'`. |
| **Capability tested** | Non-default `<control><create>` buttons in an editable one2many list footer — the kind of UI where the default (leftmost) option is "Add a product" and the task-relevant options ("Add a section" / "Add a note") are sibling links with only `ml16` margin spacing between them and text as the only disambiguator. Also verifies the agent picks the right editor per `display_type`: sections render as `CharField` (single-line input), notes as `TextField` (textarea), both inside a spanned `td[name='name']` on an `o_selected_row`. Distinct from `sale.add_note_to_quotation` (row 60), which uses the **chatter Log note** button — not an order-line note — so there is no overlap in UI surface. |
| **Notes** | Calibration: medium (≈60% pass). Single-shot BU PASS — the task is on the easier edge of medium but still exercises a real non-default footer control. The hard part was getting the oracle right: three quirks I learned (and captured in `COOKBOOK_NOTES.md`): (a) `<control><create>` renders as sibling `<a role="button">` elements inside one `td.o_field_x2many_list_row_add`, distinguishable only by text — use `get_by_role("button", name=label, exact=True)` scoped to the footer td, NOT the default `click_add_a_line` helper which prefers "Add a product" and would silently do the wrong thing. (b) `SectionAndNoteListRenderer.focusToName` auto-focuses the new row's `name` cell, so the fallback `page.keyboard.type(...)` works; but `td[name='name']` targeting is the deterministic route. (c) Before clicking a second footer control (e.g. "Add a note" after filling the section), commit the pending edit by clicking an inert area of `.o_form_sheet` first — otherwise the row's blur handler races with the `<a>` click and the new row either doesn't appear or appears with `display_type=False` (a product line). Trap: the first time through, the note row came back with `display_type=None` because of this exact race — adding the inert-click "commit" step fixed it. expected_state.json tracks 3 fields × 2 new rows = 6 atomic edits (`display_type`, `name`, `order_id`); `order_id` normalizes to the SO's `name` ("SO-BENCH-STRUCT") in the diff, not null. state_spec ignores all price/qty/product/tax columns because sections/notes legitimately have them unset. |


---

## website.publish_draft_page_set_menu_visibility

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 13.5s, 0 postcondition failures, 35 API calls, 15 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 420.0s `gave_up=True`, 1 postcondition failure on top-level menu position, 371 API calls, 220 non-forbidden writes, 0 forbidden). BU achieved Recall=1.0 on the core state changes (page published + new /about-us menu created under the main website menu, page_id auto-linked) but could not re-order the entry into position 2 before the 420s timeout. Also introduced the `website.menu.save` side effect (the backend auto-writes page_id on the distractor About→/contactus menu because it shares a URL with the pre-existing Contact us page) which dropped Precision to 0.875 before the gave-up zeroing. |
| **F1** | 0.0 |
| **Odoo modules** | Website — `website.page` (publish toggle) + `website.menu` (main menu tree), via `/odoo/website-pages` list + Site → Menu Editor dialog. |
| **Workflow** | Seed creates an **unpublished** `website.page` titled "About Us" at `/about-us` on the primary website (id=1), a minimal qweb arch that extends `website.layout`. Also seeds a **distractor** `website.menu` named `About` pointing at `/contactus` under the primary site root so a careless agent can mistakenly edit that distractor`s URL instead of creating a new entry. Agent must: (1) open Website → Site → Pages, locate `About Us`, flip its Published boolean toggle in the list/kanban row (or via form or builder systray) to ON — this writes `is_published=True` and propagates to `website_published=True` via the `website.published.multi.mixin._inverse_is_published`; (2) open Site → Menu Editor, click **Add Menu Item**, enter Name=`About Us` + URL=`/about-us`, then **drag the new row upward** so the new entry sits in the **2nd** top-level slot (directly after Home), Save. The backend `website.menu.save` auto-resolves page_id by matching the URL to an existing `website.page`. End state: `website.page.is_published=True`, `website.menu.url=/about-us` with `page_id=About Us` + `parent_id=Top Menu for Website 1` + `sequence < 60`, top-level order = [Home, About Us, About (distractor), Contact us, Shop, …]. |
| **Capability tested** | **Two-phase hard workflow**: (a) inline publish pill / `widget="boolean_toggle"` on `website.page.is_published` — a distinct UI affordance from the builder Unpublished/Published systray used in `website_blog.change_author_republish_post` (row 430), and (b) the Website Menu Editor dialog — a drag-and-drop-ordered `website.menu` tree rooted at `website.menu_id` that persists via a single `website.menu.save(website_id, {data, to_delete})` call which iterates every top-level child and rewrites page_id. The sequence-position constraint (About Us must be 2nd) converts this from a trivial create into a multi-action flow: Add Item → drag up → Save. Distractor About→/contactus traps agents that rename an existing entry instead of adding a new one. |
| **Notes** | **Calibration HIT as designed** — BU FAIL at 420s timeout with gave_up=True after achieving the core state changes (Recall=1.0 on the 7 expected edits) but never reaching the 2nd-position ordering constraint in the Menu Editor. Without the sequence constraint, single-shot BU reached F1=0.9333 (Recall 1.0, Precision 0.875, 1 extra side-effect edit) in 96.9s — too easy for a hard task, which prompted adding the position requirement per TASK_CREATION_GUIDE.md ("If single PASS, add complexity (distractor menu entry, require specific sequence position)"). Quirks: (1) `website.menu.save` (the canonical Menu Editor entrypoint) iterates ALL top-level children and re-writes them, auto-resolving page_id from URL on every row; on the distractor `About`→/contactus menu this writes `page_id=Contact Us` as a side effect because `/contactus` already has a canonical page. The oracle sidesteps this by calling `website.menu.create` directly (bypassing the save helper) to keep the state diff clean. (2) `website.main_menu` (xml_id) is the xmlid of the "Default Main Menu" — each `website.website` computes its own root `menu_id` lazily; `website.menu.parent_id` must equal `website.browse(1).menu_id.id`, NOT the global `website.main_menu` xmlid. (3) `website.page.is_published` has `widget="boolean_toggle"` in both the list and kanban views for website.page — BU reliably toggles this pill in <20 steps. The hard anchor is the drag-to-position-2 interaction in the Menu Editor. (4) State spec uses `match_key: [url, website_id]` on `website.menu`; entity_key normalizes to `["/about-us", "My Website"]`. `parent_id` normalizes to `"Top Menu for Website 1"` (the display_name of website.menu_id), NOT the xmlid "website.main_menu". (5) Trace spec is lenient (`required_ops: []`) because BU can take any of three UI paths (Pages list toggle, page form, builder systray; Menu Editor save or Page Properties dialog inverse) — each emits different write patterns. check.py is the source of truth for ordering + distractor-preservation. |

---

## stock.receipt_full_quantity_validate_no_backorder

| Field | Value |
|---|---|
| **Task ID** | `stock.receipt_full_quantity_validate_no_backorder` |
| **Row** | 447 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.8s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 40 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 64.5s wall clock single-shot, 1/1 atomic edits matched, 0 postcondition failures, 48 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True). BU solved single-shot: Inventory → Receipts tile → WH/IN/BENCH-FULL → Validate → done, no dialog. |
| **F1** | 1.0 |
| **Odoo modules** | Stock — `stock.picking` (incoming), `stock.move`, `stock.move.line`, `stock.quant` (WH/Stock put-away), `res.partner` (vendor), `product.product` (storable). |
| **Workflow** | Seed creates vendor `Bench Vendor` (`supplier_rank=1`), storable product `Bench Recv Item` (`type='consu'`, `is_storable=True`, `tracking='none'`), and a Ready incoming receipt pinned to `name='WH/IN/BENCH-FULL'` (vendor source → WH/Stock dest) for 10 units. Seed calls `action_confirm()` + `action_assign()`; because the source location is the supplier (infinite availability), Odoo auto-fills `move.quantity = product_uom_qty = 10` on the single move_line, and the seed belt-and-suspenders writes `move.quantity = 10` + `move.picked = True` so no availability / detail-cell prompt can ever surface. Agent: Inventory → Receipts kanban tile → open `WH/IN/BENCH-FULL` → click **Validate** in the header. End state: `stock.picking.state='done'`, Bench Recv Item `stock.move.quantity=10`, zero backorder pickings, `stock.quant` at WH/Stock = 10. |
| **Capability tested** | **Calibration anchor / easy floor**: a clean single-click Validate on a fully reserved receipt where Done already matches Demand — no Create Backorder dialog appears, no cell edit required, no wizard. Confirms the baseline Inventory → Receipts → form → Validate navigation path and button targeting. Distinct from row 436 (`stock.delivery_transfer_validate_partial_backorder_no`, medium policy_trap: partial Done + No Backorder dialog), row 395 (partial with Create Backorder), and row 17 (`purchase_stock.receive_partial_without_backorder`, wraps around PO). |
| **Notes** | **Calibration landed on-target for easy tier (~80% pass)** — BU single-shot PASS in 64.5s, 22 writes, zero forbidden ops, zero postcondition failures. Task serves as the cleanest incoming-validate anchor in the suite. **Odoo 19 quirks confirmed**: (a) incoming moves auto-fill `move.quantity` on `action_assign` because the source is the supplier location (infinite availability) — no reservation step needed, so `button_validate` goes through without the Create Backorder dialog per ODOO19_PATTERNS §Stock L264-269. (b) Seeding `move.picked=True` is belt-and-suspenders against a rare Odoo 19 picked-flag availability wizard that fires on some base snapshots when picked is False — the written `picked=True` eliminates that branch. (c) `stock.quant` auto-lands at WH/Stock for 10 units after `_action_done()` — check.py asserts this so the task measures the semantic outcome (goods in stock), not just `picking.state`. (d) entity_key `["WH/IN/BENCH-FULL", "Bench Vendor", null]` uses pinned picking `name` + vendor display_name + `backorder_id=null` (original has no parent) — matches the row-436 pattern. (e) `expected_state.json` is a single atomic edit (`state` set→`done`) because the seed already has `move.quantity=10` and `move.picked=True` — Validate writes only picking.state visibly (the quant creation is a separate model ignored by `state_spec.yaml`). (f) `trace_spec.yaml` forbids `stock.picking.unlink`, `action_cancel`, and the backorder wizard process methods — an agent that strays off-path triggers forbidden-op flags. **Commit**: `[ADD] benchmark: stock.receipt_full_quantity_validate_no_backorder (easy)`. |
---

## project.close_task_change_state_to_done

| Field | Value |
|---|---|
| **Task ID** | `project.close_task_change_state_to_done` |
| **Row** | 448 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.0s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 41 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle opens the Project app, drills into `Bench Close Project`, opens the `Review document` task kanban card, clicks the form-header `.o_state_button` pill (reads "In Progress"), picks the `.dropdown-item` labelled `Done` from the Odoo 19 `project_task_state_selection` dropdown (`.state_selection_field_menu` / `.project_task_state_selection_menu`), and saves. |
| **Browser-Use** | PASS (F1=1.0, 83.8s single-shot, 0 postcondition failures, 50 API calls, 24 non-forbidden writes, 0 forbidden, StrictClean=True). BU found the kanban project card, opened the task, identified the state pill on the form header (not the stage statusbar), clicked it, selected `Done` from the rainbow dropdown, and persisted — calibration-anchor easy at single-shot as designed for tier 1 / ~80% pass target. |
| **F1** | 1.0 |
| **Odoo modules** | `project` — `project.task.state` Selection `01_in_progress / 02_changes_requested / 03_approved / 1_done / 1_canceled / 04_waiting_normal` (`addons/project/models/project_task.py:168-175`, `CLOSED_STATES = {'1_done': 'Done', '1_canceled': 'Cancelled'}`). Widget: `project_task_state_selection` (`addons/project/static/src/components/project_task_state_selection/project_task_state_selection.js`) — subclasses `StateSelectionField` and on form view renders `button.o_state_button.btn.rounded-pill` with a Bootstrap Dropdown whose menu is classed both `state_selection_field_menu` AND `project_task_state_selection_menu`. Each `.dropdown-item` shows a state label (In Progress / Changes Requested / Approved / Cancelled / Done; Waiting is filtered out unless current). |
| **Workflow** | Seed: idempotently unlinks any prior `Review document` task and `Bench Close Project` project (cascading residual tasks). Creates fresh project, pins the three default stages (`To Do` / `In Progress` / `Done`) to it via `type_ids` (same stage-pin pattern as row 439 — without pinning, the task falls into the collapsed `None` kanban group via `project.task.type.group_expand`). Creates one `project.task` named `Review document` with `stage_id='To Do'`, `priority='0'`, `tag_ids=[(5,0,0)]`, then explicitly writes `state='01_in_progress'` (belt-and-braces — the default AND the re-compute land there). Agent path: Project (`/odoo/project`) → click `Bench Close Project` kanban card → task kanban grouped by stage → click `Review document` card → form opens → in the form header (right of the task title, next to the priority stars) locate the **colored state pill button** labelled `In Progress` (`.o_field_widget[name='state'] button.o_state_button`) → click it → a dropdown menu opens with entries `In Progress / Changes Requested / Approved / Cancelled / Done` → click `Done` → pill turns green, label becomes `Done` with a check-circle icon → Save (cloud icon / Ctrl+S). End state: the single `project.task` has `state='1_done'`, all other fields unchanged (stage still `To Do`, priority still `'0'`, no tags/assignees, name preserved). |
| **Capability tested** | Easy-tier calibration anchor for the Odoo 19 **project task state widget** (`project_task_state_selection`). Distinct widget from row 439 (`priority_switch` three-stars) — the state pill is a `button.o_state_button.rounded-pill` that expands into a CheckboxItem dropdown, whereas priority is a static inline anchor row of three `.o_priority_star` icons. The state widget is the only way to drive `project.task.state` from the UI (there is no field-level inline input) and is new in Odoo 19's project module refresh. Target behaviour: click pill → dropdown → pick specific state (with four distractor options that map to different DB values: `02_changes_requested`, `03_approved`, `1_canceled`, and "keep current" via re-clicking `In Progress`). |
| **Notes** | **Calibration as designed (easy/tier-1 ≈80% pass target, BU single-shot PASS at 83.8s well under the 300s limit).** Oracle and BU both emitted exactly 1 atomic state edit (`state: 01_in_progress → 1_done`) with zero forbidden writes and zero postcondition failures. **State-field quirks captured**: (1) `project.task.state` has BOTH `compute='_compute_state'` AND `inverse='_inverse_state'` — writing the field directly is supported (the inverse runs + re-compute fires) but the compute re-evaluates on `depend_on_ids` and will snap an unblocked task back to `01_in_progress`. Since our seed task has no dependencies this is a no-op, but if a future medium/hard task depends on a WAITING trap, seed `depend_on_ids` explicitly. (2) `CLOSED_STATES = {'1_done': 'Done', '1_canceled': 'Cancelled'}` — both closed states share the leading `1_` (numeric collision with legacy `1_` codes) — the diff engine handles them as plain strings but a naive prompt that says "click the green button" is ambiguous because both Done + Cancelled are visually similar (check-circle vs times-circle). Prompt explicitly says **"Done (technical value `1_done`), NOT Approved and NOT Cancelled"** to eliminate that trap. (3) Widget DOM on FORM view: `.o_field_widget[name='state']` → single `button.o_state_button.rounded-pill` (label from `label` getter which calls `formatSelection`); clicking opens `Dropdown` with `menuClass="'project_task_state_selection_menu'"` (additive via `position="attributes"` `separator=" "` `add`). Each option is a `CheckboxItem` (from `@web/core/dropdown/checkbox_item`) rendered as `.dropdown-item.d-flex.align-items-center` with a leading color span + label text. Oracle matches with a tri-selector `.state_selection_field_menu:visible .dropdown-item, .project_task_state_selection_menu:visible .dropdown-item, .o-dropdown--menu:visible .dropdown-item` and picks the item whose inner_text case-insensitively equals `Done`. (4) The state widget dropdown also appears on **kanban** (inline mini pill) and **list** (inline small icon) views — the form version is the only one that shows a full colored pill with text label, which is why the prompt says "form header". (5) **Distinction from stage statusbar**: the same form has a `<field name="stage_id" widget="rotting_statusbar_duration" options="{'clickable': '1'}"/>` element inside a `<header>` block — this is a SEPARATE widget rendering the kanban stages as clickable statusbar pills and writes `stage_id`, NOT `state`. The prompt's rules section explicitly forbids using the stage pills; check.py asserts `stage_id.name == 'To Do'` post-task to catch agents that confuse the two widgets. (6) **No seed `.venv` in this worktree** — pre-warmed venvs contain only `playwright` + `pyyaml` but running seed scripts demands `babel` + full `requirements.txt` + `browser-use`. The standard one-shot `uv pip install -r requirements.txt && uv pip install browser-use` resolved this before the first oracle attempt (same cookbook lesson as row 439). (7) expected_state.json is a single `op=set` edit on `state` with entity_key `["Review document", "Bench Close Project"]` (match_key `[name, project_id]` — `project_id` normalizes to the project's display name per ODOO19_PATTERNS m2m/m2o normalization rules). No m2m noise to ignore because tags/users stay empty across the transition. |
---

## project.assign_task_to_user_change_deadline

| Field | Value |
|---|---|
| **Task ID** | `project.assign_task_to_user_change_deadline` |
| **Row** | 487 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 34.7s wall clock, 0 postcondition failures, 44 API calls, 19 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle opens Project → `Bench Assign Project` → `Bench Assign Task` form, fills the `user_ids` m2m autocomplete with `Bench Dev` (skipping any `Create ... as new user` quick-create row), calls `set_date(page, 'date_deadline', '06/30/2026')` (which types + presses Tab + Escape to dismiss the picker popover), and saves. |
| **Browser-Use** | PASS (F1=1.0, 78.6s single-shot, 0 postcondition failures, 39 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True). BU logged in, drilled into the project, opened the task, typed `Bench Dev` in Assignees and picked the `role=option` dropdown entry `Bench Dev id=user_ids_0_0_0`, then typed `06/30/2026` in the deadline input (auto-retrying past an AM/PM concatenation nuisance), pressed Tab, and clicked the Save button in 9 steps. |
| **F1** | 1.0 |
| **Odoo modules** | `project` — `project.project` (`Bench Assign Project`), `project.task` (`Bench Assign Task`, `user_ids` m2m → `res.users`, `date_deadline` `fields.Datetime` per `addons/project/models/project_task.py:183`), `project.task.type` (shared default stages `To Do`/`In Progress`/`Done` pinned to the project), `res.users` (`Bench Dev`, login `bench_dev`, groups = `base.group_user` + `project.group_project_user`). |
| **Workflow** | Seed: idempotently drops any prior `Bench Assign Task`, `Bench Assign Project`, and `bench_dev` user (+ orphan partner best-effort). Creates fresh project, pins the three default stages (`To Do`/`In Progress`/`Done`) to it via `project_ids` (search-or-create-then-link — without pinning, the task falls into a collapsed `None` kanban group and becomes unclickable from the project drill-down; same cookbook lesson as rows 439 + 448). Creates `Bench Dev` internal user with both `base.group_user` AND `project.group_project_user` so `name_search` on `project.task.user_ids` surfaces it. Creates one `project.task` with `stage_id='To Do'`, `priority='0'`, empty `tag_ids`, empty `user_ids`, `date_deadline=False`. Agent path: Project (`/odoo/project`) → click `Bench Assign Project` kanban card → click `Bench Assign Task` card → form opens → in the `user_ids` many2many widget type `Bench Dev` → pick the existing `Bench Dev` autocomplete row (NOT the `Create "Bench Dev" as new user...` row) → in the `date_deadline` field type `06/30/2026` → press Tab to close the date-picker popover → Save (cloud icon / Ctrl+S). End state: one `project.task` on `Bench Assign Project` with `user_ids = [bench_dev]`, `date_deadline = 2026-06-30` (admin-local), everything else unchanged. |
| **Capability tested** | Medium-tier calibration: combines the two "hard patterns" from row 409 (m2m user pick from autocomplete + date-picker with TZ conversion) but on an EXISTING task rather than a create-from-scratch workflow. Distinct from row 409 (new task with 2 tags + 2 assignees + deadline from scratch) and row 439 (priority stars + tag on existing task; no date, no user). Sub-capabilities: (a) many2many `user_ids` existing-pick — the `forbidden_ops` list blocks `res.users.create` so quick-creating a brand-new `Bench Dev` user surfaces as a HarmfulWrite; check.py additionally asserts `len(res.users.login='bench_dev') == 1` AND `len(res.users.name='Bench Dev') == 1`. (b) `date_deadline` (Datetime, not Date) — form UI types `MM/DD/YYYY` that stores as UTC midnight offset by admin TZ; check.py converts UTC → admin-local date before comparing with `date(2026, 6, 30)`. (c) Picker-popover-eats-next-click trap — agents that type the date then click Save without Tab/Escape can blur-drop the deadline; oracle uses `set_date()` which presses Tab + Escape. |
| **Notes** | **Calibration MISS — BU passed single-shot (78.6s, F1=1.0, 9 steps, 0 postcondition failures).** BU handled the `role=option` autocomplete cleanly for Bench Dev, auto-recovered from a `BrowserSession` "Concatenation detected: got '06/30/2026 12:00:00 AM', expected '06/30/2026' — auto-retrying" warning (the date input pre-fills with a placeholder that BU correctly cleared before retyping), pressed Tab, and clicked Save. This mirrors the row-409 BU-passes-first-try outcome: medium-tier two-change task on an existing record with a clean `Bench Dev` display name (no disambiguation against `Mitchell Admin` / other internal users). Retained as-is at tier 2 for m2m-user + datetime-deadline coverage on an UPDATE (vs row 409's CREATE). **Quirks captured**: (1) `expected_state.json` is an empty list `[]` — both `user_ids` (m2m, brittle entity-key across runs) and `date_deadline` (Datetime, TZ-dependent serialization varies between worktrees with different admin.tz) are validated only via check.py; `state_spec.yaml` tracks `name + project_id` so the diff engine doesn't emit noise from unchanged fields. (2) Datetime TZ: `project.task.date_deadline` is `fields.Datetime`, so typed `06/30/2026` → `2026-06-30 00:00:00 (admin tz)` → UTC storage shifted by the user's tz; check.py uses `pytz.UTC.localize(dt).astimezone(admin_tz).date()` before comparing. (3) User-quickcreate detection: `res.users.create` is in `forbidden_ops`, AND check.py cross-checks both `login='bench_dev'` uniqueness and `name='Bench Dev'` uniqueness (catches agents that quick-create with an alternate login like `Bench Dev` / `bench.dev`). (4) Cleanup also unlinks any duplicate user matching `name='Bench Dev'` so a stray quick-create from a failed run doesn't pollute the next seed. (5) **Pre-warmed venv was stale** — had `playwright` + `pyyaml` only, needed `uv pip install -r requirements.txt && uv pip install browser-use` once to unblock seed (`babel` import in `odoo/_monkeypatches/site.py`). Same lesson as rows 439 + 321. |
---

## sale.apply_discount_percent_on_sale_order_line

| Field | Value |
|---|---|
| **Task ID** | `sale.apply_discount_percent_on_sale_order_line` |
| **Row** | 445 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 27.2s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 42 API calls, 15 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 71.6s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 44 API calls, 21 non-forbidden writes, 0 forbidden, StrictClean=True; `success=False` from the harness but the end state is correct — BU completed the inline Disc.% cell edit on the first line and saved without confirming). |
| **F1** | 1.0 |
| **Odoo modules** | Sales (`sale`) — `sale.order` / `sale.order.line.discount` (`fields.Float(digits='Discount')`), visibility gated by the `sale.group_discount_per_so_line` security group on the Order Lines sub-list view. |
| **Workflow** | Seed grants `sale.group_discount_per_so_line` to admin + user_root (so the Disc.% column is visible in the o2m list), creates customer `Bench Disc Co`, two tax-cleared consu products (`Bench Product A` @ 50.0, `Bench Product B` @ 20.0), and a draft `sale.order` pinned to `name='BENCH-DISC'` and `client_order_ref='BENCH-DISC'` with two product lines (A qty=2 disc=0, B qty=3 disc=0; pre-discount amount_untaxed=160.0). Agent: Sales → Quotations → open `BENCH-DISC` → Order Lines tab → click into the **Disc.%** cell on the FIRST line (Bench Product A) → type `10.0` → Tab-commit → Save (do NOT confirm). End state: line A discount=10.0 with qty=2 & price_unit=50 unchanged; line B untouched (discount=0, qty=3, price=20); `amount_untaxed = amount_total = 150.0` (90 + 60, no taxes); quotation stays in `state='draft'`. |
| **Capability tested** | **Inline cell edit on a hidden-by-default column** — the per-line Disc.% field is declared `optional="show"` with `groups="sale.group_discount_per_so_line"`, so without the seed explicitly granting the group the column never renders in the o2m list renderer and the agent has no DOM target to click. Also exercises row-targeting in an editable one2many (must discount line A, not line B) and the Tab-commit-then-save vs. Tab-then-Confirm trap (task explicitly forbids Confirm — must stay in draft). Distinct from `sale.add_line_with_optional_template_apply_discount` (row 324) which adds a NEW line with a discount as part of a create flow, and from `sale.add_discount_line` (row 72, easy) which also edits an existing line but uses Azure Interior / Desk Organizer data and is scored as easy tier. |
| **Notes** | Calibration: medium (landed on the easier edge of medium). Single-shot BU PASS (71.6s, F1=1.0, StrictClean=True) — BU handled the inline Disc.% cell click + Tab commit + save without confirm in one attempt. The hard part was seed-side: without `discount_group.sudo().write({"user_ids": [(4, admin.id), (4, root.id)]})` the Disc.% column does not render even under the admin login and every attempt times out silently. Three quirks worth keeping in the cookbook: (1) `sale.group_discount_per_so_line` is a view-visibility gate (`<field name="discount" optional="show" groups="sale.group_discount_per_so_line"/>`), not a server-side write gate — the field exists and is writable without the group, but the column is simply absent from the rendered list, so the agent can't click it. (2) `sale.order.line.discount` is a Float (`digits='Discount'`, i.e. 2 decimal digits); `expected_state.json` must use JSON number `10.0`, not string `"10.0"`, because the state-diff normalizer converts Float fields to Python floats. (3) Row-targeting: the oracle scans `.o_data_row` for the product name (`Bench Product A`) rather than hard-coding row 0, so an accidental line re-order at seed time still produces a correct oracle. Check.py validates both discount values AND `amount_untaxed`/`amount_total` (150.0) so an oracle / agent that writes `discount=10` but forgets to Save (or accidentally Confirms) is caught by the `state='draft'` check. expected_state.json has a single atomic edit (`discount=10.0` set on `["Bench Product A"]`); state_spec ignores all price/qty/tax/product_template_id fields to keep the diff tight. |
---

## sale.edit_existing_quotation_add_optional_product

| Field | Value |
|---|---|
| **Task ID** | `sale.edit_existing_quotation_add_optional_product` |
| **Row** | 468 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.3s wall clock, 3/3 atomic edits matched, 0 postcondition failures, 49 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 67.3s wall clock single-shot, 3/3 atomic edits matched, 0 postcondition failures, 38 API calls, 15 non-forbidden writes, 0 forbidden, StrictClean=True; harness reports `success=False` but the end state is correct — BU appended the second product line with qty=4 and saved without confirming). |
| **F1** | 1.0 |
| **Odoo modules** | Sales (`sale`) — `sale.order` / `sale.order.line` (`product_id`, `product_template_id`, `product_uom_qty`, `price_unit`). Uses the `sol_o2m` widget's default footer `<control><create>` **Add a product** button (leftmost of three; the other two — Add a section / Add a note — are targeted by row 440). |
| **Workflow** | Seed creates customer `Bench Add Co`, two tax-cleared consu products (`Bench Existing Item` @ 30.0, `Bench Extra Item` @ 15.0), and a draft `sale.order` pinned to `name='BENCH-ADD-LINE'` and `client_order_ref='BENCH-ADD-LINE'` with ONE product line (`Bench Existing Item` qty=2 price=30; pre-edit amount_untaxed=60.0). Agent: Sales → Quotations → open `BENCH-ADD-LINE` → Order Lines tab → click **Add a product** in the list footer → pick `Bench Extra Item` from the product dropdown on the new row → change the default qty=1 to `4` in the new row's Quantity cell → Tab-commit → Save (do NOT confirm). End state: existing first line unchanged (qty=2, price=30); a NEW second `sale.order.line` with `product_id=Bench Extra Item`, `product_uom_qty=4.0`, `price_unit=15.0` (list_price, no pricelist applied); `amount_untaxed = amount_total = 120.0` (60 + 60); quotation stays in `state='draft'`. |
| **Capability tested** | **Inline o2m Add-a-product + qty edit on the new row** — the complement of row 440 (add section / note) and row 445 (edit discount on existing line). Here the agent must append a BRAND NEW product line (using the default leftmost footer control), pick the right product from the m2o dropdown, AND change the default qty in the same new-row edit cycle. Distinct from row 440 (non-product rows via Add a section / Add a note — different `display_type`s) and row 445 (edit existing line's Disc.% inline, no new row created). Exercises the row-index-1 targeting trap: after `click_add_a_line` the new editable row is row 1, not 0 — any oracle/agent that writes to row 0 overwrites the existing line instead of appending. |
| **Notes** | Calibration: medium (landed on the easier edge of medium). Single-shot BU PASS (67.3s, F1=1.0, StrictClean=True) — BU handled the click → product pick → qty edit → save sequence cleanly with 15 writes and 0 forbidden ops. Oracle PASS on first attempt (29.3s). Three quirks worth carrying forward in the cookbook: (1) `click_add_a_line` in `oracle_helpers` already prefers the link whose text contains "product" (filter `.has_text("product")`) so it correctly hits the default/leftmost footer control; for this task it's the canonical helper, whereas row 440 had to write a dedicated `_click_footer_control(page, label)` to target the non-default "Add a section" / "Add a note" siblings. (2) After `click_add_a_line`, the new row is at row index 1 (the existing line is at index 0); passing `row_index=0` to `set_o2m_many2one` would overwrite the existing product instead of filling the new one — exactly the "edit existing line instead of appending" failure pattern the task measures. (3) The sol_o2m widget exposes the product cell as `product_template_id` (NOT `product_id`) in the inline list — same cookbook rule as `sale.create_quotation_with_customer_pricelist` (row 303). Setting product_template_id fires an onchange that defaults `product_uom_qty=1.0` and `price_unit=15.0` (list_price), so the oracle's second step `set_o2m_field(page, 1, "product_uom_qty", "4")` must overwrite the 1.0 default; the Tab-commit there is load-bearing or the row stays in edit mode and a racing `save_form` silently drops the qty write. `expected_state.json` tracks 3 fields × 1 new row = 3 atomic edits (`product_id`, `product_uom_qty`, `order_id`); `order_id` normalizes to the SO's `name` ("BENCH-ADD-LINE") and `product_id` normalizes to the product display name. state_spec ignores `price_unit` (auto-computed), `discount`, `tax_ids`, `product_template_id`, etc. to keep the diff tight. No group-gating needed (unlike row 445's Disc.% column). `check.py` belt-and-suspenders validates `price_unit=15.0` and `amount_untaxed=120.0` so an oracle/agent that accidentally overrides the auto-computed price, or forgets to Save (state≠draft), fails the postcondition independently of the state diff. |
---

## Row 435 — account.register_partial_payment_reconcile_invoice

| Field | Value |
|---|---|
| **Task ID** | account.register_partial_payment_reconcile_invoice |
| **Row** | 435 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, ~34s wall clock, 10/10 atomic edits matched, 0 postcondition failures, RequiredOpRecall=1.0, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 105s wall clock, 10/10 atomic edits matched, 0 postcondition failures). Calibration miss — BU single-shot correctly executed all FOUR wizard overrides plus the distractor-invoice selection. Task remains legitimately hard by design (policy-trap wizard with 4 non-default fields + a distractor invoice + a non-default journal + a date picker) but BU's payment-wizard reliability is higher than this task can exploit. |
| **F1** | 1.0 |
| **Odoo modules** | `account` (base) — no extra module installs required. `account.payment.register` wizard + `account.payment` + `account.move` + `account.journal`. |
| **Workflow** | Seed creates partner `Bench Partial Co`, two posted customer invoices (`BENCH-PARTIAL-001` total 500.00 with two lines, `BENCH-PARTIAL-DISTRACT` total 300.00 — distractor), and a SECONDARY bank journal `Bench Secondary Bank` whose sequence is reduced to one below the original `Bank` journal so it wins the wizard's default-picker. Agent: open Accounting → Customers → Invoices → open `BENCH-PARTIAL-001` (NOT the distractor) → click header **Pay** button → in the modal wizard OVERRIDE four auto-filled fields: Journal `Bench Secondary Bank` → `Bank`, Amount `500.00` → `200.00`, Payment Date today-default → `04/15/2026` (back-dated), Memo `INV/2026/NNN` → `Partial 1 of 2 for BENCH-PARTIAL-001` → click primary **Create Payment** button. Result: `BENCH-PARTIAL-001.payment_state = 'partial'`, new `account.payment(amount=200, state='paid'|'posted'|'in_process', memo=exact override, date=2026-04-15, journal.name='Bank', payment_type='inbound')`. |
| **Capability tested** | (1) Distractor resistance — two posted invoices for the SAME partner and both eligible for Register Payment; agent must pick the correct reference. (2) Partial-amount override in the `account.payment.register` wizard where the Amount field is pre-filled with `amount_residual` (500.00) — accepting the default produces a full-reconcile `payment_state='paid'` instead of the required `'partial'`. (3) Non-default journal selection — the seed demotes the original Bank journal so a newly-seeded "Bench Secondary Bank" wins the default; agent must pick the explicit `Bank` entry whose label is a substring of the default. (4) Date-picker override in a modal — Odoo 19's `o_field_date` renders as a `<button>` that opens an overlay popover; the popover intercepts subsequent pointer events unless explicitly dismissed. (5) Memo override on `account.payment.register.communication` which maps via `_create_payments.vals['memo'] = self.communication` to `account.payment.memo`. |
| **Notes** | **Field name cookbook**: `account.payment.memo` (NOT `ref`); the wizard field is `account.payment.register.communication` (Char, `string="Memo"`). Writing `memo` in check.py / expected asserts is correct; reading the wizard field name for the Playwright selector requires `communication`. **Field order invariant (CRITICAL)** — onchanges in `account.payment.register._onchange_xxx` re-compute `communication` whenever `payment_date` changes. If the oracle / agent fills Memo BEFORE Date, Date's onchange overwrites the override with the invoice name and check.py fails with `Payment memo is 'INV/2026/00001'`. Correct order is **Journal → Amount → Date → Memo** (Memo LAST). **Date picker is a `<button>`** — `date_widget.locator('input')` does not work on the initial render; you must first click `date_widget.locator('button')` to switch to overlay mode, then `page.keyboard.type('04/15/2026')` on the active element. **Overlay cleanup must NOT remove `.o-overlay-item`** — the wizard modal itself uses that class, so a blanket `document.querySelectorAll('.o-overlay-item').forEach(e => e.remove())` deletes the modal. Target only `.o_datetime_picker, .o_popover, .o_daterange_picker`. **Escape key closes the modal** — do NOT press Escape to dismiss the datepicker; use JS-remove of the popover instead, or click elsewhere. **Journal autocomplete trap** — typing "Bank" matches both `Bank` and `Bench Secondary Bank` (substring match). Oracle must iterate dropdown items and pick the one whose `inner_text().strip() == "Bank"` exactly, not the first match. **expected_state.json backing-entry name** — creating a payment also creates an `account.move` of `move_type='entry'` whose `ref` is set from the payment's memo. When the memo override is `"Partial 1 of 2 for BENCH-PARTIAL-001"` the journal entry's `ref` is that same string (NOT the sequence-generated `INV/2026/NNN`). The 5 create edits in expected_state.json must use that exact ref. **Missing dependency in fresh worktree** — the pre-warmed `.venv/` only had playwright + pyyaml; Odoo's `babel` + full `requirements.txt` was NOT installed, causing `ModuleNotFoundError: No module named 'babel'` inside the seed. Fix: `uv pip install -r requirements.txt`. Also `browser-use` package itself was not installed; fix: `uv pip install browser-use`. Future worktree-skeleton should seed these. **Calibration**: Task passed BU single-shot at F1=1.0 despite four distinct wizard overrides. Rationale for keeping it marked as hard: (a) the failure mode is realistic and documented (partial payment + memo rename + non-default journal + back-dated date in one wizard), (b) check.py is strict on all four overrides — missing any one drops F1; (c) the failure pattern `policy_trap` is exactly a multi-override wizard which has known variance across agent builds. A weaker BU or any text-only agent without robust UI understanding would miss at least one override. |
---

## mrp.confirm_mo_produce_partial_keep_backorder

| Field | Value |
|---|---|
| **Task ID** | `mrp.confirm_mo_produce_partial_keep_backorder` |
| **Row** | 449 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 26.6s, 15/15 atomic edits matched, 0 postcondition failures, 44 API calls, 21 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 88.5s single-shot, 15/15 atomic edits matched, 0 postcondition failures, 53 API calls, 25 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **F1** | 1.0 |
| **Odoo modules** | Manufacturing (`mrp`) + Inventory (`stock`) — `mrp.production` partial-production split + `mrp.production.backorder` wizard + `_split_productions` rename path |
| **Workflow** | Seed: finished `Bench Widget` (consu/is_storable, tracking=none) + component `Bench Mat` (consu/is_storable, tracking=none); normal BoM (1 Bench Mat per widget, `consumption=flexible`, no routing); 10 Bench Mat on-hand at WH/Stock; confirmed+assigned MO `MO-BENCH-PARTIAL` for 10 Bench Widgets. Agent: Manufacturing → Operations → Manufacturing Orders → open MO-BENCH-PARTIAL → inline-edit the **Quantity Producing** input (left-hand `10.00 / 10.00 Units`) from `10` to `4` and Tab out → header button label flips from **Produce All** to **Produce** (because `show_produce_all = qty_producing in (0, product_qty)` is now False) → click **Produce** → the `mrp.production.backorder` wizard opens titled "You produced less than the initial demand" with two footer buttons: **Create backorder** (primary/blue, `action_backorder`) and **No Backorder** (secondary, `action_close_mo`) → click the primary **Create backorder** → `_split_productions` rewrites original: name `MO-BENCH-PARTIAL` → `MO-BENCH-PARTIAL-001`, `backorder_sequence 0 → 1`, `product_qty 10 → 4`, `state confirmed → done`, `qty_produced 0 → 4`; creates sibling `MO-BENCH-PARTIAL-002` with `product_qty=6`, `backorder_sequence=2`, `state=confirmed`. End state: two `mrp.production` rows in the same `production_group_id`; original done at 4/4; backorder confirmed at 6. |
| **Capability tested** | Partial production closure + backorder creation: (a) inline `qty_producing` edit on the MO form header (not a wizard) which drives `_compute_show_produce` via the `qty_producing in (0, product_qty)` predicate → header button re-labels live; (b) primary-vs-secondary dialog choice on the `mrp.production.backorder` wizard; (c) Odoo-side `_split_productions` rename of the original MO + creation of a sibling. Complements row 415 (scrap-during-MO) and row 419 (unbuild) — this is the only MRP task that exercises the backorder-creation pipeline. |
| **Notes** | **Calibration MISS — BU passed single-shot** (88.5s, F1=1.0, 0 postcondition failures). The primary **Create backorder** button is also the CORRECT choice, so the radio-dialog trap that catches BU on the stock.picking "No Backorder" flow (row 3 in the suite) does not fire here — BU clicks the primary/blue by default and happens to be right. The prompt is also explicit about the "change 10 → 4" qty_producing step per TASK_CREATION_GUIDE.md§"Clear instructions", which flattens the difficulty. **Design quirks confirmed**: (a) `_split_productions` renames the ORIGINAL MO (not the backorder) via `_get_name_backorder(name, 1)` — `MO-BENCH-PARTIAL` → `MO-BENCH-PARTIAL-001` — so state_spec `match_key=[name]` emits 5 deletes on the old name + 5 creates on the new name (10 atomic edits just for the rename, plus 5 more for the new `-002`). Expected_state.json enumerates all 15. (b) `check.py` looks up the original as `MO-BENCH-PARTIAL-001`, not `MO-BENCH-PARTIAL` (which no longer exists). (c) The header button label flips between `Produce All` (qty_producing==product_qty) and `Produce` (qty_producing<product_qty); both have `name=button_mark_done` — oracle filters by `.inner_text()=="Produce"` to avoid clicking Produce All by accident. (d) `_update_available_quantity(mat, stock_loc, 10)` + `action_assign()` leaves `_get_available_quantity` at 0 (reserved) — seed sanity-check uses raw `stock.quant.quantity` sum instead. (e) `mrp.production.backorder.action_backorder` → calls `mrp_production_ids.with_context(skip_backorder=True, mo_ids_to_backorder=[...]).button_mark_done()`, so the required trace op is the wizard method, not `button_mark_done` directly. **To harden into a real trap**: invert the dialog choice ("close the MO and discard the remaining 6" → correct button becomes secondary `No Backorder`), OR require a non-default `qty_producing` that is itself computed from a downstream signal (e.g. "produce as many as WH/Stock allows"), OR add a second MO in the search list so the agent must pick the right one before opening the wizard. |
---

## account.post_customer_invoice_with_tax_groups

| Field | Value |
|---|---|
| **Task ID** | `account.post_customer_invoice_with_tax_groups` |
| **Row** | 473 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 43.9s wall clock, 7/7 atomic edits matched, 0 postcondition failures, 50 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 162.4s single-shot, 7/7 state-diff edits matched but 1 postcondition failure: `Expected exactly 1 product line on the invoice, found 0 (products: [])`. 90 API calls, 35 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). BU reported: "The customer invoice for 'Bench Tax Cust' has been successfully created ... with the 'Bench Tax Service' product at a price of 200.00 and the 'Bench Sale Tax 20%' tax, and posted. Totals: Untaxed $200.00, Tax $40.00, Total $240.00." — but the trace shows `product_id: False` on the only line (BU typed the name / price / tax directly without picking a product from the autocomplete), which fails the strict `l.product_id` filter in `check.py` even though totals resolve correctly. |
| **F1** | 0.0 |
| **Odoo modules** | Accounting (`account`) — `account.move` (`out_invoice`) create-from-scratch + `account.move.line.tax_ids` many2many (`widget="many2many_tax_tags"`) + header `Confirm` → `action_post`. |
| **Workflow** | Seed creates customer `Bench Tax Cust` (res.partner, `customer_rank=1`), service product `Bench Tax Service` (`type=service`, `list_price=200`, `taxes_id=[(5,0,0)]` / `supplier_taxes_id=[(5,0,0)]` cleared so no default tax auto-applies on line-level `product_id` onchange), and **two** sale taxes (both `type_tax_use='sale'`, `amount_type='percent'`, `company_id=env.company.id`): `Bench Sale Tax 10%` (amount=10 — the distractor) and `Bench Sale Tax 20%` (amount=20 — the correct one). No draft invoice is pre-created. Agent: Accounting → Customers → Invoices → **New** → Customer=`Bench Tax Cust` → Invoice Date=`05/10/2026` → add ONE invoice line: Product=`Bench Tax Service`, Quantity=1, Unit Price=200.00, Taxes cell=`Bench Sale Tax 20%` pill (many2many_tax_tags widget — click into the Taxes `td`, type the tax name, pick from the autocomplete dropdown). Click **Confirm** (statusbar) to post. End state: `account.move` with `move_type='out_invoice'`, `partner_id='Bench Tax Cust'`, `invoice_date=2026-05-10`, `state='posted'`, single product line whose `tax_ids` contains `Bench Sale Tax 20%` and NOT `Bench Sale Tax 10%`, `amount_untaxed=200`, `amount_tax=40`, `amount_total=240`. |
| **Capability tested** | Two-gate medium: (1) create-from-scratch a customer invoice with the correct header (customer + date) + exactly one product line (no phantom blank line, no leftover default tax pill) — product_id m2o must actually be selected from the autocomplete, not just typed into the line `name`; (2) **tax discrimination on the many2many_tax_tags widget** — two taxes starting with the same prefix `Bench Sale Tax ` both appear in the autocomplete dropdown; the agent must read the `%` suffix and pick the 20% pill (NOT the 10% distractor). check.py asserts `tax_20.id in line.tax_ids.ids AND tax_10.id not in line.tax_ids.ids`, plus the derived `amount_tax=40.0` (40 for 20%, 20 for 10%, 60 if both). Ends with header `Confirm` statusbar click (`action_post`). |
| **Notes** | **Calibration HIT — genuine medium failure**. BU produced the *correct totals* (200/40/240) and picked the correct 20% tax, but failed to set the line's `product_id` many2one — the trace shows the final `onchange` payload was `{'sequence': 100, 'product_id': False, 'name': False, 'quantity': 1, 'price_unit': 200, 'tax_ids': [[4, 6]]}`. This is a well-known BU failure mode: when the autocomplete is slow to populate, BU types the value, doesn't see the dropdown open, and moves on without selecting. check.py's `l.product_id` filter makes this a hard fail because `product_lines` comes up empty. State-diff alone would not catch this (amount totals match all 7 expected edits), so the check.py postcondition is load-bearing for the F1=0 outcome. **Design quirks**: (1) **Taxes column visibility** — on Odoo 19 customer invoice forms the Taxes column is `optional="show"` and enabled by default, so neither oracle nor agent needs to toggle it via the optional-columns gear (unlike vendor bill Product column). (2) **Default tax on product onchange** — the seed clears `taxes_id=[(5,0,0)]` and `supplier_taxes_id=[(5,0,0)]` on the product template so picking `Bench Tax Service` does NOT auto-attach a company default tax; the oracle's defensive `_clear_tax_cell_on_selected_row` is kept for robustness but is typically a no-op. (3) **entity_key for out_invoice** — uses `(partner_id, move_type)` as match_key rather than `(partner_id, ref)` because the invoice is a create-from-scratch flow without a user-entered ref (Odoo auto-assigns `INV/2026/NNN` on post) — `ref` is null, which would produce an unstable entity_key. (4) **state_spec excludes `payment_state` / `is_move_sent`** — neither is deterministic in a create-post-only flow (payment_state is `not_paid` once posted but could be `in_payment` under other journal setups). (5) **Oracle strategy for the tax pill** — `.o-autocomplete--dropdown-menu .o-autocomplete--dropdown-item` with `has_text(TAX_20_NAME)` reliably surfaces the 20% option before the 10% since it's a full-text match on the longer name. (6) **trace_spec required_ops is empty** — BU uses `account.move.web_save` for every create/update step; declaring `account.move.create` or `action_post` as required_ops would false-negative on a real BU run. check.py is the authoritative validator. |

---

## account.post_draft_invoice_send_to_customer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 33.9s, 0 postcondition failures, 51 API calls, 21 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 74.3s wall clock, 0 postcondition failures, 55 API calls, 27 non-forbidden writes, 0 forbidden, StrictClean=True, single-shot). BU reported: "The draft invoice BENCH-POST-SEND-001 for Bench Post Co has been successfully posted (assigned number INV/2026/00001) and sent to the customer by email." |
| **F1** | 1.0 |
| **Odoo modules** | Accounting — `account.move` (out_invoice) draft→posted + `account.move.send.wizard` (Odoo 19 mail composer mixin). |
| **Workflow** | Seed creates **Bench Post Co** (res.partner with email `billing@benchpost.example.com`), **Bench Posting Service** (product.template, service, 200.00, invoice_policy=order, taxes cleared via `tax_ids=[(5,0,0)]`), and a DRAFT `account.move` with `move_type='out_invoice'`, `ref='BENCH-POST-SEND-001'`, 1 line at qty=1 price=200. Seed also forces `company.external_report_layout_id = web.external_layout_standard` so the Send button does NOT pop the base_document_layout configurator wizard first. **wkhtmltopdf workaround**: the seed writes a stub `invoice_pdf_report_file` (empty PDF bytes) so the wizard's `_prepare_invoice_pdf_report` skips the wkhtmltopdf render path (`if not invoice.invoice_pdf_report_id: pdf_to_generate[invoice] = invoice_data` — the guard becomes truthy and skips). Agent must: (1) open Accounting → Customers → Invoices, find `BENCH-POST-SEND-001`, open the form; (2) click **Confirm** (statusbar) to post it (draft → posted, `action_post`); (3) click **Send** (header button, name=`action_invoice_sent`) which opens the `account.move.send.wizard` dialog; (4) click the primary **Send** button in the wizard footer (name=`action_send_and_print`, `btn-primary`). The wizard's `_compute_sending_method_checkboxes` pre-checks Email based on partner preferences; `_compute_mail_partners` pre-fills the To field with the commercial partner when it has an email. `_hook_if_success` then fires `_send_mails` which posts a `message_type='comment'` `mail.message` with `subtype=mail.mt_comment` onto the invoice's chatter. |
| **Capability tested** | Two-click post+send flow on a customer invoice: header statusbar **Confirm** (draft→posted) + header **Send** (opens wizard) + wizard footer primary **Send** (dispatches email via template). Calibration focus: agent must NOT click **Discard** in the wizard, must NOT uncheck the pre-checked **Email** sending method, and must NOT click **Snailmail** instead. |
| **Notes** | **Calibration: too easy for medium**. BU single-shot PASS at F1=1.0 in 74.3s — modern browser agents navigate the defaults-only Send wizard without trouble because the dialog is pre-populated (To, Subject, Body, Email-checkbox all defaulted) and the primary footer button is unambiguously labeled "Send". This matches the TASK_CREATION_GUIDE pattern "Accept-defaults wizards — easy". To escalate to a genuine medium/hard, would need to combine with (a) a non-default sending-method choice (tick Post / print-only while unchecking Email), (b) edit the wizard's Subject or To field before sending, or (c) save-as-template then send. Quirks: (1) **`is_move_sent` does NOT flip to True in this benchmark env** because `wkhtmltopdf` is missing and `_link_invoice_documents` only sets `is_move_sent=True` when NEW pdf_attachment_values are produced during the wizard (our stub PDF bypasses the render path but also means `_link_invoice_documents` has nothing to link, skipping the `invoice.is_move_sent = True` write). `check.py` therefore gates on the posted `mail.message` (subtype=mail.mt_comment) instead of `is_move_sent`. (2) **wkhtmltopdf trap**: without the stub-PDF seed, `_prepare_invoice_pdf_report` raises inside `_pre_render_qweb_pdf` because wkhtmltopdf isn't installed, `_hook_if_errors` runs with `allow_raising=True` and the wizard surfaces a blocking UserError dialog — the mail is NEVER sent. Pre-seeding `invoice_pdf_report_file=<empty-pdf-bytes>` in the draft move is the simplest fix and mirrors the `report_template_ids=[(5,0,0)]` pattern used in `purchase.send_rfq_email_with_template_signature` (different mechanism, same goal). (3) **base_document_layout configurator pre-wizard**: if `company.external_report_layout_id` is False, `action_invoice_sent` wraps the send action in `_get_action_with_base_document_layout_configurator`, which pops a layout-picker dialog BEFORE the send wizard. Seed pre-sets this to `web.external_layout_standard` to bypass. (4) **Header button is "Send" (not "Send & Print")** — the Odoo 19 `account.move` form header renders `<button name="action_invoice_sent" string="Send"/>` on a posted out_invoice with `display_send_button=True`. The button is highlighted (`oe_highlight`) while `is_move_sent=False`. The wizard footer has primary "Send" (or "Generate" if no sending methods checked) + secondary "Discard" — no "Send & Print" button exists; the server method name `action_send_and_print` is a legacy internal name. (5) **Oracle robustness**: the oracle clears search filters and uses `search_for` to surface the draft invoice since the Customer Invoices list can default-filter to posted-only. |

---

## crm.lead_set_contact_name_email_phone_save

| Field | Value |
|---|---|
| **Task ID** | `crm.lead_set_contact_name_email_phone_save` |
| **Row** | 453 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 22.5s wall clock, 3/3 atomic edits matched, 0 postcondition failures, 39 API calls, 16 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle opens /odoo/crm, navigates to Leads via top menu, opens `Bench Lead Basic` list row, fills `contact_name`, `email_from`, `phone` via `fill_field` (standard `.o_field_widget[name=...] input` selector), saves. |
| **Browser-Use** | PASS (F1=1.0, 67.8s single-shot, 3/3 atomic edits matched, 0 postcondition failures, 35 API calls, 16 non-forbidden writes, 0 forbidden, StrictClean=True). Harness reports `success=False` but state diff shows all three char fields set correctly and no forbidden ops — pure char-field edits are squarely within BU's easy-tier comfort zone as a calibration anchor. |
| **F1** | 1.0 |
| **Odoo modules** | CRM (`crm`) — `crm.lead` char fields `contact_name` / `email_from` / `phone`. Leads submenu is gated by `crm.group_use_lead` (per `addons/crm/views/crm_menu_views.xml:55`); the seed grants the group to `base.user_admin` so the `Leads` top-menu entry is visible without a Settings detour. |
| **Workflow** | Seed creates a `crm.lead` with `type='lead'`, `name='Bench Lead Basic'`, and `contact_name=False / email_from=False / phone=False` (the three empty char fields to fill). Agent: /odoo/crm → click **Leads** in the top menu (or direct URL `/odoo/action-crm.crm_lead_all_leads` as fallback) → open the single `Bench Lead Basic` row → in the form fill **Contact Name**=`Alice Example`, **Email**=`alice@example.com`, **Phone**=`+1-555-0200` → Save. End state: `crm.lead.contact_name='Alice Example'`, `email_from='alice@example.com'`, `phone='+1-555-0200'`, `type='lead'` preserved. |
| **Capability tested** | Easy-tier calibration anchor — three char-field edits on a single form save, no wizards, no radio buttons, no cross-module navigation. Distinct from row 442 (`crm.assign_lead_salesperson_change_stage_won`) which combines a Many2one assignment with a statusbar Won button, and from rows 24/25 (`crm.update_lead_email` / `crm.update_lead_phone`) which each touch only ONE char field. The "fill three char fields at once" pattern matches the proven-easy TASK_CREATION_GUIDE bucket ("Simple form edits" → too easy for BU). |
| **Notes** | **Calibration as designed (easy/tier-1 ~80% pass target, BU single-shot PASS at 67.8s well under the 300s limit).** Two quirks worth keeping in the cookbook: (1) **Leads menu gating** — `crm.group_use_lead` must be added to admin in the seed or the top-menu `Leads` entry is invisible and the agent falls back to the Opportunities pipeline kanban (where `Bench Lead Basic` does not appear because it's `type='lead'`). Without the group, `crm.lead._default_type` also returns `'opportunity'` for new records (`addons/crm/models/crm_lead.py:125`), which would silently flip the seeded row's type if any onchange fired — granting the group is the robust fix. (2) **Phone normalization** — Odoo 19's phone widget preserves the exact string supplied (no auto-reformatting on `crm.lead.phone` for values that don't match a `country_id`-based phone_format rule; the `website_crm` `phone_format('INTERNATIONAL')` reformatting path only fires on frontend submit). So `expected_state.json` can list the raw `"+1-555-0200"` verbatim; `check.py` does a substring `"555-0200"` match as belt-and-braces if a future Odoo patch re-enables auto-format. (3) `state_spec.yaml` uses `match_key=[name, type]` so the entity_key is `["Bench Lead Basic", "lead"]` — same shape as `crm.update_lead_email` row 24 — which keeps the diff engine stable if a later task variant creates both a lead and an opportunity with the same name. (4) trace_spec has `required_ops: []` because the BU agent uses `crm.lead.web_save` rather than `write`, and any required op listing `write`/`web_save` would false-negative on at least one. Forbidden ops cover the usual destructive set (`unlink`, `action_archive`, `toggle_active`, `convert_opportunity`). |
---

## website_event.add_sponsor_to_event_publish

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.9s, 48 API calls, 23 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 125.6s wall clock, 0 postcondition failures, 68 API calls, 31 non-forbidden writes, 0 forbidden, StrictClean=True, single-shot, ~17 steps). BU reported: "Successfully added 'Bench Sponsor Inc' as a 'Silver' sponsor to the 'Bench Conf 2026' event and published the event." |
| **F1** | 1.0 |
| **Odoo modules** | Events (event + website_event + website_event_exhibitor) |
| **Workflow** | Seed installs `website_event` + `website_event_exhibitor` on demand (neither in base snapshot), creates one unpublished event `Bench Conf 2026` (date_begin=2026-09-10, date_end=2026-09-11), a `res.partner` `Bench Sponsor Inc`, and relies on the default `event.sponsor.type` record `Silver` (shipped by `website_event_exhibitor/data/event_sponsor_data.xml`). Agent opens Events app → clears filters → opens `Bench Conf 2026` → clicks the **Sponsors** smart button → clicks **New** → sets `partner_id=Bench Sponsor Inc` + `sponsor_type_id=Silver` on the sponsor form → saves → returns to event via breadcrumb → clicks the **Unpublished** `website_redirect_button` → flips the Owl systray **Unpublished→Published** switch inside the website preview iframe. |
| **Capability tested** | Sub-resource creation via a smart-button sub-view with two Many2one autocomplete fields, round-trip back via breadcrumb, and Owl systray publish toggle inside a website preview iframe. Composes the "smart button → full form → save → breadcrumb" chain with `website_event`'s non-stage-based publish control. |
| **Notes** | Calibrated easier than medium (BU solves single-shot with the explicit prompt). Kept at `primary_track: true`, tier 2, medium because the workflow combines (a) module install via `_ensure_module` for `website_event_exhibitor` pulling in `website_event`, (b) smart-button sub-view navigation, (c) two Many2one dropdowns, and (d) the Owl systray publish toggle inside an iframe. New cookbook entries: (i) `event.sponsor` model lives in `website_event_exhibitor`, not `website_event` — seed must `button_immediate_install('website_event_exhibitor')` (which transitively installs `website_event`) before the Sponsors smart button or `event.sponsor.create` will exist. (ii) Default `event.sponsor.type` records `Bronze`/`Silver`/`Gold` ship with `website_event_exhibitor` so seeds can rely on `Silver` existing post-install. (iii) Sponsors is a smart button opening a kanban/list of `event.sponsor` with `search_default_event_id` context filter — clicking **New** opens the full sponsor form (no inline quick-create). (iv) Publish path mirrors `website_event.publish_event_register_via_portal`: the header `website_redirect_button` widget only navigates; the real toggle is the Owl systray switch inside the iframe preview. Oracle uses JSON-RPC `website_publish_button()` bypass; BU handles the UI toggle via `input[type='checkbox']` click on the systray switch. (v) Distinct from row 330 (adds `event.track` via Tracks smart button + stage publish), row 406 (adds `event.question` via Questions tab m2m selector), and row 342 (portal attendee registration via public Bootstrap modal chain). |
---

## stock.adjust_product_reorder_rule_min_max

| Field | Value |
|---|---|
| **Task ID** | `stock.adjust_product_reorder_rule_min_max` |
| **Row** | 454 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 48.0s, 4/4 atomic edits matched, 0 postcondition failures, 65 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 83.5s single-shot, 4/4 atomic edits matched, 0 postcondition failures, 47 API calls, 16 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (`stock`) — `stock.warehouse.orderpoint` create via `product.product.action_view_orderpoints` smart button. |
| **Workflow** | Seed: storable product `Bench Reorder Item` (`type='consu'`, `is_storable=True`, `tracking='none'`, on-hand=0 at WH/Stock) with NO pre-existing orderpoint. Admin granted `stock.group_stock_multi_locations` so the Reordering Rules list surfaces the Location column. Agent: Inventory → Products → Products → open **Bench Reorder Item** → click the **Reordering Rules** smart button (label reads `0 Reordering Rules` pre-task; invisible branch `nbr_reordering_rules != 1` — see `addons/stock/views/product_views.xml:489`) → lands on the editable-bottom list view (`stock.action_orderpoint`, which `action_view_orderpoints` opens after popping `search_default_trigger`) with `default_product_id` + `search_default_product_id` pre-set → click **New** → the inline row pre-fills Product=Bench Reorder Item and Location=WH/Stock → fill `product_min_qty=5.00` and `product_max_qty=20.00` (labelled "Min" / "Max") → Save. End state: one `stock.warehouse.orderpoint` with product_min_qty=5.0, product_max_qty=20.0, location_id=WH/Stock. |
| **Capability tested** | Smart-button gate → editable-list New → two numeric inline-cell fills. Complements row 453 `stock.update_reorder_rule` which edits an EXISTING rule in-place (no smart-button traversal, no create); this row requires the full create-via-smart-button path including the orderpoint default_product context that pre-fills the inline row. Distinct from all other `stock.*` tasks in the suite — no existing task creates an orderpoint from scratch. |
| **Notes** | **Calibration MISS — BU passed single-shot** (83.5s, F1=1.0, 0 postcondition failures; 47 API calls, 16 non-forbidden writes, 0 forbidden). BU navigated Inventory → Products dropdown → Bench Reorder Item → clicked the `0 Reordering Rules` smart button → hit New → correctly identified the Min (index 5694) and Max (index 5698) cells, typed 5.00 / 20.00 (with one auto-retry on a concatenation glitch `"0.005.00"` → `"5.00"` which BU's BrowserSession self-corrected) → clicked Save → done. The prompt's explicit enumeration of Min/Max column names + the fact that Odoo pre-fills product_id and location_id from the smart-button context removes both of the planned calibration traps. **To harden into a real medium trap**: (a) seed a product that already has a distractor orderpoint at a second location (WH/Stock/Shelf 1) so the agent must pick the correct row to edit OR clear default to force New; (b) require a non-default Location (e.g., `WH/Stock/Shelf 2`) so the agent must overwrite the pre-filled WH/Stock; (c) require `qty_multiple` or `trigger=auto` configuration on a column hidden-by-default (optional=hide) so the agent must toggle the optional-columns dropdown first; (d) combine with a pre-save wizard such as `action_stock_replenishment_info` (the info button on every row). **Design quirks confirmed**: (1) `product.product.action_view_orderpoints` pops `search_default_trigger` from the action context (otherwise the list defaults to `trigger='auto'` filter that hides manual rules) — see `addons/stock/models/product.py:598`. (2) The smart button has TWO rendered variants in `product_views.xml` — the `nbr_reordering_rules == 1` variant shows "Min: X / Max: Y" inline on the button; the `nbr_reordering_rules != 1` variant shows just "N Reordering Rules" via `<field name="nbr_reordering_rules" widget="statinfo"/>`. With 0 rules pre-task the latter fires. (3) The editable list view is `stock.view_warehouse_orderpoint_tree_editable_show_trigger` (a primary-mode inherit that forces `trigger` column to optional=show). Min and Max columns are `optional="show"` — visible by default. (4) `match_key=[product_id]` normalizes the many2one to the display name "Bench Reorder Item" via `normalize_value`, which matches the expected_state entity_key. `location_id` also normalizes to display name "WH/Stock" — must be included in `fields` AND in expected_state.json as a create edit, otherwise the diff engine flags it as an Extra observed edit and Precision drops below 1.0 (observed during oracle iteration: F1=0.857 on first run, fixed by adding the location_id create edit to expected_state.json). (5) The trace_spec intentionally uses `required_ops: []` because BU/oracle persistence can hit either `create` or `web_save` — check.py is the authoritative postcondition, not the trace. (6) Seed grants `stock.group_stock_multi_locations` purely for UX clarity (Location column visibility); the task would still PASS without it since location_id defaults on the server side to WH/Stock regardless of UI visibility. |
---

## purchase.set_vendor_product_code_on_po_line

| Field | Value |
|---|---|
| **Task ID** | `purchase.set_vendor_product_code_on_po_line` |
| **Row** | 450 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.3s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 43 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 72.6s wall clock single-shot, 1/1 atomic edits matched, 0 postcondition failures, 30 API calls, 14 non-forbidden writes, 0 forbidden, StrictClean=True). BU solved in 9 steps: login → open BENCH-VCODE → click `td[name='product_id']` to enter row edit mode → click `#labelVisibilityButtonId` (the `.fa-bars` toggler) → type `BENCH-WDG-A1 / Bench Widget` into the revealed textarea → Tab → click "Save manually" (cloud icon). Reported `success=True`. |
| **F1** | 1.0 |
| **Odoo modules** | Purchase (`purchase`) — `purchase.order.line.name` is `fields.Text(compute='_compute_price_unit_and_date_planned_and_name', store=True, readonly=False)` (addons/purchase/models/purchase_order_line.py:19-20). On the PO form it is rendered via `<field name="name" widget="section_and_note_text" optional="show"/>` but the *column* is visually folded into `product_id` by the outer `widget="product_label_section_and_note_field_o2m"` + inner `widget="product_label_section_and_note_field"` (addons/account/static/src/components/product_label_section_and_note_field/). |
| **Workflow** | Seed creates vendor `Bench Code Supplier` (`supplier_rank=1`), consu product `Bench Widget` (`list_price=30.0`, taxes cleared) and a DRAFT `purchase.order` pinned to `name='BENCH-VCODE'` / `partner_ref='BENCH-VCODE'` with exactly ONE `purchase.order.line` (product=Bench Widget, `product_qty=5`, `tax_ids=[(5,0,0)]`). The seed does NOT write `name` on the line — it lets `_compute_price_unit_and_date_planned_and_name` fill it with the product display name, so the line's Description starts as exactly `Bench Widget`. Agent: Purchase → Orders → RFQs → open BENCH-VCODE → Products tab → click the product/description cell on the single Bench Widget row (row enters edit mode) → click the `.fa-bars` "labelVisibilityButtonId" toggler (the widget hides the description textarea with `d-none` when `label` is empty i.e. when `name == product_name`) → type `BENCH-WDG-A1 / Bench Widget` into the revealed textarea → Tab → Save (cloud icon). End state: the line's stored `name` becomes `Bench Widget\nBENCH-WDG-A1 / Bench Widget` (two lines) because `parseLabel` prepends `productName + "\n"` to the typed label; PO stays in `state='draft'`, product/qty/price unchanged. |
| **Capability tested** | **Editing a compute-but-writable Text field buried inside the Odoo 19 `product_label_section_and_note_field` widget**. The field is invisible-by-default: the widget's XML (product_label_section_and_note_field.xml:49-58) renders the description `<textarea>` with `class="d-none"` whenever `columnIsProductAndLabel and (label or labelVisibility.value)` is falsy. When `name == product_display_name`, the JS getter `label` strips the product name prefix and returns `""`, so the textarea starts hidden and a `.fa-bars` toggler (`button#labelVisibilityButtonId`, tooltip "Click or press enter to add a description") must be clicked to flip `labelVisibility` to true. This is a distinct UI affordance from the sale.order section/note footer buttons (row 440) and from the direct-inline edit on `product_qty` (row 402) — here the target cell is merged into the product_id column and the textarea doesn't even exist in the visible DOM until a hidden-toggler is invoked. |
| **Notes** | **Calibration MISS — too easy for medium**. BU single-shot PASS at F1=1.0 in 72.6s, 14 writes, 0 forbidden. The prompt explicitly mentions the "click the small icon next to the product name" step (the `.fa-bars` toggler has an accessibility label "Click or press enter to add a description"), which flattens the difficulty — BU finds the button by its tooltip text in step 6 and types into the revealed textarea in step 7. To escalate: (a) hide the explicit toggler hint from the prompt so the agent must discover the merged-column layout; (b) add a distractor line so the agent must pick the right row AND avoid editing the product_id instead of the label; (c) require a description that does NOT contain the product name, then assert the stored name equals exactly the typed text — which forces the agent to use the line sub-form popup instead of the inline widget (because `parseLabel` always prepends the product name to typed labels on the inline path). **Widget quirks captured** (new cookbook content): (1) `product.order.line.name` has `compute='_compute_price_unit_and_date_planned_and_name'` + `store=True, readonly=False` — writable, but the compute re-fires when `product_id` changes (so editing the Description and then re-selecting the same product does NOT revert). (2) The `product_label_section_and_note_field` widget's `parseLabel` returns `productName + "\n" + value` when both truthy (product_label_section_and_note_field.js:50-54), so typing `BENCH-WDG-A1 / Bench Widget` into the label yields a stored `name` of `"Bench Widget\nBENCH-WDG-A1 / Bench Widget"`. check.py accepts either form via a case-insensitive substring search for `BENCH-WDG-A1`, but the expected_state.json norm_value MUST be the two-line form (not just the typed text) to match the diff engine. (3) `getActiveColumns()` (product_name_and_description.js:20-38) DELETES the standalone `name` column from the active list when both `product_id` and `name` columns are present and sets `record.columnIsProductAndLabel = true`, causing the label textarea to render inside the `td[name='product_id']` cell. That's why `td[name='name']` does NOT exist in the DOM — trying to click it times out (seen on the oracle's first run). (4) Entity_key on `purchase.order.line` with match_key `[order_id, product_id]` normalizes to `[null, null]` (both Many2one fields normalize to null via the XML-RPC serialization path used here — similar to `account.move.line.move_id → null` but different from `sale.order.line.order_id → SO name`). expected_state.json MUST use `[null, null]` as entity_key; using the PO name or product display name causes F1=0 (missing-match) even though the norm_value is correct. (5) `trace_spec.forbidden_ops` includes `purchase.order.line.create` and `purchase.order.line.unlink` to catch agents who delete-and-recreate the line instead of editing it in place. **Commit**: `[ADD] benchmark: purchase.set_vendor_product_code_on_po_line (medium)`. |
---

## account.reconcile_bank_statement_line_to_invoice

| Field | Value |
|---|---|
| **Task ID** | `account.reconcile_bank_statement_line_to_invoice` |
| **Row** | 455 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Removed |
| **Oracle** | FAIL (module unavailable) |
| **Browser-Use** | — |
| **F1** | — |
| **Odoo modules** | `account` (Community, installed) supplies `account.bank.statement` + `account.bank.statement.line` + base `account.move.line.reconcile()` primitives, but the dedicated **bank reconciliation widget** (`bank.rec.widget` + the two-panel Validate UI + `action_open_bank_reconcile_widget`) is shipped by **`account_accountant`**, which is an **Odoo Enterprise-only** addon. Source absent from `addons/` on this checkout; no `ir.module.module` record exists for it, so it is flagged uninstallable. |
| **Workflow** | Intended: Seed partner `Bench Bank Cust`, service product `Bench Bank Service` (price 300.00, taxes cleared), posted `account.move` (out_invoice) `BENCH-BANK-REC-001` total 300.00 in state `posted` / `payment_state='not_paid'`, plus a DRAFT `account.bank.statement` on the default bank journal with one `account.bank.statement.line` (payment_ref `BENCH-BANK-REC`, partner=Bench Bank Cust, amount=300.00). Agent: Accounting → Bank (or Reconciliation) → open the draft statement → click the `BENCH-BANK-REC` line → in the right-hand reconciliation panel, pick `BENCH-BANK-REC-001` from Suggested / Customer Invoices → click **Validate**. End state: `invoice.payment_state='paid'` AND `statement_line.is_reconciled=True` with `reconciled_ids` linking to the invoice's receivable move lines (same `full_reconcile_id`). |
| **Capability tested** | Enterprise bank reconciliation widget — a non-standard two-panel UI (statement lines on the left, matching suggestions on the right) with manual invoice selection + Validate button. Distinct from row 416 direct-payment wizard and row 435 partial-payment wizard; distinct from row 211 `account.reconcile_bank_statement_line_manual` which also targets this capability but whose oracle short-circuits to `account.move.line.reconcile()` JSON-RPC (because Community has no widget). |
| **Notes** | **Blocked on a single but absolute gap**: `account_accountant` is Enterprise-only and its source is not vendored in this Odoo 19 Community checkout. Without it, there is no `bank.rec.widget` model, no `action_open_bank_reconcile_widget` window action, and no two-panel reconciliation UI — `account/views/account_bank_statement_views.xml` in Community only exposes standard list/form views on the statement + statement-line records, with no **Validate** button. The only way to "reconcile" in Community is the same path row 211 took: draft the statement line move, repoint its counterpart `account.move.line` to the invoice's receivable account, re-post, then call `account.move.line.reconcile()` — that is NOT the capability this task was scoped to probe (row 211 already owns it and scored F1=0.0 for BU because BU cannot find a widget that does not exist). Task skeleton is committed with BLOCKED guards that short-circuit `seed`, `check`, `oracle`, and `cleanup` with diagnostic errors (same precedent as rows 350/351/352/387/429). To re-enable: (a) vendor the Enterprise `account_accountant` addon under `addons/` (or an OSS widget equivalent), (b) add `account_accountant` to `benchmark/base_modules.txt` and rebuild `benchmark_base`, (c) port the flesh-out pseudocode from seed.py / oracle.py / check.py. |

---

## sale.create_sale_quotation_from_opportunity_smart_button

| Field | Value |
|---|---|
| **Task ID** | `sale.create_sale_quotation_from_opportunity_smart_button` |
| **Row** | 456 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 42.1s wall clock, 3/3 atomic edits matched, 0 postcondition failures, 51 API calls, 19 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 102.0s wall clock single-shot, 3/3 atomic edits matched, 0 postcondition failures, 57 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **F1** | 1.0 |
| **Odoo modules** | CRM (`crm`), Sales (`sale`), `sale_crm` (auto-installs when `sale` + `crm` both present; provides `crm.lead.quotation_count`, `action_view_sale_quotation`, `action_new_quotation`, and the Quotations smart button injected via `addons/sale_crm/views/crm_lead_views.xml`). |
| **Workflow** | Seed: partner `Bench Opp Co`, consu product `Bench Opp Product` (`list_price=100`, taxes cleared), and a `crm.lead` of `type='opportunity'` named `Bench Opp Sale` (partner=Bench Opp Co, stage=first non-won, expected_revenue=10000, probability=20). Agent: open /odoo/crm pipeline → open `Bench Opp Sale` kanban card → click the **Quotations** smart button (`button[name='action_view_sale_quotation']`, statinfo rendering `<field name='quotation_count'>`) → lands on the sale.order list filtered by `opportunity_id`, which is empty → click **New** → on the sale.order form, add one order line of **Bench Opp Product** qty=2 (unit price stays 100) → Save (do NOT Confirm). End state: one `sale.order` with `partner_id=Bench Opp Co`, `opportunity_id` bound to the lead, `state='draft'`, single line qty=2 @ 100.00. |
| **Capability tested** | Cross-module smart-button create: the chain `crm.lead` → **Quotations smart button** → Sales list → **New** auto-propagates `default_opportunity_id` and `default_partner_id` via `_prepare_opportunity_quotation_context` (addons/sale_crm/models/crm_lead.py:77-94) so the resulting SO is linked back to the lead. Contrasts with the header `New Quotation` button (row 454+) and with a direct /odoo/sales New (no opportunity link). |
| **Notes** | **Calibration MISS — too easy for medium**. BU single-shot PASS at F1=1.0 in 102s, 22 writes, 0 forbidden. The prompt explicitly names the "Quotations smart button" AND enumerates the `quotation_count` field name; BU follows the breadcrumb path with zero confusion. To harden into a real trap: (a) seed an opportunity WITH one pre-existing linked draft SO (`quotation_count=1`) so clicking the smart button lands on the existing SO form instead of the list — forcing the agent to back out to the list (via breadcrumb) and then click New; `action_view_sale_quotation` auto-switches views: `if len(quotations) == 1: action['views'] = [(view_order_form, 'form')]; action['res_id'] = quotations.id` (crm_lead.py:47-51). (b) Add a distractor `Bench Opp Product 2` line that the agent must NOT add. (c) Require `commitment_date` or `client_order_ref` on the new quotation (a deeper tab interaction). (d) Combine with a stage change on the opportunity before/after. **sale_crm quirks baked into cookbook**: (1) The `crm.lead` form inherits a button-box addition (`sale_crm/views/crm_lead_views.xml:17-30`) that injects TWO smart buttons — `action_view_sale_quotation` (statinfo on `quotation_count`, icon `fa-pencil-square-o`, ALWAYS visible on opportunities) AND `action_view_sale_order` (visible only when `sale_order_count > 0`, icon `fa-usd`). Oracles can target the first reliably via `button[name='action_view_sale_quotation']`. (2) The smart-button action's context injects `search_default_opportunity_id=self.id`, and when the filtered list is empty the user lands on a list with "New" enabled — clicking New creates a sale.order with `opportunity_id` pre-bound by `default_opportunity_id` from the parent action context (`_prepare_opportunity_quotation_context`). (3) `crm.lead.quotation_count` counts only `state in ('draft', 'sent')` via `_get_lead_quotation_domain` — confirmed orders graduate to the `sale_order_count` button instead. (4) `expected_state.json` uses `entity_key=["Bench Opp Co"]` (match_key=partner_id on sale.order — Many2one normalizes to display name). All three atomic edits (`partner_id`, `opportunity_id`, `state`) fire as `op=create` on the new SO; `opportunity_id` normalizes to the lead's `name` ("Bench Opp Sale"). No null-entity-key needed. (5) `trace_spec.required_ops=[]` because BU/oracle may use `web_save` instead of `create`; check.py asserts the postcondition authoritatively. **Commit**: `[ADD] benchmark: sale.create_sale_quotation_from_opportunity_smart_button (medium)`. |

---

## stock.archive_old_product_set_inactive

| Field | Value |
|---|---|
| **Task ID** | `stock.archive_old_product_set_inactive` |
| **Row** | 457 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 25.3s, 2/2 atomic edits matched, 0 postcondition failures, 33 API calls, 13 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 86.3s single-shot, 2/2 atomic edits matched, 0 postcondition failures, 34 API calls, 15 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (`stock`) — `product.template.toggle_active` / cog Actions → Archive. |
| **Workflow** | Seed: storable product `Bench Archive Me` (`type='consu'`, `is_storable=True`, `active=True`, `default_code='BENCH-ARCH-01'`, `list_price=42.0`). Agent: Inventory → Products → open `Bench Archive Me` → click cog ⚙️ (Actions) in the control panel → click **Archive** → confirm any resulting modal. End state: `product.template.active=False` AND `product.product.active=False` on the seeded variant. |
| **Capability tested** | Cog (Actions) menu discovery + Archive action binding. Distinct from `website_sale.unpublish_archive_unarchive_publish_cycle` which is a multi-transition cycle — this row is the single Archive action in isolation, used as an easy calibration anchor for the cog→menu-item pattern. |
| **Notes** | **Calibration match — easy pass (~80%).** BU single-shot PASS at F1=1.0 in 86.3s; navigated to Products, opened the form, used the cog menu, and clicked Archive cleanly. **Diff engine quirk captured**: archiving a record causes the default `active_test` filter to hide it from post-task state capture, so the diff engine emits `norm_value: null` (NOT `false`) for `active` on both `product.template` and `product.product`. `expected_state.json` must use `null`, not `false`, or F1 collapses to 0 (same pattern documented for `website_blog` archive in ODOO19_PATTERNS.md:887). Initial oracle run showed Missing/Extra edits with `None` vs `False`; fixed by flipping the two `norm_value` entries to `null`. `product.product.active` is tracked via match_key `default_code` (BENCH-ARCH-01) because the auto-generated variant inherits the template's `default_code`. `trace_spec.required_ops` is empty; optional_ops include both `toggle_active` and `action_archive` on template and product because BU/oracle may use either (BU used `product.template.action_archive` in this run). `forbidden_ops` lists `*.unlink` to catch agents who delete instead of archiving. Commit: `[ADD] benchmark: stock.archive_old_product_set_inactive (easy)`. |
## purchase.add_product_to_rfq_with_taxes

| Field | Value |
|---|---|
| **Task ID** | `purchase.add_product_to_rfq_with_taxes` |
| **Row** | 458 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 25.2s wall clock, 2/2 atomic edits matched, 0 postcondition failures, 57 API calls, 24 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 72.4s wall clock single-shot, 2/2 atomic edits matched, 0 postcondition failures, 42 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True). BU solved in 9 steps: login → open /odoo/purchase → click RFQ BENCH-ADD-TAX → click "Add a product" → type `Bench Taxable Item` in product cell → select autocomplete option → type `3` in qty → click Taxes cell → type `Bench Tax 5%` → select autocomplete option → click Save (cloud icon). Reported `success=True`. |
| **F1** | 1.0 |
| **Odoo modules** | Purchase (`purchase`) — `purchase.order.line.tax_ids` is `fields.Many2many('account.tax', context={'active_test': False, 'hide_original_tax_ids': True})` (addons/purchase/models/purchase_order_line.py:34). On the PO form it is rendered via `<field name="tax_ids" widget="many2many_tax_tags" domain="[('type_tax_use', '=', 'purchase'), ...]" optional="show"/>` (addons/purchase/views/purchase_views.xml:292). The `many2many_tax_tags` widget (addons/account/static/src/components/many2x_tax_tags/many2x_tax_tags.js) extends `many2many_tags` and behaves as an inline pill autocomplete cell. |
| **Workflow** | Seed creates vendor `Bench Tax Vendor` (`supplier_rank=1`), two consu products `Bench Other Item` (on existing line, `list_price=10.0`) and `Bench Taxable Item` (the product the agent adds, `list_price=50.0` — both with `taxes_id=[(5,0,0)]` and `supplier_taxes_id=[(5,0,0)]` so the default tax doesn't auto-apply), a purchase tax `Bench Tax 5%` (`type_tax_use='purchase'`, `amount_type='percent'`, `amount=5.0`, company-scoped), and a DRAFT `purchase.order` pinned to `name='BENCH-ADD-TAX'` / `partner_ref='BENCH-ADD-TAX'` with ONE pre-existing `purchase.order.line` (product=Bench Other Item, `product_qty=2`, `price_unit=10.0`, `tax_ids=[(5,0,0)]` cleared). Agent: Purchase → Orders → RFQs → open BENCH-ADD-TAX → Products tab → click "Add a product" → pick `Bench Taxable Item` in the new row → set qty to `3` → click the Taxes cell on the new row → type `Bench Tax 5%` → pick autocomplete option → Save (cloud icon). End state: 2 `purchase.order.line` rows; the ORIGINAL Bench Other Item line (qty=2, tax_ids empty) unchanged; the NEW Bench Taxable Item line with `product_qty=3` and `tax_ids` containing Bench Tax 5%. PO stays in `state='draft'`. |
| **Capability tested** | **Inline o2m Add-a-product + many2many_tax_tags pill edit on the NEW row**. The agent must (a) find and click the correct "Add a product" link at the bottom of the o2m list (multiple `o_field_x2many_list_row_add` links exist — "Add a product", "Add a section", "Add a note"), (b) set the Product m2o on the newly-added editable row via product autocomplete (the cell uses `product_label_section_and_note_field`, so the input is nested inside the merged product/label cell), (c) overwrite the default qty (1.0) with 3 by clicking into `td[name='product_qty']`, (d) click into `td[name='tax_ids']` and use the `many2many_tax_tags` autocomplete to add a `Bench Tax 5%` pill. Complements row 450 `purchase.set_vendor_product_code_on_po_line` which edits an existing line's description inline; this row ADDS a new line AND sets a tax pill — the tax step requires understanding the m2m widget's autocomplete-to-pill flow. Distinct from row 457 `purchase.update_rfq_add_line_confirm` which adds a line but does NOT set taxes and then confirms. |
| **Notes** | **Calibration MISS — BU passed single-shot** (72.4s, F1=1.0, 0 postcondition failures; 42 API calls, 17 non-forbidden writes, 0 forbidden). BU's trace is clean: it correctly identified "Add a product" among the three add-a-line variants, used the product autocomplete, typed qty=3, clicked into the Taxes cell, typed `Bench Tax 5%`, and picked from the autocomplete dropdown. No wrong-row trap fired (BU edited only the new row's Taxes, not the existing row's). **To harden into a real medium trap**: (a) seed TWO distractor taxes (e.g., `Bench Tax 10%`, `Bench Tax Zero`) so the agent must pick the exactly-named one from autocomplete; (b) require a NON-DEFAULT unit price (e.g., `price_unit=42.50` that overrides the list_price default) so the agent must also edit the price column; (c) require REMOVING an existing tax pill from the original line AND adding a new pill on the new line, forcing both m2m-add and m2m-remove interactions; (d) use a `tax_group_id` / tax with `include_base_amount=True` so downstream price_subtotal changes, letting the agent fail the computed-total assertion if they set the tax on the wrong row. **Design quirks confirmed**: (1) `purchase.order.line.tax_ids` is the Odoo 19 field (renamed from v17 `taxes_id` — see ODOO19_PATTERNS.md line 40). The view uses `widget="many2many_tax_tags"` with a `domain=[('type_tax_use', '=', 'purchase'), ...]` so only purchase-scope taxes appear in autocomplete. (2) The `many2many_tax_tags` widget (addons/account/static/src/components/many2x_tax_tags/many2x_tax_tags.js) subclasses `Many2ManyTagsField` and uses `Many2XTaxTagsAutocomplete` which always appends "Search More" — the simple autocomplete-and-click path still works for a named tax. (3) The Taxes column is `optional="show"` in the XML (visible by default), so no optional-columns-dropdown toggle is needed before the Taxes cell becomes clickable. (4) Seed MUST clear `taxes_id` AND `supplier_taxes_id` on BOTH product templates — if `supplier_taxes_id` is left as company default, the onchange on product_id auto-applies a default tax to the new line and the agent's added `Bench Tax 5%` either replaces it or stacks with it, breaking the check's "contains Bench Tax 5%" assertion if the default is a different tax and the `compute_price_unit_from_tax` onchange fires again. (5) Entity_key on `purchase.order.line` with match_key `[order_id, product_id]` normalizes to `[null, "Bench Taxable Item"]` on the new line — `order_id` (Many2one) serializes to `null` via XML-RPC (same as row 450), `product_id` serializes to its display name. Subtle: this differs from row 450 where the entity_key is `[null, null]` because the PRE-EXISTING line's product_id normalizes differently than the newly-created line's. Used `[null, "Bench Taxable Item"]` in expected_state.json — verified against the oracle's state_diff.json output. (6) `tax_ids` is deliberately EXCLUDED from `state_spec.fields` (moved to `ignore_fields`) because the tax's numeric DB id is ephemeral across runs — check.py verifies `tax_ids contains Bench Tax 5%` by name lookup. (7) `trace_spec.forbidden_ops` includes `purchase.order.button_confirm` and `purchase.order.line.unlink` so agents who confirm the PO or delete a line are caught, even if the state accidentally lines up. **Commit**: `[ADD] benchmark: purchase.add_product_to_rfq_with_taxes (medium)`. |

---

## mrp.create_bom_kit_type_for_product

| Field | Value |
|---|---|
| **Task ID** | `mrp.create_bom_kit_type_for_product` |
| **Row** | 460 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 39.7s wall clock, 9/9 atomic edits matched, 0 postcondition failures, 44 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 5.6s, gave_up=True, infra — missing `DASHSCOPE_API_KEY` on this worktree so `translate_task_to_english` raised `openai.OpenAIError` before the browser launched. Design intent is a genuine hard-tier FAIL via the Kit radio trap described in Notes). |
| **F1** | 0.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Manufacturing (`mrp`) — `mrp.bom` create with `type='phantom'` and two `bom_line_ids`. Uses the Bills of Materials action (`/odoo/action-mrp.mrp_bom_form_action`). |
| **Workflow** | Seed creates three storable `product.product` records (`Bench Kit Finished`, `Bench Kit Comp A`, `Bench Kit Comp B`) with `type='consu'`, `is_storable=True`, `tracking='none'`. **No** BoM is pre-seeded — the sanity probe asserts all three products start with zero `mrp.bom` rows. Agent: Manufacturing → Products → Bills of Materials → **New** → select Product=`Bench Kit Finished` → click the **Kit** radio on the `BoM Type` field (`widget="radio"` group with three options: *Manufacture this Product* DEFAULT / **Kit** / *Subcontracting*) → Components tab → **Add a line** → product=`Bench Kit Comp A`, qty=`2` → **Add a line** → product=`Bench Kit Comp B`, qty=`3` → Save. End state: exactly one `mrp.bom` with `product_tmpl_id=Bench Kit Finished`, `type='phantom'`, `product_qty=1.0`, 2 `bom_line_ids` ((Comp A, 2.0), (Comp B, 3.0)). |
| **Capability tested** | **Create-from-scratch BoM with a non-default radio selection on a 3-option `widget="radio"` group + o2m inline lines with exact qtys.** The BoM Type default is `Manufacture this Product` (→ `type='normal'`); leaving it produces a regular manufacturing BoM, not a kit. This is distinct from row 377 `mrp.bom_with_kit_component_confirm_mo` (which already seeds the kit BoM and tests MO confirm/explode) and row 433 `mrp.create_bom_with_components` (which sets `code='BOM-REFERENCE'` and 3 lines but leaves type on default). No other task in the suite exercises the kit-radio create path. |
| **Notes** | **Calibration — hard, as designed**. Oracle ran clean on first try (9/9 edits, F1=1.0, 39.7s). BU infra failure (5.6s, gave up in the LLM translate step because `DASHSCOPE_API_KEY` / `OPENAI_API_KEY` were both missing in the worktree env; see `~/.zshrc` absence in the agent's working dir). With a valid key, the task is expected to fail BU on the BoM-Type default: empirical BU weakness on non-default radio groups (rows 16 Backorder, row 7 Calendar recurrence "This Event") reliably leaves the default option selected. **Design quirks confirmed**: (1) `mrp.bom.type` is NOT a selection dropdown but a `widget="radio"` group — set via the UI by clicking the `<label>` inside `div[name='type']`. Do NOT use `set_selection(page, 'type', ...)`; it requires a native `<select>` and would silently no-op. (2) `mrp.bom._compute_display_name` is `f"{code + ': ' if code else ''}{product_tmpl_id.display_name}"` — because we do NOT set `code`, the BoM display_name is just `"Bench Kit Finished"`, which makes `mrp.bom.line.bom_id` normalize to `"Bench Kit Finished"` (the ONLY entity_key component). This differs from row 433 `create_bom_with_components` where `code='BOM-REFERENCE'` produces display_name `"BOM-REFERENCE: Bench Assembled Gadget"`. Using the wrong display_name format in `expected_state.json` drops F1 to 0 via missing-match on bom_line_ids. (3) `product_qty=1.0` is the default on `mrp.bom`, but since the pre-state has no BoM at all, the diff engine emits a `product_qty` create edit — include it in `expected_state.json`. (4) `trace_spec.forbidden_ops` blocks `mrp.bom.unlink`, `mrp.bom.line.unlink`, and any write to `product.template/product.product` (the pre-seeded products must remain untouched) plus `mrp.production.create/action_confirm` (distractor: an agent misreading the task may try to create an MO). `required_ops: []` because the oracle and BU paths both hit `mrp.bom.web_save` — which is a general op, not a unique identifier of success; check.py is the authoritative postcondition. (5) The Components tab is the default active tab on a fresh BoM form, so no explicit `click_tab(page, 'Components')` is needed — `click_add_a_line(page)` works immediately after the type radio click. **Commit**: `[ADD] benchmark: mrp.create_bom_kit_type_for_product (hard)`. |

## hr.create_public_holiday_calendar_entry

| Field | Value |
|---|---|
| **Task ID** | `hr.create_public_holiday_calendar_entry` |
| **Row** | 459 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.3s wall clock, 4/4 atomic edits matched, 0 postcondition failures, 30 API calls, 12 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 120.8s wall clock single-shot, 4/4 atomic edits matched, 0 postcondition failures, 55 API calls, 26 non-forbidden writes, 0 forbidden, StrictClean=True). BU navigated Time Off → Configuration → Public Holidays, clicked New, filled the inline row's Name/Start/End cells, and saved. Final URL was `/odoo/action-704` (numeric alias for `hr_holidays.open_view_public_holiday`). |
| **F1** | 1.0 |
| **Odoo modules** | Time Off (`hr_holidays`) — the Public Holidays menu is at **Time Off → Configuration → Public Holidays** (requires `group_hr_holidays_manager`). Menu id `hr_holidays_public_time_off_menu_configuration` routes to action `hr_holidays.open_view_public_holiday` (addons/hr_holidays/views/hr_holidays_views.xml:116-122, resource_views.xml:83-98). The action is a filtered, editable-bottom `list,form` view over `resource.calendar.leaves` with `domain=[('resource_id','=',False)]` and the inheriting tree view `resource_calendar_leaves_tree_inherit` that adds `editable="bottom"` and column-invisibles `resource_id` + `company_id`. |
| **Workflow** | Seed forces `admin.tz='UTC'` and grants admin the three `hr_holidays.group_hr_holidays_{user,responsible,manager}` groups so the Configuration menu is visible and the list is editable. No record is pre-created; the agent adds one. Agent: open Time Off → Configuration → Public Holidays → click **New** (`button.o_list_button_add`) → a blank inline row appears selected at the bottom → fill `name="Bench Founder Day"` in `td[name='name'] input` → click `button[data-field='date_from']` (daterange-start widget) → type `06/01/2026 00:00:00` into the now-exposed `input[data-field='date_from']` → Tab → type `06/01/2026 23:59:59` into `input[data-field='date_to']` (already exposed after the first Tab) → Tab → click outside the picker (breadcrumb, NOT Escape) → Save the list (`button.o_list_button_save`). End state: one `resource.calendar.leaves` row with `name='Bench Founder Day'`, `resource_id=False`, `calendar_id=False` (placeholder "All Schedules" — keeping the default is the prompt contract), `time_type='leave'`, `date_from`/`date_to` covering the 2026-06-01 calendar day. |
| **Capability tested** | **Settings-area record creation on an editable-bottom inline list with a `daterange` datetime widget**. Three medium-tier traps compound: (1) menu discovery — the action lives under a two-level Configuration submenu inside Time Off, NOT on the main app dashboard; (2) the `daterange` widget renders as buttons initially (`<button data-field="date_{from,to}">`) and only exposes `<input data-field="...">` after the first button is clicked, at which point BOTH start/end inputs are available simultaneously with a floating picker popover; (3) `Escape` on an inline list row **discards** the entire pending row — the correct "close the picker without losing edits" gesture is Tab-out + click a neutral area (breadcrumb), not Escape. |
| **Notes** | **Calibration MISS — BU passed single-shot**. BU solved it at F1=1.0 in 120.8s — the menu breadcrumb Time Off → Configuration → Public Holidays is obvious from labels and the inline list accepts typed datetimes in the `MM/DD/YYYY HH:MM:SS` format without needing the picker. To escalate to tier-3: (a) require `calendar_id` to be pinned to a specific non-default working schedule (forces the m2o autocomplete + dropdown), (b) add a distractor "Bench Founder Day" that already exists with a different date so the agent must spot & replace it instead of creating a duplicate, (c) require a second holiday (multi-row create) — the editable-bottom row loses `o_selected_row` between saves and the agent often conflates the two. **Quirks captured** (new cookbook content): (1) **Escape discards inline rows**. In a `<list editable="bottom">` view, pressing Escape while a new row is selected unmounts the row and loses all edits. Oracles that typed a datetime value + Escape (a common pattern from form-view daterange usage) see the row vanish, end up saving an empty list, and get 0 records. The fix is Tab to advance focus and a neutral-area click (e.g. on `.o_breadcrumb`) to close the popover. (2) **`resource.calendar.leaves.calendar_id` default is empty** in the Public Holidays view (placeholder "All Schedules"), NOT the company's `resource_calendar_id` as the task spec implied. The `_compute_calendar_id` depend is `resource_id.calendar_id`; with `resource_id=False` the compute leaves calendar_id empty, and `_compute_company_id` falls back to `self.env.company`. A company-wide public holiday with `calendar_id=False` is valid and semantically "applies to all schedules". expected_state.json encodes the empty-default path as `calendar_id: null` — if a task tightens the contract to require a specific calendar, the oracle must explicitly pick one from the m2o autocomplete. (3) **Datetime widget tz drift.** Typed strings like `06/01/2026 00:00:00` are interpreted by the Odoo web widget in the browser's local tz (not the admin's Odoo tz), so on a PDT host they store as `2026-06-01 07:00:00 UTC` (= `2026-05-31 midnight` in admin-local UTC). The check accepts any span that covers 2026-06-01 in ANY of a small set of common tzs (UTC / America/Los_Angeles / America/New_York / Europe/Paris / Asia/Shanghai / Asia/Singapore) so the oracle passes regardless of harness tz — same tolerance strategy as `calendar.create_recurring_meeting_weekly_pattern`. (4) **`op: create` not `set` for the new row's state_diff entries.** Because the record didn't exist in before_state, every tracked field (name, resource_id, calendar_id, time_type) diffs as `op=create` even when norm_value is null. expected_state.json must mirror all four create entries exactly or the diff engine emits "Unexpected extra edits" and drops precision. (5) **`state_spec.yaml` must NOT set `optional: true`** on the only tracked model or the diff engine skips it entirely → 0 atomic edits observed → 0/expected recall. The optional flag is for models tracked for check.py purposes only (like `calendar.event` in the recurring-meeting task, which uses check.py alone with `expected_state.json: []`); when you want the diff engine to score your created record, leave optional out. **Commit**: `[ADD] benchmark: hr.create_public_holiday_calendar_entry (medium)`. |

---

## product.set_product_category_change

| Field | Value |
|---|---|
| **Task ID** | `product.set_product_category_change` |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 24.8s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 38 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 80.7s wall clock single-shot, 1/1 atomic edit matched, 0 postcondition failures, 47 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **F1** | 1.0 |
| **Odoo modules** | Inventory / `product` — task operates on `product.template.categ_id` in the standard Products list (action `stock.product_template_action_product`, URL `/odoo/inventory/products` or `/odoo/action-stock.product_template_action_product`). |
| **Workflow** | Seed creates a `consu` product `Bench Cat Item` with `categ_id` pinned to the `All` root category (`product.product_category_all`), and ensures a `product.category` named `Office Supplies` exists at root level. Agent: Inventory → Products → open `Bench Cat Item` → click the **Product Category** m2o field (currently "All") → type `Office Supplies` → pick the single dropdown match → Save. End state: `product.template.categ_id -> Office Supplies`. |
| **Capability tested** | Single many2one field change on a product form save — the canonical easy "form edit + save" anchor on the TASK_CREATION_GUIDE "simple form edits" list. Used as an easy-tier calibration target to cross-check that the harness (state diff + API trace) behaves correctly for a minimal m2o set. |
| **Notes** | **Well-calibrated easy (~80% pass expected — BU single-shot PASS here).** The task is intentionally trivial: one m2o, one autocomplete, one Save. Oracle uses `set_many2one("categ_id", "Office Supplies")` from `oracle_helpers.py` and `save_form(page)`. State_spec tracks only `product.template` by `name`; the single expected edit is `{"field": "categ_id", "op": "set", "norm_value": "Office Supplies"}` — Many2one display-name normalization works out-of-the-box. **Quirks / choices**: (1) Seed pins `categ_id=product.product_category_all` so the "before" value is unambiguously the root **All** category, giving the prompt a clear "from X to Y" contract; a base snapshot default of `categ_id` being the first non-root seed category would still produce a diff but would make the prompt less self-describing. (2) `trace_spec.yaml` forbids `product.category.create` so an agent attempting to create a NEW "Office Supplies" (instead of picking the seeded one) is flagged; the autocomplete on `categ_id` offers a quick-create option when no match exists — because the seed creates the target first, the dropdown has an exact match and the quick-create is not selected. (3) `product.template.unlink` / `product.product.unlink` forbidden to catch "archive/delete instead of recategorize" errors. **Commit**: `[ADD] benchmark: product.set_product_category_change (easy)`. |
---

## sale.cancel_confirmed_order_restore_draft

| Field | Value |
|---|---|
| **Task ID** | `sale.cancel_confirmed_order_restore_draft` |
| **Row** | 462 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 24.3s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 45 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **Browser-Use** | PASS (F1=1.0, 67.9s wall clock single-shot, 1/1 atomic edit matched, 32 API calls, 16 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **F1** | 1.0 |
| **Odoo modules** | Sales — seeds a confirmed `sale.order` (`client_order_ref='BENCH-CANCEL-RESTORE'`, `state='sale'`) for `Bench Cancel Co` with two untaxed consu lines (`Bench Cancel Item A` qty 2 @ 40.00, `Bench Cancel Item B` qty 3 @ 25.00). The statusbar `Cancel` button (`name='action_cancel'` in `addons/sale/views/sale_order_views.xml:357-363`) carries `confirm="Are you sure you want to cancel this order?..."` which fires an Odoo `Dialog` component with a primary Ok button. The `Set to Quotation` button (`name='action_draft'`, lines 364-369) is guarded by `invisible="state != 'cancel'"` and calls `action_draft` (`sale/models/sale_order.py:1050-1057`), which writes `state='draft'` and clears `signature/signed_by/signed_on`. |
| **Workflow** | Open `/odoo/sales/{id}` → click statusbar `Cancel` → confirm the "Are you sure?" modal → state becomes `cancel` and `Set to Quotation` appears → click it → state becomes `draft`. No wizard is launched because the seed SO has no delivered quantities and no invoices (`_action_cancel` only opens the `sale.order.cancel` wizard path when `invoice_ids` with `state=='posted'` exist; vanilla confirmed orders go straight to `action_cancel` → `write({'state':'cancel'})`). |
| **Capability tested** | Two sequential statusbar actions gated by a native confirmation dialog. The design bet was that BU would (a) dismiss the confirm dialog by clicking the wrong button or (b) stop at `state='cancel'` without noticing the newly-rendered `Set to Quotation` button. |
| **Notes** | **Calibration MISS — BU passed single-shot in 67.9s**. The prompt explicitly names both buttons ("Cancel" then "Set to Quotation") and BU followed the script verbatim, including clicking Ok on the confirmation modal. To escalate to tier 3 without redesigning from scratch: (a) seed posted draft `account.move` invoices tied to the SO so `action_cancel` triggers the `sale.order.cancel` wizard (has radio buttons for "Cancel and keep invoices" vs "Cancel and cancel invoices"); (b) combine with a "Customer Reference" edit on the now-draft order before the agent is allowed to leave the form — the mid-workflow field edit traps BU. **Quirks captured**: (1) The Cancel button's `confirm=...` attr triggers an Odoo `Dialog`, NOT a browser `window.confirm()`, so oracles must click a `.modal-footer button.btn-primary` — not handle a JS dialog. (2) `sale.order.action_draft` on a cancelled order fires `sale.order.write` on the tracked fields, so the state_spec only needs `state` in its fields list for the diff engine to record the `cancel→draft` transition; the `signature/signed_by/signed_on` resets must be added to `ignore_fields` or the diff engine reports extras. (3) `client_order_ref` is stable across the cancel/restore cycle (no `copy=False` issue since we're not duplicating), so using it as `match_key` gives a deterministic entity_key `["BENCH-CANCEL-RESTORE"]` that the diff engine reproduces exactly. |

---

## stock.set_putaway_rule_default_location

| Field | Value |
|---|---|
| **Task ID** | `stock.set_putaway_rule_default_location` |
| **Row** | 466 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 34.6s wall clock, 4/4 atomic edits matched, 0 postcondition failures, 37 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 91.7s wall clock single-shot, 4/4 atomic edits matched, 0 postcondition failures, 35 API calls, 15 non-forbidden writes, 0 forbidden, StrictClean=True). BU navigated Inventory → Configuration → Putaway Rules, clicked New, filled location_in_id + product_id + location_out_id inline, and saved. |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (`stock`). Menu path is Inventory → Configuration → Putaway Rules (menu id `stock.menu_putaway`, groups=`stock.group_stock_multi_locations`). Action xmlid `stock.action_putaway_tree` → list view `stock.stock_putaway_list` (`editable="bottom"`). See `addons/stock/views/product_strategy_views.xml:3-117`. |
| **Workflow** | Seed grants admin `stock.group_stock_multi_locations` (menu + Location columns visible) AND `stock.group_adv_location` (paired advanced-routing group). Creates storable product `Bench Putaway Item` (`type='consu' + is_storable=True`) and sub-location `WH/Stock/Shelf B` (`stock.location` with `usage='internal'`, `location_id=WH/Stock`, `name='Shelf B'`). No rule is pre-created. Agent: Inventory → Configuration → Putaway Rules (or `/odoo/action-stock.action_putaway_tree`) → New → inline row appears selected → fill `location_in_id=WH/Stock`, `product_id=Bench Putaway Item`, `location_out_id=WH/Stock/Shelf B` → save list. End state: one `stock.putaway.rule` with matching product_id + location_in_id + location_out_id, `category_id=False`, `sublocation='no'` (default). |
| **Capability tested** | Configuration-submenu navigation + three-m2o inline row creation without leaving a phantom placeholder row. Product vs Product Category column disambiguation (mutually-readonly — filling one greys out the other, which turns out to be BU-friendly). |
| **Notes** | **Calibration MISS — BU passed single-shot** at F1=1.0 in 91.7s, consistent with the prior finding on `stock.create_putaway_rule_for_specific_category` (documented in ODOO19_PATTERNS.md / its COOKBOOK_NOTES). With only three m2o fields to fill in a plainly-labelled editable-bottom list, BU has no trouble. This row was spec'd as medium (tier 2) — matches calibration: medium is the right label and the task primarily serves as a configuration-menu + multi-m2o reference point rather than a hard-tier trap. **Reused patterns**: the (entity_key, expected_state, state_spec) trio is cloned from `stock.create_putaway_rule_for_specific_category` with `product_id` and `category_id` roles swapped — a product-level rule uses entity_key `["Bench Putaway Item", null, "WH/Stock"]` (match_key `[product_id, category_id, location_in_id]` → `[name, null, complete_name]`). `check.py` asserts `category_id` is empty (not swapped) and guards against stray blank placeholder rows. **To push to hard tier** would require (a) adding a Storage Category dropdown that becomes required when `sublocation='closest_location'`, (b) multi-row creation (two rules in one save), or (c) forcing the non-default `sublocation='closest_location'` Selection field — same escalation ladder already noted in the category-rule COOKBOOK notes. **Commit**: `[ADD] benchmark: stock.set_putaway_rule_default_location (medium)`. |
---

## hr.request_reimbursement_expense_report

| Field | Value |
|---|---|
| **Task ID** | `hr.request_reimbursement_expense_report` |
| **Row** | 465 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 42.6s wall clock, 2/2 atomic edits matched — `hr.expense.state='posted'` and `hr.expense.approval_state='approved'` — 0 postcondition failures, 48 API calls, 21 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | PASS (F1=1.0, 74.4s wall clock single-shot, 11 BU steps: login → navigate → click expense row → Submit → Approve → Post Journal Entries → confirm Post Expenses wizard → done. 2/2 atomic edits matched, 0 postcondition failures, 58 API calls, 28 non-forbidden writes, 0 forbidden, StrictClean=True). BU correctly observed each state transition in the statusbar and clicked the wizard's primary button without touching the defaults. |
| **F1** | 1.0 |
| **Odoo modules** | Expenses (`hr_expense`) + Accounting (`account`). Odoo 19 removed `hr.expense.sheet`; the approval pipeline now lives directly on `hr.expense` with `approval_state ∈ {False,'submitted','approved','refused'}` and a computed `state ∈ {'draft','submitted','approved','posted','in_payment','paid','refused'}` that mirrors approval_state plus the account.move state. Form statusbar exposes three sequential buttons: `action_submit` (Submit), `action_approve` (Approve), `action_post` (Post Journal Entries). The last opens a `hr.expense.post.wizard` modal whose primary button `action_post_entry` ("Post Expenses") creates + posts the `account.move` bill that reimburses the employee. |
| **Workflow** | Seed: create a dedicated `bench_expense_manager` user + employee and pin `admin.employee_id.expense_manager_id` to that user so `_can_be_autovalidated` returns False on submit (otherwise admin submitting their own expense jumps straight from Draft to Approved, collapsing the 3-step workflow). Grant admin the 3 hr_expense groups + `account.group_account_invoice` so Submit/Approve/Post Journal Entries are all visible. Create a draft `Bench Travel Expense` (total 150.00, own_account, service product `Bench Travel Service` with `standard_price=0.0` to keep the Total editable for cleanup reruns) on admin's employee. Agent: open /odoo/expenses → click the Bench Travel Expense row → click Submit → click Approve → click Post Journal Entries → in the modal click Post Expenses (accept Journal + Accounting Date defaults). End state: `hr.expense.state='posted'`, `hr.expense.approval_state='approved'`, `hr.expense.account_move_id` populated and posted (BILL/2026/04/0001). |
| **Capability tested** | **Multi-step statusbar lifecycle with a wizard confirmation at the tail.** The task tests four sequential UI interactions with state-dependent button visibility: draft→submit→approve→post_with_modal_confirm. It also tests whether the agent recognises that the modal's two pre-filled fields (Journal, Accounting Date) must be left alone and only the primary button clicked. |
| **Notes** | **Calibration MISS — BU solved single-shot F1=1.0 in 74.4s / 11 steps.** Confirms the row 368 cookbook lesson: sequential multi-click workflows without non-default radio/select widgets or create-from-scratch do not reliably trip BU, even across 3 state transitions + 1 accept-defaults modal. BU correctly observed state transitions in the statusbar between clicks. Kept at tier 3 because the backlog row flagged calibration risk as "hard" and the task preserves a pathway (full draft→posted reimbursement lifecycle) that no other task in the bench exercises end-to-end. To actually escalate for BU difficulty: (a) force a non-default journal pick in the Post Expenses wizard (BU tends to accept defaults), (b) seed duplicate expenses with matching descriptions so Approve triggers the `hr_expense.hr_expense_approve_duplicate_action` wizard (forces a non-default radio choice — "Approve Anyway" vs "Back"), or (c) require the agent to add an attachment (the `nb_attachment >= 1` branch of the form view has different statusbar button classes + positioning — bu often misses the re-rendered layout). **Quirks captured** (new cookbook content): (1) **Admin submitting their own expense auto-validates** unless the employee's `expense_manager_id` points to a different user. `hr.expense._can_be_autovalidated` returns True if `(not manager_id and not employee.expense_manager_id)` OR `manager_id == employee.user_id`. Seeding a dummy `bench_expense_manager` user and assigning it via `admin.employee_id.expense_manager_id = manager_user.id` is the minimal fix — admin still has can_approve=True via `group_hr_expense_manager` (is_hr_admin=True short-circuits the "own expense" check in `_get_cannot_approve_reason`), so all three buttons remain actionable. (2) **Post Journal Entries button visibility**. The statusbar button `action_post` (label "Post Journal Entries") is gated on `state == 'approved'` AND `account.group_account_invoice`. Seed must grant admin that group; the three hr_expense groups alone are not enough. (3) **Post wizard primary button label.** The `hr.expense.post.wizard` footer button is literally `"Post Expenses"` (not "Confirm" or "Post"), with `name='action_post_entry'`. Oracle targets `button[name='action_post_entry']` for selector stability across versions. (4) **State-diff entity_key normalization.** `hr.expense.employee_id` and `product_id` (Many2one) normalize to display names in the diff engine, so `state_spec.yaml` with `match_key=[name]` correctly produces entity_key `["Bench Travel Expense"]` (singular string). The two interesting state transitions — `state: draft→posted` and `approval_state: False→approved` — are both `op=set` (not `op=create`) because the record existed in before_state. (5) **account.move side-effect is NOT in expected_state.** The Post Expenses wizard creates a new `account.move` with `move_type='in_receipt'` (bill) and posts it. state_spec intentionally tracks only `hr.expense`; the account.move creation is validated via `check.py` (`expense.account_move_id` exists and `move.state='posted'`) rather than the diff engine, because the move's name (`BILL/YYYY/MM/####`) is sequence-dependent and brittle as an entity_key across reruns. (6) **hr.expense.sheet removal is load-bearing for prompt design.** The task spec originally mentioned `hr.expense.sheet.state='done'`, but that model no longer exists in Odoo 19 (already recorded in row 368 cookbook). The v19 equivalent of the old `sheet.state='done'` (fully-approved-and-posted expense report) is `hr.expense.state='posted'` — verified by the `_compute_state` method that returns `'posted'` when `account_move_id.state in ('posted', 'draft')` and `payment_state='not_paid'`. Prompt.md explicitly calls this out so the agent doesn't look for a non-existent sheet. **Commit**: `[ADD] benchmark: hr.request_reimbursement_expense_report (hard)`. |
---

## website_blog.schedule_post_future_date_unpublish

| Field | Value |
|---|---|
| **Task ID** | `website_blog.schedule_post_future_date_unpublish` |
| **Row** | 461 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 12.4–15.5s wall clock across two consecutive runs, 2/2 atomic edits matched, 0 postcondition failures, 33–35 API calls, 13–15 non-forbidden writes, 0 forbidden, StrictClean=True). JSON-RPC `blog.post.write` sets `is_published=False`, `website_published=False`, and `published_date` to the admin-local 2026-08-15 12:00:00 UTC equivalent in one call. |
| **Browser-Use** | FAIL (F1=0.0, 262.1s wall clock single-shot, 2/2 state-diff edits matched on publish flags — BU DID toggle the pill OFF — but the trace shows BU wrote `post_date='2026-08-15 04:00:00'` UTC, i.e. typed `12:00` in the datetime widget and the Owl service interpreted it in the harness browser's local tz, storing the wrong UTC instant that renders as `04:00:00` in admin-local (benchmark admin `tz='UTC'`). check.py flags the mismatch; score precision/recall/f1 are force-zeroed by `eval.py:503-506` when postcondition_failures is non-empty. The specific single-shot run captured also had a transient `odoo-bin shell` infra flake (concurrent-worktree `.conf` tmp-file cleanup) that contributed to the "Postcondition check failed to return JSON" entry, but the design trap is real — BU consistently loses the tz conversion on datetime widgets in this harness. |
| **F1** | 0.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Website Blog (`website_blog`) — `blog.post` with `website.published.mixin`. Backend form route `/odoo/action-website_blog.action_blog_post/<id>` or list at `/odoo/blog-post-pages`. |
| **Workflow** | Seed creates blog `Bench News` (shared, idempotent) and a single *live* post `Bench Future Post` with `is_published=True`, `website_published=True`, `published_date=utcnow()`, author=admin, short HTML body. Agent: Website → Site → Blog Posts → open `Bench Future Post` → click the **Published** pill in the form header to flip it OFF (unpublish) → in Publishing Options, change **Publishing date** (`post_date`) to `08/15/2026 12:00:00` via the datetime widget → Save. End state: `is_published=False`, `website_published=False`, `post_date/published_date == datetime(2026, 8, 15, 12, 0, 0)` in admin-local TZ; title, blog, author, content unchanged; exactly one post named `Bench Future Post`. |
| **Capability tested** | **Two-surface hard combo on a single save**: (a) the `website_publish_button` pill toggle (Bootstrap pill; BU typically handles it but can confuse "Published" vs "Unpublish" prompts), and (b) the Owl datetime widget on `post_date` (button-vs-input swap + tz interpretation — the proven-hard anchor from `create_post_with_cta_seo_schedule`). Either surface can be silently no-op'd. The task is the only one in the suite exercising a True→False transition on `is_published`/`website_published` of a **pre-existing** record simultaneously with a `post_date` future reschedule — distinct from row 430 (pure author swap, keeps published) and row 358 (fresh-create scheduled post, never published). |
| **Notes** | **Calibration — hard, as designed**. Oracle deterministically passes via JSON-RPC write; BU single-shot FAILS with the datetime-widget tz-drift trap (typed 12:00 → stored 04:00 UTC on PDT host). **Design quirks captured** (new cookbook content): (1) **null-vs-false extends to `op: "set"`**. Previously documented for `op: "create"` (archive / fresh-schedule), the same False→`null` normalization applies when flipping True→False on a pre-existing record via `set`. `expected_state.json` for `is_published`/`website_published` MUST use `"norm_value": null` (NOT `false`); encoding `false` emits a mirror-image missing+extra edit pair and drops F1 to 0. This is the first task to prove the quirk is a property of the value normalizer, not the create-vs-set code path. (2) **Pill toggle OFF flips BOTH flags via mixin inverse**. Clicking the `website_publish_button` pill OFF fires `website.published.mixin._inverse_is_published` which writes `website_published = is_published = False` in the same ORM write, producing TWO `op: "set"` entries in the state diff from a single user gesture. (3) **Datetime widget typed-value tz is browser-local, not admin-local**. The Owl `DateTimeField` parses `<input>` values using the browser's Intl locale, which on the Playwright launch default is the harness host's tz. Writing to admin-tz='UTC' then appears offset by the harness tz. For an oracle that ALSO needs the browser path, call `page.evaluate` to resolve admin `tz` via JSON-RPC and pre-convert the typed string to the compensating local wallclock. The JSON-RPC shortcut (used here) sidesteps the whole issue by writing the UTC Datetime directly on `published_date`. (4) **Oracle uses JSON-RPC despite a pure-UI prompt.** Pattern from `mass_mailing.create_mailing_select_list_schedule_send` — when the UI has two independently-fragile widgets (pill + datetime), the oracle asserts *reachability* by navigating to `/odoo/blog-post-pages` and then commits end-state via `call_kw`. `trace_spec.forbidden_ops` blocks `blog.post.action_archive` (archive also auto-flips publish flags via the mixin — an agent could satisfy F1 by archiving instead of unpublishing, which violates the prompt). (5) **`published_date` is the storage field**; `post_date` is the inverse-compute alias. Seeds set `published_date` directly; check.py reads `post.published_date or post.post_date` for tolerance. **Commit**: `[ADD] benchmark: website_blog.schedule_post_future_date_unpublish (hard)`. |
---

## calendar.create_meeting_invite_attendees_send

| Field | Value |
|---|---|
| **Task ID** | `calendar.create_meeting_invite_attendees_send` |
| **Row** | 464 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 28.5s wall clock, 2/2 atomic edits matched, 0 postcondition failures, 61 API calls, 34 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 360.0s wall clock, single-shot, gave_up=True, 2 postcondition failures: `Expected exactly 1 event named 'Team Sync', found 2` and `Event local start date is 2026-04-19, expected 2026-05-20`. Agent created two Team Sync events via `calendar.event.web_save x2` — first at today's date from a kanban date-cell click, second attempt also drifted from the 2026-05-20 target). |
| **F1** | 0.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Calendar — `calendar.event` create with `partner_ids` many2many (two seeded `res.partner` rows). Start URL: `/odoo/calendar`. |
| **Workflow** | Seed wipes any prior `Team Sync` events + invitation.ics attachments and ensures two `res.partner` rows exist: `Attendee Alpha` (alpha@bench.test) and `Attendee Beta` (beta@bench.test). Agent: Calendar → New → name=`Team Sync`, start=`2026-05-20 10:00`, stop=`2026-05-20 11:00` (1h), add `Attendee Alpha` + `Attendee Beta` via the Attendees (`partner_ids`) many2many_tags autocomplete → save. End state: exactly 1 non-recurring non-all-day `calendar.event` named `Team Sync` on 2026-05-20 10:00-11:00 local (admin tz), with both seeded partners linked via `partner_ids` AND `attendee_ids`. |
| **Capability tested** | **Calendar new-event create targeting a SPECIFIC future date (not today) + dual many2many_tags picks.** Distinct from row 413 recurring (no recurrence), row 376 location+reminder (no location/alarm), row 337 agenda+attachment (no file upload). The specific trap: Odoo Calendar's default "New" click from the calendar kanban creates an event at the currently-viewed date/time, so agents that click a date cell and type the title end up with the wrong `start`. Correct path is click the toolbar **New** button, fill the `start` `daterange` input explicitly, and let `duration` compute `stop = start + 1h`. |
| **Notes** | **Calibration CORRECT (medium)**: BU FAIL single-shot, F1=0.0. BU created 2 Team Sync events both at the wrong date (today 2026-04-19 instead of 2026-05-20), failing both "exactly 1 event" and "correct date" postconditions. This matches the reference calendar.create task trap — agents clicking a date cell or typing into the calendar grid get today's date, and the kanban-style "Add Event" popover does NOT surface the full datetime picker. Oracle uses the canonical cookbook pattern: explicit `.o_field_widget[name="start"] input` type + `.o_field_widget[name="duration"] input` set to `01:00` to deterministically produce `stop = start + 1h`. New cookbook data point: BU single-shot emitted 0 "📍 Step" markers in stdout (empty agent_stdout.txt) despite making 2 calendar.event.web_save calls — the event creation happened but step tracking didn't surface, likely because BU timed out at the 360s wall clock limit during an autocomplete retry loop. Task is a clean BU-fail medium: legitimate capability test of datetime-to-specific-target, solvable via oracle in <30s, not pointlessly hard. **Commit**: `[ADD] benchmark: calendar.create_meeting_invite_attendees_send (medium)`. |
---

## crm.bulk_archive_lost_leads

| Field | Value |
|---|---|
| **Task ID** | `crm.bulk_archive_lost_leads` |
| **Row** | 470 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 30.8s wall clock, 3/3 atomic edits matched, 0 postcondition failures, 32 API calls, 12 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle path: navigate `/odoo/action-crm.crm_lead_all_leads` → `ensure_list_view` → `clear_search_filters` → type `Bench Lost` in `.o_searchview_input` + Enter → tick `.o_list_record_selector input[type='checkbox']` on the 3 matching rows → open `.o_cp_action_menus` dropdown → click `.dropdown-item:has-text('Archive')`. No confirm modal appears for bulk-archive in Odoo 19 (single-form archive prompts, list bulk does not). |
| **Browser-Use** | PASS (F1=1.0, 80.0s wall clock single-shot, 3/3 atomic edits matched, 0 postcondition failures, 27 API calls, 10 non-forbidden writes, 0 forbidden, StrictClean=True). BU solved it in under 90s — the list-view multi-select + cog Actions → Archive pattern is straightforward for BU when the prompt spells out the targets and the distractor by name. |
| **F1** | 1.0 (both) |
| **Odoo modules** | CRM — `crm.lead` list (action `crm.crm_lead_all_leads`, view `crm.crm_case_tree_view_leads` via search view `crm.view_crm_case_leads_filter`). Archive action is the generic `action_archive` / `toggle_active` on `crm.lead`. Requires `crm.group_use_lead` so the "Leads" top menu is visible. |
| **Workflow** | Seed: enable `crm.group_use_lead` on admin; create `crm.lost.reason` "Deferred to next fiscal year"; create 3 leads `Bench Lost 1/2/3` with `type='lead'`, `active=True`, `probability=0`, `lost_reason_id=<reason>`, distinct `contact_name` + `email_from`; create 1 distractor `Bench Keep 4` with `probability=30` and no lost reason. Agent: CRM → Leads (list view), clear default filters, search `Bench Lost`, tick the 3 target row checkboxes (skip `Bench Keep 4`), open cog Actions menu → **Archive**. End state: `Bench Lost 1/2/3` all have `active=False`; `Bench Keep 4` stays `active=True`; no lead is deleted. |
| **Capability tested** | **List-view multi-select + cog Actions → Archive bulk action.** Distinct from row 50 `crm.batch_mark_lost_with_reason` (multi-select → Mark Lost wizard, does not archive — `action_set_lost` on active leads archives them, but that task goes through the wizard with reason+note), row 319 merge (multi-select → Merge wizard), and row 457 `stock.archive_old_product_set_inactive` (single-record cog Archive on a product form). This row is the **list-view bulk Archive** path in isolation with a negative-guard distractor. |
| **Notes** | **Calibration notes** — task was specced as medium, but BU passed single-shot in 80s. The pattern "filter list → tick 3 checkboxes → cog Actions → Archive" with named targets and a named distractor is well within current BU capability when the filter criterion is a searchable substring. F1=1.0 on both tracks. **Design quirks captured**: (1) **Odoo 19 "Lost" list filter is strict**: both `crm.crm_case_tree_view_leads` and `crm.view_crm_case_leads_filter` declare `filter_won_status_lost` / `lost` with domain `[('won_status','=','lost'),('active','=',False)]`. Because `won_status` compute (`crm/models/crm_lead.py:613-620`) requires `active=False` AND `probability=0` to become `'lost'`, an "active lost lead" (probability=0 with lost_reason_id but still active) surfaces as `won_status='pending'` and is NOT matched by the built-in Lost filter. The prompt therefore asks the agent to search by the shared name prefix `Bench Lost` instead of toggling the Lost filter — this avoids the doability trap. (2) **`action_set_lost` auto-archives**: calling `crm.lead.action_set_lost()` sets `probability=0` AND calls `action_archive()` in one go (`crm_lead.py:1121-1125`). Seeding "lost but not yet archived" requires writing `probability=0` + `lost_reason_id` directly and leaving `active=True`. (3) **No confirmation modal on bulk list Archive** in Odoo 19 — the oracle's `_confirm_modal_if_present` check is a no-op guard but kept for robustness. (4) **`state_spec.yaml` ignores `probability` / `lost_reason_id`** because those fields are stable pre-vs-post (set during seed, not touched by the agent) — only `active` changes, keeping the state-diff minimal and the F1 scoring clean. **Commit**: `[ADD] benchmark: crm.bulk_archive_lost_leads (medium)`. |

---

## account.create_vendor_bill_from_scratch_pay

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 46.0s wall clock, 18/18 atomic edits matched, 0 postcondition failures, 59 API calls, 28 non-forbidden writes, 0 forbidden, StrictClean=True) |
| **Browser-Use** | FAIL (F1=0.0, 127.2s wall clock, single-shot, outcome_success=False, success=True self-report BUT 1 postcondition failure: `Expected exactly 1 product line on the bill, found 0`. BU filled Vendor + Ref + Date + typed "Bench Bill Item" into the product autocomplete + set qty=2 + price=75, clicked Save manually, then Confirm, then Pay, then Create Payment — and the bill+payment flow completed end-to-end with `payment_state='paid'` and amount_total=150.00, BUT the product_id on the invoice line was never committed from the autocomplete dropdown, so check.py's `l.product_id` filter returned 0 product lines.) |
| **F1** | 0.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Accounting (account) — `account.move` with `move_type='in_invoice'` + `account.payment.register` wizard + `account.payment`. Start URL: `/odoo/accounting`. |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Workflow** | Seed only the vendor `Bench Bill Vendor` (supplier_rank=1) and a consumable product `Bench Bill Item` (standard_price=75.0, taxes cleared). Agent: Accounting → Vendors → Bills → **New** → fill Vendor=Bench Bill Vendor, Bill Date=05/10/2026, Bill Reference=`BENCH-VBILL-001`, enable the Product optional column, add one line `Bench Bill Item` qty=2 price=75 → Confirm (post) → Pay in header → accept all wizard defaults → click **Create Payment**. End state: account.move (move_type='in_invoice', state='posted', payment_state='paid') + single linked account.payment (amount=150, payment_type='outbound', state='in_process'). |
| **Capability tested** | **Three sequential gates in one hard task**: (1) create-from-scratch with EXACT single product line — the canonical phantom-empty-line failure mode plus the product-autocomplete-commit failure mode; (2) post the bill via statusbar Confirm; (3) open the Register Payment wizard via statusbar Pay and click the primary `action_create_payments` button (not Discard). Distinct from row 435 (partial payment with 4-field wizard overrides) and row 446 (post draft + send email) — this one is fully accept-defaults on the wizard, so the bottleneck is the three-gate sequence plus the product-autocomplete trap. |
| **Notes** | **Calibration CORRECT (hard)**: BU FAIL single-shot at 127s well under the 480s limit. BU hit a subtle failure mode that the oracle doesn't: it typed the product name into the autocomplete but never clicked a dropdown option, so the line got `name='Bench Bill Item'` but `product_id=False`. The bill totals still computed (price_unit+quantity set directly), the Confirm passed, the Pay wizard worked, and the state-diff matches all 18 expected edits perfectly — so the observable accounting state looks identical. But the prompt's "add a line Bench Bill Item" implicitly requires the product relation, which check.py's `l.product_id` filter enforces (consistent with row 440 `account.create_vendor_bill_confirm`'s check). All 18 atomic state edits matched (F1 on state-diff alone would be 1.0), but Strict mode zeros the score on postcondition failure. Key takeaway for future tier-3 accept-defaults tasks: chaining 3 statusbar+wizard gates is NOT sufficient difficulty by itself (BU handles Confirm+Pay+Create-Payment cleanly); the create-from-scratch step carries the actual difficulty via the autocomplete-commit + Product-column-hidden-by-default + phantom-line traps. Consider this calibrated correctly as hard because BU genuinely fails AND the failure is on a realistic product-id-commit mistake that a human reviewer would also catch. New cookbook data: the `account.move` state-diff for a full-payment flow needs 7 rows for the bill (partner/ref/state/move_type/payment_state/invoice_date/amount_total) + 6 rows for the `#dup1` backing payment move (partner/ref/state/move_type='entry'/payment_state='not_paid'/invoice_date=null/amount_total=150.0) + 4 rows for `account.payment` (partner/amount/state='in_process'/payment_type='outbound') — 18 total, with `#dup1` needed because the backing move's ref equals the bill's ref (the wizard's default memo is the bill ref). **Commit**: `[ADD] benchmark: account.create_vendor_bill_from_scratch_pay (hard)`. |

---

## product.configure_stock_route_for_product

| Field | Value |
|---|---|
| **Task ID** | `product.configure_stock_route_for_product` |
| **Row** | 472 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 34.0s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 44 API calls, 16 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle flow: open Inventory > Products, search `Bench MTO Item`, click the row, switch to the `Inventory` notebook tab, locate the Routes `many2many_checkboxes` widget in the Operations group, tick `Replenish on Order (MTO)`, save. |
| **Browser-Use** | PASS (F1=1.0, 71.9s single-shot, 1/1 atomic edits matched, 30 API calls, 14 non-forbidden writes, 0 forbidden, StrictClean=True). BU solved it cleanly in ~2x oracle time. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Product, Stock — `product.template.route_ids` many2many to `stock.route`. Start URL: `/odoo/inventory/products`. |
| **Workflow** | Seed activates `stock.route_warehouse0_mto` (ships `active=False` in fresh DBs), ensures `product_selectable=True` on that route, grants admin `stock.group_adv_location` + `stock.group_stock_multi_locations`, then creates a storable product `Bench MTO Item` (`type='consu'`, `is_storable=True`, default_code `BENCH-MTO-01`) with `route_ids=[]`. Agent: Inventory app > Products > Products > open `Bench MTO Item` > click the **Inventory** notebook tab > find the Routes checkbox group inside the `Operations` group > tick `Replenish on Order (MTO)` (and only that) > Save. End state: `product.template.route_ids == [stock.route_warehouse0_mto]`, no other route enabled, product identity fields (name/type/is_storable) unchanged. |
| **Capability tested** | **Notebook-tab navigation + `many2many_checkboxes` widget with a specific checkbox pick.** Distinct from row 417 (attribute-line add), row 454 (orderpoint smart-button), row 466 (putaway list config). The Routes group is hidden until the agent switches off the default General Information tab to Inventory, and only the single named checkbox among several (Buy, Manufacture, etc. depending on installed modules) satisfies the assertion. |
| **Notes** | **Calibration: BELOW medium target** — BU PASS single-shot, F1=1.0. This matches the earlier `stock.set_putaway_rule_default_location` calibration where a well-labelled tab + single-field pick on a product form is solvable by BU. Kept as documented medium per the spec (tier-2, non-primary-distinguishing). **Seed quirks captured**: (1) `stock.route_warehouse0_mto` ships with `active=False` — seed MUST flip to active before `has_available_route_ids` compute returns True and the Operations group renders. (2) `product_selectable` default=True on stock.route so activation alone is sufficient; no extra route plumbing needed. (3) The Routes checkbox widget is on the **Inventory** tab (not Purchase — the Purchase tab page is marked `invisible="1"` in Odoo 19). (4) `expected_state.json` uses `"op": "set"` + `"norm_value": [1]` — the diff engine tracks m2m cardinality not ids, so `[1]` is the canonical "has one route" normalization. **Commit**: `[ADD] benchmark: product.configure_stock_route_for_product (medium)`. |
---

## stock.transfer_create_internal_transfer_validate

| Field | Value |
|---|---|
| **Task ID** | `stock.transfer_create_internal_transfer_validate` |
| **Row** | 469 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 43.2s wall clock, 3/3 atomic edits matched on the new `stock.picking` — `op: create` on `location_id`, `location_dest_id`, `state` → 'done' — 0 postcondition failures, 52 API calls, 24 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **Browser-Use** | PASS (F1=1.0, 296.3s wall clock single-shot, 3/3 atomic edits matched, 0 postcondition failures, 129 API calls, 59 non-forbidden writes, 0 forbidden, StrictClean=True). BU final message: "Successfully created and validated the internal transfer WH/INT/00001. 5 units of 'Bench Move Item' were moved from WH/Stock to WH/Stock/Shelf C. The transfer is now in the 'Done' state." |
| **F1** | 1.0 |
| **Odoo modules** | Inventory (`stock`) — `stock.picking` create with `picking_type_id.code='internal'`. Start URL: `/odoo/inventory`. Navigation target: `/odoo/inventory/internal` (action `stock.action_picking_tree_internal`, context `restricted_picking_type_code='internal'` so clicking New pre-seeds an internal draft picking). `stock.picking_type._compute_display_name` formats internal picking types as `"<warehouse.name>: Internal Transfers"` (`addons/stock/models/stock_picking.py:282-286`). |
| **Workflow** | Seed grants admin `stock.group_stock_multi_locations` (unlocks Source/Destination columns + Internal Transfers operation type on the picking form), ensures `WH.int_type_id.active=True`, creates the storable product `Bench Move Item` (`type='consu'` + `is_storable=True`), seeds 10 on-hand at WH/Stock via `stock.quant._update_available_quantity`, and creates sub-location `WH/Stock/Shelf C` (`usage='internal'`, `location_id=WH/Stock`). Agent: Inventory → Transfers → navigate Internal Transfers (or click the Internal Transfers kanban tile) → New → picking_type defaults to Internal; override **Destination Location**=`WH/Stock/Shelf C` (source auto-fills to WH/Stock) → Operations tab: add one move line `Bench Move Item` Demand=5 → Mark as Todo (`action_confirm` — reserves the 5 units from WH/Stock, auto-fills Quantity=5 on the single move_line) → Validate. Because Quantity==Demand==5, NO Create Backorder dialog appears; the picking goes straight to `state='done'`, landing a 5-unit quant at WH/Stock/Shelf C and reducing the WH/Stock quant from 10 to 5. |
| **Capability tested** | **Create-from-scratch `stock.picking` with a sub-location destination + Mark as Todo + Validate.** Distinct from (a) row 447 `stock.receipt_full_quantity_validate_no_backorder` (pre-seeded incoming receipt, agent only clicks Validate); (b) row 436 `stock.delivery_transfer_validate_partial_backorder_no` (pre-seeded outgoing delivery, agent edits Done cell + handles backorder dialog); (c) legacy `stock.internal_transfer_between_locations` (pre-seeded internal transfer, agent only fills qty + validates). This is the only internal-transfer task that exercises the *create* path end-to-end, including the Operation Type m2o + editable move_ids list + two-stage confirm (Mark as Todo → Validate). |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 296.3s. BU successfully navigated New → picked the Internal Transfers operation type (in fact it came pre-selected from the `/odoo/inventory/internal` action context, so BU effectively only had to set the destination + one line), changed the destination to Shelf C, added the Bench Move Item line with Demand 5, clicked Mark as Todo, and Validated — producing `WH/INT/00001` in state `done`. Calibration for this row was called **medium**; empirically it behaves closer to easy-medium because the context-bound "New" pre-fills picking_type_id so the agent never has to disambiguate Receipts vs Delivery Orders vs Internal. **To push to hard tier** would require either (a) forcing navigation via the generic `/odoo/inventory/transfers` list where picking_type_id is NOT pre-bound (agent must pick Internal Transfers from a dropdown of 3+ types) or (b) adding a second product line + partial-qty edit to trigger a Create Backorder dialog trap. **Cookbook data points** (new / reinforced): (1) **`/odoo/inventory/internal` action context pre-selects picking_type_id on New.** The action xmlid `stock.action_picking_tree_internal` (`addons/stock/views/stock_picking_views.xml:441-449`) sets `restricted_picking_type_code='internal'` in context, which Odoo's picking_type `_search_display_name` + form default_get use to pre-populate `picking_type_id` to the warehouse's `int_type_id`. This is why the agent never has to pick the operation type manually when navigating via the Internal Transfers tile. (2) **Picking-type display_name is warehouse-qualified.** `picking_type.display_name = f"{picking_type.warehouse_id.name}: {picking_type.name}"` (`stock/models/stock_picking.py:285`). Using `picking_type_id` as a state_spec `match_key` produces entity keys like `"YourCompany: Internal Transfers"` which are **not stable across base-DB variations** — DROP `picking_type_id` from match_key (kept in ignore_fields here) and use `(location_id, location_dest_id)` as the match instead. The pair is unique enough because `Shelf C` is a brand-new sub-location seeded for this task, so no pre-existing picking targets it. (3) **Seed pattern for stock on-hand.** `stock.quant._update_available_quantity(product, stock_loc, qty)` is the idiomatic call for seeding on-hand at an internal location (ODOO19_PATTERNS.md §Storable product on-hand). Setting the destination sub-location is via a vanilla `stock.location.create({'usage': 'internal', 'location_id': parent_stock.id, 'name': 'Shelf C'})`. (4) **Expected-state entity_keys for create-from-scratch pickings.** Since a fresh picking has a sequence-generated name (e.g., `WH/INT/00001`) that is NOT deterministic across reruns (could be `00001` or `00002` depending on prior-run sequence state), do NOT use `name` in match_key. Use the pair (source, destination) — both resolve to `complete_name` via the normalizer, both are seed-determined, both are stable. All three `op: create` entries in `expected_state.json` share the same entity_key `["WH/Stock", "WH/Stock/Shelf C"]`. (5) **Reservation auto-fills Quantity on Mark as Todo.** `action_confirm()` triggers reservation for an internal picking because `int_type_id.reservation_method` defaults to `at_confirm` (unlike some outgoing types). The single move_line gets `quantity=5` auto-filled, so clicking Validate with no cell edits goes straight to `done` — no backorder dialog at full demand. **Commit**: `[ADD] benchmark: stock.transfer_create_internal_transfer_validate (medium)`. |

---

## hr.promote_employee_set_new_job_title_save

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 25.8s wall clock, 1/1 atomic edit matched — `op: set` on `hr.employee.job_title` to 'Senior Analyst', 0 postcondition failures, 37 API calls, 16 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **Browser-Use** | PASS (F1=1.0, 89.8s wall clock single-shot, 1/1 atomic edit matched, 0 postcondition failures, 93 API calls, 43 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **F1** | 1.0 |
| **Odoo modules** | HR (`hr`) — `hr.employee.job_title` (Char field). Start URL: `/odoo/employees`. |
| **Workflow** | Seed `hr.employee` `Bench Promote Me` with `job_title='Analyst'` and `work_email='bench.promote@example.com'` (no `job_id`). Agent: Employees → open `Bench Promote Me` → on the default Work tab, replace the Job Title char field value `Analyst` → `Senior Analyst` → Save. |
| **Capability tested** | **Single char-field edit (easy anchor).** Targets `hr.employee.job_title` — the free-text Char field directly below the Job Position many2one in the Work tab of the employee form (`addons/hr/views/hr_employee_views.xml:161`). Distinct from row 341 `hr.add_employee_skill` / row 425 `hr.generate_employee_card_set_badge_id` / row 438 `hr.update_employee_department` and from the misleadingly-named `hr.update_employee_job_title` which actually edits the `job_id` many2one. |
| **Notes** | **Calibration on target** — easy anchor, BU passed single-shot F1=1.0 as expected (~80 0.000000e+00asy pass rate). Key Odoo 19 subtlety documented in the cookbook: `hr.employee` has BOTH `job_id` (m2o, label "Job Position") AND `job_title` (Char, label "Job Title"), stacked one above the other in the Work tab. The prompt explicitly disambiguates "the free-text char field directly below Job Position" so the agent cannot confuse the two. Check guards against spurious `job_id` writes. **Commit**: `[ADD] benchmark: hr.promote_employee_set_new_job_title_save (easy)`. |
---

## website_forum.upvote_question_mark_as_answer

| | |
|---|---|
| **Row** | 477 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 15.5s, 6/6 edits) |
| **Browser-Use** | PASS (F1=1.0, 55.8s single-shot, 9 steps, 0 postcondition failures) |
| **F1** | 1.0 |
| **Odoo modules** | `website_forum` (installed on demand; not in base snapshot) |
| **Workflow** | Seed installs `website_forum`, creates a public forum `Bench Forum` (mode=`questions`, one-answer-per-question), a portal user `benchbot` with karma 5000, a seeded question `How do I install?` by benchbot (parent_id=False, is_correct=False, zero votes), and ONE seeded answer by benchbot (parent=question, is_correct=False). Agent opens `/forum` → Bench Forum → opens the question → clicks the caret-up Upvote arrow on the question (`button.vote_up[aria-label='Upvote']`) → clicks the circle-check Accept icon (`.o_wforum_validate_toggler`) on the seeded answer. |
| **Capability tested** | Frontend forum vote + accept interactions distinct from row 394 (which posts a NEW answer then accepts among TWO candidates). This row exercises the `/forum/<forum>/post/<post>/upvote` JSON-RPC controller (which creates a `forum.post.vote` row with `vote='1'`, `user_id=admin.id`, `recipient_id=benchbot.id`) + the `/toggle_correct` controller on an existing single answer. No textarea posting, no candidate disambiguation. |
| **Notes** | **Calibration MISS — BU PASSED single-shot** (F1=1.0, 9 steps, 55.8s). BU found both targets via aria-label: `aria-label='Upvote'` on the caret-up button and `aria-label='Mark as Best Answer'` on the circle-check toggler. Unlike row 394 (where the Accept icon has NO aria-label and the agent loop-detected hunting through selectors), the presence of explicit aria-labels here + only ONE answer (no canonical-vs-decoy disambiguation) + no required textarea posting collapses the task to two discoverable clicks. To escalate to hard: (a) add 2-3 distractor answers (mode='discussions') so BU must pick the right one to Accept, (b) require downvoting a decoy AND upvoting the question (two polarity-distinct vote actions), (c) force a karma grant step before the votes can register. Kept as medium/tier:2 per backlog spec (calibration risk was MEDIUM; BU PASS is compatible with medium difficulty, just on the easy edge). New cookbook entries appended to `ODOO19_PATTERNS.md § website_forum`: (1) **Upvote button IS aria-label-discoverable** (`button.vote_up[aria-label='Upvote']`, template `website_forum.post_vote`), unlike the Accept toggler which only has title+data-href; this is the mechanistic reason row 477 is easier than row 394. (2) **`/forum/.../upvote` controller self-vote guard** mirrors `/toggle_correct` — `if request.env.uid == post.create_uid.id: return {'error': 'own_post'}`; admin bypasses karma via `is_admin()` but NOT the self-vote guard, so both question and answer must be authored by a non-admin seeded user (benchbot). (3) **`forum.post.vote` state-diff match_key** is `(post_id, user_id, vote)` which normalizes to `(question_title, user_name, selection_string)` — `vote` field is Selection `'1'|'-1'|'0'`, not int. (4) **`forum.post.vote.recipient_id`** is `related="post_id.create_uid"` stored, so it fills automatically at create time — include it in state_spec.fields to capture as a `create` edit with the post author's display name. (5) **`mode='questions'` one-answer cap** enforced at template render (Your Answer block hidden once an answer exists) — use for single-answer tasks; `mode='discussions'` for multi-answer tasks (row 394). **Commit**: `[ADD] benchmark: website_forum.upvote_question_mark_as_answer (medium)`. |
---

## mrp.unreserve_raw_material_on_mo

| Field | Value |
|---|---|
| **Task ID** | `mrp.unreserve_raw_material_on_mo` |
| **Row** | 475 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 18.9s wall clock, 3/3 atomic edits matched, 0 postcondition failures, 33 API calls, 14 non-forbidden writes, 0 forbidden, StrictClean=True). Oracle navigates `/odoo/manufacturing`, clears default filters, opens the list row `MO-BENCH-UNRES`, and clicks the statusbar button with `name='do_unreserve'`. |
| **Browser-Use** | PASS (F1=1.0, 97.3s wall clock single-shot, 3/3 atomic edits matched, 0 postcondition failures, 74 API calls, 36 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **F1** | 1.0 |
| **Odoo modules** | Manufacturing (`mrp`) + Inventory (`stock`) — `mrp.production.do_unreserve` → `stock.move._do_unreserve` cascade on both `move_raw_ids` and `move_finished_ids`. |
| **Workflow** | Seed: `Bench Unres Product` (consu + is_storable, tracking=none), component `Bench Unres Mat` (consu + is_storable, tracking=none) with 10 on-hand at WH/Stock; normal BoM (1 component per finished unit, flexible consumption); confirmed+assigned MO `MO-BENCH-UNRES` for 5 finished units (`action_confirm()` + `action_assign()` — raw move state = 'assigned', `quant.reserved_quantity = 5.0`). Agent: Manufacturing → Operations → Manufacturing Orders → clear default filters → open `MO-BENCH-UNRES` → click the statusbar **Unreserve** button (view declares `<button name="do_unreserve" type="object" string="Unreserve" invisible="not unreserve_visible" data-hotkey="w"/>`). `do_unreserve()` cascades to `(move_finished_ids \| move_raw_ids).filtered(state not in ('done','cancel'))._do_unreserve()` which unlinks `move_line_ids` and `_recompute_state()` flips both moves from 'assigned' → 'confirmed'. End state: MO state stays 'confirmed'; `reservation_state` flips from 'assigned' to 'confirmed'; raw move.state='confirmed' (released); finished move.state='confirmed' (released); `quant.reserved_quantity` at WH/Stock drops 5.0→0.0; on-hand stays 10.0. |
| **Capability tested** | Single-click statusbar action recognition on a confirmed-not-in-progress MO: the agent must identify **Unreserve** among a crowded header (Produce All / Check availability / Plan / Unplan / Start / Cancel / Unbuild / status statusbar) and NOT conflate it with **Cancel** (MO-level cancel) or **Check availability** (re-reserves the move). Complements row 449 `mrp.confirm_mo_produce_partial_keep_backorder` (partial-produce + backorder wizard) and row 415 (scrap) — this is the only MRP task that exercises the `do_unreserve` server method. |
| **Notes** | **Calibration: MEDIUM baseline, BU passed single-shot** (97.3s). The button has a distinct label and the prompt names it explicitly, so BU completed without issue. `do_unreserve` is a type='object' button (direct method call, no wizard / no modal), which is easier than the Produce-backorder wizard trap. **Design quirks captured**: (1) **`do_unreserve` cascades to BOTH move_raw_ids AND move_finished_ids** (see `addons/mrp/models/mrp_production.py:2376-2377`). Both moves change state 'assigned' → 'confirmed', so `expected_state.json` MUST list two stock.move set-edits, not one. First oracle run missed the finished-move edit → Precision=0.667. (2) **`stock.move` `read_state` only reads fields declared in `fields:`, NOT match_key fields**. To get stable entity_keys via `raw_material_production_id` + `product_id`, those fields must be duplicated in both `match_key` AND `fields` of state_spec. Verified empirically: omitting them from `fields` causes every stock.move to land at `entity_key=[null, null]` and the diff engine appends `#dupN` suffixes (2 stock.moves → `[null, null]` + `[null, null, "#dup1"]`). (3) **`raw_material_production_id` is False on the finished move**, so the finished move's entity_key normalizes to `[null, "Bench Unres Product"]` while the raw move's is `["MO-BENCH-UNRES", "Bench Unres Mat"]` — both are distinct. (4) **`unreserve_visible` gate**: `_compute_unreserve_visible` requires `state not in ('done','cancel') AND move_raw_ids.move_line_ids AND not any(move.picked)`. A fresh-confirmed MO with `action_assign()` ticks all three; an MO that was confirmed but NEVER assigned shows the **Check availability** button instead (reserve_visible=True) — the seed must call `action_assign()` explicitly after `action_confirm()` or the Unreserve button is invisible. (5) **`action_confirm()` alone does NOT reserve** because `picking_type_id.reservation_method` on manufacturing is typically 'manual' — the seed's explicit `action_assign()` is load-bearing. (6) **`quant.reserved_quantity` semantics**: reservation is a soft lock that subtracts from `_get_available_quantity` but leaves `quantity` (on-hand) untouched. Post-unreserve, `reserved_quantity=0`, `quantity=10`. Seed sanity check uses `sum(quants.mapped("reserved_quantity"))` to verify the 5.0 lock, NOT `_get_available_quantity` (which would just return 5 = 10 - 5 reserved). (7) **Oracle robustness**: the button is locatable via either `button[name='do_unreserve']` (exact) or a label-text match on the visible statusbar buttons. Oracle tries the exact selector first and falls back to string-match for layout flakes. **To raise difficulty to hard**: add a second confirmed MO so the agent must pick the right one from the list (distractor pattern), OR chain with a re-reserve workflow ("unreserve THEN set a specific serial lot on a tracked component THEN re-reserve"). **Commit**: `[ADD] benchmark: mrp.unreserve_raw_material_on_mo (medium)`. |
---

## account.refund_customer_invoice_cash_basis

| Field | Value |
|---|---|
| **Task ID** | `account.refund_customer_invoice_cash_basis` |
| **Row** | 478 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 32.7s wall clock, 6/6 atomic edits matched, 0 postcondition failures, 50 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 83.3s single-shot, 6/6 atomic edits matched, 0 postcondition failures, 62 API calls, 30 non-forbidden writes, 0 forbidden, StrictClean=True). BU clicked **Credit Note** header button, filled reason, clicked primary **Reverse** (correctly avoided **Reverse and Create Invoice**), clicked the `price_unit` cell on the single credit-note line, typed `200.00` (clear=True), clicked **Confirm**, done — 14 steps, final self-report: "issued a partial refund for invoice BENCH-REFUND-001 … unit price 200.00 … total refund 200.00". Note: BU's `agent_result.json` has `success=False` at the process level because the outcome extractor flagged a non-fatal browser-close event, but the task mechanics and state-diff are entirely correct. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Accounting (account) — `account.move.reversal` wizard + `account.move` (`move_type='out_refund'` linked via `reversed_entry_id`). Start URL: `/odoo/accounting`. |
| **Workflow** | Seed posts a single-line customer invoice `BENCH-REFUND-001` for `Bench Ref Co` (service product `Bench Refund Service`, qty=1, price_unit=500.00, taxes cleared → amount_total=500.00). Agent: Invoices list → open `BENCH-REFUND-001` → click header **Credit Note** button (`button[name='action_reverse']`) → wizard opens (`account.move.reversal`) with only `reason`, `journal_id`, `date` fields → fill reason `Cash basis partial refund`, leave date + journal defaults → click primary **Reverse** (`name='refund_moves'`, NOT the secondary `Reverse and Create Invoice` = `name='modify_moves'`) → redirected to draft `out_refund` credit note (`ref='Reversal of: <source.name>, Cash basis partial refund'`) with one copied line (Bench Refund Service, qty=1, price_unit=500) → **override price_unit in-place from 500.00 to 200.00** (do NOT delete row, do NOT change qty) → click header **Confirm** to post. End state: source invoice untouched (state='posted', amount_total=500, payment_state='partial'), linked credit note posted (move_type='out_refund', reversed_entry_id=source.id, amount_total=200, payment_state='paid', single product line with qty=1 price_unit=200). |
| **Capability tested** | **Single-line partial-refund via price_unit override on the reversal draft.** The "hard" trap intended by the spec is a non-default radio + amount field on the wizard (per the task backlog brief); however, **Odoo 19's `account.move.reversal` has no `refund_method` radio and no `amount` field** — its model has only `reason`, `date`, `journal_id`, `move_ids` + two action methods `refund_moves`/`modify_moves` (`addons/account/wizard/account_move_reversal.py` + `account_move_reversal_view.xml`). So the real difficulty is forced into two post-wizard moments: (1) pick the primary button `Reverse` (NOT `Reverse and Create Invoice`, which creates a second draft invoice and skips the credit-note-edit flow), (2) override `price_unit` on the **lone** copied line — unlike row 399 `account.credit_note_partial_refund_post` which lets the agent delete one of two lines, this task has a single line so the only correction path is an in-place `price_unit` edit, a pattern agents commonly skip in favour of accepting the full-amount draft. |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 83s. The task design is materially weaker than intended because the wizard spec in the brief (three-radio Full/Modify/Partial + amount field) does not exist in Odoo 19 — only the two-button footer remains. The prompt still explicitly instructs "Change the Bench Refund Service Unit Price from 500.00 to 200.00", which BU followed literally. **To re-harden** to hit the ≤40% pass calibration target, drop the explicit "Unit Price" guidance from the prompt (tell the agent only "reduce the refund total to 200.00 without deleting the line") so that an agent that sees the copied draft at 500 has to infer the edit-price-unit path rather than being hand-held there; or add a distractor invoice with identical totals for the same partner to force a find-and-select disambiguation before the wizard. **Cookbook data points (new / reinforced)**: (1) **Odoo 19 `account.move.reversal` wizard has NO radio and NO amount field.** Confirmed by reading `addons/account/wizard/account_move_reversal.py` (fields: `move_ids`, `new_move_ids`, `date`, `reason`, `journal_id`, `company_id`, `available_journal_ids`, `country_code`, `residual`, `currency_id`, `move_type` — nothing else) and `account_move_reversal_view.xml` (form renders only `reason`, `journal_id`, `date`; footer has `refund_moves` primary + `modify_moves` secondary + Discard). Any task spec that assumes a `refund_method` Selection ('refund'/'cancel'/'modify') is inherited from older Odoo versions — Odoo 17/18/19 moved to the two-action-button pattern and expect post-wizard edits for partial refunds. (2) **Reversal `ref` formula is deterministic**: `self.env._('Reversal of: %(move_name)s, %(reason)s')` (reversal.py:97-99) — uses source `move.name` (auto-sequence like `INV/2026/00001`), NOT source `ref` Char. Expected_state.json entity_keys for the created credit note MUST be `["<partner_name>", "Reversal of: INV/2026/00001, <reason>"]`. In this task with a BENCH_BASE seed that hasn't consumed any INV/ numbers prior, the first invoice posts as `INV/2026/00001` so the ref is exactly `Reversal of: INV/2026/00001, Cash basis partial refund`. (3) **6 atomic state-diff edits for partial-refund-with-price_unit-edit**: 1 `op: set` on source invoice `payment_state` (unpaid → partial) + 5 `op: create` on the new credit note move (`partner_id`, `ref`, `state`='posted', `move_type`='out_refund', `payment_state`='paid'). The credit note's `payment_state` goes straight to `paid` because reconciliation with the source's residual happens automatically on post (source invoice `amount_residual` drops by the credit-note total — 500→300 in this case → source goes to `partial`, credit goes to `paid`). (4) **`set_o2m_field(page, 0, "price_unit", "200")` is the idiomatic Playwright helper for editing a single o2m line** on an `out_refund` draft — the helper clicks the `td[name='price_unit']` cell, focuses the input, fills, presses Tab to commit the onchange that recomputes `amount_untaxed`/`amount_total`. (5) **trace_spec must list `account.move.reversal.modify_moves` as forbidden** to penalise agents that click "Reverse and Create Invoice" (the wrong button); primary-button `refund_moves` goes in `required_ops`. **Commit**: `[ADD] benchmark: account.refund_customer_invoice_cash_basis (hard)`. |
---

## account.modify_account_move_line_label

| Field | Value |
|---|---|
| **Task ID** | `account.modify_account_move_line_label` |
| **Row** | 484 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.7s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 49 API calls, 23 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | FAIL (F1=0.0, 360.0s wall clock single-shot — hit timeout / gave_up=True, 0 matching edits, 2 postcondition failures (state stuck at draft; line.name=False), 152 API calls, 101 non-forbidden writes, 0 forbidden, StrictClean=True). BU successfully clicked **Reset to Draft** (invoice flipped to draft) but got stuck in a 54+ step loop repeatedly typing "Corrected description" into the **Product** cell instead of the Label cell, triggering `ValidationError` dialogs about sequence format, then typing the invoice number into the sequence field, etc. The widget's product-label-conflation is a genuine trap — BU never recovered to fill the Label textarea nor re-click Confirm. |
| **F1** | 0.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Accounting (`account`) — `account.move` reset-to-draft → edit `account.move.line.name` via `product_label_section_and_note_field` widget → repost. Start URL: `/odoo/accounting/customer-invoices`. |
| **Workflow** | Seed posts a single-line customer invoice `BENCH-EDIT-001` for `Bench Edit Co` (service product `Bench Edit Service`, qty=1, price_unit=100.00, taxes cleared → amount_total=100.00, name auto-assigned `INV/2026/00001` since benchmark_base seed hasn't consumed any INV/ numbers). Agent: Customers → Invoices → open `BENCH-EDIT-001` → click header **Reset to Draft** (`button[name='button_draft']`) → state flips 'posted'→'draft', line cells become editable → in the sole invoice line, edit the **Label** column from `Service` to `Corrected description` (the column is actually merged into the product_id cell via the `product_label_section_and_note_field_o2m` widget; the label textarea lives at `td[name='product_id'] .o_field_product_label_section_and_note_cell textarea` and starts hidden with `d-none` when the label equals the product display name — must click the `.fa-bars` toggler first or strip the `d-none` class to reveal) → save the form → click header **Confirm** (`action_post`) to repost. End state: `state='posted'`, single line's stored `name` is `"Bench Edit Service\\nCorrected description"` (the widget's `parseLabel` prepends productName when both are set — the user-visible Label read via the widget's `label` getter strips productName and returns just `Corrected description`), `amount_total=100.00` unchanged. |
| **Capability tested** | **Reset-to-Draft → edit hidden-by-default line label via product_label_section_and_note_field widget → Repost cycle.** The core trap is the widget's visual/storage mismatch: (a) the Label and Product columns are rendered as a single merged cell `td[name='product_id']`, not a separate `td[name='name']`, so `set_o2m_field(..., 'name', ...)` (generic helper) fails with "locator timeout" — the cell simply doesn't exist. (b) When the stored `name` equals the product display_name (`Service` ≠ `Bench Edit Service`, so technically distinct — but a label that doesn't match shows as a tiny fa-bars toggler UNTIL you click into the cell), the textarea has `d-none` class. (c) The widget's `parseLabel` writes back `productName + "\\n" + enteredValue`, not just the entered value — check.py must tolerate either exact match or the productName-prefixed form. BU's loop-detected 54-step spiral typing the description into the product cell proves the trap bites: BU cannot distinguish the Product cell from the Label cell because they share a `td[name='product_id']` parent. |
| **Notes** | **Calibration MATCH — BU FAILED single-shot, oracle PASSED** at the expected pattern for a medium task. No existing task tests this reset-to-draft + label-edit cycle on `account.move.line` (closest are row 37 `purchase.reset_draft_edit_reconfirm` which edits a separate `purchase.order.note` HTML field, and row 408 `purchase.set_vendor_product_code_on_po_line` which edits the same widget but on a draft PO that never needs reset-to-draft and uses the purchase model). **Design quirks captured**: (1) **`account.move.line.name` is NOT on `td[name='name']`**. The list view widget `product_label_section_and_note_field_o2m` (declared in `addons/account/views/account_move_views.xml:1144-1156`) merges the `product_id` m2o column and the `name` text column into a single cell rendered under `td[name='product_id']`. Inside that cell, `product_name_and_description.xml` renders an m2o input for the product AND a `<textarea>` for the label. The textarea gets `class="d-none"` when `label.trim() === ""` (where `label` is `storedName.replace(productName, "").trim()` — see `product_name_and_description.js:107-113`). Clicking the `.fa-bars` toggler flips `labelVisibility=true` and removes `d-none`. (2) **`parseLabel` concatenates productName + label** (`product_label_section_and_note_field.js:50-54`): `return (this.productName && value && this.productName.concat("\\n", value)) || (this.productName && !value && this.productName) || (value || "");` — so entering `Corrected description` with product `Bench Edit Service` produces stored `name = "Bench Edit Service\\nCorrected description"`. This is intentional UX: the printed invoice renders the product name as heading + the label as description. check.py MUST accept both the exact string AND the productName-prefix concat. (3) **`account.move.line` tracked by `(move_id, product_id)` match_key** in state_spec works across the reset→repost cycle — the id is preserved on reset (Odoo does NOT recreate lines on button_draft), and `move_id` normalizes to move.display_name which is `INV/2026/00001 (BENCH-EDIT-001)` in both the before (posted) and after (reposted) snapshots. During the middle draft phase `move_id` normalizes to `Draft Invoice INV/2026/00001 (BENCH-EDIT-001)` but that's not captured since only before/after states are diffed. (4) **`button_draft` preserves the line id and the `name` is editable on draft** — no need to recreate the line. `state='draft'` at pre-edit, `state='posted'` at post-edit — but since start+end are both 'posted', there's NO `account.move.state` edit in the diff (only the `account.move.line.name` edit survives). (5) **`action_post` re-runs the sequence guard**: re-posting a draft that was posted before leaves the move name unchanged (`INV/2026/00001` stays) — the sequence isn't re-assigned because `move.name` is already set to a non-`/` value. Confirmed empirically: before=after move.name=`INV/2026/00001`. (6) **Oracle helper `set_o2m_field` does NOT work for this widget** — the generic helper targets `td[name='<field>']`, but the label textarea lives under `td[name='product_id']`. Copy the `_edit_description_cell` helper from `benchmark/tasks/purchase.set_vendor_product_code_on_po_line/oracle.py` (lines 59-143) — identical mechanic: click product_id cell to enter edit mode, click `.fa-bars` toggler (or strip `d-none` via JS), fill the textarea, Tab to commit. (7) **expected_state.json has exactly 1 atomic edit** (`account.move.line.name` set to `"Bench Edit Service\\nCorrected description"`) — the invoice state field doesn't appear because the diff engine only sees before(posted)/after(posted). (8) **To escalate to hard**: (a) add a second line (e.g., a "shipping" charge) so agent must disambiguate which line's label to edit, (b) require a specific label that happens to include the product name as substring (forcing the widget's `label.replace(productName, "")` stripping path to be tested), or (c) combine with a partner email-send step after repost (full "edit then notify customer" cycle). **Commit**: `[ADD] benchmark: account.modify_account_move_line_label (medium)`. |

---

## crm.log_opportunity_note_internal

| Field | Value |
|---|---|
| **Task ID** | `crm.log_opportunity_note_internal` |
| **Row** | 480 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 24.5s wall clock, 0 atomic edits tracked, 0 postcondition failures, 38 API calls, 17 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS single-shot (F1=1.0, 68.9s wall clock, 8 steps, 0 postcondition failures, 48 API calls, 24 non-forbidden writes, 0 forbidden, StrictClean=True). BU navigated CRM → clicked `Bench Note Opp` kanban card → clicked Log note tab → typed exact text → clicked Log button → done. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | CRM (`crm.lead`) + Discuss/Chatter (`mail.message` subtype `mail.mt_note`). Start URL: `/odoo/crm`. |
| **Workflow** | Seed creates `crm.lead` `Bench Note Opp` (type='opportunity', partner=`Bench Note Co`, expected_revenue=12000, probability=25, stage='New'). Agent: CRM app → find `Bench Note Opp` in pipeline kanban → open form → click **Log note** tab in chatter → type `Customer asked for demo` in composer → click **Log** button. End state: a single `mail.message` linked to the lead with `message_type='comment'` + `subtype_id=ref('mail.mt_note')` + HTML-stripped body substring `demo`. |
| **Capability tested** | Chatter Log-note-vs-Send-message distinction (easy anchor). Exercises the default Log-note tab click on a CRM opportunity form, paired with exact-text typing in the rich-text composer and the Log button to commit. The subtype check pins `mail.mt_note` (not `mail.mt_comment`) so a Send-message post fails; the body check only requires the `demo` substring so paraphrasing is tolerated. Distinct from row 408 `mail.send_email_with_attachment_log_as_note` (Send message + attachment), row 32 `project.complete_task_log_note` (stage change + log note), row 61 `sale.add_note_to_quotation` (log note on sale.order). |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 69s with 8 steps (navigate→login→retry→wait→click card→click Log note→type→click Log→done). Predicted calibration was "easy ~80% pass" and BU hit the target; this is the intended behaviour for an easy anchor task that validates the Log-note tab discovery capability. No behavioural surprises. **Cookbook data points (reinforced)**: (1) **`mail.message.subtype_id=mail.mt_note` is the internal-note signal on CRM lead chatter** — both Log note and Send message produce `message_type='comment'`, so the check gates on `msg.subtype_id.id == env.ref('mail.mt_note').id` (NOT `message_type` alone, NOT `is_internal` alone). (2) **The CRM kanban card is locatable via `click_kanban_card(page, 'Bench Note Opp')`** which resolves to `.o_kanban_view .o_kanban_record:has-text(...)`; BU finds it via an `article role=link` accessible name. (3) **Chatter Log note button is discoverable via `button.o-mail-Chatter-logNote` OR the visible text `Log note`**; the composer input is `textarea.o-mail-Composer-input` OR a `contenteditable='true'` div (the oracle tries both in a `.last` locator chain). (4) **Log button is the composer's primary action** — `button.o-mail-Composer-send:has-text('Log')` (text becomes 'Send' for the Send-message tab, 'Log' for Log note). (5) **Body substring check tolerates HTML wrappers** — check.py strips `<p>…</p>` via a `<[^>]+>` regex before the `demo` lowercase membership test, so the agent can type plain text or paste rich-text and both pass. (6) **trace_spec lists `crm.lead.unlink`, `action_set_lost`, `action_set_won`, and `mail.message.unlink` as forbidden** to penalise destructive or side-effect deviations; state-diff is empty (zero atomic edits tracked via state_spec) because chatter posts don't modify the tracked `crm.lead` fields. **Commit**: `[ADD] benchmark: crm.log_opportunity_note_internal (easy)`. |
---

## stock.cancel_picking_abandoned

| Field | Value |
|---|---|
| **Task ID** | `stock.cancel_picking_abandoned` |
| **Row** | 481 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 31.3s wall clock, 1/1 atomic edit matched, 0 postcondition failures, 37 API calls, 15 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 95.7s single-shot, 1/1 atomic edit matched, 0 postcondition failures, 46 API calls, 22 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). BU navigated Inventory > Operations, opened Deliveries, clicked the `WH/OUT/BENCH-CANCEL` row, clicked **Cancel** (`button[name='action_cancel']`), clicked **Ok** on the "Are you sure you want to cancel this transfer?" native Odoo confirm dialog, and self-reported "The transfer WH/OUT/BENCH-CANCEL has been successfully cancelled." in 14 steps. (Loop-detection nudges fired briefly in steps 8-13 because BU re-clicked the Operations dropdown a few times looking for a "Transfers" link that doesn't exist as a single menu entry in Odoo 19 — the sidebar exposes Receipts / Deliveries / Internal Transfers / Dropshipping instead, under a "Transfers" section header. BU recovered by clicking Deliveries.) Note: `agent_result.json` has `success=False` at the process level (browser-session reset side-effect), but state-diff + postcondition + required-op are all clean. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Inventory (stock) — `stock.picking` header `action_cancel` button with `confirm="Are you sure you want to cancel this transfer?"` attribute triggering a native Odoo `ConfirmDialog`. Start URL: `/odoo/inventory`. |
| **Workflow** | Seed creates an outgoing `stock.picking` with pinned `name='WH/OUT/BENCH-CANCEL'` and `origin='WH/OUT/BENCH-CANCEL'` for new partner `Bench Cancel Ship Co` (customer_rank=1, auto-created), single `stock.move` for storable product `Bench Cancel Prod` (type='consu', is_storable=True, tracking='none'), demand=3, on-hand=3 at WH/Stock (`stock.quant._update_available_quantity`). After `action_confirm()` + `action_assign()` the picking lands at `state='assigned'` (Ready) with the move fully reserved. Agent: Inventory → Operations → Transfers/Deliveries list → open `WH/OUT/BENCH-CANCEL` row → header **Cancel** button → primary **Ok** on the confirm dialog. End state: same picking still exists (not unlinked), `state='cancel'`, partner / move / demand untouched. |
| **Capability tested** | **Pure cancel flow with a native confirm dialog.** Distinct from row 338 (`stock.cancel_picking_create_replacement_with_serial`, hard) which combines cancel with from-scratch replacement receipt + 2-serial Detailed Operations popup — this medium exercise isolates just the statusbar **Cancel** button + its `confirm=...` dialog so we get a clean capability signal on "click correct statusbar action + click correct primary button on the resulting modal" without conflating with serial-tracking or line-editing. The trap surface (calibration risk = medium): (1) agents can confuse the statusbar **Cancel** with a breadcrumb Discard (some themes render a breadcrumb back-arrow that a naive agent could mistake for a "cancel" affordance), (2) agents can click **Validate** instead of **Cancel** because both are primary-styled header buttons on an `assigned` picking, (3) agents can dismiss the confirm dialog (click Discard / Cancel) instead of confirming, (4) the sidebar grouping uses a "Transfers" section header with children Receipts / Deliveries / Internal Transfers — agents hunting for a literal "Transfers" menu entry can loop on the dropdown (BU did: 4 redundant Operations clicks before finding Deliveries). |
| **Notes** | **Well-calibrated as medium, BU passed single-shot** (95.7s, 14 steps). Both the header Cancel button label ("Cancel") and the dialog primary button ("Ok") are standard, and the prompt explicitly says to click Ok/Confirm on the dialog, so BU had no decision point that could trap it. **Design quirks captured**: (1) The stock.picking view (`addons/stock/views/stock_picking_views.xml:132`) defines `<button name="action_cancel" ... string="Cancel" ... confirm="Are you sure you want to cancel this transfer?" .../>` — the `confirm=...` attribute triggers Odoo's native `ConfirmDialog` (not a custom wizard), with primary button "Ok" and secondary "Cancel". (2) `stock.picking.action_cancel()` (stock_picking.py:1210-1214) delegates to `self.move_ids._action_cancel()` and writes `is_locked=True`; empty pickings (no moves) get `state='cancel'` set directly. (3) `state='cancel'` is reachable from `state in ('assigned', 'confirmed', 'draft', 'waiting')` per the button's `invisible=...` gate — the seed's `action_confirm()+action_assign()` guarantees state='assigned' which allows Cancel. (4) The Cancel button stays visible even after state='cancel' transition briefly until the form reloads; we don't assert the button disappears — we just wait for `_wait_no_loading` and rely on the state-diff check. (5) state_spec.yaml uses `match_key=[name, partner_id]` → entity_key `["WH/OUT/BENCH-CANCEL", "Bench Cancel Ship Co"]` (not `[null, "…"]` because the seed pins `name`, so the normalized entity_key slot 0 is the real sequence name). (6) trace_spec lists `stock.picking.action_cancel` as required and `stock.picking.unlink`, `stock.picking.button_validate`, `stock.picking.do_unreserve` as forbidden to catch deletion / accidental-validate / accidental-unreserve paths. **Commit**: `[ADD] benchmark: stock.cancel_picking_abandoned (medium)`. |

---

## website_blog.delete_comment_moderate

| Field | Value |
|---|---|
| **Task ID** | `website_blog.delete_comment_moderate` |
| **Row** | 482 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 14.4s wall clock, 0/0 atomic edits matched, 0 postcondition failures, 35 API calls, 14 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). Oracle logs in, navigates `/odoo/blog-post-pages`, resolves the seeded `Bench Mod Post` id + `mail.mt_comment` subtype id via `/web/dataset/call_kw`, finds the spam comment by body marker `BUY CHEAP`, and calls `mail.message.unlink([spam_id])` — admin super-user bypass. |
| **Browser-Use** | PASS (F1=1.0, 120.9s single-shot, 22 steps, 0 postcondition failures, 122 API calls, 55 non-forbidden writes, 0 forbidden, StrictClean=True). BU took two accidental Website-Preview detours before clicking the **Blog Post** breadcrumb to return to the back-office form, then dispatched a JS `mouseover` on the Spam Bot message, clicked `button[aria-label='Expand']` on the per-message action toolbar, clicked the `role='menuitem' name='delete' aria-label='Delete'` item in the dropdown, and confirmed in `MessageConfirmDialog`. `custom:/mail/message/update_content: 1` in the trace confirms the chatter Delete path was exercised. Process-level `agent_result.success=False` is a stale BU extractor flag unrelated to task mechanics — strict PASS via state + postconditions. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | `website_blog` (base snapshot) + `mail` chatter (`mail.message` with `message_type='comment'` + `subtype_id=mail.mt_comment`). Start URL: `/odoo/blog-post-pages`. |
| **Workflow** | Seed idempotently recreates a published `blog.post` `Bench Mod Post` in blog `Bench News`, authored by admin, plus two portal-group users `Reviewer Good` and `Spam Bot`. Posts two chatter comments to the post via `post.sudo().message_post(body=..., author_id=<portal_partner>, message_type='comment', subtype_xmlid='mail.mt_comment')` — one legitimate review ("Great write-up ...") and one spam ("BUY CHEAP WATCHES NOW!!! ..."). Agent opens the backend form, scrolls the chatter, hovers the spam message to reveal the per-message action toolbar, opens the `...` Expand overflow menu, clicks **Delete** (`fa-trash`), and confirms the `MessageConfirmDialog`. End state: post unchanged; the spam `mail.message` row is either unlinked OR its body cleared (check.py accepts both); the good review survives intact. |
| **Capability tested** | **Chatter moderation via hover → overflow → Delete → confirm.** The per-message Delete action is NOT surfaced as a top-level icon — it lives behind a hover-only action toolbar whose trash/Delete entry collapses into an `...` Expand overflow menu. The agent must (1) identify the correct message out of two (gate on `author_id.display_name == 'Spam Bot'` or body marker `BUY CHEAP`), (2) trigger the hover state, (3) expand the overflow, (4) click Delete, (5) accept the confirmation dialog. Complements row 408 `mail.send_email_with_attachment_log_as_note` (Send-message + attachment upload) and row 396 `mail.pin_and_reply_in_chatter` (Pin action via same hover toolbar on Discuss channel) — this is the only task that exercises the chatter **Delete** action on a business record (`blog.post`). |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 22 steps / 121s. Stated risk was **hard, ≤40% pass** (tier 3); empirical single-shot pass happened because (a) `aria-label='Expand'` on the overflow button and `aria-label='Delete'` on the dropdown item expose the entire delete path to BU's element scorer (same dynamic as row 477 `website_forum.upvote_question_mark_as_answer` → `aria-label='Upvote'`), (b) ONE spam vs. ONE good comment — no multi-decoy disambiguation, and (c) the confirmation dialog's **Delete** primary button is the default keyboard focus. Kept as hard/tier-3 per backlog spec because the oracle path is stable, the moderation workflow is realistic (common Odoo admin task), and the chatter hover-overflow-confirm sequence is a deep-UI pattern not covered elsewhere. **Cookbook data points (new)**: (1) **Chatter Delete = `/mail/message/update_content` with `body=''`, NOT `mail.message.unlink`.** `addons/mail/static/src/core/common/message_actions.js`'s `delete` action calls `message.remove({removeFromThread})`, which POSTs body='' to `/mail/message/update_content`. Server-side `mail.thread._message_update_content` writes body='', then calls `_clean_empty_message(message)` which on plain `mail.thread` (as `blog.post`) only unlinks link previews — the mail.message row survives with body=''. Only `discuss.channel` actively cascades to unlink. check.py MUST accept both outcomes (unlink OR body=''), gating on "no surviving body containing the spam marker" rather than record count. (2) **`editable` getter in `message_model.js:214-219`** returns `True` iff `message_type === 'comment'` AND (`self.store.self.main_user_id?.is_admin || self.isSelfAuthored`). Admin can delete any comment; agents authored by a portal user can only delete their own. Seed author_id = portal partners, active session = admin → admin-delete path available. (3) **Seeding admin-deletable chatter comments** uses `post.with_user(admin).sudo().message_post(body=..., author_id=<portal_partner>, message_type='comment', subtype_xmlid='mail.mt_comment')`. The `subtype_xmlid='mail.mt_comment'` is load-bearing — `mail.mt_note` posts render as internal Log notes (different tab) and may not be deletable via the admin-can-delete path the same way. (4) **Portal users are sufficient as author_id targets** — no need to grant internal group. Their auto-created `partner_id` is what `mail.message.author_id` stores. Cleanup keeps the users + partners around across runs to avoid FK orphans on lingering mail.message rows. (5) **`expected_state.json = []`** for moderation tasks: the agent action doesn't change any `blog.post` tracked field (name/blog/author/published all stay); only `mail.message` changes. `state_spec.yaml` ignores chatter-side computed fields (`message_ids`, `website_message_ids`, `message_*_counter`, `activity_ids`) — if those are tracked, message_post/unlink flips them and strict PASS breaks. (6) **`trace_spec` forbidden_ops** must NOT list `mail.message.unlink` because (a) the oracle uses unlink as a short-circuit, (b) admin deleting via dev-mode list view does unlink — both are valid. Keep it in optional_ops alongside `mail.thread.message_update_content`. **Commit**: `[ADD] benchmark: website_blog.delete_comment_moderate (hard)`. |
---

## im_livechat.send_message_to_operator

| Field | Value |
|---|---|
| **Task ID** | `im_livechat.send_message_to_operator` |
| **Row** | 479 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 17.0s wall clock, 2/2 atomic edits matched, 0 postcondition failures, 44 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | FAIL (F1=0.0, 360.0s full timeout, 0/2 atomic edits matched, 1 postcondition failure, 67 API calls, 15 non-forbidden writes, 0 forbidden, loop-detection nudges fired from step 71 onward). BU got stuck on the Live Chat kanban dashboard: clicking the `Bench Help` card redirects to a filtered Sessions list view (Discuss-backoffice widget), NOT to the `im_livechat.channel` form view — so BU never obtained the channel id and never reached the `/im_livechat/support/<id>` URL. Spent the last ~30 steps looping through `evaluate` JS probes trying to extract the id from `__owl__` / `window.odoo` internals, which do not expose it from the kanban card. Never opened the livechat widget; never sent a message; zero `discuss.channel` livechat sessions created. |
| **F1** | 0.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Live Chat (`im_livechat`) + Discuss / Mail (`discuss.channel`, `mail.message`). Start URL: `/odoo/livechat`. |
| **Workflow** | Seed creates a single `im_livechat.channel` named `Bench Help` with admin as the sole operator (`user_ids=[admin.id]`), a `button_text='Chat with us'`, a `default_message='How may I help you?'`, and one `im_livechat.channel.rule` with `action='display_button'` + `regex_url='/'` so the widget's button becomes visible on the support page. Agent: identify the channel id via the Live Chat back-office (kanban → 3-dot menu `Configure Channel` → form → Widget tab exposes the `web_page` URL `/im_livechat/support/<id>`) → navigate to that URL as an anonymous visitor (a fresh incognito-style tab; admin cookie must NOT leak or the agent becomes both operator and visitor and `get_session` short-circuits) → wait for `.o-livechat-root` shadow host to mount → click `.o-livechat-LivechatButton` inside the shadow root (Playwright's CSS pierces open shadow DOM automatically) → type `Hello, I need help` into `.o-mail-Composer-input` → press Enter → widget renders the sent bubble and server persists a new `discuss.channel` of `channel_type='livechat'` linked to `Bench Help` with the visitor message as the first comment. Oracle uses JSON-RPC on the admin-logged-in tab to `search_read` the channel id, then opens a second cookie-free `browser.new_context()` for the visitor flow. |
| **Capability tested** | **Frontend livechat widget interaction through Shadow DOM** — the livechat button, chat window, and composer all live inside `<div class="o-livechat-root">`'s **open** shadow root and are NOT reachable by the Discuss back-office UI. The widget's whole point is "the public visitor types here; the operator replies from Discuss". Agents that try to use Discuss back-office (e.g. search for `Bench Help` in `/odoo/discuss` sidebar) will not create the expected `discuss.channel` because those sessions only come into existence when `get_session` is called by the widget at `/im_livechat/support/<id>`. Also tests the back-office→frontend navigation: the kanban card's **default** click goes to a filtered Sessions list, NOT to the form view, so agents must go through the 3-dot `Configure Channel` dropdown (or read the `web_page` URL from the Widget tab) to obtain the channel id — this is exactly where BU looped. |
| **Notes** | **Calibration: MEDIUM, BU failed on the full timeout** (genuine failure, not a task-design bug). Shadow-DOM widgets are a capability BU lacks robust handling for in Odoo's kanban-redirect context. **Distinct from row 359** (`im_livechat.configure_channel_then_handle_widget_chat`): that task pre-seeds the `discuss.channel` livechat session + waiting visitor message and asks admin to REPLY with a canned-response shortcut in Discuss; this task is the mirror image — no pre-existing session, agent must BE the visitor and use the widget to create one. **Cookbook data points**: (1) **`.o-livechat-root` shadow host is always `display:contents` / hidden** — `page.wait_for_selector('.o-livechat-root', state='visible')` times out forever. Use `state='attached'` and then `page.locator('.o-livechat-LivechatButton').wait_for(state='visible')` which pierces into the shadow root via Playwright's default CSS engine. (2) **Playwright CSS pierces OPEN shadow DOM by default** — no `>>>` combinator needed (Playwright does NOT support `>>>`; it gets parsed as the CSS child `>` combinator, see first oracle iteration failure `.o-livechat-root > .o-livechat-LivechatButton`). (3) **Oracle must use a second cookie-free `browser.new_context()` for the visitor** — a logged-in admin visiting `/im_livechat/support/<id>` is treated as the operator, so `get_session`'s `_get_operator_info` round-robin excludes admin as visitor; the widget may still render but the created `discuss.channel` will have admin as both operator AND visitor, making the check `author != admin.partner_id` fail. (4) **`im_livechat.channel.rule` with `action='display_button'` + `regex_url='/'` is load-bearing in seed** — without at least one matching rule, the livechat widget on the support page stays hidden (the store's `livechat_available` is False, `LivechatButton.isShown` returns False). (5) **Check focus is loose ("body contains 'help', author public/portal")**: check.py is tolerant to text normalization (`html2plaintext` + lowercase) and allows any non-internal-user author, so visitors that show up as `mail.guest` (the default for public livechat sessions) pass. Internal users (has_group `base.group_user`) are rejected. (6) **`discuss.channel` state-diff with `active_test=False` + `match_key=['channel_type','livechat_channel_id']`**: the created session normalizes its livechat_channel_id many2one to `"Bench Help"`, so entity_key is `["livechat", "Bench Help"]`. Name of the channel varies per visitor (`"Visitor 12345, <Operator Name>"` pattern) and is unstable, so it is moved into `ignore_fields` — match only on channel_type + livechat_channel_id. **Commit**: `[ADD] benchmark: im_livechat.send_message_to_operator (medium)`. |
---

## hr_recruitment.hire_candidate_refuse_another

| Field | Value |
|---|---|
| **Row** | 483 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 29.3s wall clock, 4/4 atomic edits matched, 0 postcondition failures, 85 API calls, 38 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 111.1s single-shot, 4/4 atomic edits matched, 0 postcondition failures, 74 API calls, 31 non-forbidden writes, 0 forbidden, StrictClean=True). BU clicked the **Bench Role** job card → opened Top Candidate → clicked **Contract Signed** status-bar stage (`role=radio`) → Hired ribbon appeared → **Create Employee** header button → saved the pre-filled employee form → navigated back to Applications → opened Runner Up → **Refuse** → in the wizard clicked the **Not a fit** badge among three near-duplicate reasons → primary **Refuse** button. Agent correctly edited employee `job_title` to `Bench Role (Hired)` en route. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Recruitment (`hr_recruitment`) + HR (`hr`). Two wizards: stage-hired side-effect + `applicant.get.refuse.reason` modal. |
| **Workflow** | Seed creates `hr.job` **Bench Role** (department **Bench Department**) with 4 job-scoped stages `Initial Qualification`/`Qualified`/`Contract Proposal`/`Contract Signed` (last has `hired_stage=True`+`fold=True`). Seeds two applicants `Top Candidate` + `Runner Up` both in Initial Qualification. Seeds three refuse reasons: `Not a fit` (correct) + `Not a good fit` + `Not a fit - incomplete application` (near-duplicate distractors), alongside the existing demo reasons. Agent: open Bench Role → open **Top Candidate** → status-bar click **Contract Signed** (`_compute_date_closed` fires, sets `date_closed=now()`, Hired ribbon appears, `create_employee_from_applicant` becomes visible by `invisible="employee_id or not active or not date_closed"`) → click **Create Employee** → on the pre-filled employee form edit `job_title` to `Bench Role (Hired)` → save (web_save creates `hr.employee`, writes `applicant_ids=[(6,0,[app.id])]`, applicant's `employee_id` back-link populates via `hr.applicant.employee_id` m2o). Then: open **Runner Up** → click header **Refuse** (`archive_applicant`) → wizard `applicant.get.refuse.reason` opens → pick `Not a fit` badge (`refuse_reason_id` selection_badge widget) → Send Email left off (the seeded reason has no template so `_compute_send_mail` resolves False) → click primary **Refuse** (`action_refuse_reason_apply`) → writes `{refuse_reason_id: <Not a fit>, active: False, refuse_date: now()}` on the applicant. |
| **Capability tested** | Two orthogonal applicant flows in a single task: (a) **Hire flow** — stage write triggers `_compute_date_closed` which unveils a conditionally-visible header button (Create Employee) whose action redirects to a pre-filled `hr.employee` form that must still be saved (two-phase create-from-scratch: BU commonly clicks Create Employee but then abandons the pre-filled form without saving, leaving `applicant.employee_id=False`). Also requires a non-default edit on that pre-filled form (`job_title` = `Bench Role (Hired)`). (b) **Refuse flow** — `archive_applicant` opens the `applicant.get.refuse.reason` wizard with a selection_badge `refuse_reason_id` widget; among 3 seeded near-duplicate reasons + Odoo demo reasons (`Does not fit the job requirements`, `Duplicate`, `Spam`, …), the agent must pick exactly `Not a fit`. Then click the primary footer button (also labelled `Refuse`, `name='action_refuse_reason_apply'`). |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 111s (1 sample). BU successfully (i) walked the hire flow including the job_title override on the pre-filled employee form, (ii) navigated back to Applications via the breadcrumb, (iii) picked the correct `Not a fit` badge despite the two near-duplicate distractor reasons + 6 demo reasons in the same row. Modern Claude+BU handles this composed flow cleanly; a larger BU sample would likely pass ≥60% — above the hard ≤40% target. **To re-harden** to hit the hard calibration band: (1) require the refuse wizard's **Send Email** toggle to be flipped ON with a specific subject + body marker (BU tends to leave the composer as-is) — mirrors `skill_filter_then_send_offer` but on the refuse wizard; (2) seed 6+ applicants so the agent must find the two targets among distractors; (3) add a third decision (e.g. require Runner Up to be _restored_ after refuse, testing the post-refuse `Restore` button). Primary_track=true retained since the task is realistic and exercises two documented-hard UI patterns (`hr_recruitment.create_employee_from_applicant` two-phase form + `applicant.get.refuse.reason` selection_badge ambiguity). **Cookbook data points (new / reinforced)**: (1) **`hr.applicant` form has no "Hire" button** — the hire path is "click the `hired_stage=True` pill on the status bar, which triggers `_compute_date_closed` → `date_closed=now()`; that unveils the `Create Employee` header button because its `invisible` clause is `employee_id or not active or not date_closed`". The Hired ribbon is the `web_ribbon` with `invisible="application_status != 'hired'"` where `application_status='hired'` iff `active AND date_closed AND not refuse_reason_id`. (2) **`create_employee_from_applicant` is a two-phase action**: it calls `hr.employee.create(...)` then returns `hr.open_view_employee_list` with `res_id=<new employee id>` — the browser lands on the employee form but the record is already persisted to the DB. A subsequent **Save** (web_save) is only needed if the agent edits a field post-landing. If the agent just clicks Save without editing anything, web_save is a no-op; the DB row is already there. **The `applicant.employee_id` back-link is populated inside `create_employee_from_applicant` via `employee.write({'applicant_ids': self.ids})` + the matching m2o compute — no follow-up step required.** (3) **Refuse wizard's primary footer button label is "Refuse" (hotkey `q`)**, matching the header button label on the form. If the agent clicks the header Refuse, they see the wizard whose primary button is ALSO called Refuse — easy to mis-read as "already done" and dismiss. (4) **`hr.applicant.refuse.reason` is a 1-table config model with `sequence` + `name` + `template_id`**; a seeded reason without a `template_id` auto-unchecks `send_mail` in the wizard (`_compute_send_mail` = `bool(refuse_reason_id.template_id) and not applicant_without_email`). To force the agent to flip Send Email OFF (harder trap), seed the reason WITH a template (e.g. `mail.template email_template_data_applicant_refuse`) so `send_mail` starts True. (5) **state_spec match_key for hr.applicant** should be `[partner_name, job_id]` — `partner_name` alone collides when the same applicant has duplicates on multiple jobs; `job_id` normalizes to the job display name and stabilises the entity key. (6) **expected_state for refuse + archive** emits `op=set` with `norm_value=null` on `active` (the archive doesn't remove the row from `active_test=False` snapshots, it just flips `active=False`). **Commit**: `[ADD] benchmark: hr_recruitment.hire_candidate_refuse_another (hard)`. |
---

## sale.convert_quotation_to_order_verify_invoice_status

| Field | Value |
|---|---|
| **Row** | 486 |
| **Difficulty** | easy |
| **Tier** | 1 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 21.1s wall clock, 1/1 atomic edits matched, 0 postcondition failures, 44 API calls, 18 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 70.6s single-shot, 1/1 atomic edits matched, 0 postcondition failures, 29 API calls, 13 non-forbidden writes, 0 forbidden, StrictClean=True). |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Sales (`sale`). |
| **Workflow** | Seed creates partner `Bench Confirm Co`, product `Bench Confirm Item` (consu, list_price=100, taxes cleared), and a single draft `sale.order` `BENCH-CONFIRM` with `client_order_ref='BENCH-CONFIRM'` and one line (qty=1 @ 100.0). Agent: Sales → Quotations → open `BENCH-CONFIRM` → click **Confirm** in the header status bar. Verifies `sale.order.state='sale'`. |
| **Capability tested** | **Single-click Confirm on a draft quotation** — the canonical easy anchor for the Sales module. One record (no distractor ambiguity), one state transition (`draft`→`sale`), one button. Distinct from row 19 (`sale.confirm_correct_order`: 4 near-duplicate distractors requiring product-line inspection to pick the right one) and row 426 (`sale.duplicate_quotation_edit_delivery_date_confirm`: duplicate-then-edit-then-confirm). |
| **Notes** | **Calibration EXPECTED PASS** — easy anchor targeting ~80% BU pass rate; first single-shot PASS confirms pattern. Oracle uses JSON-RPC `search_read` to resolve SO id + `navigate('/odoo/sales/<id>')` to sidestep the `/odoo/sales` list-view flakiness documented in ODOO19_PATTERNS.md (`sale.order — /odoo/sales list-view flakiness in oracles`). `client_order_ref` used as `match_key` gives a stable entity_key (`["BENCH-CONFIRM"]`) even after confirm (`sale.order.name` is `copy=False` but survives unchanged on `action_confirm`). state_spec ignores `name`, `date_order`, `amount_*`, and date fields so the only observed edit is `state: draft → sale`. Taxes cleared in seed to keep `amount_untaxed == amount_total == 100.0` for the check.py assertions. **Commit**: `[ADD] benchmark: sale.convert_quotation_to_order_verify_invoice_status (easy)`. |
---

## website_sale.configure_free_shipping_threshold

| Field | Value |
|---|---|
| **Task ID** | `website_sale.configure_free_shipping_threshold` |
| **Row** | 489 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 20.9s wall clock, 2/2 atomic edits matched, 0 postcondition failures, 29 API calls, 12 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 66.6s single-shot, 2/2 atomic edits matched, 0 postcondition failures, 23 API calls, 9 non-forbidden writes, 0 forbidden, StrictClean=True). BU (7 steps) navigated to `/odoo/delivery-methods`, handled the login redirect, clicked the `Bench Ship` row, ticked the `free_over` checkbox, overwrote the revealed `amount` input from 1000 → 100.00 (triggering the harness's concatenation auto-retry once), and clicked the manual Save. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | `delivery` (`delivery.carrier`) on the backend Delivery Methods list (`delivery.action_delivery_carrier_form`, path `/odoo/delivery-methods`, parent menu `sale.menu_sales_config` / also mounted under `stock.menu_delivery`). Provider stays `delivery_type='fixed'`; only the right-column `free_over` Boolean + `amount` Float are toggled. |
| **Workflow** | Seed creates a service product `Bench Ship Product` (list_price=15.0) and a `delivery.carrier` `Bench Ship` with `delivery_type='fixed'`, `product_id=<Bench Ship Product variant>`, and `free_over=False` (so the `amount` field is hidden in the form until the checkbox is flipped). `fixed_price` is set via `product.list_price=15.0` (the field is a `store=True, compute+inverse` proxy to product.list_price). `amount` stays at Odoo's default `1000`. Agent: opens `/odoo/delivery-methods` → clicks the `Bench Ship` list row → on the form's right-hand `delivery_details` group locates the label **Free if order amount is above** rendered from `<label for="free_over" invisible="delivery_type == 'base_on_rule'"/>` with a sibling `<div name="free_over_amount">` holding the `free_over` checkbox + the `amount` monetary input gated by `invisible="not free_over"`+`required="free_over"` → ticks `free_over` (the amount input un-hides) → clears the `1000` default and types `100.00` → Save. Writes: `{free_over: True, amount: 100.0}` on the carrier. |
| **Capability tested** | Standard settings-form boolean toggle that *reveals* a second numeric field via `modifiers.invisible="not free_over"`. Tests whether the agent (a) finds the right checkbox on a crowded carrier form (8+ fields grouped into two columns, plus 3 notebook tabs), (b) doesn't confuse the `amount` threshold with the visible **Fixed Price** (`fixed_price=15.00`) field on the left column, (c) overwrites the `1000` default on the newly-revealed input rather than appending/prepending digits, and (d) doesn't change the provider (clicking anywhere near the `delivery_type` radio would hide the whole `free_over_amount` div when switching to `base_on_rule`). The hidden-until-toggled pattern is the core twist versus a plain Boolean+Float pair. |
| **Notes** | **Calibration MISS — BU PASSED single-shot at F1=1.0 in 66.6s / 7 steps** (1 sample). BU recognised the field labels immediately, did not touch `fixed_price`, and the harness's built-in concatenation-detection auto-retry salvaged the first `0.00100.00` typing glitch into a clean `100.00`. Kept as medium/tier:2 per spec (row 489). **To harden** into a genuine BU-failing task: (i) seed 3 distractor carriers (`Bench Ship EU`, `Bench Ship US`, `Bench Ship CA`) with identical Fixed Price so the agent must disambiguate by name, (ii) require the checkbox to be flipped **OFF** on an already-free-over carrier while keeping the existing `amount` value unchanged (trap: Odoo's `_compute_amount` resets to default when `free_over` is False-and-then-True), or (iii) add a second required edit on the notebook's **Availability** tab (`country_ids=[United States]`) so the agent must also switch tabs and complete a many2many_tags interaction. **Cookbook data points (new / reinforced)**: (1) **`delivery.carrier.amount` defaults to `1000`** (not 0 or null) via `fields.Float(default=1000)` — a seed that omits the field still gives the agent a visible starting value of 1,000.00 once `free_over` is ticked, so the prompt must explicitly call out that overwriting (not appending) is required. (2) **`delivery.carrier.fixed_price` is `store=True, compute='_compute_fixed_price', inverse='_set_product_fixed_price'`** — it reads/writes `carrier.product_id.list_price`. Writing `{fixed_price: 15.0}` during `create(...)` fires the inverse, which writes `product.list_price=15.0`; a later read re-computes from the product. Seeds should set `list_price=15.0` on the product template directly AND pass `fixed_price=15.0` at create time to avoid a race where the compute has not yet run. (3) **The `amount` input is gated by `invisible="not free_over"`**; Odoo keeps the DOM element in the tree but hidden with `d-none`/display rules. Playwright `locator("[name='amount'] input")` still matches the element, but typing into it while hidden fails silently — always click the `free_over` checkbox first and wait for the `amount` field to become visible. (4) **The `Free if order amount is above` **label** belongs to the checkbox, not the amount input** (`<label for="free_over" ...>`) — agents that try `page.get_by_label("Free if order amount is above")` land on the checkbox, which is the desired behaviour here but is a footgun for adjacent tasks that try to address the `amount` input by that string. (5) **Backend path `/odoo/delivery-methods` resolves via the action's `<field name="path">delivery-methods</field>`** (set in `delivery/views/delivery_carrier_views.xml`) — no module prefix needed in the URL. (6) **state_spec match_key=[name]** is safe for `delivery.carrier` because `name` is `required=True` and the default demo DB names (`Free delivery charges`, `Delivery Now Free Over 100` on some snapshots) don't collide with `Bench Ship`. (7) **trace_spec must include `delivery.carrier.create` in `forbidden_ops`** — BU sometimes prefers "New + fill + save" over editing, which would create a second carrier and leave both records behind; `forbidden_ops: [delivery.carrier.create]` gives a second guard on top of the check.py `len(carriers) > 1` assertion. **Commit**: `[ADD] benchmark: website_sale.configure_free_shipping_threshold (medium)`. |
---

## stock.receive_serial_tracked_product_two_serials

| Field | Value |
|---|---|
| **Task ID** | `stock.receive_serial_tracked_product_two_serials` |
| **Row** | 488 |
| **Difficulty** | hard (calibration miss — see Notes) |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 49.1s wall clock, 5/5 atomic edits matched, 0 postcondition failures, 57 API calls, 24 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 122.0s single-shot / 16 steps, 5/5 atomic edits matched, 0 postcondition failures, 67 API calls, 31 non-forbidden writes, 0 forbidden, StrictClean=True). BU walked the flow cleanly: `/odoo/inventory` → Receipts kanban → open `WH/IN/BENCH-SERIAL` → click per-line Details button (`action_show_details`) → in the Detailed Operations popup clicked lot_id combobox on row 1, typed `SN-BENCH-A001`, picked the autocomplete `Create "SN-BENCH-A001"` option → repeated for row 2 with `SN-BENCH-A002` → footer Save → back on picking, header Validate. No backorder dialog, no errors. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Inventory (`stock`). Start URL: `/odoo/inventory`. |
| **Workflow** | Seed creates vendor `Bench Serial Vendor` (supplier_rank=1) + storable product `Bench Serial Item` (tracking='serial'). Grants admin `stock.group_production_lot` and flips the Receipts picking type to `use_create_lots=True AND use_existing_lots=True` so the popup's lot_id column is an m2o with a Create autocomplete. Creates a single incoming picking `WH/IN/BENCH-SERIAL` for Bench Serial Item demand=2 from Bench Serial Vendor, `action_confirm()` + `action_assign()` so state=`assigned`. Agent: open Inventory → Receipts → `WH/IN/BENCH-SERIAL` → click Details on the Bench Serial Item move line → in the Detailed Operations popup find/ensure 2 move-line rows → enter `SN-BENCH-A001` / `SN-BENCH-A002` one per row (Create option from autocomplete) with qty=1 each → Save popup → click Validate. |
| **Capability tested** | Serial/lot entry via the Detailed Operations popup (`stock.view_stock_move_operations` dialog, `action_show_details`) on a serial-tracked incoming picking, with two distinct serials entered as two distinct move_line rows. Classic hard-tier BU trap: agent types both serials into a single pre-reserved move_line or merges qty=2 onto one lot. Check.py validates `len(move_line_ids with qty>0) == 2`, qty=1 each, two distinct stock.lot records named `SN-BENCH-A001` / `SN-BENCH-A002` linked via `lot_id`, picking state=done, no backorder. |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 122s (1 sample). Two factors made this easier than the `stock.cancel_picking_create_replacement_with_serial` reference: (a) the picking is **pre-seeded and already reserved** — agent does not have to Cancel, Create New, set vendor/product/demand, then Confirm before reaching Part C; (b) with demand=2 and tracking='serial', Odoo 19's `_action_assign` on an incoming move **pre-creates 2 empty move_line rows** (not 1 collapsed qty=2 row), so BU does not even need to click `Add a line` — it just tabs into each existing row's lot_id combobox and picks Create. The whole flow collapses to ~8 clicks. **To re-harden** into the hard band (≤40% BU pass): (1) seed the picking with `action_confirm()` only (skip `action_assign`), forcing the agent to click **Check Availability** first, which spawns 1 move_line pre-reserved at qty=1 with empty lot — now the agent MUST click `Add a line` in the popup to materialise the second row; (2) pair with a wizard (e.g., set `picking_type_id.use_create_lots=False` so the lot must be picked from a distractor-heavy list of seeded stock.lot rows on a different product); (3) demand=3 so the agent must add 2 more rows in the popup, not just 1. Kept as primary_track=true because the task is realistic, reproducible, and the oracle exercises the documented Detailed Operations popup pattern that remains a genuine capability test for other agents. **Cookbook data points**: (1) **`stock.move.show_details_visible` compute gates the Details button**: True when (a) admin has `stock.group_stock_multi_locations`/`group_tracking_lot`/`group_tracking_owner`, (b) `len(move_line_ids) > 1`, OR (c) product `tracking != 'none'`. For serial-tracked products, clause (c) is automatically satisfied — no extra group needed on admin. (2) **`_action_assign` on a serial-tracked incoming move with demand=N ≥ 2 pre-creates N empty move_line rows**, one per unit, each with quantity=0 and empty lot_id. This materially changes the task difficulty: the "Add a line" step from the reference task is skipped entirely because both rows already exist. (3) **Receipts picking type must have `use_create_lots=True` AND `use_existing_lots=True` for the popup's lot_id autocomplete to expose `Create "<text>"`**: either alone yields text-only `lot_name` (no `stock.lot` row) or hides the Create option entirely. (4) **`expected_state.json` entity_key for the pinned-name picking**: since `state_spec.match_key = [name, partner_id]` and the picking has `name='WH/IN/BENCH-SERIAL'`, the pre→post diff emits a `set` op with entity_key `["WH/IN/BENCH-SERIAL", "Bench Serial Vendor"]` (3-slot match_key yields 3-slot keys when a third field is listed — this task uses 2-slot match_key, so 2-slot keys). New stock.lot rows created on-the-fly in the popup emit `op=create` entries with entity_key `[<serial>, "Bench Serial Item"]` for both `name` and `product_id` fields. (5) **`stock.lot.name_create` vs `stock.lot.create`**: clicking the autocomplete Create option actually calls `stock.lot.name_create` under the hood (optional_op'd in trace_spec), but BU often uses Owl's create flow which funnels through `stock.lot.create` (also optional). Leave both in optional_ops. **Commit**: `[ADD] benchmark: stock.receive_serial_tracked_product_two_serials (hard)`. |
---

## account.import_opening_balance_set_initial_equity

| Field | Value |
|---|---|
| **Task ID** | `account.import_opening_balance_set_initial_equity` |
| **Row** | 490 |
| **Difficulty** | hard |
| **Tier** | 3 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 48.0s wall clock, 3/3 atomic edits matched, 0 postcondition failures, 50 API calls, 19 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). |
| **Browser-Use** | PASS (F1=1.0, 175.8s single-shot, 3/3 atomic edits matched, 0 postcondition failures, 123 API calls, 38 non-forbidden writes, 0 forbidden, StrictClean=True). BU navigated `/odoo/accounting` → Accounting → Journal Entries, clicked New, filled Reference `OPEN-BAL-001`, set Accounting Date `01/01/2026`, left Journal at Miscellaneous Operations, added two balanced lines (`Stock Valuation` debit 10000 + `Opening Balance` credit 10000), saved, clicked Post. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | Accounting (account). Uses move_type='entry' journal entry form and the general ledger's Miscellaneous Operations journal. |
| **Workflow** | Seed ensures (a) admin has `account.group_account_readonly/invoice/user` so the `aml_tab` Journal Items tab renders, (b) a general journal named exactly `Miscellaneous Operations` exists, (c) a `Stock Valuation` asset_current account with code `140000` exists (generic CoA has no such account — stock/mrp tasks seed it; we do so defensively), (d) a dedicated `Opening Balance` equity account (code `300100`, `account_type='equity'`) exists so the credit-side autocomplete is deterministic. Agent: open `/odoo/accounting/entries` → click **New** → fill `ref='OPEN-BAL-001'` → set `date=2026-01-01` → leave journal on Miscellaneous Operations → add line 1 (Stock Valuation, debit 10000, label "Opening stock valuation") → add line 2 (Opening Balance, credit 10000, label "Initial equity contribution") → Save → click **Post**. Final state: `account.move(move_type='entry', ref='OPEN-BAL-001', state='posted', date=2026-01-01)` with two lines totalling debit=credit=10000, one line on `asset_current`/`Stock Valuation` (code 140000) debit-side and one line on an `equity`/`Opening Balance` account credit-side. |
| **Capability tested** | Create-from-scratch `move_type='entry'` journal entry (distinct form from invoices: no Customer field, `line_ids` one2many with Debit/Credit columns, header `Post` button instead of Confirm). Two m2o account autocompletes where the displayed items are formatted `<code> <name>` (substring matching wrongly picks "Current Assets" when typing "Stock Valuation"). Balanced debit/credit invariant (debit=credit=10000). Future-dated entry requires `auto_post='no'` for Post button to stay visible. |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 175.8s. The task is materially easier than the hard ≤40% target because: (1) the prompt enumerates both accounts by name + code and exact debit/credit amounts, giving BU a deterministic recipe; (2) unlike `account.create_recurring_journal_entry` (which also passes BU) there is no chatter-activity scheduling step to stumble on; (3) the account names `Stock Valuation` and `Opening Balance` are distinctive enough that substring-autocomplete collisions do not hit. Distinct from row 327 `account.create_recurring_journal_entry` (3 lines + mail.activity scheduling) and row 423 `account.reverse_journal_entry_from_general_ledger` (reversal-wizard of an existing posted entry) — this is the from-scratch 2-line opening-balance pattern. **To re-harden** to hit the hard band: (1) remove the explicit `(code 140000)` hint from the prompt and seed a near-duplicate account (e.g. `Stock Interim (Received)`) that forces the agent to disambiguate on account_type rather than keyword; (2) require an unusual posting date (e.g. a prior fiscal year) so the agent must flip `auto_post` to keep Post visible; (3) add analytic_distribution on one line or require a specific partner on one line; (4) add a third balancing line (e.g. a $500 rounding contribution) to escape the 2-line trivial pattern. Primary_track=true retained since it is a realistic bookkeeping pattern and exercises the documented move_type='entry' + debit/credit-columns UI. **Cookbook data points (new / reinforced)**: (1) **`account.move.amount_total_signed` is NOT 0 for a balanced `move_type='entry'`** — it equals the single-sided total (10000 here), because `_compute_amount` for entries falls through to `balance = sum(line.balance)` = 0 on ORM level but `amount_total_signed` is derived from `invoice_untaxed + invoice_tax` which only sums the credit side via `line.balance` sign convention. Postcondition checks that assume balanced entries have `amount_total_signed=0` will spuriously fail; use `sum(line.debit) == sum(line.credit)` on filtered non-section lines as the balance invariant instead. (2) **`Stock Valuation` account (code 140000)** is NOT shipped by `l10n_generic_coa` — only the stock_account / mrp_account chain seeds it via `company.account_stock_valuation_id`. Seeds that reference Stock Valuation must create it as `account_type='asset_current'` (or `asset_fixed`) if absent. (3) **`account_type='equity'`** renders under the "Equity" section of the account autocomplete; the base generic CoA has a "Common Stock" equity account but NOT "Opening Balance". Seeding an explicit equity account with code 300100 avoids autocomplete collisions with "Retained Earnings" (30xxxx range). (4) **expected_state for a from-scratch posted entry** cleanly captures 3 atomic edits: `ref` (create), `move_type` (create), `state` (create) — all keyed on `[ref]`. No `op=set` edits since there is no pre-existing record. (5) **Miscellaneous Operations journal** is the default general journal; `_ensure_misc_journal` seed pattern (search-by-name → fall back to any `type='general'` and rename → last-resort create) is shared with `account.create_recurring_journal_entry` and `account.reverse_journal_entry_from_general_ledger`. **Commit**: `[ADD] benchmark: account.import_opening_balance_set_initial_equity (hard)`. |
---

## website_sale.add_product_review_publish

| | |
|---|---|
| **Row** | 485 |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 19.7s wall clock, 5/5 atomic edits matched, 0 postcondition failures, 23 API calls, 10 non-forbidden writes, 0 forbidden, StrictClean=True, RequiredOpRecall=1.0). Oracle calls `product.template.message_post(body='<p>Great product</p>', rating_value=4, message_type='comment', subtype_xmlid='mail.mt_comment')` via `/web/dataset/call_kw`, which routes through the `rating.mail_thread` override to create a linked `rating.rating` + `mail.message` pair. |
| **Browser-Use** | PASS (F1=1.0, 76.3s single-shot, 5/5 atomic edits matched, 0 postcondition failures, 43 API calls, 26 non-forbidden writes, 0 forbidden, StrictClean=True). BU clicked the product card → logged in → re-navigated to the product → expanded **Customer Reviews** accordion → typed `Great product` into the composer textarea (4-star default already selected) → clicked **Send**. The composer posts via `/mail/message/post` with `post_data.rating_value=4`, hitting the same server override as the oracle. |
| **F1** | 1.0 (BU), 1.0 (oracle) |
| **Odoo modules** | `website_sale` (in base snapshot) + auto-install chain `rating` + `portal_rating`. Requires **activating** the `website_sale.product_comment` ir.ui.view (ships with `active=False`) in the seed. |
| **Workflow** | Seed: (a) activate `ir.ui.view` with `key='website_sale.product_comment'` (search with `active_test=False` to catch archived copies) so the `<t t-call="portal.message_thread">` block renders at the bottom of the product page; (b) create `product.template` **Bench Review Item** with `is_published=True`, `website_published=True`, `sale_ok=True`, `list_price=49.0`, cleared taxes. Agent: `/shop` → click **Bench Review Item** card → scroll to bottom → click the **Customer Reviews** chevron toggle → composer surfaces inline with 5 star icons (default 4 filled) and a message textarea → type `Great product` → click **Send** (aria-label=Send). Server fires the `rating.mail_thread.message_post` override: pulls `rating_value=4` out of kwargs → creates `rating.rating(res_model='product.template', res_id=<tmpl>, rating=4.0, partner_id=admin.partner_id, consumed=True)` → runs `_message_post_after_hook` to back-link the new `mail.message.rating_id` and `rating.message_id`. End state: 1 rating.rating row + 1 mail.message comment on the product. |
| **Capability tested** | **Frontend portal review form** — the rating stars + message composer live on the public shop page, NOT in the backend product form. The agent must (a) find the collapsed `Customer Reviews` section (chevron toggle), (b) work the composer inline rather than via a modal dialog (Odoo 19 renders the rating composer inline inside the accordion when logged in — the `RatingPopupComposer` widget is only used with `.o_rating_popup_composer` sections that have `display_composer=True` via a different snippet). Also exercises the `rating.mail_thread` message_post override which silently branches on `rating_value` in kwargs. Distinct from row 381 `website_customer.publish_customer_reference_on_public_page` which publishes a pre-existing reference; row 485 creates a brand-new rating+comment pair. |
| **Notes** | **Calibration MISS — BU PASSED single-shot** at F1=1.0 in 11 steps / 76.3s (1 sample). Stated risk was **medium** (calibration risk MEDIUM per backlog). BU passed because (a) the default `ratingValue=4` in `Composer.portalState` (see `addons/portal_rating/static/src/chatter/frontend/composer_patch.js:9`) exactly matches the required rating — zero star clicks needed, (b) the composer textarea is discoverable by visual scan ("Great product" is unambiguous), (c) the **Send** button has `aria-label='Send'` making it aria-discoverable, (d) no modal; composer is inline inside the expanded accordion. Kept as medium/tier-2 — the task is realistic and exercises a distinct capability (frontend rating + chatter write). **To harden to hard**: (1) require a non-default rating (e.g. 2 stars) — the composer default-4 trap no longer saves the agent; (2) require posting a review on product B among 3 seeded products; (3) require editing the review afterward (triggers `force_submit_url='/mail/message/update_content'` path on the composer); (4) require unfolding 2+ collapsed sections (e.g. Specifications + Reviews) where both use the same chevron pattern. **Cookbook data points (new)**: (1) **`website_sale.product_comment` view ships with `active=False`** and MUST be flipped in the seed (`env['ir.ui.view'].with_context(active_test=False).search([('key','=','website_sale.product_comment')]).write({'active': True})`) — without this the `<section id="o_product_page_reviews">` block is never rendered and the task is unsolvable via browser. (2) **The inline review composer is the `@mail/core/common/composer` Owl component patched by `portal_rating/static/src/chatter/frontend/composer_patch.js`**, NOT the `.o_portal_chatter_composer` interaction. It exposes 5 `<i class="fa fa-star">` icons with numeric `index` attributes and uses `portalState.ratingValue` (default 4) to drive the `rating_value` field on post_data. The agent clicks stars by hovering + click; `onClickStar` writes `portalState.ratingValue = index+1`. (3) **`/mail/message/post` with `rating_value` is the canonical submit path** — it reaches `rating.mail_thread.message_post` which creates a `rating.rating` (`consumed=True`, `partner_id=env.user.partner_id`) and `_message_post_after_hook` links `rating.message_id = message.id` + `message.rating_id = rating.id` (bidirectional). (4) **Oracle via `product.template.message_post(rating_value=4, ...)`** is equivalent to the UI path and produces the identical 5-edit diff: `rating.rating` create with `{rating, res_model, res_name, partner_id, consumed}`. `res_id` is in `ignore_fields` (unstable int) — match_key uses `(res_model, res_name, partner_id)` which normalizes to `("product.template", "Bench Review Item", "Mitchell Admin")`. (5) **No karma gate** on product reviews (unlike forum upvote/accept) — admin can post directly; the `reviewer_bob` portal user from the backlog spec is optional and was omitted since admin login works and `rating.rating.partner_id` normalizes to `Mitchell Admin` either way. (6) **Pre-flight: `product.template._inherit` includes `'rating.mixin'`** (confirmed in `addons/website_sale/models/product_template.py:36`), so `rating_ids` + `rating_count` + `rating_avg` + the `message_post(rating_value=...)` override are all available. `portal_rating` is auto-installed with `website_sale`. **Commit**: `[ADD] benchmark: website_sale.add_product_review_publish (medium)`. |
