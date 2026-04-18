# Lunch module cookbook (Odoo 19)

## Model naming

- The vendor model is `lunch.supplier` (NOT `lunch.vendor`, which does
  not exist).  The UI label is "Vendor" but all field refs use
  `supplier_id` / `supplier_*`.
- `lunch` is NOT in `benchmark/base_modules.txt` -- seed must
  `button_immediate_install()` it.  Admin is auto-added to
  `lunch.group_lunch_manager` by the module's security data, so
  Configuration menus render after install without extra ACL tweaks.

## `lunch.supplier` form field gotchas

- `name = fields.Char(related='partner_id.name', readonly=False)`.
  Picking an existing partner from the `partner_id` autocomplete
  writes the partner's name into the `name` field, clobbering
  whatever was typed earlier.  Typing into `name` writes BACK to the
  partner (renaming it).  Oracle/human flow must PICK PARTNER FIRST,
  then type the vendor name.  Seed cleanup should handle BOTH the
  seeded partner name and the final vendor name when releasing the
  partner record.
- `delivery` Selection `[('delivery','Delivery'),('no_delivery','No Delivery')]`
  renders via Odoo 19's `o_select_menu` custom widget (not a native
  HTML `<select>`).  The oracle helper `set_selection` (which calls
  `select_option`) times out.  Working pattern:
  ```python
  page.locator(".o_field_widget[name='delivery'] .o_select_menu_toggler").click()
  page.locator(".o_select_menu_menu .o_select_menu_item:has-text('Delivery')").click()
  ```
- The weekday availability widget is `widget="week_days"`
  (`addons/web/static/src/views/widgets/week_days/`).  It renders a
  2-row `<table>` -- row 1 = Mon/Tue/.../Sun `<th>` headers, row 2 =
  `<CheckBox>` components without `name` attributes.  Toggle by
  matching header text to a column index, then click the checkbox in
  the same column of row 2.
- Default availability is Mon-Fri only; Sat/Sun are False.  If the
  test runs on a weekend (admin tz-dependent) the supplier is
  `available_today=False` and the Add To Cart button is hidden.
  Tasks that require "order for today" must instruct the agent to
  enable all 7 days, OR pin the test date.

## `lunch.order` kiosk modal (`/odoo/lunch`)

- `/odoo/lunch` opens the `lunch_product_action_order` kanban with a
  side-bar `LunchDashboard` Owl component.
  `LunchKanbanRenderer.getGroupsOrRecords` returns `[]` when
  `searchModel.lunchState.locationId` is falsy.  Locations are
  populated via the `/lunch/infos` RPC at mount, which returns
  `user_location = user.last_lunch_location_id` (falls back to
  `lunch.location.search([], limit=1)`).  Seed SHOULD set
  `admin.last_lunch_location_id` to the seeded `HQ Office` location
  to avoid a race where the dashboard renders before the fallback
  resolves.
- Clicking a product kanban card triggers `LunchKanbanRecord.
  onGlobalClick` -> bus event `lunch_open_order` ->
  `LunchRendererMixin.openOrderLine` which does
  `action.doAction({res_model: 'lunch.order', views: [[false, 'form']], target: 'new', context: {default_product_id: ...}})`.
  The resulting dialog is a standard `.o_dialog` wrapping the
  `lunch.order` form view.  Select with
  `.o_dialog:has(.o_form_view)`.
- Inside the dialog, the `Add To Cart` footer button has
  `invisible="order_deadline_passed or not display_add_button"`.
  BOTH conditions are computed at form-new time:
  - `order_deadline_passed` for a `new` record with `date=today` and
    `send_by='phone'` supplier = `not supplier.available_today` =
    `not supplier[WEEKDAY_TO_NAME[today.weekday()]]`.
  - `display_add_button` = `get_wallet_balance(user) >= price`.
    `get_wallet_balance` returns
    `sum(cashmoves) + company.lunch_minimum_threshold`.  Seed must
    set `res.company.lunch_minimum_threshold >= product.price` so
    the button is visible without requiring the agent to top up a
    wallet.
- `add_to_cart` is a **no-op** Python method that returns True.  The
  record is actually created by the form controller's `web_save`
  BEFORE the object method runs.  State at creation = `new`.
- Closing the dialog fires the bus event `lunch_update_dashboard`
  which re-fetches `/lunch/infos`.  The sidebar then shows the
  pending line and the "Order Now" button.
- "Order Now" is an Owl button bound to `LunchDashboard.orderNow`
  which POSTs to `/lunch/pay`.  The controller calls
  `action_order()` on all `state='new'` lines for the current user
  today, transitioning to `state='ordered'`.  **This is the only
  state-transition step** -- forgetting it leaves the order at
  `new` and fails the postcondition.

## Other

- `lunch.product.supplier_id` renders as the supplier's
  `display_name` in the state-diff engine.  Supplier display_name
  computes to `"{name} {phone}"` when phone is set (see
  `_compute_display_name` on `lunch.supplier`).  If the task pins a
  phone ("+1 555 0199"), expected_state must encode
  `"Bench Cafe +1 555 0199"`, not just `"Bench Cafe"`.
- `fields.Date.context_today(admin)` can differ from the UTC date by
  1 day depending on admin's timezone (default seed admin tz =
  `Asia/Singapore`, +8h from UTC).  check.py should accept `today`,
  `today-1d`, `today+1d` as valid `lunch.order.date` candidates.
