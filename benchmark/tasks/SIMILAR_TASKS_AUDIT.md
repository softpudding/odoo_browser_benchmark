# Similar-Tasks Audit

Clustering of near-duplicate tasks in the benchmark. Based on reading task names
for all 431 task directories (424 in `STATUS.md`) and spot-verifying 20 prompts
covering the tightest candidates.

- **Tier S** — truly identical flow, only fixture names/values differ
- **Tier A** — near-duplicate, but one task adds a step/field/sub-feature
- **Tier B** — by-design field-parallel tasks (same action across different fields)
- **Tier C** — broader thematic clusters (same module/flow, distinct sub-features)

## Headline

| Tier | Clusters | Tasks | Droppable |
|------|----------|-------|-----------|
| **S (truly identical)** | **8** | **16** | **8** |
| A (near-dup, meaningful variation) | ~10 | ~24 | ~14 |
| B (by-design parallel) | 3 | 12 | 0–10 (depends on goal) |

If the goal is to prune redundancy with zero loss of behavioral coverage,
**drop one task from each Tier S pair** — 8 deletions.

## Tier S — Truly identical

All verified by reading both prompts. In each pair the steps, field sets, and
assertions match exactly.

| # | Cluster | Tasks | What differs |
|---|---------|-------|--------------|
| 1 | Fleet: create vehicle + log odometer | `fleet.add_vehicle_log_odometer`, `fleet.register_vehicle_log_odometer` | Plate (`FLEET-ADD-01` vs `BENCH-001`), date, reading value |
| 2 | Putaway rule per product → sublocation | `stock.create_putaway_rule`, `stock.create_putaway_rule_for_product` | Product name, sublocation name |
| 3 | Add one IBAN to company contact via Invoicing tab | `contacts.add_bank_account_iban`, `contacts.add_bank_account_to_partner` | Partner name, IBAN value |
| 4 | Open product → set price + website description → publish | `website_sale.publish_product_set_price`, `website_sale.publish_shop_product` | Product name, price, description |
| 5 | Receive serial-tracked product via Detailed Operations | `stock.receive_serial_tracked_product`, `stock.receive_serial_tracked_product_two_serials` | N serials (3 vs 2) |
| 6 | Scrap component on in-progress MO via cog → Actions → Scrap, then Produce All | `mrp.scrap_component_during_partial_production`, `mrp.scrap_consumed_component_during_production` | Component name, qty (1 vs 2) |
| 7 | Create department + manager + reassign N employees | `hr.create_department_assign_manager_two_employees`, `hr.create_department_assign_manager_three_employees` | N employees (2 vs 3), names |
| 8 | Swap vehicle driver + edit Drivers History start date | `fleet.transfer_vehicle_new_driver`, `fleet.transfer_vehicle_between_drivers_log_history` | Vehicle plate, driver names, date |

**Tier S total: 8 clusters × 2 tasks = 16 tasks; 8 droppable.**

## Tier A — Near-duplicate but meaningfully different

| Cluster | Tasks | Key difference |
|---------|-------|----------------|
| Update RFQ note | `purchase.update_rfq_note` vs `purchase.update_rfq_note_quantity_confirm` | Second also changes qty + Confirms |
| Refuse leave | `hr_holidays.refuse_leave_request` vs `hr_holidays.refuse_leave_with_reason` | Second also posts chatter message with reason |
| Schedule interview | `hr_recruitment.schedule_interview_for_applicant` vs `hr_recruitment.new_applicant_schedule_interview` | Second also creates the applicant first |
| Produce MO | `mrp.produce_and_close_mo` vs `mrp.confirm_produce_close_mo` | Second also clicks Confirm (draft → confirmed) |
| Scrap with reason tag | `mrp.scrap_component_during_production` vs the 2 Tier-S scrap tasks | This one adds `Defective batch` reason tag + explicit source location |
| Publish product (no description) | `website_sale.publish_product_shop` vs the 2 Tier-S publish tasks | This one skips the description field |
| Create company + supplier tag | `contacts.create_company_add_supplier_tag` vs `contacts.create_company_set_supplier_tag` vs `contacts.create_company_add_supplier_finance_tags` vs `contacts.update_company_with_supplier_tag` | Differ by address-field set, #tags, and create-vs-update |
| Convert lead → opportunity | `crm.convert_lead_to_opportunity_simple` vs `crm.duplicate_lead_convert_to_opportunity` | Second duplicates the lead first and creates a new customer on-the-fly |
| Cancel confirmed SO | `sale.cancel_confirmed_order_restore_draft` vs `sale.cancel_confirmed_recreate_send_email` vs `sale.cancel_reissue_wrong_customer` | Differ by follow-up: restore draft / recreate + email / reissue with new customer |
| Mark opportunity won | `crm.mark_opportunity_won_update_revenue` vs `crm.update_opportunity_revenue_priority_won` vs `crm.assign_lead_salesperson_change_stage_won` | Differ by the extra field touched (revenue / priority / salesperson) |

