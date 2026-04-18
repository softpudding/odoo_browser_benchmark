ROW: 384
TASK_ID: lunch.create_vendor_product_order_for_today
DIFFICULTY: medium
SUMMARY: Install the Lunch module, create lunch.supplier 'Bench Cafe' (delivery=Delivery, all-week) + lunch.product 'Veggie Wrap' @ 8.00 EUR, then submit a lunch.order for today via the kiosk-style /odoo/lunch dashboard.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## lunch.create_vendor_product_order_for_today

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Lunch (installed on demand; not in base snapshot) |
| **Workflow** | Open Lunch -> Configuration -> Vendors -> New; pick partner, type vendor name (renames partner via related field), set Delivery selection, flip Sat/Sun checkboxes on the week_days widget, Save. Then Configuration -> Products -> New; name + Sandwich category + Bench Cafe vendor + price 8.00, Save. Navigate `/odoo/lunch`, click the Veggie Wrap kanban card to open the kiosk order modal, fill Notes="no onions", click Add To Cart, then click Order Now in the sidebar to move state from `new` -> `ordered`. |
| **Capability tested** | Navigating Odoo's non-standard Lunch kiosk UI: LunchDashboard sidebar RPCs, LunchKanbanRecord onGlobalClick -> modal form, `footer` Add To Cart vs sidebar Order Now two-step submission. Selection SelectMenu widget + week_days table widget + related-field partner/name rewrite order all bite calibration. |
| **Notes** | Oracle single-shot PASS 48s, 13/13 atomic edits. BU created THREE duplicate `lunch.supplier` rows (retry loop on the SelectMenu delivery dropdown) and never reached the product step. Key quirks: `lunch.supplier` (model name is `lunch.supplier` NOT `lunch.vendor` as older Odoo docs suggest); vendor `name` is `related='partner_id.name', readonly=False` so picking an existing partner clobbers whatever was typed - must pick partner FIRST then re-type name; `delivery` Selection renders via `o_select_menu` (not native `<select>`) so `set_selection` helper times out; Add To Cart button in the kiosk order modal is `invisible="order_deadline_passed or not display_add_button"` - order_deadline_passed fires when the supplier has the weekday flag off for today, so Mon-Fri defaults break weekend tests; `display_add_button` gates on `get_wallet_balance >= order.price` which includes `res.company.lunch_minimum_threshold` - seed must bump that >= product price or the button silently hides. Admin's lunch location (`last_lunch_location_id`) must be pre-populated; without it LunchKanbanRenderer returns [] from getGroupsOrRecords and the kanban is empty. |