**Tier A total: ~24 tasks in ~10 clusters; ~14 could be dropped without losing distinct coverage.**

## Tier B — By-design field-parallel

Same action repeated across different fields. Likely intentional if you want to
measure field-handling consistency; otherwise collapse to one representative per
group.

- `contacts.update_contact_{email, mobile, phone, website}` — 4 tasks
- `hr.update_employee_{department, job_title, mobile, work_email, work_phone}` — 5 tasks
- `crm.update_lead_{email, phone}` + `crm.update_opportunity_revenue` — 3 tasks

## Tier C — Thematic clusters

Not redundancy, but worth knowing when describing coverage. Counts are
approximate (by name inspection only).

| Theme | Approx count |
|-------|--------------|
| Calendar create event (recurring / all-day / attendee / description / video / organizers) | 10 |
| Create/update RFQ (add line, deadline, note, source, reference, quantity, vendor…) | 10 |
| Duplicate / cancel / update quotation | 10 |
| Account invoice / credit note / refund / post | 12 |
| HR holidays request/approve/refuse/allocate | 15 |
| HR expense create/submit/approve/refuse/post | 12 |
| CRM lead/opportunity create/convert/update/won/lost | 15 |
| MRP produce MO + scrap + unbuild + BoM | 18 |
| Stock receive / transfer / scrap / adjust / putaway | 20 |
| Website page / menu / snippet / blog / contact form | 15 |
| Website sale product publish / cart / checkout / promo | 15 |

## Method

1. Listed all 431 task directory names under `benchmark/tasks/`.
2. Grouped by `<module>.<verb>_<object>` patterns to surface near-name-duplicates.
3. For the 8 tightest candidate clusters, read both `prompt.md` files and
   checked whether the steps, field sets, and assertions are isomorphic.
4. Classified verified pairs into Tier S (identical) vs Tier A (meaningful
   variation); left unverified candidates in Tier A/C with the caveat that
   they are name-inferred.

Tasks read during verification (Tier S confirmations and Tier A demotions):

- `fleet.{add,register,create}_vehicle_log_odometer`
- `fleet.transfer_vehicle_{new_driver, between_drivers_log_history}`
- `stock.create_putaway_rule{,_for_product}`
- `stock.receive_serial_tracked_product{,_two_serials}`
- `contacts.add_bank_account_{iban, to_partner}`
- `contacts.create_company_{add_supplier_tag, set_supplier_tag}`
- `website_sale.{publish_product_set_price, publish_shop_product, publish_product_shop}`
- `mrp.{produce_and_close_mo, confirm_produce_close_mo, create_mo_consume_produce_done}`
- `mrp.scrap_component_{during_production, during_partial_production, consumed_component_during_production}`
- `mrp.unbuild_{finished_goods_to_recover_components, product_back_to_components}`
- `hr.create_department_assign_manager_{two,three}_employees`
- `hr_holidays.refuse_leave_{request, with_reason}`
- `hr_recruitment.{schedule_interview_for_applicant, new_applicant_schedule_interview}`
- `purchase.update_rfq_{note, note_quantity_confirm}`
- `crm.{convert_lead_to_opportunity_simple, duplicate_lead_convert_to_opportunity}`
