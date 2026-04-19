# Odoo 19 patterns and gotchas — for benchmark task builders

**Read this BEFORE writing seed.py, oracle.py, or check.py.** It encodes quirks
empirically discovered across 20+ benchmark tasks. Saves rediscovery time and
avoids known bugs.

As you discover new quirks in your task, **append them here** (be terse).

---

## Module install status in base snapshot

The base snapshot is built from `benchmark/base_modules.txt`. Some bridge
modules require additional modules that are NOT in the base:

| Feature | Required module | In base snapshot? |
|---------|----------------|-------------------|
| `service_policy='delivered_timesheet'` | `sale_timesheet`, `hr_timesheet` | **No** — seed must `button_immediate_install` or abort |
| `service_policy='delivered_milestones'` | `sale_project`, `project` | Yes (project.milestone model exists) |
| Dropship route | `stock_dropshipping` | **No** — seed must `button_immediate_install` |
| Replenishment dashboard | `stock`, `purchase_stock` | Yes; lives at `/odoo/replenishment` |
| Survey | `survey` | Yes (after early-batch installs) |
| Maintenance | `maintenance` | Yes (after early-batch installs) |
| Alternative RFQs / Compare Product Lines | `purchase_requisition` | **No** — seed must `button_immediate_install`; also grant admin `purchase_requisition.group_purchase_alternatives` so the **Alternatives** tab and **Create Alternative** button become visible on `purchase.order` form |

Pattern to install on demand (see `survey.create_feedback_survey_with_sections/seed.py`):

```python
mod = env["ir.module.module"].search([("name", "=", "stock_dropshipping")])
if mod and mod.state != "installed":
    mod.button_immediate_install()
```

---

## Field name surprises (Odoo 19)

### Common fields that were renamed

- `tax_ids` not `tax_id` on `sale.order.line` and `account.move.line`
- `group_ids` not `groups_id` on `res.users`
- `memo` not `ref` on `account.payment`
- `product_qty` not `quantity` on `purchase.order.line`

### Feature-specific field names

- `slide.question.question` (Char) — **not** `name` or `title`
- `slide.answer.text_value` — **not** `value` or `name`; has `is_correct` Boolean
- `mailing.mailing.mailing_model_name` must be set alongside `mailing_model_id`
- `mailing.mailing.email_from` is required (DB constraint) — set on JSON-RPC create
- `maintenance.equipment.expected_mtbf` (writable) replaces the removed `period` field
- `maintenance.equipment.mtbf` is computed/readonly — do not write to it
- `blog.post.published_date` is the storage field; `post_date` is computed with an inverse
- `blog.post.author_id` is a Many2one on `res.partner`, not `res.users`

### Event / event_sale / event_track

- `event.track` publish: the backend form's "Go to Website" button (widget
  `website_redirect_button`) ONLY navigates — it does NOT toggle `is_published`.
  Canonical publish path is to move `stage_id` to one with
  `is_fully_accessible=True` (default data: the "Published" stage at
  sequence 4); the `_synchronize_with_stage` hook flips `is_published=True`
  as a side-effect.
- `website_event` and `website_event_track` are NOT in the base snapshot;
  seed must `button_immediate_install` both before touching `event.track`.
- `event.event.event_ticket_ids` auto-materializes a default "Registration" ticket on create
- `event_sale` is auto-installed when both `event` and `sale` are present; no manual install
- Invoicing a paid registration goes through the Sales app (SO → event configurator wizard)
- The attendee-details wizard pre-fills name/email from the partner; non-default override needed
  if the attendee differs from the buyer
- The `event_configurator` wizard fires on `sale.order.line.product_template_id` onchange iff
  the picked product has `event_ok=True` (computed from `service_tracking='event'`). Inside the
  modal, both `event_id` and `event_ticket_id` are required m2o fields — the OK footer button is
  enabled only when both are set. In oracles, use
  `modal.locator(".o_field_widget[name='event_id'] input").fill(...)` / dropdown click, then the
  same for `event_ticket_id`, then click the primary footer button. No save on the parent SO
  happens inside the wizard; the wizard just writes the two fields back onto the SO line.
- Seeding both a paid ticket and the auto-default `Registration for …` placeholder on
  `event.event.event_ticket_ids` in the same `create()` suppresses the auto-materialisation,
  keeping the post-run diff clean of phantom ticket rows.
- `event.registration.state` defaults to `'open'` (Registered), so saving a new attendee
  immediately fires `_check_seats_availability` — but only if `event_ticket_id` is set
  (a ticketless registration is unconstrained). Browser-use frequently leaves
  `event_ticket_id` blank on the registration form (it's not required), which silently
  bypasses any `seats_max` cap. Tasks that test seat-limit enforcement must validate
  that the registration is linked to the right ticket in `check.py` — relying on the
  ValidationError firing alone is not enough.
- The seat-limit ValidationError raised by `_check_seats_availability` shows up as a
  modal dialog with title "Validation Error" and body containing "There are not enough
  seats available for &lt;Event Name&gt;". Oracle scripts can detect it by selector
  `.modal:visible .modal-body:has-text('not enough seats')`.
- `event.event.is_published` in the backend form uses `website_redirect_button` widget
  (**navigation only**, NOT a toggle). The inline `website_publish_button` "Publish" link
  in the right-hand Event Details group is hidden by default because
  `website_visibility` defaults to `'public'` and the button is
  `invisible="website_published or website_visibility == 'public'"`. Canonical publish
  paths: (a) JSON-RPC `event.event.website_publish_button()` — oracles use this for
  determinism; (b) navigate to frontend preview and click the Owl systray
  `Unpublished/Published` toggle (fragile under Playwright). Unlike `event.track`, there
  is no stage-bar publish on `event.event`.
- Public portal registration is a **two-modal chain**: `#modal_ticket_registration`
  (Bootstrap, opened via `data-bs-toggle` from event page) contains a ticket counter
  (default 1 for single-ticket events) and a `.a-submit` button whose click handler JSON-
  RPCs `/event/<slug>/registration/new` and **inserts** the returned HTML into
  `document.body` as `#modal_attendees_registration`. Attendee inputs are named
  `{registration_index}-{question_type}-{question_id}` (e.g. `1-name-1`, `1-email-2`).
  Match via substring `name*='-name-'`, NOT suffix `name$='-name'` — the suffix is the
  numeric question id. Submit to `/registration/confirm` navigates to a success page.
- `event.registration.create` in the portal flow is called via `sudo()` inside the
  `/registration/confirm` controller AND the route carries the event slug in
  canonical_op (`custom:/event/<slug>/registration/confirm`). Neither form matches a
  static `required_ops` entry — leave `required_ops: []` and rely on state diff +
  `check.py` for portal-registration tasks.
- New `event.event` records with no `event_type_id` auto-attach the three
  `is_default=True` questions (Name mandatory / Email mandatory / Phone optional) via
  `_compute_question_ids` fallback — no seed work needed for the portal form to render.
- `event.event.question_ids` is a **Many2many** (with `_compute_question_ids`
  inverse, `readonly=False`, `store=True`). The Questions tab renders it with a
  plain `<list>` (NOT `editable`) so clicking **Add a line** opens a `SelectCreate`
  m2m selector dialog. Inside, click **New** to surface the `event.question` form
  (`event_question_view_form`). The form has radio `question_type`, nested notebook
  **Answers** tab (invisible unless `question_type='simple_choice'`) with an inline-
  editable one2many on `answer_ids`. **Save & New** chains to the next question;
  **Save & Close** returns to the event form. BU handles this composite flow
  cleanly single-shot (~19 steps) when the prompt names the radio labels ("Text
  Input" / "Selection") and the checkbox labels ("Mandatory" / "Once per Order") —
  the backend form's label text is unambiguous.
- `event.question.question_type` values: `simple_choice` (label "Selection"),
  `text_box` (label "Text Input"), `name`, `email`, `phone`, `company_name`. Tasks
  that ask for a "textbox" field must use `text_box`, NOT `textbox` — the
  underscore matters and check.py string-equality will silently miss the typo.
- `event.question.once_per_order` / `is_mandatory_answer` booleans normalize to
  `null` (not `false`) on the state diff engine's create path when False. Tasks
  asserting `once_per_order=False` in `expected_state.json` must use
  `"norm_value": null` to hit F1=1.0 — same gotcha as other boolean fields across
  the benchmark. Validate via `check.py` for the True-vs-False distinction.
- `event.event.website_publish_button()` (from `website.published.mixin`) is the
  canonical method the Owl systray Published toggle calls. Writing
  `is_published=True` directly ALSO flips `website_published=True` via the
  `_inverse_is_published` hook; JSON-RPC oracles often do both for safety.

### Fleet

- `fleet.vehicle.write({'driver_id': ...})` auto-creates a `fleet.vehicle.assignation.log`
  entry with `date_start = fields.Date.today()`. If your test needs a specific `date_start`,
  do NOT pick today's date (date coincidence makes the task easier than intended)
- `fleet.vehicle.log.services.odometer` is a **computed Float with an inverse**
  (`_set_odometer`) that creates a `fleet.vehicle.odometer` row linked to the same
  vehicle with `value = odometer` and `date = log.date or today()`. Filling the
  Odometer Value field on the service form is sufficient to satisfy an "add an
  odometer reading" step — no separate Odometers-list navigation needed. Guard:
  `create()` drops `odometer=0` from vals (so zero-value fills silently no-op).
- `fleet.vehicle.log.services.state` is a **clickable statusbar** (values
  `new / running / done / cancelled`, `widget="statusbar"`
  `options="{'clickable': '1'}"`). Click target is
  `.o_statusbar_status button.o_arrow_button:has-text('Done')` — no
  confirmation dialog, click persists immediately. `state` IS the stage
  (there is no `stage_id`).
- `fleet.vehicle.log.services.currency_id` is `related='company_id.currency_id'`
  (readonly). To make the Cost monetary widget render with EUR (or any other
  currency), seed must flip `env.company.currency_id` to the target currency
  and activate the currency record if `active=False` (the default for
  non-USD currencies in a fresh base snapshot).
- **Browser-use decimal-separator trap on fleet numeric fields**: typing
  a thousands-separator value like `25,000` into the Odometer Value
  Float input makes Owl's numeric parser treat the comma as a decimal
  point, resulting in `value = 0.0025` — and BU often **retries 3+ times**,
  spawning phantom `fleet.vehicle.odometer` rows at 0.0025 each. Tasks
  that want this as a calibration trap should phrase the prompt with a
  bare-numeric value (`25000`) and enforce row-count in `check.py`.

### Purchase / purchase_requisition

- `res.groups` field is `user_ids` (Many2many), NOT `users` — writing
  `grp.users = [(4, admin.id)]` raises `AttributeError`.  Use
  `grp.user_ids = [(4, admin.id)]`.
- `Create Alternative` wizard copies `origin` from the source PO onto every
  alternative.  After running the wizard twice, list rows are ambiguous when
  searching by `origin` — search by partner name instead.
- `Compare Product Lines` opens `purchase_order_line_compare_tree` with
  `search_default_groupby_product=True`.  The group starts **collapsed**
  (`tr.o_group_header.o_group_has_content`) regardless of `expand="1"` on
  the view.  Click the group header row before trying to locate `.o_data_row`
  — Playwright `.o_data_row` queries return 0 until the group is expanded.
- `purchase.order.button_confirm` raises the
  `purchase.requisition.alternative.warning` wizard when the PO has any
  draft/sent/to-approve alternatives.  The two actionable branches are
  `action_cancel_alternatives` and `action_keep_alternatives`; there is no
  "default" — agents must explicitly pick the non-default branch to cancel
  rivals.
- **`purchase.order` form has NO "Create Bill" status-bar button in
  Odoo 19 Community.** The `action_create_invoice` button lives ONLY on
  the Purchase Orders **list view** header (`<button
  name="action_create_invoice" string="Create Bills"/>`, note plural),
  visible after selecting one or more PO rows via checkbox. The PO form
  header only has Send RFQ / Confirm Order / Cancel / Lock buttons plus
  the `Upload Bill` widget (which attaches a PDF to a generated bill).
  Tasks that say "click Create Bill on the PO" must route the agent
  through `/odoo/purchase-orders` → checkbox-select → Create Bills. With
  exactly one selected PO, `action_view_invoice` redirects straight to
  the created bill's form view.
- **`purchase.order.action_create_invoice` + "just-opened bill form" =
  clean Owl state (Save button disabled).** After the redirect to
  `/odoo/purchase-orders/bills/<id>`, a plain `fill_field("ref",...)`
  does NOT dirty the form — the Save button stays disabled, and
  `button[name='action_post']` ("Confirm") clicks silently no-op. Two
  workarounds validated in oracle runs: (1) set a different field FIRST
  via the date picker (e.g. `set_date("invoice_date", ...)`) which
  transitions the form into edit mode, THEN `fill_field("ref", ...)`
  persists, or (2) re-navigate to `/odoo/bills/<id>` via a fresh action
  to force a clean form open. Agents that just type into the ref input
  and hit Confirm will see no state change.

### Stock

- `stock.picking` line editing: "Done" qty is an inline-cell edit — notoriously hard to persist
  via browser UI (cell doesn't always save on blur). Good hard pattern.
- Backorder dialog: "Create Backorder" is the **default/primary** button in Odoo 19
  (used to be non-default in older versions). Flip the task design accordingly.
- Dropship picking has a different `picking_type_id` from regular customer delivery;
  smart button is labeled "Dropship", not "Receipt"
- `stock.picking.origin` inherits from `sale.order.name`, NOT `client_order_ref`.
  If you want a deterministic `origin` for state-diff entity_key matching, pin
  `sale.order.name` in seed (e.g. `"name": "S-BENCH-DLV-002"`).
- Oracle JSON-RPC `button_validate` on a Ready picking with no `move.picked`/`move.quantity`
  returns a wizard action. Cleanest oracle pattern: write `move.quantity = product_uom_qty`
  and `move.picked = True` on every move, then call `button_validate` with
  `context: {skip_backorder: True}`.

### Delivery / shipping providers (`stock_delivery`)

- Base snapshot only has two providers: `fixed` and `base_on_rule`. Both
  `fixed_send_shipping` and `base_on_rule_send_shipping` return
  `tracking_number: False` — there is NO auto-generated carrier_tracking_ref
  for the built-in providers. Tasks that need a tracking ref must have the
  agent **type it manually** into the `carrier_tracking_ref` field.
- The form-header "Send to Shipper" and "Print Return Label" buttons are
  hidden (`invisible`) for `delivery_type in ['fixed', 'base_on_rule']`.
  The generic "Print" header button (present on any done picking) opens the
  delivery-slip report — use it as the "trigger a PDF" step.
- `delivery.carrier` requires a `product_id` (service product). Use the
  create-and-edit autocomplete shortcut in the UI; in JSON-RPC / seed, create
  a `product.product` with `type='service'` first.
- After validating an original picking with backorder, agents often click
  "Return" instead of opening the existing backorder. The backorder is
  reachable via SO breadcrumb → Delivery smart button (now shows count = 2).
- A reservation-reducing edit (e.g., Done 5→0 on an `assigned` backorder) flips
  `stock.picking.state` from `assigned` back to `confirmed` because reserved
  stock is released. expected_state.json must encode `confirmed`, not `assigned`.
- To force the inline-cell Done-edit pattern on a partial delivery: seed the
  partial product with **enough stock for the full demand** so the original
  picking auto-reserves the full quantity — the agent must MANUALLY decrease
  Done before validating to trigger the backorder split. Seeding only the
  partial amount (e.g., 3 of 8) makes Done auto-fill to the partial amount,
  removing the cell-edit step entirely.
- **Detailed Operations popup (`action_show_details` on a move row).** The
  "Details" button in the Operations list is gated by
  `stock.move.show_details_visible`, which is True only when (i) the user
  has `stock.group_stock_multi_locations` / `group_tracking_lot` /
  `group_tracking_owner`, (ii) `len(move_line_ids) > 1`, OR (iii) the
  product has non-`none` tracking (lot/serial). For a single-move / single
  move_line / untracked task, seed **must grant
  `stock.group_stock_multi_locations` to admin** or the Details button is
  absent. The button launches a secondary `stock.move` form dialog
  (`stock.view_stock_move_operations`, target='new') containing an
  editable-bottom `move_line_ids` list (`stock.view_stock_move_line_operation_tree`)
  whose columns include `quantity` (Quantity). Editing the `quantity`
  cell + Tab + clicking the technical modal's footer Save button
  (label "Save & Close" or `.o_form_button_save` inside the dialog)
  is what persists. BU reliably types the new quantity but fails to
  persist it — the outer picking-form Save click gets intercepted by
  the still-open popup, and validating afterwards silently promotes
  the reserved full qty (so no backorder dialog ever appears). Oracle
  pattern: click the popup-footer Save first; if the modal is still
  visible, press Escape to force-close (editable-list x2m saves on
  close by default).
- **Reservation gating:** `stock.picking.action_confirm()` does NOT
  reserve stock when `picking_type_id.reservation_method` is the default
  `manual` — picking ends in state `confirmed`, NOT `assigned`. To force
  the agent through the Check Availability header button, seed with
  `action_confirm()` only; if the picking auto-reserves (some types
  default to `at_confirm`), call `picking.do_unreserve()` after
  confirmation. Skipping Check Availability in the UI triggers the
  Immediate Transfer wizard on Validate, NOT the Create Backorder
  dialog — a good hard-tier trap for partial-ship tasks.

### Website / website_sale

- `is_published` on products: the Sales-tab "Ecommerce Shop" toggle writes the value;
  the form-header "Go to Website" button only navigates, it does NOT toggle
- Webshop Products list defaults to kanban with `search_default_published=1` — must
  switch to list view AND clear filters to see archived / unpublished records
- After toggling `is_published` on the Sales tab, the form stays on that tab; if the
  next step is on a different tab (e.g., General for `default_code`), re-open it
- **Category filter on `/shop` is a URL PATH, not a query param.** Clicking a
  category sidebar link redirects to `/shop/category/<slug-id>` (see
  `website_sale.categorie_link` + `_get_shop_path` in
  `website_sale/controllers/main.py`). There is no "x on category facet" chip.
  Removing the category filter = clicking the **All Products** link at the top
  of the Categories sidebar, which navigates back to plain `/shop` while
  preserving existing query params (`min_price`, `max_price`, `tags`, etc.) via
  the Jinja `keep(...)` helper.
- **Price filter is a dual-handle multirange slider.** Rendered from
  `addons/website/static/lib/multirange/multirange_custom.js`; the `<input
  type="range" multiple="multiple" class="form-range range-with-input">`
  has **two hidden `<input type="number">` counters** inserted alongside the
  `$<value>` spans. Clicking the counter span toggles the number input
  visible; typing a value + Enter fires `newRangeValue`, which redirects to
  `?max_price=<value>`. Playwright drag-handle automation is fragile; the
  reliable oracle pattern is **direct URL navigation** (e.g.
  `page.goto("/shop/category/<id>?max_price=100")`).
- **`/shop/cart/add` is a `type='jsonrpc'`, `auth='public'` route**
  (`website_sale/controllers/cart.py`). Payload:
  `{product_template_id, product_id (variant_id), quantity, ...}`. Session
  cookie drives cart ownership: admin-logged = admin cart; no login = public-
  user cart. **Postcondition checks for public-shop tasks must find the cart
  by line content (product name), not by `partner_id`**, because a BU run
  that skips login will silently own the cart as the public user and a
  `partner_id=admin` filter will miss it.
- **`product.public.category` is the correct model name** for a website
  (eCommerce) product category — common backlog misspellings
  `website.sale.category` / `product.category.public` do not exist. The m2m
  on `product.template` is `public_categ_ids`.

### Website / website_sale_wishlist (heart icon + /shop/wishlist)

- **No share-by-email feature exists.** Odoo 19 Community
  `website_sale_wishlist` ships NO share controller, NO share template,
  NO share JS (`grep -rn "share" addons/website_sale_wishlist/` returns
  zero matches). Only routes exposed by `controllers/main.py` are
  `/shop/wishlist/add`, `/shop/wishlist`, `/shop/wishlist/remove/<id>`,
  `/shop/wishlist/get_product_ids`. Backlog rows that ask for "wishlist
  share via email" must be re-scoped to wishlist-persistence
  verification (product.wishlist row).
- **Heart button selectors.** On the product detail page the heart is
  `a.o_add_wishlist_dyn` (inside `#product_option_block`, rendered by
  `website_sale_wishlist.product_add_to_wishlist`). On `/shop` tiles and
  on `/shop/cart` "Save for Later" links, the class is
  `.o_add_wishlist` (with `<button>` and `<a>` variants). The JS handler
  (`AddProductToWishlistButton.addProduct`) binds to `.o_add_wishlist,
  .o_add_wishlist_dyn` — a single selector union covers both.
- **Wishlist row ownership depends on login.** `/shop/wishlist/add` is
  `auth='public'`. When the session is admin-logged-in,
  `ProductWishlist._add_to_wishlist` writes `partner_id=admin.partner_id.id`
  on the new row. When the session is anonymous, `partner_id=False` and
  the wishlist id is pushed into `request.session['wishlist_ids']` —
  the row is orphaned to the session cookie and `current()` filters it
  through the session. Tasks that verify wishlist persistence must
  either assert `partner_id` equals the expected user (deterministic
  only if the oracle/agent is logged in) OR accept partner_id=False +
  verify via `request.session`.
- **product.wishlist has a UNIQUE constraint** on `(product_id, partner_id)` —
  seeds that run twice must `cleanup()` the prior row before
  re-creating, or the seed will crash with `duplicate key value violates
  unique constraint "product_wishlist_product_unique_partner_id"`.
- **state_spec match_key for `product.wishlist`.** Use
  `match_key: [product_id]` — the diff engine normalizes the Many2one to
  the product's display_name. `partner_id` normalizes to the partner's
  display name (e.g. "Mitchell Admin" for the admin user in the base
  snapshot).

### Website / website_sale_stock (stock-availability banner)

- **`website_sale_stock` is NOT in the base snapshot**, and neither are its
  hard deps `sale_stock` and `stock_delivery`. It is marked
  `auto_install=True`, but auto-install only fires when ALL deps are
  already installed. Seed must walk the dep chain explicitly:
  ```python
  for mod_name in ("sale_stock", "stock_delivery", "website_sale_stock"):
      mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
      if mod and mod.state != "installed":
          mod.button_immediate_install()
  ```
- **The "X in stock" badge on the product page is the `threshold_message`
  block** (QWeb `website_sale_stock.product_availability`,
  `addons/website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml`).
  Render conditions: `is_storable=True` AND `show_availability=True` AND
  `free_qty > 0` AND `free_qty <= available_threshold`. Defaults are
  `show_availability=False` and `available_threshold=5.0`, so a seed that
  wants the banner visible at arbitrary qty must flip
  `show_availability=True` AND raise the threshold above the seeded
  on-hand qty.
- **`product.template.is_storable=True` is the Odoo-19 storable flag for a
  `type='consu'` product.** The legacy `type='product'` selection value is
  gone; a "storable" product is `type='consu' + is_storable=True`.
- **`/shop/cart/add` does NOT enforce the on-hand cap while
  `allow_out_of_stock_order=True` (the default).** Even if the banner
  advertises "5 Units in stock", a JSON-RPC POST of `quantity=999`
  succeeds. Tasks that want a hard UI cap must flip
  `allow_out_of_stock_order=False`; tasks that just need the banner
  rendered can keep the default.
- **BU is trivially good at product-detail quantity bump + Add-to-cart.**
  `input[name="add_qty"]` is directly adjacent to `#add_to_cart` — no
  modal, no dual-handle slider. Do NOT build a medium task around just
  the qty bump; combine with filter/category nav, optional-product
  upsell, or a cart-level edit to escalate.

### Loyalty / sale_loyalty / website_sale_loyalty

- `loyalty.program.program_type='loyalty'` (Loyalty Cards) **cannot be applied with a code** —
  `sale.order._try_apply_code` returns `{'error': "This program cannot be applied with code."}`
  for both `loyalty` and `ewallet`. For "apply at checkout via code" tasks use
  `program_type='promo_code'` (UI label "Discount Code") with `trigger='with_code'`.
- A `loyalty.program` cannot be `unlink`ed while `active=True` (`_unlink_except_active`
  guard). Cleanup must `write({'active': False})` before `unlink()`.
- Backend menu path is `/odoo/discount-loyalty` (action xmlid
  `loyalty.loyalty_program_discount_loyalty_action`). Domain hides gift_card and ewallet.
- Admin/internal users can have a website cart: `_get_and_cache_current_cart` will
  resurrect the abandoned draft `sale.order` matching `partner_id=admin.partner_id`
  + `website_id=current` + `state='draft'`. Seed accordingly to give the agent a
  pre-populated `/shop/cart`.
- Apply discount code from the website cart by POSTing to `/shop/pricelist?r=/shop/cart`
  with form fields `promo=<CODE>` and `csrf_token=<form token>`. The form is rendered
  by template `website_sale.coupon_form` (visible by default on `/shop/cart`).
- **`program_type='coupons'` vs `'promo_code'`**: both accept a code at
  checkout but store it differently. `'promo_code'` puts the code on
  the `loyalty.rule` itself (`rule.code='FOO'`, `trigger='with_code'`)
  and the SAME code redeems unlimited uses. `'coupons'` keeps the rule
  codeless and stores EACH redeemable code as an individual
  `loyalty.card` record (one-shot by default, `points=1` consumed per
  use). For "pre-generated coupon code list" tasks, seed the program
  with `program_type='coupons'`, `trigger='with_code'`, no `code` on
  the rule, then create `loyalty.card` rows with explicit `code` + 
  `points=1`. `sale.order._try_apply_code` will dispatch the
  customer-typed string to the `loyalty.card` branch (same path as
  gift cards).
- **Auto-attached delivery line on /shop/payment**: even when the
  checkout UI never surfaces a carrier picker, the base snapshot's
  published shipping method (`Delivery_007 Standard delivery`)
  attaches a zero-priced `sale.order.line` with `is_delivery=True` to
  the SO during `/shop/payment`. `check.py` for any completed-checkout
  task must filter `is_delivery` out of "unexpected extra product
  lines" assertions (alongside `is_reward_line`), or a PASS run will
  false-fail on the auto-attached line.
- **`state_spec` match_key for a post-checkout `sale.order`**: when
  the pre-task state has zero orders, a `match_key=[partner_id,
  amount_total]` resolves to `(null, <total>)` in the observed diff
  because the partner is not populated on create capture. The
  `expected_state.json` entity_key MUST mirror `[null, <total>]` with
  `op='create'` — using a name-based key gives F1=0 on an otherwise
  perfect run.

### Website / website_forum

- **`website_forum` is NOT in the base snapshot.** Seed must
  `button_immediate_install` the module before creating any forum / post
  (the `forum.forum` and `forum.post` models won't exist otherwise).
- **Frontend Accept-answer controller blocks self-accept unconditionally**
  (karma-independent). From
  `addons/website_forum/controllers/website_forum.py`:
  `def post_toggle_correct: if request.env.uid == post.create_uid.id:
  return {'error': 'own_post'}`. Any "agent posts an answer and then
  accepts it" task MUST seed a non-admin user to author the answer that
  should be accepted — admin cannot click Accept on their own post.
  Karma override does not help.
- **Karma is a non-issue for admin.** `forum.post._compute_post_karma_rights`
  branches on `self.env.is_admin()` first and sets `can_ask / can_answer /
  can_accept / can_edit / can_close / ... = True` regardless of the karma
  fields. So seeds don't need to write `admin.karma = ...` to unblock
  the frontend flow. The only guard that still fires on admin is the
  own-post block above.
- **Accept checkmark selector is `.o_wforum_validate_toggler`** (an `<a>`
  whose `data-href` posts to `/forum/<forum>/post/<answer>/toggle_correct`).
  The visible affordance is a small Font Awesome icon `i.fa-check-circle-o`
  (empty) / `i.fa-check-circle.text-success` (filled/accepted). BU reliably
  FAILS to find this selector — it is the natural calibration trap for any
  forum-acceptance task.
- **Answer textarea has `minlength="50"`** (see template `post_answer`):
  agent prompts must specify a long-enough answer body or the form will
  reject it client-side (`required` + `minlength` HTML attributes).
- **Forum `mode='questions'` caps answers at 1; `mode='discussions'`
  allows many.** If the task seeds two pre-existing answers for a single
  question so the agent has a "decoy" to avoid, use `mode='discussions'`.
- **`forum.post` match_key for state-diff:** use `[name, parent_id,
  create_uid]` — two seeded answers from the same user with the same
  `Re: <title>` name collide, so give distinct backend `name` values
  (the frontend renders only `content`, so `name` is safe to differentiate
  without leaking task structure).
- **`forum.post` create edits emit `is_correct=null` (not False)** — same
  null-vs-false quirk documented for `blog.post`. `expected_state.json`
  for a create must use `"norm_value": null` for `is_correct`, not
  `false`.
- **`forum.post.name` auto-prefix for answers:** the frontend controller
  sets `name = 'Re: %s' % post_parent.name` when posting via `/new`. In
  seed you can pick any name for the bot-authored answers; the frontend
  shows only `content` to users.
- **Tag `forum.tag.name` is scoped per-forum** (`forum_id` FK). Uniqueness
  constraint is `(name, forum_id)`. Public forum creation in seed must
  also create any tags referenced in the pre-seeded question via
  `forum_id._tag_to_write_vals(...)` OR direct `(6, 0, [tag.id])`.

### Survey

- Form hides Time Limit field when `survey_type='survey'`; use `'custom'` to expose it
- Question type `scale` (1–5 opinion scale) exists in Odoo 19
- Sections are `survey.question` records with `is_page=True`
- `_check_answers_integrity` requires each quiz question to have ≥1 correct AND
  ≥1 incorrect answer (enforces natural "mark exactly one correct" constraint)

### CRM / crm_iap_enrich

- `crm.lead` has NO `ref` field — do not use it as a state-diff `match_key`.
  Use `name` (unique within the seed) instead. `search_read` with an invalid
  field raises `ValueError: Invalid field 'ref' on 'crm.lead'`.
- `crm_iap_enrich` module is NOT in the base snapshot. Seed must
  `button_immediate_install` it on demand before creating any
  `iap_enrich_done`-carrying leads.
- `crm.lead.create()` (in the enrich bridge) triggers the
  `ir_cron_lead_enrichment` cron when
  `crm.iap.lead.enrich.setting='auto'` (the default). For deterministic
  test state seed `ir.config_parameter` key `crm.iap.lead.enrich.setting`
  to `'manual'` BEFORE creating leads — otherwise the cron may flip
  `iap_enrich_done` under you.
- `iap_enrich()` short-circuits BEFORE any external IAP call when
  `tools.email_normalize(lead.email_from).split('@')[1]` is in
  `iap_tools._MAIL_PROVIDERS` (gmail.com, yahoo.com, hotmail.com,
  outlook.com, icloud.com, aol.com, 163.com, qq.com, ..., plus the
  dummy `example.com`). In that branch it flips `iap_enrich_done=True`
  and posts the `crm_iap_enrich.mail_message_lead_enrich_notfound`
  template on the lead ("No company data found based on the email
  address or email address is one of an email provider. No credit was
  consumed."). This is the credit-free, network-free deterministic
  path for bench tasks that need to exercise the Enrich action.
- The `Enrich` server action is `crm_iap_enrich.action_enrich_mail`
  with `binding_model_id=crm.model_crm_lead` and `state='code'` running
  `records.iap_enrich()`. It surfaces in the list-view control-panel
  **Actions** dropdown when ≥1 `crm.lead` row is ticked — separate
  from the per-record **Enrich** form-header button (same label, same
  underlying method). Multi-select + Actions-menu pattern is solvable
  by browser-use in ~140s once rows are named uniquely.
- `crm.lead.partner_id` on the **lead** form (type='lead') is gated by
  `invisible="not is_partner_visible"` and `is_partner_visible` is
  `bool(type == 'opportunity' or partner_id or is_debug_mode)`. So on a
  lead that has no partner yet, the Customer m2o widget is NOT rendered.
  Tasks that need to set the customer on a lead must either (a) convert
  to opportunity first, or (b) set the customer inside the
  `crm.lead2opportunity.partner` wizard via `action='exist'`.
- `crm.lead2opportunity.partner` wizard: `_compute_name` auto-selects
  `merge` when `_get_lead_duplicates(partner, email)` finds ≥2 hits
  (include_lost=True). If you Duplicate a lead via the cog Actions menu,
  the copy inherits `email_from`, so the wizard's auto-pick becomes
  `merge` (not `convert`) — the agent/oracle must explicitly click the
  **Convert to opportunity** radio. `_compute_action` sets the
  `Related Customer` radio to `'exist'` only if `_find_matching_partner()`
  returns a partner — otherwise it defaults to `'create'`. The
  `action='create'` branch auto-generates a partner from
  `contact_name`/`partner_name`, so tasks that require a *specific new
  partner name* must pick `action='exist'` and quick-create in the
  partner_id autocomplete (the `Create "<name>"` option calls
  `res.partner.name_create`).
- `crm.lead.copy()` (cog Actions → Duplicate) copies `email_from`,
  `contact_name`, `description`, `tag_ids`, `expected_revenue`, and
  `type`. The copy's default name is `<original_name> (copy)`.

---

## UI navigation surprises

### Hidden or moved entry points

- Recruitment kanban "New" opens a stub modal with only name + alias. Full job form
  needs clicking "Configure" on the kanban card afterward.
- Live Chat kanban card opens the discuss session (chat UI), NOT the form. Use the
  3-dots kanban menu → "Configure Channel" to reach the form with the Rules tab.
- Replenishment: `Inventory → Operations → Procurement → Replenishment` (NOT directly
  under Operations). The per-row action button is labeled **"Order"** (name
  `action_replenish`), not "Replenish".

### Wizard buttons

- Public-portal job apply form requires either LinkedIn URL OR Resume attachment
  (client-side JS validation `hr_recruitment_form.js`). Prompt/oracle must supply one.
- Backorder dialog: agents often click "Create Backorder" correctly because it's
  the default — but inline qty edits before validation often fail silently (they
  report "I changed it" but the cell didn't commit).

### Widgets

- `boolean_toggle` widget: click the inner `<input>` element, not the surrounding widget div
- `many2one_avatar`: standard m2o autocomplete still works; the avatar is decorative
- Datetime fields in admin timezone: the browser-use agent may enter `09:00:30` when
  asked for `09:00:00`. Either accept ±60 seconds in check.py OR phrase the prompt
  so the agent is likely to type exact HH:MM:00.

---

## Seed patterns

### Cleanup ordering

Always cleanup in child-first order, with `active_test=False`:

```python
env["sale.order"].with_context(active_test=False).search([
    ("name", "=", "S-BENCH-XXX"),
]).sudo().unlink()
```

### Taxes for exact totals

If prompt quotes exact untaxed totals, clear taxes on lines:

```python
"tax_ids": [(5, 0, 0)],  # clear all taxes
```

### Storable product on-hand via stock.quant

```python
env["stock.quant"]._update_available_quantity(product, stock_location, 5.0)
```

### Features that may be disabled

Enable groups/settings in seed if the task needs them:

```python
env["ir.config_parameter"].sudo().set_param("account.use_credit_limit", "True")
group = env.ref("sale.group_discount_per_so_line")
group.users |= env.ref("base.user_admin")
```

---

## Oracle patterns

### When UI is too fragile (filters, complex nested widgets)

Use JSON-RPC `call_kw` to set canonical state deterministically. This is
allowed by the benchmark spec for *oracle.py only* — the browser-use agent
must still solve via UI.

```python
page.evaluate("""
  await fetch('/web/dataset/call_kw', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      jsonrpc: '2.0',
      method: 'call',
      params: { model: 'mailing.mailing', method: 'create', args: [[{...}]], kwargs: {} }
    })
  });
""")
```

Examples: `survey.review_submitted_responses_filter/oracle.py`,
`mass_mailing.create_segmented_mailing_save_draft/oracle.py`.

### Timezone-safe date comparison in check.py

```python
import pytz
user_tz = pytz.timezone(env.user.tz or "UTC")
post_dt_local = pytz.utc.localize(post.published_date).astimezone(user_tz)
expected_local = user_tz.localize(datetime(2026, 4, 25, 9, 0, 0))
assert post_dt_local == expected_local
```

See `project_todo.reorder_notes_add_due_dates_bulk/check.py` for a working reference.

---

## state_spec.yaml / expected_state.json gotchas

- The diff engine emits `is_correct=null` (not `False`) for unchecked Booleans;
  match in `expected_state.json`
- m2m fields like `tag_ids` can produce noisy diffs; use `ignore_fields` and verify in check.py
- Datetime fields that Odoo auto-normalizes (e.g., `date_deadline`) may produce
  spurious diffs from timezone differences between oracle and browser-use — add to
  `ignore_fields` and verify in check.py
- `web_save` is the browser-use write op; `create`/`write` are ORM-level.
  In `trace_spec.yaml`, put `create`/`write` in `optional_ops` (browser-use rarely
  hits them directly) unless the task explicitly triggers an action method.

---

## Discuss / mail side effects

- Visiting `/odoo/discuss` auto-creates an `Administrator, OdooBot` DM channel. This
  shows up in `state_diff.json` regardless of agent action. `check.py` should be
  the source of truth — don't rely on strict F1 with Discuss state in scope.

---

## mail.message subtype_id — chatter Send message vs Log note

The chatter composer's **Log note** and **Send message** tabs both
produce `mail.message.message_type = 'comment'`, so filtering on
`message_type` alone cannot tell them apart. The distinguishing field
is `subtype_id`:

| UI tab | `subtype_xmlid` | `is_internal` |
|--------|-----------------|---------------|
| Log note (default tab) | `mail.mt_note` | True |
| Send message | `mail.mt_comment` | False |

Checks that want to pin "the agent actually clicked Send message, not
Log note" must gate on `msg.subtype_id == env.ref('mail.mt_comment')`
— NOT on `message_type`, NOT on `is_internal` alone (which is stable
but easy to misread as inverted).

Oracle pattern to reproduce a Send-message post via JSON-RPC without
driving the chatter UI:

```js
await callKw(
    'res.partner',                  // or any thread model
    'message_post',
    [[threadId]],
    {
        body: 'Attached our welcome kit',
        message_type: 'comment',
        subtype_xmlid: 'mail.mt_comment',   // <-- critical
        attachment_ids: [attachmentId],
    },
);
```

## res.partner Send-message posts can have empty partner_ids

Out of the box in the benchmark base, a `res.partner` record does NOT
auto-follow itself — `_message_get_auto_subscribe_followers` returns
an empty recordset for res.partner. Consequence: a Send-message post
via `message_post(subtype_xmlid='mail.mt_comment')` can legitimately
land with `mail.message.partner_ids == Recordset()`. Gating the
Send-vs-Log discrimination on `partner.id in msg.partner_ids.ids` is
a false-positive trap that rejects even a correct oracle post. Pin
the distinction on `subtype_id` alone.

## Chatter paperclip file upload — hidden <input type=file>

The chatter composer's paperclip (`button[aria-label="Attach files"]`)
is wrapped in the `FileUploader` component
(`addons/web/static/src/views/fields/file_handler.xml`). The button
itself has `class="d-none"` — the clickable visible surface is a
pseudo-button on the composer toolbar that forwards clicks. The actual
`<input type="file">` is rendered with
`class="o_input_file d-none"` and can be driven from Playwright with
`set_input_files` even though it's not visible:

```python
input_el = page.locator(
    ".o-mail-Composer input.o_input_file[type='file']"
).first
input_el.set_input_files("/abs/path/to/welcome_kit.txt")
```

Browser-use cannot drive it reliably, and the benchmark runner does
NOT pass `available_file_paths=[...]` through to the Agent
constructor, so BU's own upload fallback fails with
`File path ... is not available`. Any task that requires uploading a
seeded artifact through the chatter paperclip is effectively a BU
calibration trap until the runner is updated.

## Oracle bypass: ir.attachment res_model='mail.compose.message'

To attach a file to a `message_post` call without driving the
paperclip UI, create the `ir.attachment` with
`res_model='mail.compose.message'` and `res_id=0`, then pass its id
to `message_post(attachment_ids=[id])`. `_process_attachments_for_post`
migrates the attachment onto the newly-created mail.message and
rewrites `res_model`/`res_id` to the thread. Passing
`res_model='<target_model>', res_id=<target_id>` directly creates the
attachment on the thread's Files pane but does NOT automatically link
it to the posted mail.message.

---

## Parallel execution hygiene

- The default `auto-isolate` mode in eval.py starts a dedicated Odoo process per run
  and uses per-run DB names. Parallel agents don't collide **as long as nobody calls
  the legacy `pkill -f odoo-bin` or wildcard `benchmark_*` cleanup paths.**
- Do NOT run `benchmark-eval cleanup` unless you know it's scoped to your own run —
  it may drop ephemeral DBs owned by sibling worktrees.

---

## Reference tasks by pattern

When you need to copy a pattern, these are the cleanest examples:

| Pattern | Reference task |
|---------|---------------|
| Simple form edit + save (easy) | `project_todo.reorder_notes_add_due_dates_bulk` |
| Cross-module smart-button chain (hard) | `sale_purchase.dropship_so_to_po_chain_validate` |
| Wizard with non-default radio (hard) | `event_sale.configure_paid_ticket_register_with_invoice` |
| Inline-cell edit failure (hard) | `sale_stock.partial_stock_warning_confirm_anyway` |
| File upload (medium) | `mail.create_channel_set_custom_avatar_pin_two_messages` |
| Datetime precision (medium) | `website_blog.edit_post_change_author_add_tags_schedule` |
| State-machine cycle (medium) | `website_sale.unpublish_archive_unarchive_publish_cycle` |
| Nested polymorphic form (hard) | `website_slides.add_quiz_lesson_to_existing_course` |
| Multi-step kanban modal (hard) | `website_hr_recruitment.publish_job_from_backoffice_then_apply_portal` |
| Module install on demand | `survey.create_feedback_survey_with_sections/seed.py` |
| JSON-RPC oracle bypass | `survey.review_submitted_responses_filter/oracle.py` |

---

## Live Chat (im_livechat) — Options tab fields

The `im_livechat.channel` model has **NO** `offline_form_text`, `offline_email`,
or any `offline_*` fields in Odoo 19 (often confused with older versions or
other products). The Options tab only exposes:
- `button_text` (Char, "Notification Text")
- `default_message` (Char, "Welcome Message")
- `header_background_color`, `title_color`, `button_background_color`, `button_text_color` (color widgets)
- `review_link` (Char)
- `max_sessions_mode`, `max_sessions`, `block_assignment_during_call` (Session Limits group)

If a task description implies offline-form configuration, map to `button_text` /
`default_message` or skip — seeding non-existent fields raises `ValueError`.

---

## website_blog archive + state-diff null-vs-false

- For a record **created in the same task and then archived** (active=False), the state-diff engine emits `op: "create"` with `norm_value: null` (NOT `false`) for `active`, `is_published`, and `website_published`. `expected_state.json` must use `null` for these fields, not `false`.
- `blog.post.action_archive` is the canonical UI/JSON-RPC method (mirrors form's Action > Archive). Auto-flips `is_published`/`website_published` to False as a side effect.
- `blog.blog` records surface their `active` field in the diff (`norm_value: true` on fresh create) — include in `expected_state.json` or `ignore_fields`.
- Same null-vs-false quirk applies to **create-and-schedule** (future `published_date` + keep `is_published=False`): both `is_published` and `website_published` diff as `op: "create"` / `norm_value: null`, not `false`. See `website_blog.create_post_with_cta_seo_schedule`.
- `blog.post.content` is the Html body (`sanitize=False`), NOT `arch_db` (which belongs to `ir.ui.view`). Free-form HTML produces noisy diffs; keep it in `ignore_fields` and validate the CTA / keywords via a tolerant regex in `check.py` (accept any `<a href='...'>Label</a>` regardless of class attribute order).
- `blog.post` also exposes the **Optimize SEO** cog dialog in the BACKEND form (via `website.seo.metadata` mixin + `OptimizeSEODialog`), not just on the frontend. Contrast with `website_sale` where the product SEO dialog is frontend-only.
- **Pure author-swap on a pre-existing published post** does NOT trigger the null-vs-false quirk: when `is_published`/`website_published` are True before AND after the task (only `author_id` changes), the state diff emits exactly one `op: "set"` edit on `author_id` and nothing on the published flags. See `website_blog.change_author_republish_post` (row 430) — clean single-edit `expected_state.json`, no null sentinels needed. The null-vs-false trap only fires when a field is being **created** or **toggled False** in the same transaction as a record create.

---

## website_slides — sections, sequencing, and copy

- `slide.slide.is_category=True` rows ARE the sections of a `slide.channel`; no separate section model.
- `slide.slide.category_id` is **computed** from sequence ordering, NOT writable. To move a lesson, change its `sequence` to fall after that section's marker.
- `slide.slide.copy_data()` resets `sequence=0` on the duplicate (lands at top, uncategorized). Agent must re-sequence/pick section.
- New `is_category` slides default to `slide_category='document'` and `website_published=True` even though they aren't real lessons.
- BU failure mode: asked to "duplicate the lesson via Actions menu", BU tends to land on the COURSE cog menu and duplicate the whole `slide.channel` instead.
- **`slide.channel.copy()` drags slides along via `copy_data`** — duplicating the whole channel copies every `slide.slide` under it (both is_category sections and regular lessons) onto the new channel with fresh ids. If the task says "duplicate the course and add one new slide", oracles must `slide.slide.unlink()` the auto-copied slides on the new channel before creating the single new slide, otherwise check.py sees N+1 slides on the copy. Seen in `website_slides.duplicate_course_edit_add_slide` (row 424). Counter-calibration: BU solved that task single-shot in 107s, F1=1.0 — duplicating a whole `slide.channel` via the course-form cog is **NOT** a hard pattern (contrast with the lesson-level cog Duplicate in `duplicate_lesson_to_new_section` which *does* trip the course-vs-lesson cog confusion). The channel-level Duplicate button is unambiguous in the form header cog menu.
- **`slide.channel` + `slide.slide` `website_published` diffs as `op: "create"`, `norm_value: null` (not `true`) on fresh creates/copies.** Same null-vs-false diff-engine quirk as `website_blog.create_post_with_cta_seo_schedule`. `expected_state.json` must encode `null` — encoding `true` causes a spurious missing/extra edit pair even though the record is actually published.

---

## project_todo / web.PriorityField — star indexing

`project.task.priority` is a Selection `[('0','Low'),('1','Medium'),('2','High')]`. The widget renders **N-1 stars**, skipping `value_first`:
- Star 1 (`.o_priority_star` index 0) → priority `'1'` (Medium / one filled star)
- Star 2 (`.o_priority_star` index 1) → priority `'2'` (High / both filled stars)

Default (no star filled) is `'0'` (Low). Prompt phrasing matters: "set High by clicking the star" gets BU to click the rightmost star (priority `'2'`). For priority `'1'` say "click only the FIRST star (Medium)".

---

## project.task — no bulk "Move to Project" + list project_id is readonly

`project.task` in Odoo 19 Community exposes **no** "Move to Project" /
"Change Project" bulk action in the list or kanban cog Actions menu.
The only server action bound to `model_project_task` is
`mail.compose.message` ("Send Email"). In parallel,
`project_task_view_tree_main_base` pins
`<field name="project_id" ... readonly="1"/>` on the column, so list
`multi_edit="1"` cannot be used to bulk-retarget tasks either. The
canonical project reassignment path is **open each task's form →
change the `Project` many2one → Save**. For "move N of M tasks"
benchmark tasks the distractor trap is natural (Delta stays put while
Alpha/Bravo/Charlie are reassigned one form edit at a time).

Browser-use failure mode on this pattern: after the first successful
form edit, the re-rendered `o-autocomplete--input` for `project_id`
trips BU's dropdown-type detection (`Element and its children (depth 4)
are not recognizable dropdown types`); BU misattributes to an
ACL/"write access" error and aborts, leaving a partial
1-of-N completion. Oracles should use JSON-RPC `web_save` of
`project_id` for determinism — the UI path is noisy.

---

## survey.survey + CopyClipboardChar widget

- `survey.survey` has **no `state` field** in Odoo 19. "Ready to share" = `active=True` + `access_mode='public'` + populated `access_token`. Don't query a non-existent state field.
- `widget="CopyClipboardChar"` (e.g. `survey.invite.survey_start_url`) renders as `<span>` in readonly mode, NOT `<input>`. `page.input_value()` will time out. Read via `text_content()` on the field widget div, with input fallback.
- `survey.survey.action_send_survey` returns a `survey.invite` wizard with `default_send_email=False` for public surveys, so closing the wizard has no DB side effect.

---

## Browser-use failure mode: cog→Duplicate spam loop

When asked to "Duplicate via Actions menu, then edit the copy", BU on `mailing.mailing` (and likely other forms) clicked Duplicate **repeatedly**. After the first Duplicate, the form navigates to the new copy with subject still equal to the source; BU's policy of "find original, click Duplicate" reads the heading as still-not-yet-duplicated and tries again.

Implication: when the *only* visible signal of Duplicate success is a URL/id change (not a subject change), BU loops. Either phrase the prompt so post-duplicate state is visually distinct, or accept as canonical FAIL mode and test via "exactly N records" assertion in check.py.

For mass_mailing oracles: prefer JSON-RPC `copy() + write()` over UI navigation — the domain tree editor + Recipients autocomplete are notoriously fragile.

**Counter-calibration data point (`mass_mailing.duplicate_mailing_edit_subject_send`):** the spam loop is NOT deterministic. When the post-duplicate edit list is short enough (just change subject + add one m2o list, no domain editor) and the Send button is explicit ("Send" top button), BU completes the flow in ~10 steps on the first try and lands the new mailing in state='done' with F1=1.0. The spam loop triggers primarily when BU gets stuck on a brittle subsequent widget (domain tree editor in the sibling task) and loops back to re-Duplicate as a recovery strategy. Summary: the Duplicate-then-edit pattern is only reliably hard when paired with a second failure anchor (domain widget, non-default radio, etc.). `mailing.mailing.copy_data` copies `contact_list_ids` verbatim, so seeding the source with empty `contact_list_ids=[(6,0,[])]` forces the agent to explicitly add the target list to the duplicate — a useful discriminator that does NOT induce the spam loop.

---

## POS / pos_discount

- `pos_discount` is NOT in the base snapshot — seed must `button_immediate_install()` on demand.
- To enable Discount button: `pos.config.module_pos_discount=True`, `iface_discount=True`, `discount_pc=<float>`, `discount_product_id` (data record `pos_discount.product_product_consumable`).
- UI: Discount button lives inside the **Actions popup** (ellipsis `more-btn`), not the top bar. In Odoo 19 `control_buttons.xml` moves secondary actions (Pricelist, Refund, Fiscal position, Discount, etc.) into ControlButtonsPopup.
- Oracle pattern: prefer JSON-RPC `call_kw` over UI-driven POS oracle — `o_technical_modal` sometimes stays in DOM and intercepts pointer events.
- **pos_discount is PERCENT-only, never fixed currency.** `pos_discount.ControlButtons.clickDiscount` opens `NumberPopup` titled "Discount Percentage", clamped 0–100. To simulate a "fixed EUR" discount, seed `discount_pc` to the percentage that rounds to the target amount against the exact subtotal (e.g. 20+15=35, target -5.00 → `discount_pc=14.29` → 14.29%×35=5.0015 ≈ 5.00). The popup is **pre-filled** with `discount_pc`, so the agent just accepts the default. Confirmed easy-to-solve pattern for browser-use: `point_of_sale.apply_fixed_discount_before_payment` (row 420) passes F1=1.0 in 111s — even a non-default decimal like 14.29 is not a hard anchor. Escalation: split payment (Cash+Bank) with discount, non-default pct distinct from `discount_pc`, mid-order customer change forcing price recompute.
- Check tolerances for pos_discount percent→EUR rounding: `amount_total ± 0.2`, discount line `price_subtotal_incl ± 0.5` absorbs the drift across oracle and UI paths.
- Seed quirk: tax-free POS products need `taxes_id=[(5,0,0)]` on **both** `product.product` and `product.product_tmpl_id` — clearing only on product.product leaves the template with company defaults that re-apply on POS load.

---

## calendar.event — duration is the reliable end-time handle

`calendar.event.stop` is `invisible="1"` on the main form. `start` uses
`widget="daterange" options="{'end_date_field': 'stop'}"` with a
`.o_daterange_end` pill that opens a secondary `.o_datetime_picker` +
`.o_time_picker_input` for the stop time.

Driving that popover with `fill("4:00pm")` / `Tab` is flaky whenever the
default stop is already 1h past start: Playwright's fill gets silently
dropped and stop stays at start+1h. Oracles that happen to use a 1h
duration (e.g. `calendar.invite_external_attendee_by_email`) hide this
bug because the default is already correct.

Reliable oracle pattern for any non-1h duration: write the visible
`duration` float_time input directly.

```python
duration_input = page.locator('.o_field_widget[name="duration"] input').first
duration_input.click(click_count=3)
duration_input.fill("02:00")
duration_input.press("Tab")
```

This deterministically produces `stop = start + duration` on web_save.

---

## calendar.event.alarm_ids — many2many_tags with `no_quick_create=True`

The Options tab exposes `alarm_ids` as
`widget="many2many_tags" options="{'no_quick_create': True}"`. Agents
MUST pick an existing `calendar.alarm` record from autocomplete; typing
a free-form label creates nothing.

Odoo ships seven default alarms in `calendar/data/calendar_data.xml`
covering 15/30 min + 1/2 h notifications + 1 d notification + 3/6 h
email reminders. The `Notification - 1 Hours` record is the canonical
"1 hour before" answer. Task `check.py` should assert
`duration_minutes == 60`, not a specific alarm name/xmlid, and
`trace_spec.yaml` should put `calendar.alarm.create`/`unlink` in
`forbidden_ops` to pin the agent to the seeded records.

---

## calendar.event — recurrence panel lives on the Options tab

The recurrence controls (`recurrency` boolean_toggle, `rrule_type_ui` SelectMenu,
`calendar_week_days` widget, `end_type` SelectMenu, `count`, `until`) are all
inside the **Options** notebook tab in
`addons/calendar/views/calendar_views.xml:250-289`, NOT on the main form body.

Oracles that call `set_boolean(page, "recurrency", True)` before switching to the
Options tab will time out (60s) waiting on
`.o_field_widget[name='recurrency'] input[type='checkbox']`. Always
`click_tab(page, "Options")` first.

The week-day widget `.o_recurrent_weekdays` uses locale `weekStart`-indexed
buttons. For the default US locale (weekStart=Sunday):
`0=Sun 1=Mon 2=Tue 3=Wed 4=Thu 5=Fri 6=Sat`. The active-state class on each
`.o_calendar_week_days_rounded` is `text-bg-action`; toggling is a simple
`.click()`. The widget pre-selects today's weekday, so "Monday-only" oracles
MUST iterate all 7 indices and explicitly deactivate every non-target day
(same pattern as `calendar.schedule_recurring_steering_sync/oracle.py`).

`end_type` + `count` end-type is a Selection rendered via the standard
SelectMenu (options: "End date" / "Number of repetitions" / "Forever"). Agents
that type `count` into a visible number input without first flipping `end_type`
to "Number of repetitions" will have the `count` field invisible (gated by
`invisible="end_type != 'count'"`).

Additional quirk on harnesses where the browser's local tz ≠ admin's Odoo tz
(e.g. Asia/Singapore host vs admin tz=UTC): the datetime widget interprets
typed strings in the browser's local tz, not the admin's Odoo tz. Checks that
compare stored UTC datetimes against a literal string will fail. Use the
`calendar.configure_meeting_with_location_and_reminder` pattern: `pytz`-convert
stored UTC to admin-local and compare the local date (± hour tolerance), not
the absolute UTC string.

---

## calendar.event.set_discuss_videocall_location is a no-op on the server

In Odoo 19, `calendar.event.set_discuss_videocall_location()` is a no-op that returns True — the actual URL generation happens in JS (intercepted on the frontend). The private `_set_discuss_videocall_location()` does the real work but isn't callable via JSON-RPC.

For JSON-RPC oracles that need a Discuss videocall URL, craft it manually and write `videocall_location` + `access_token` directly:
```python
import secrets
token = secrets.token_hex(16)
videocall_location = f"/calendar/join_videocall/{token}"
```

---

## crm.lead form: team_id hidden on opportunities

In Odoo 19, `crm.crm_lead_view_form` has TWO copies of the user_id/team_id group:
- Under `<group invisible="type == 'lead'">` — shows just `user_id` (with `many2one_avatar_leader_user` widget). Visible on opportunities.
- Under `<group invisible="type == 'opportunity'">` — shows BOTH `user_id` and `team_id`. Visible on leads.

On an **opportunity**, `team_id` is NOT in the main form header. Only editable copy is under the **Contacts** notebook tab → **Ownership** group. Tasks that "change Sales Team" on an opportunity must explicitly tell the agent to open the Contacts tab.

---

## mrp / stock.scrap quirks

- `stock.scrap.reason` is **many2many** `scrap_reason_tag_ids` (model `stock.scrap.reason.tag`), NOT a Char field. Seed must create the tags (Odoo ships none by default). Phrase prompts as "add the existing tag X" so agent picks from autocomplete.
- The "Scrap" action on an MO is `mrp.action_production_order_scrap` (`ir.actions.server`, `binding_view_types="form"`) — accessed via cog Actions menu, NOT a header status-bar button. The **same pattern** applies to `stock.picking`: `stock.action_scrap` (`binding_model_id=stock.picking`, `binding_view_types=form`) lives in the picking-form cog Actions menu, NOT on the header status-bar.
- `stock.scrap.scrap_qty` defaults to 1.0 — agents often forget to override it. Good calibration trap for hard tier. **Corollary — BU-passable pattern**: when the prompt asks for `scrap_qty=1` AND the source MO has a single-component BoM (no component-picking ambiguity) AND no `scrap_reason_tag_ids` is required, the scrap-from-MO workflow becomes a "find cog menu → click Scrap → accept defaults → Validate" flow that BU completes single-shot (~210s, F1=1.0). Empirically verified on `mrp.scrap_consumed_component_during_production` (Bench Screw qty=1 of 3 in a 1-line BoM). To raise difficulty reliably you need at least ONE of: (a) `scrap_qty != 1`, (b) multi-component BoM forcing a product-picker choice, or (c) a reason-tag m2m_tags field; the combination of (a)+(b)+(c) is what makes `mrp.scrap_component_during_partial_production` a BU trap.
- `stock.scrap.production_id` as match_key emits an extra "create" diff row that must be in expected_state.json.
- `stock.scrap.scrap_location_id` defaults to the per-company `Virtual Locations/Scrap` (the auto-created inventory-usage location from `_create_scrap_location`). For a task that requires a custom scrap destination (e.g. `WH/Lost`), seed must create a new `stock.location` with `usage='inventory'` + `location_id=warehouse.view_location_id` so its `complete_name` resolves to `WH/<name>`. Both `scrap_location_id` AND `location_id` fields on the wizard are gated by `groups="stock.group_stock_multi_locations"` — seed must add the admin to that group or the fields are invisible and silently default.
- A validated scrap launched from a `stock.picking` (via `picking_id` in the wizard context) **auto-creates a `stock.move` on the parent picking** (`move._prepare_move_values` sets `picking_id=self.picking_id.id` and `scrap_id=self.id`). Consequence: `picking.move_ids` grows by one after scrap, so `check.py` assertions like `len(picking.move_ids)==1` MUST filter `not m.scrap_id`.
- The Inventory menu **Operations > Scrap** action is `stock.action_stock_scrap` (server-action URL `/odoo/action-stock.action_stock_scrap`). Opens as a `stock.scrap` list view with a standard **New** button; clicking New yields a blank form (no `picking_id` / no `production_id` pre-binding). This is the clean-path creation flow for the `stock.create_scrap_order_for_damaged_qty` / `inventory.scrap_product` tasks. BU empirically handles this form flow well (single-screen, standard statusbar Validate) — a scrap task without extra modals or reason tags is solidly **medium / tier 2**, not hard. To push to tier 3, layer either a scrap-reason m2m tag, a non-default Scrap Location (`WH/Lost`), or a picking-context launch on top.
- For a standalone scrap from `WH/Stock`, when `source.qty_available >= scrap_qty` Odoo's `action_validate` does NOT open any downstream `stock.warn.insufficient.qty.scrap` wizard — the button synchronously flips `state='draft' → 'done'`. Seeding 10 on-hand against a scrap of 3 gives the oracle a clean click-through.

## mrp — phantom/kit BoM expansion + `mrp.production.name` UI trap

- `mrp.bom.type` is a Selection with values `'normal'` (UI label "Manufacture
  This Product") and `'phantom'` (UI label **"Kit"**). Do not seed
  `type='kit'` — `'phantom'` is the correct selection key.
- `mrp.production.action_confirm` calls `_get_moves_raw_values` which invokes
  `bom.explode(product, factor, ...)`. `explode()` walks each BoM line; for
  lines whose `product_id` has its own phantom BoM, it **recursively drills
  in** and pushes the sub-components onto the todo queue. The final
  `lines_done` only contains leaves (atomic components), so `move_raw_ids`
  on the confirmed MO reflects the **fully expanded** leaf set — NOT the
  immediate children of the primary BoM. An MO for product P whose normal
  BoM has `[1x K, 1x F]` where `K` has phantom BoM `[1x A, 2x B]` will
  confirm into 3 raw moves: `A=1, B=2, F=1`. Agent must NOT add/edit
  Components tab manually.
- Phantom expansion requires no stock / no routes / no rules — it's driven
  purely by `_bom_find(product, bom_type='phantom')` at confirm time.
- For a confirmed-but-not-produced MO, check `move.product_uom_qty`
  (demand) on `move_raw_ids` — `move.quantity` is 0.0 until Produce All
  is clicked.
- **`mrp.production.name` has no editable Reference input on the draft
  form.** The Odoo 19 `mrp.production_form_view` displays the auto-generated
  `WH/MO/####` sequence in the breadcrumb but provides no inline Char
  input for `name` in the form body. The only UI paths to override `name`
  are (a) click the breadcrumb text in the top bar and overwrite (fragile
  in Playwright, browser-agents rarely discover this) or (b) JSON-RPC
  `create({'name': '...', ...})` (oracle path).
- The Miscellaneous tab exposes `origin` (label "Source") as a free-text
  Char. Browser-use empirically types the prompt's "reference" into
  **Source** when the prompt says "Reference field". This is a deep-UI
  trap for hard-tier tasks that need a deterministic `name` match in
  `check.py` — even when the agent is correct about every other step
  (product, BoM, qty, confirm), the missing `name` override triggers an
  entity_key mismatch in state_diff AND a "MO not found" postcondition
  failure. BU may also hallucinate success by conflating Source with
  the MO reference in its memory log.

## mrp — work-order lifecycle + serial-tracked component consumption

- `mrp.workorder.button_finish` internally calls
  `move._set_quantity_done(qty)` on every unpicked raw move, which
  **replaces** `move_line_ids` with vals derived from fresh reservation
  lookups. Consequence: if the agent overrides `lot_id` on a
  serial-tracked component move line via the MO form's Details popup
  and then clicks WO `Done`, the override can be overwritten by
  `_set_quantity_done` unless the move's `picked` flag is already
  `True` (lines with `picked=True` are skipped by `button_finish`'s
  move-picking loop, so the agent's serial choice sticks). Oracle path
  sets `stock.move.picked = True` explicitly after writing the SN-B
  move line, BEFORE calling `button_finish`.
- The MO Components-tab row for a serial-tracked product has two UI
  entry points for picking a specific serial: (a) inline `lot_ids`
  many2many_tags column (readonly until MO is in progress,
  `show_lot_ids`-gated), and (b) the `Details` button (per-row), which
  opens `stock.move.action_show_details` → `view_stock_move_operations`
  modal with an editable `move_line_ids` O2M list. The per-line
  `lot_id` m2o in that list is the reliable way to **override** an
  already-reserved serial. Browser-use empirically types the serial
  name into the `lot_name` Char (typed autocomplete fallback) instead
  of picking from the `lot_id` dropdown — which creates an unassigned
  line that `button_mark_done` silently discards, leaving
  `consumed_lots = []`.
- On `mrp.production.action_confirm` with a serial-tracked component
  and multiple on-hand lots, the auto-reservation picks the lot with
  the **lowest `stock.lot.id`** (FIFO by creation order), NOT by
  `name` lexicographic order. Seed serials in the exact order you want
  them reserved (e.g. create SN-A first so SN-A has lowest id ⇒ SN-A
  is the default reserved ⇒ agent has a clear "not the default"
  target like SN-B).
- `mrp.workorder` entity_key with `match_key: [production_id,
  workcenter_id]` normalizes to `[null, null]` in `expected_state.json`
  — both Many2one fields read back as null through the instrumentation
  cursor. Use literal `"entity_key": [null, null]` in expected_state.
- `button_start` on a work order with `qty_producing == 0` auto-sets
  `qty_producing = qty_remaining` (usually 1 for a single-unit MO).
  No separate `qty_producing` edit needed before clicking Done.
- Two distinct `Done`-style buttons cause UI confusion: the work-order
  row's `Done` (→ `mrp.workorder.button_finish`) vs the MO header's
  `Mark as Done` (→ `mrp.production.button_mark_done`). The correct
  order is WO-Done FIRST, then MO-Mark-as-Done. Clicking
  `button_mark_done` first on an in-progress MO with unfinished
  workorders raises `UserError('You need to finish the Work Order before marking the Manufacturing Order as Done.')` in
  some configurations — but on single-WO MOs Odoo auto-finishes the
  WO when the MO is marked done, so BU often gets away with a
  "happy path" that skips the WO Done button.

## mrp.unbuild — product-driven vs MO-linked; action URL; BU-passable form

- **Two flows, same model**: (a) *MO-linked unbuild* with `mo_id` set to a
  Done MO — finished product is consumed from the MO's destination, BoM
  comes from `mo.bom_id`, and unbuild `lot_id` defaults to the produced
  lot. (b) *Product-driven unbuild* with `mo_id=False`, `product_id`
  picked from the list of products with an active BoM, and `bom_id`
  auto-filled by the `_onchange_product_id` handler to the first matching
  normal BoM on that product. Both land in the same statusbar
  `action_validate` (labeled **Unbuild**) with identical behavior.
- **Menu entry lives under Products, not Operations**: in Odoo 19 the
  `mrp.mrp_unbuild` action is reachable via Manufacturing > **Products**
  > Unbuild Orders. The direct action URL `/odoo/action-mrp.mrp_unbuild`
  is the stable deep-link for oracles (saves a menu click and dodges any
  menu-reshuffle across Odoo minor versions).
- **Form auto-completes everything**: picking `product_id` triggers
  `_onchange_product_id` → fills `bom_id` to the first BoM found and
  leaves `product_qty=1.0`, `location_id=WH/Stock` (primary warehouse
  stock), `location_dest_id=WH/Stock`. The agent only needs to set
  Quantity and click Unbuild. This makes the clean-path
  product-driven-unbuild flow **tier 2 / medium-equivalent**: BU passed
  `mrp.unbuild_product_back_to_components` F1=1.0 in 132s on a "hard"
  calibration because there's no wizard, no radio dialog, no
  cross-module navigation. To push to genuine tier 3 you need one of:
  (a) two candidate BoMs on the same product (BoM picker ambiguity),
  (b) `tracking='serial'` + a specific lot to select, (c) a non-default
  destination like `WH/Stock/QC` requiring `stock.group_stock_multi_locations`.
- **`mrp.unbuild.state` starts at `draft`, flips directly to `done`** on
  `action_validate` — there is no intermediate `confirmed` state. The
  state_diff will always be `field=state, op=create, norm_value=done`
  for a successful task (never `set` transitions because the record is
  born in this run).
- **`mrp.unbuild.mo_id=False` shows up in state_diff as `norm_value:
  null`, `op=create`**. Expected_state must include this explicitly —
  omitting it means the diff engine reports an extra observed edit and
  F1 drops below 1.0 (Precision=0.75 on a 3-edit expected / 4-edit
  observed). Seen empirically on first oracle run of the unbuild task.
- **`match_key: [product_id]`** works cleanly for product-driven unbuilds
  (one unbuild per product in the task) and normalizes to the product's
  display_name. Using `[mo_id]` as in the MO-linked unbuild task
  normalizes to `null` when mo_id is False, so it only works as a key
  when the task expects a non-null MO.
- **Consumption**: `action_validate` creates two sets of `stock.move`s:
  a consume-from-WH/Stock move for the finished product (qty =
  `product_qty`), and N produce-to-WH/Stock moves (one per BoM line) at
  `bom_line.product_qty * product_qty`. All moves are born `done`, not
  `confirmed`. Postcondition can assert via
  `stock.quant._get_available_quantity(product, stock_loc)` — no need
  to walk the move graph.
- **No forbidden-op risks** from the form alone: `action_validate`
  doesn't call `mrp.production.create`, so a clean product-driven unbuild
  leaves no stray MO. Listing `mrp.production.create` in `forbidden_ops`
  makes a good "did the agent stray into creating an MO instead" trap.

## purchase_stock / sale_stock — origin and demand quirks on pickings

- `stock.picking.origin` on a PO-generated receipt inherits from **`purchase.order.name`**, NOT from `purchase.order.origin`. If the task relies on a deterministic `origin` for `state_spec.match_key`, pin `po.name` in the seed (e.g. `name="P-BENCH-DMG-001"`). Same pattern as the previously documented `sale.order.name` → delivery `origin`.
- **Validate-with-backorder rewrites the original move's demand.** When `picking.button_validate()` is called with the backorder dialog's **Create Backorder** choice, Odoo's `_action_done()` splits the split-moves: the original picking's `move.product_uom_qty` is REDUCED from the full demand to the actually-Done quantity, and a fresh move with the remaining demand is created on the backorder picking. Do NOT assert `product_uom_qty == original_full_demand` on the done picking — assert `== Done quantity`.
- Backorder picking inherits `origin` from the original picking (via `copy()`), so `backorder.origin == original.origin`. To distinguish original vs backorder in `state_spec.match_key`, add `backorder_id` to the key list: the original has `backorder_id=False → null` and the backorder has `backorder_id=<original picking display_name>`. Pin `original_picking.name` in seed to make that display_name deterministic across runs.

---

## hr_expense changes in Odoo 19

- `hr.expense.sheet` model is **REMOVED**. The legacy "Expense Report" wrapper is gone — submission/approval/posting now happens directly on `hr.expense`. Tasks ported from older versions that say "create an expense report" must be redesigned. Vestige: `hr.expense.former_sheet_id` (Integer) preserves legacy id for migrated data only.
- `hr.expense.currency_id` dropdown has `groups="base.group_multi_currency"` — invisible without that group on the user. Seed must add `admin.group_ids |= env.ref("base.group_multi_currency")` for foreign-currency tasks.
- `res.currency` records (EUR, USD, etc.) start `active=False` in fresh DBs — seed must `currency.write({"active": True})` and ensure a `res.currency.rate` is set.
- `res.currency.rate.rate` semantics: rate=0.925 with company_currency=USD means **1 USD = 0.925 EUR** (currency-per-company-currency).
- `hr.expense` approval pipeline uses two fields: `approval_state ∈ {False, 'submitted', 'approved', 'refused'}` (writable via actions) and a computed `state` that mirrors approval_state plus `'posted'/'paid'` when `account_move_id` exists. There is **no per-line refuse on a sheet** (because no sheet) — each `hr.expense` is refused individually via the `hr.expense.refuse.wizard` (single required `reason` Char; confirm button calls `action_refuse` → `_do_refuse` which posts the `hr_expense.hr_expense_template_refuse_reason` mail template to the expense chatter).
- Admin needs **all three** of `hr_expense.group_hr_expense_team_approver` + `group_hr_expense_manager` + `group_hr_expense_user` to see Approve/Refuse on another employee's submitted expense. The employee being approved also needs `expense_manager_id` pointing to the approver.
- Manager "all expenses" approver list is the action xmlid `hr_expense.hr_expense_actions_my_all`, reachable via `/odoo/action-hr_expense.hr_expense_actions_my_all`. Bare `/odoo/expenses` opens **My Expenses** only (admin's own).
- `hr.expense.action_split_wizard` opens `hr.expense.split.wizard` (a one2many editor with default 2 lines summing to the original amount). It only works on a single `hr.expense` in draft/submitted state, and it mutates the original expense to the FIRST split-line values while `copy()`-ing the rest into new `hr.expense` rows with `split_expense_origin_id` back-pointing. Not a "sheet split" — it splits one expense into multiple expenses.
- Browser-use empirically **passes** a 3-record per-line triage loop ("refuse one with wizard reason, approve the remaining two") in ~140s single-shot. Pure per-line loops without non-default radios/dropdowns or create-from-scratch do not reliably trip BU — add a secondary non-default widget if you want to re-tier upward.
- **`hr.expense` Total field is READONLY when `product_has_cost=True`.** `product_has_cost` is computed as `not company_currency.is_zero(product.standard_price)`. The form view `hr_expense_views.xml` has two alternative "Total" layouts: (a) `total_amount_currency` (editable input) visible only when `product_has_cost=False`; (b) `total_amount` (readonly, computed from `quantity * price_unit`) visible when `product_has_cost=True`. If your seed sets `standard_price > 0`, the user CANNOT type a number into the Total field — they must change `quantity` instead, or have the product changed. Fix for tasks that require the agent to type an arbitrary total: seed the expensable `product.template` with `standard_price=0.0` (keep `list_price` set as a reference price if you want) so `product_has_cost=False` and the Total input is editable. Verified empirically: with `standard_price=25`, oracle `fill("45.00")` on every `.o_field_widget[name='total_amount*'] input` selector still produced `web_save` payload `{total_amount: 25, total_amount_currency: 25}`.

---

## product.template / event_product gotchas

- The base snapshot has TWO pre-existing 'Gift Card' product.template records with different list_price. With `match_key: [name]` the diff engine swaps them non-deterministically, emitting phantom `list_price` edits. Fix: extend `match_key: [name, service_tracking, list_price]`.
- `product.template.service_tracking` field is `invisible` in the base product view. `event_sale` (auto-installed) removes the invisible attr, exposing the `event` ('Event Registration') option contributed by `event_product`. No manual install needed for event_sale → event_product.

---

## product.template attribute_line_ids + variant auto-generation

Configuring variants on a `product.template` via the Attributes & Variants
tab writes `attribute_line_ids` with a `(0, 0, {attribute_id,
value_ids:[(6,0,[…])]})` command. The ORM's `_create_variants` fires on
save for every attribute whose `create_variant='always'` (the default),
creating one `product.product` per combination of the cross-product of
`value_ids` across all lines. There is no separate "generate variants"
button — the save itself is sufficient.

Seed + diff implications:

1. **Do NOT pre-seed `product.product` rows** when the task is "add an
   attribute line with N values" — let the template save create them.
   Pre-seeding them would double up or mismatch the auto-generated set.
2. **`product.attribute.value.match_key` must be `[attribute_id, name]`**
   — value names collide across attributes in the base snapshot (e.g.,
   the demo 'Legs' attribute has a 'Steel' value, and other attributes
   might too). Keying on `name` alone causes cross-attribute entity-key
   aliasing.
3. **State diff after a "add one attribute line with 3 values" save**
   emits exactly 9 atomic edits: `product.template.attribute_line_ids =
   [1]`, `product.attribute.create×2` (name + create_variant), and 6
   `product.attribute.value.create` rows (one `name` + one `attribute_id`
   per value). `create_variant='always'` is the default but IS in the
   diff because the attribute is a newly created record. Bake all 9 into
   `expected_state.json` for F1=1.0.
4. **Seed cleanup order matters**: to unlink a `product.attribute` that
   has been used on another template, first unlink every
   `product.template.attribute.line` referencing that attribute (across
   all templates), then `value_ids.unlink()`, then `attribute.unlink()`.
   Skipping the line unlink raises a PSQL FK error.
5. **Quick-create of both the attribute and each value works from the
   Attributes tab inline m2o / tags dropdowns** — typing a new name and
   clicking "Create" spawns the record without leaving the form, which
   is how BU completed this task single-shot in 269.7s.

See `benchmark/tasks/product.configure_variant_attribute_two_values/`.

---

## Discuss invite-by-email — no "Email tab" and SMTP is mandatory

The channel Invite People side panel (`discuss.ChannelInvitation`) has a
**single unified search input** in Odoo 19, NOT a tabbed Users/Email UI.
The envelope-icon email fallback row (`selectable_email`) appears only
when (a) the typed text fully matches `single_email_re`, (b) no
selectable partner matches, (c) `thread._allow_invite_by_email()` returns
True (`channel_type='group'` or public `channel`), (d) no existing
channel member has that email. Clicking the row + "Invite to Group Chat"
calls `discuss.channel.invite_by_email`.

`invite_by_email` calls `mail.mail.send(raise_exception=True)` **in the
same transaction**. SMTP failure → `MailDeliveryException` →
`UserError`, which HTTP dispatcher rolls back — the `mail.mail` is NOT
persisted. Seed requirements for a test that must verify the mail.mail:

1. `admin.partner_id.email` must be non-empty (else
   `_build_email__` raises `You must provide a sender address
   explicitly`).
2. Set `mail.catchall.domain` + `mail.default.from` ICPs.
3. Configure a working outgoing `ir.mail_server`. Simplest approach:
   spawn a detached `aiosmtpd` Sink Controller on `127.0.0.1:2525` from
   seed.py (`subprocess.Popen(..., start_new_session=True)`) and register
   an `ir.mail_server` pointing at that host/port. The venv already has
   `aiosmtpd` installed.

See `mail.invite_external_email_to_existing_channel/seed.py` for the
full working pattern.

---

## sale_loyalty Gift Card flow

- Quick way to create a gift-card program: `loyalty.program.create_from_template('gift_card')` (also `'loyalty'`, `'discount'`, etc.).
- `sale.order._try_apply_code` has a `loyalty.card` branch that lets a gift-card code be applied via the same `/shop/pricelist?r=/shop/cart` POST as a promo code (no separate "redeem gift card" endpoint).
- Backend menu xmlid: `/odoo/gift-cards-ewallet` (Discount & Loyalty → Gift Cards & eWallets).

## sale_loyalty free-product reward lines: discount=100, NOT price_unit=0

`sale_loyalty.sale.order._get_reward_values_product` creates a `reward_type='product'`
reward line with `price_unit = product.list_price`, `discount = 100`, and the
product's own taxes. The cart effective total is zero because of the 100%
discount — NOT because `price_unit` is zero. check.py for free-product
tasks must assert `price_subtotal` or `discount == 100`, not `price_unit`.
Distinct from `reward_type='discount'` lines, which do carry a negative
`price_unit` directly.

Auto-apply entry point: `website_sale_loyalty.Cart.cart` invokes
`order._update_programs_and_rewards()` + `_auto_apply_rewards()` on every
GET of `/shop/cart`. For a single-reward `program_type='promotion'` with
`trigger='auto'` whose rule qty condition is met, navigating to /shop/cart
is sufficient — no button/code/wizard needed.

Free-product reward JSON-RPC payload: `reward_product_id` must be a
`product.product` (variant) id, not `product.template`. Resolve via
`product.template.product_variant_id`.

---

## event_sale / website_event_sale — multi-ticket portal checkout

- **`modal_ticket_registration` counter input pattern**: for events
  with >1 `event.event.ticket`, the Tickets modal renders one row per
  ticket, and each ticket's counter input is
  `name="nb_register-<ticket_id>"` with `+`/`-` buttons carrying
  `data-input-name="nb_register-<ticket_id>"`. The row's wrapper has
  `name="<ticket_name>"` which is the easiest row selector.
- **Paid-event Attendees modal button label**: `website_event_sale`
  inherits `registration_attendee_details` and swaps the
  `Confirm Registration` submit button for `Go to Payment` whenever
  `any(ticket.price > 0)`. Selectors that match `has-text('Confirm')`
  will time out on paid events — match
  `button[type='submit'].btn-primary` instead.
- **Per-attendee heading**: `<h5>Ticket #N - <ticket_name></h5>`
  (space-dash-space) for each section. Inside each section, a hidden
  input `<input name="{counter}-event_ticket_id" value="{ticket.id}">`
  gives the `counter -> ticket id` map. Inputs for name/email/phone are
  named `{counter}-{question_type}-{question_id}` — still match by
  `name*='-name-'` substring (the suffix is the question id).
- **Wire Transfer ends the SO in `state='sent'`, NOT `'sale'`**.
  `payment_custom._apply_updates()` sets the tx to `pending`. The Sale
  override of `PaymentTransaction._post_process` then runs
  `action_quotation_sent()` on linked draft SOs, moving them to
  `sent` but NOT calling `action_confirm`. Registrations stay in
  `state='draft'` (`sale_status='to_pay'`). check.py must accept
  `state in ('sent','sale','done')` for Wire-Transfer-only flows.
- **`sale.async_emails=True` is mandatory** in the seed when the
  checkout pays via Wire Transfer in an ephemeral test DB.  Without
  it, the post-process chain calls
  `_send_payment_succeeded_for_order_mail` which runs
  `message_post_with_source(force_send=True)` synchronously. The
  missing SMTP provider raises, the cursor rolled back in
  `/payment/status/poll`, `is_post_processed` stays False, and the SO
  is stuck in `draft`. Setting the ICP
  `sale.async_emails='True'` defers the mail to a cron and lets
  `_post_process` succeed.
- **Payment providers default to `state='disabled'`**.  Seed must
  `write({'state':'enabled', 'is_published': True})` on the target
  provider. To force a deterministic payment radio (only one option
  visible on `/shop/payment`), disable every other provider in seed.
  Wire Transfer's xmlid is `payment.payment_provider_transfer`.
- **Checkout address skip**: for `try_skip_step=true` to forward
  `/shop/checkout` straight to `/shop/payment`, admin's
  `res.partner` needs the full set returned by
  `_get_mandatory_billing_address_fields` + `_get_mandatory_delivery_address_fields`
  for its country (for US that includes `state_id` and `zip`) PLUS
  name/email/phone. Missing any field triggers a redirect to
  `/shop/address` before payment.
- **Admin is not an anonymous cart**: `_is_anonymous_cart` returns
  True only when `partner_id == website.user_id.partner_id` (the
  public user).  Logged-in admin's cart's partner is NOT overwritten
  from the first attendee's name/email by
  `/event/<slug>/registration/confirm`.

---

## mail.alias on crm.team form + o_select_menu widget

- The `mail.alias` edit controls (`alias_name` + `alias_domain_id` inline inputs, `alias_contact` dropdown) are in the **Team Details** group on the main `crm.team` form — NOT in a dedicated settings panel. The block is wrapped in `invisible="not use_leads and not use_opportunities"`. Seed must enable at least one of those booleans for the fields to render.
- `alias_contact` (Selection) on `crm.team` renders as Odoo's **custom `o_select_menu` widget**, NOT a native HTML `<select>`. `oracle_helpers.set_selection` (which calls `page.locator(...).select_option(label=...)`) times out. Pattern that works:
  ```python
  page.locator(".o_field_widget[name='alias_contact'] .o_select_menu_toggler").click()
  page.locator(".o_select_menu_menu .o_select_menu_item:has-text('Authenticated Partners')").click()
  ```
- Alias-name uniqueness: `mail.alias.alias_name` has a UNIQUE constraint per domain. Seed must null out any stale alias owning the target name before re-running (otherwise the agent's Save hits `UniqueViolation`).
- `crm.lead.name` is rendered with `widget="text"` → textarea, not an input. Use `fill_text_field` in oracle, not `fill_field` (the latter queries `input` and times out).

---

## account.move.reversal wizard (Credit Note / Reverse)

- Statusbar button on a posted `account.move` is **"Credit Note"** (`button[name='action_reverse']`, `groups=account.group_account_invoice`) — NOT "Reverse". The wizard that opens is `account.move.reversal`. On `move_type='entry'` the button is labeled "Reverse Entry" instead and goes directly through `action_view_account_move_reversal`.
- **No `refund_method` radio in Odoo 19.** The 3-option radio (Partial Refund / Full Refund / Full refund and new draft) that existed in Odoo ≤16 was removed in 17+. The wizard footer now has exactly 2 buttons: **Reverse** (`btn-primary`, `name='refund_moves'`, `data-hotkey='q'`) and **Reverse and Create Invoice** (`btn-secondary`, `name='modify_moves'`, invisible when `move_type=='entry'`). The old "Partial Refund" behavior = click Reverse then edit the generated draft. Prompts must refer to buttons, not radios.
- `refund_moves` → `reverse_moves(is_modify=False)` → creates a **draft `out_refund`** credit note prefilled with copied lines + `ref='Reversal of: {source.name}, {reason}'` + `invoice_date=wizard.date` + `auto_post='at_date' if date>today else 'no'`. The agent can then edit lines (change qty, delete rows) before clicking header **Confirm** (`action_post`).
- `modify_moves` → creates the reversal AND a NEW draft invoice cloned from the source (minus payments) — the user is redirected to the new draft invoice, not a credit note. Tasks wanting the "edit credit note" flow must trace_spec `forbidden_ops: [account.move.reversal.modify_moves]`.
- Credit note `ref` is built by `_prepare_default_reversal` as `self.env._('Reversal of: %(move_name)s, %(reason)s', move_name=move.name, reason=self.reason)` — it uses source `name` (the auto-generated `INV/2026/00001`), NOT the source's `ref` Char. `expected_state.json` entity_keys for the credit note MUST match this exact pattern; if seed sets `ref='INV/BENCH/001'` the reversal ref will still be `'Reversal of: INV/2026/00001, Wrong qty'`.
- Reversal date defaults to `fields.Date.context_today`. If set to a **future** date, `auto_post='at_date'` and the header Confirm button is HIDDEN on the draft credit note — agent must either flip `auto_post` to 'No' in Other Info tab (select_menu, NOT a native select) or pick today. Tasks that say "leave date at default" sidestep this entirely.
- **Phantom-line trap on qty edit**: BU's `input(clear=True)` frequently fires `⚠️ Text field clearing failed, typing may append to existing text` on the editable list `td[name='quantity']` cell. The retry loop sometimes writes "2" into a brand-new placeholder row instead of the target row, leaving a second `account.move.line` with `display_type='product'` but `product_id=False`, `quantity=0`, `price_unit=0`. `check.py` MUST assert `len(move.invoice_line_ids.filtered(lambda l: l.display_type=='product'))==1` (or filter by `l.product_id`) to catch this — using `amount_total` alone is fooled because the phantom line has subtotal 0.
- Row-delete is the trash icon at the end of each `account.move.line` row: selectors `td.o_list_record_remove button`, `.o_list_record_remove`, `button[aria-label='Delete row']`, or (BU's hit) `button[name=delete]`. BU deletes rows reliably on the first try — the failure mode is the qty edit, not the delete.

---

## account.move type='entry' form (direct journal entries)

- Journal Entries list: `/odoo/accounting/entries` (action `account.action_move_journal_line`, context `default_move_type='entry'`). NOT the same form as invoices.
- Form differences on move_type='entry':
  - No Customer/Partner header field; `ref` is the visible "Reference" field.
  - **Journal Items** tab (`aml_tab`) replaces Invoice Lines; uses `line_ids` (not `invoice_line_ids`) with columns Account / Partner / Label / Debit / Credit / Tax Grids.
  - Header button is **Post** (not Confirm).
  - `invoice_tab` and `other_tab` are both invisible for move_type='entry'.
- `aml_tab` has `groups="account.group_account_readonly"`. If the admin user lacks that group in the base snapshot, the tab silently does not render — seed must `grp.user_ids = [(4, admin.id)]` on `account.group_account_readonly`, `group_account_invoice`, `group_account_user` to guarantee visibility. (Field is `user_ids`, not `users`.)
- `hide_post_button = state != 'draft' OR (auto_post != 'no' AND date > today)`. For a future-dated entry, keep `auto_post='no'` (default) to keep the Post button visible. `auto_post='monthly'` triggers `_copy_recurring_entries()` on post but HIDES the manual Post button until the date arrives — incompatible with a "create and post today" task.
- `line_ids` list `name` column uses widget `section_and_note_text` which renders a `<textarea>` for non-section rows (not `<input>`). Cell fillers must target `input, textarea` together.
- Account autocomplete renders items as "`<code> <name>`" (e.g. "612000 Rent"). Playwright `filter(has_text=X)` matches substrings and wrongly picks "Cur**rent** Assets" when typing "Rent". Exact-match logic: split on whitespace and compare `parts[1]` to the account name.
- Generic CoA ships "Rent" (6120, expense) and "Tax Paid" (1310, asset_current). NO "Bank" account — the default Bank journal's `default_account_id` is auto-created as `asset_cash` and inherits the journal's name ("Bank"). Seed can rename it for deterministic autocomplete.
- `mail.activity.type` for "To Do" is stored as name **"To-Do"** (with hyphen), not "To Do". `schedule_activity` helper's badge lookup needs the exact name.
- **No "General Ledger" report in Community Odoo 19** — the `account_reports` addon is Enterprise. The nearest Community equivalent for "GL → drill into an entry" is `account.action_account_moves_journal_misc` ("Miscellaneous", `res_model=account.move.line`, context `{'journal_type':'general','search_default_group_by_move':1,'search_default_posted':1,'search_default_misc_filter':1,'expand':1}`) — a grouped-by-move list. URL: `/odoo/action-account.action_account_moves_journal_misc`. Menu path: Accounting → Accounting → Miscellaneous. Group-header rows expose an anchor that navigates to the underlying `account.move` form when clicked. Tasks that ask "reverse the entry from the GL" must recast as "from the Miscellaneous Journal Items report" (or use the flat Journal Entries list at `/odoo/accounting/entries`). Same pattern applies for `action_account_moves_all_grouped_matching`, `action_account_moves_journal_sales`, `action_account_moves_journal_purchase`, and `action_account_moves_journal_bank_cash`.
- The `Reverse Entry` wizard's form-view binding: `action_view_account_move_reversal` has `binding_view_types="list,kanban"` — it appears as a cog Actions entry when `account.move` records are multi-selected in a list/kanban, but is **NOT** in the form-view cog Actions menu. On a single posted `move_type='entry'` form, the reversal access path is exclusively the header statusbar button **Reverse Entry** (`name="%(action_view_account_move_reversal)d"`, `invisible="move_type != 'entry' or state != 'posted' or payment_state == 'reversed'"`, `groups="account.group_account_invoice"`). Tasks phrased as "cog Actions → Reverse" should clarify list-vs-form context or route through the list/kanban view selection.
- `account.move.reversal.refund_moves` when `reason` is empty (hidden for `move_type='entry'`) produces a reversal with `ref='Reversal of: <source.name>'` — no trailing comma, no reason suffix. Compare to the invoice path where `ref='Reversal of: <source.name>, <reason>'`. Use the entry pattern (no suffix) in `expected_state.json` entity keys for misc-entry reversal tasks.

---

## Discuss canned-response (`mail.canned.response`) seeding quirks

- Delimiter is **`::` (double colon)**, NOT `:hello`. Single colon triggers the
  emoji picker (`suggestion_service.js::searchSuggestions` — case `":"` dispatches
  to `loadEmoji()`). Prompt / oracle must type `::hello` explicitly.
- `/mail/data` endpoint (`webclient.py`) filters canned responses by
  `create_uid = env.user.id OR group_ids in user.all_group_ids.ids`. Odoo shell
  runs as `__system__` (id=1), NOT admin (id=2), so a naive
  `env["mail.canned.response"].create({...})` yields a record the admin agent
  cannot see via Discuss. Fix:
  ```python
  env["mail.canned.response"].with_user(admin).create({
      "source": "hello",
      "substitution": "...",
      "group_ids": [(6, 0, [env.ref("base.group_user").id])],
  })
  ```
- Suggestion fetch is debounced 250 ms; wait ≥ 800 ms after typing `::` before
  expecting the `.o-mail-NavigableList-item` popover.
- Livechat sidebar category `im_livechat.channel.appCategory` has
  `hideWhenEmpty: !are_you_inside` — the seed livechat channel MUST list the
  admin in `user_ids` else the sidebar category is collapsed/hidden and the
  session is unreachable via UI.
- `discuss.channel` with `channel_type='livechat'` has a CHECK constraint
  requiring `livechat_operator_id`. Minimum viable seed vals include
  `livechat_channel_id`, `livechat_operator_id`, and both admin + visitor
  `channel_member_ids`.

---

## appointment addon is enterprise-only — uninstallable in Community

`appointment` (and by extension `website_appointment`,
`appointment_account_payment`, `appointment_hr`,
`appointment_sms`, `appointment_crm`, etc.) is an **enterprise-only**
module.  On the `odoo_benchmark` branch it registers in
`ir_module_module` as `state='uninstallable'` because no manifest is
found under any configured addons path.

- `button_immediate_install()` on an uninstallable record raises
  `UserError` — you cannot "install on demand".
- `calendar.event` is NOT a drop-in substitute for public booking
  tasks: `/calendar/meeting/view` only exposes Accept/Decline; no
  Reschedule / Cancel / public slot picker.
- Before picking any `appointment.*` or `/appointment/*` task from the
  backlog, run:
  ```sql
  SELECT name, state FROM ir_module_module WHERE name LIKE 'appointment%';
  ```
  If any row is `uninstallable`, mark the task Removed with Oracle
  `FAIL (module unavailable)` and skip the full lifecycle — match the
  precedent in STATUS.md rows 240 (`appointment.create_type_set_slots`)
  and 350
  (`appointment.public_booking_reschedule_cancel_portal`).

---

## MTO + Buy auto-RFQ (sale_purchase_stock) seed recipe

Confirming a sale order for an MTO-routed storable product auto-generates a
draft RFQ for the first-sequenced `product.supplierinfo` vendor.  The
procurement chain is silent — if the seed is misconfigured, `action_confirm`
succeeds but no PO appears, and the failure is invisible without a sanity
probe.  Required seed steps:

1. `env.ref("stock.route_warehouse0_mto").active = True` — MTO ships
   `active=False` in fresh DBs.
2. `env.ref("purchase_stock.route_warehouse0_buy").product_selectable = True` —
   Buy ships `product_selectable=False` (warehouse-level); flip it so the
   product can carry both MTO and Buy in `route_ids`.
3. `main_wh.buy_to_resupply = True` then
   `main_wh.write(main_wh._create_or_update_route())` — rebuilds the
   `mto_pull_id` rule on the warehouse after toggling MTO active.
4. `mto_route.rule_ids.write({"procure_method": "make_to_order"})` — paranoid:
   ensures MTO rules push procurement upstream rather than fall back to
   make_to_stock.
5. Product must be `type='consu' + is_storable=True`, with
   `route_ids=[mto_route, buy_route]` and ≥1 `product.supplierinfo`.  First
   seller by `sequence` is picked for the auto-generated RFQ.

**MTO-generated `purchase.order.line` does NOT carry `sale_line_id`** (that
field is only populated for dropship; see the
`if not values.get('move_dest_ids')` guard in
`sale_purchase_stock/models/purchase_order.py::_prepare_purchase_order_line_from_procurement`).
The SO↔PO linkage goes through `stock.reference.purchase_ids` (the
`sale_purchase_stock.sale_order._get_purchase_orders` override unions it
into the set returned by the `sale_purchase` bridge).  For check.py / seed
sanity: search POs via `purchase.order.origin == SO.name`, NOT via
`order_line.sale_line_id.order_id`.

**Changing `partner_id` on the draft MTO-generated RFQ silently recomputes
line `price_unit`** via `purchase.order.line._compute_price_unit_and_date_planned_and_name`.
No wizard / no confirmation prompt appears even when the new vendor's
supplierinfo price differs from the old one.

**State-diff `match_key: [partner_id]` on purchase.order** treats a vendor
swap as `delete(old_partner_key) + create(new_partner_key)` — NOT a single
`set` edit.  expected_state.json must encode both operations if the underlying
PO record is just mutating its partner_id.

---

## website_hr_recruitment / hr.job publish + preview

- `hr.job.website_description` is **frontend-only**: the only view that
  touches it is `<div t-field="job.website_description"/>` in
  `/jobs/detail/<slug>` (template
  `website_hr_recruitment.detail`). There is NO backend form field for
  it, so the only UI edit path is the website WYSIWYG overlay (fragile
  iframe). Tasks that need a specific Requirements/section content
  should **pre-seed** the HTML in `seed.py` and instruct the agent
  NOT to touch it; let `check.py` assert tokens via `html2plaintext`.
- `hr.job.description` IS on the backend form — on the Summary
  notebook tab (`<page name="job_description_page">`). Standard
  in-page HTML editor (not iframe); BU can type into it reliably.
- The `website_published` **Published** `boolean_toggle` on the job
  form has an explicit `@api.onchange('website_published')` handler
  (`addons/website_hr_recruitment/models/hr_job.py`) that mirrors the
  value to `is_published`. A single user click flips BOTH fields —
  both show up in `state_diff.json` as `op: "set"`.
- The `is_published` field rendered in the button box is
  `widget="website_redirect_button"` — it only navigates to
  `/jobs/<slug>` for preview; it is NOT a publish toggle
  (same pattern as `event.event` / `event.track`).
- Put both `description` and `website_description` in
  `state_spec.yaml` `ignore_fields`; the HTML diff is noisy on
  whitespace and sanitizer tweaks. Validate via `check.py` using
  `html2plaintext` substring checks.

---

## hr_recruitment_survey — Interview Form attach + Send Interview button

- `hr_recruitment_survey` is **NOT in the base snapshot**; seed must
  `button_immediate_install()`. Adds `hr.job.survey_id`
  (m2o → `survey.survey`, label "Interview Form") and
  `hr.applicant.survey_id` (`related='job_id.survey_id'`, readonly).
- The Interview Form m2o renders inside the Recruitment notebook tab
  (page name `recruitment_page`, XML string "Details") under the
  Hiring Process group and carries
  `domain="[('survey_type','=','recruitment')]"`. Surveys seeded with
  the default `survey_type='custom'` **do not appear** in the
  autocomplete — seed must set `survey_type='recruitment'`.
- The header **"Send Interview"** button on the applicant form has
  `invisible="not active or not survey_id"`. Attaching a survey at
  the job level is sufficient to reveal it; no applicant write is
  needed (related field propagates through the job link).
- The hr.job kanban card exposes a hidden `action_new_survey` menu
  item ("Interview Form" under New) that auto-creates a blank
  `survey.survey` titled `Interview Form: <job name>` and links it
  via the kanban menu `t-if="!record.survey_id.raw_value"` branch.
  Tasks that want the agent to **pick an existing** survey should
  forbid `hr.job.action_new_survey` (and `survey.survey.create`) in
  `trace_spec.yaml` so a BU that clicks the wrong menu doesn't get a
  cheap pass.
- `/odoo/recruitment` default kanban card click opens
  `action_hr_job_applications` (applicants), **not** the job form.
  UI paths to the job form: (a) viewswitcher → list → click row
  (BU empirically finds this first), or (b) kanban card 3-dots menu
  → "Configuration" (`type="open"`). No form-view kanban button.

---

## hr_recruitment — Applications kanban entry + quick-create fields

- `hr.applicant` kanban view `hr_kanban_view_applicant` has
  `default_group_by="stage_id"` and `quick_create_view="hr_recruitment.quick_create_applicant_form"`.
  The quick-create view exposes ONLY `partner_name` + `job_id`. To
  set `email_from`, `partner_phone`, or any other applicant field,
  the user/oracle MUST click the newly-created card to reach the
  full form after the quick-create commits. Tasks that require
  `email_from` / `partner_phone` values cannot be completed inside
  the quick-create dialog alone.
- Per-column `+` button in the Applications kanban is
  `button.o_kanban_quick_add` inside `.o_kanban_header`. Confirming
  the quick-create uses `button.o_kanban_add` (green check). The
  `hr.applicant` form's status-bar widget is
  `rotting_statusbar_duration` with `options="{'clickable': '1'}"`
  on `stage_id`, so each stage pill is a direct-click stage write.
- Default Odoo 19 demo stages are `New`, `Qualification`, `First
  Interview`, `Second Interview`, `Contract Proposal`, `Contract
  Signed` (sequences 0..5, all global — `job_ids=[]`). Tasks that
  want a custom 4-column pipeline must (a) create new
  `hr.recruitment.stage` rows with explicit sequences AND (b) pin
  them to the job via `job_ids=[(6, 0, [job.id])]`. Global stages
  (empty `job_ids`) are visible to every job, so without pinning the
  Applications kanban mixes seeded + global columns.
- Stage-name collisions between seeded and global records (e.g.
  `Contract Proposal`, `Contract Signed`) are safe as long as the
  seeded copies have `job_ids` containing the task's job — the
  kanban renders the job-scoped record, and `search([('name', '=',
  ...), ('job_ids', 'in', [job.id])])` uniquely targets the seeded
  stage.

---

## maintenance.equipment — field inventory & duplicate-create BU failure

- `maintenance.equipment` has **no `next_action_date`** field (not in Python
  or XML; only stale `.po` translation strings). Writable date fields are
  `effective_date`, `warranty_date`, `assign_date`, `scrap_date`. The
  Maintenance tab's `estimated_next_failure` / `latest_failure_date` /
  `mtbf` / `mttr` are all computed/readonly. `expected_mtbf` (Integer) is
  the writable sibling.
- `maintenance.equipment.category._unlink_except_contains_maintenance_requests`
  prevents delete while any equipment / request references the category.
  Seed cleanup order: delete equipment first, then guard-unlink the
  category only if `equipment_ids` and `maintenance_ids` are both empty.
- **Two-phase save failure mode** (save equipment, then reopen to set one
  more field): browser-use consistently creates a duplicate record on the
  second phase instead of re-editing the saved one. Reliable medium-tier
  trap without any wizard. `check.py` must assert `len(equipment) == 1`
  — the diff engine alone won't catch the duplicate because `match_key:
  [name]` produces two distinct "create" groups that both match
  expected_state.json partially. See
  `maintenance.create_equipment_schedule_preventive_plan`.

---

## DateTimeField widget: button vs input dual rendering

`addons/web/static/src/views/fields/datetime/datetime_field.xml` renders the
`DateTimeField` as a `<button class="o_input">` showing the formatted value
whenever the field has a value AND `picker.activeInput !== field`. Clicking
the button sets `picker.activeInput = field`, which re-renders as an
`<input>`. Playwright selectors that target `.o_field_widget[name='X'] input`
time out on any pre-populated datetime.

Correct oracle pattern:

```python
widget.locator("button, input").first.click()  # flip button → input
page.wait_for_timeout(400)
inp = widget.locator("input").first
inp.wait_for(state="visible", timeout=5000)
inp.fill("")
inp.type("04/17/2026 00:00:00", delay=20)
page.keyboard.press("Escape")           # close picker popover
dialog.locator(".modal-title").click()  # commit
```

Applies to every datetime field with a seeded default (e.g., `stock.lot.expiration_date` when `product.template.expiration_time > 0` auto-fills the date at lot-create time via `_compute_expiration_date`). Also applies on the existing `oracle_helpers.set_datetime` helper path — if a task needs to overwrite a pre-populated datetime in headless, inline the button-click step.

---

## product_expiry module quirks

- **Not in base snapshot** — seed must `button_immediate_install()` on the `product_expiry` module record (depends only on `stock`). Adds `use_expiration_date`/`expiration_time`/`use_time`/`removal_time`/`alert_time` (Integer days) to `product.template`, and `expiration_date`/`use_date`/`removal_date`/`alert_date` (Datetime) on `stock.lot`.
- **Receipts picking type needs BOTH `use_create_lots=True` and `use_existing_lots=True`** for the Detailed Operations popup to expose a `lot_id` m2o (with autocomplete Create + internal-link button). `use_create_lots` alone gives text-only `lot_name` (no path to the stock.lot form); `use_existing_lots` alone hides the Create option. Both True → m2o widget with Create + open.
- **Clicking the m2o internal-link arrow inside a dialog opens a NESTED `<div class="modal">`** (not a new action) because `many2one.xml` routes `openRecord('dialog')` when `env.inDialog=True`. Multiple visible modals — identify the lot dialog by the presence of `.o_field_widget[name='expiration_date']`, not `.last`.
- **`stock.lot._compute_dates` shifts `use_date`/`removal_date`/`alert_date` every time `expiration_date` changes.** On a fresh write, these start at `expiration_date - template.{use,removal,alert}_time`. On re-write they get shifted by the `expiration_date` delta. So oracle must set `expiration_date` BEFORE `removal_date` — writing removal first gets clobbered.
- **`stock.lot.display_complete`** is True iff the lot `id` is set OR the context has `display_complete=True`. When opened as a nested-dialog from a popup m2o, `id` is truthy (the lot was created on the fly), so the full form renders (Dates group + expiration_date after ref). No extra context plumbing needed.

---

## website_slides — publish / prerequisite / attendees gotchas

- `slide.channel.prerequisite_channel_ids` field renders as
  `widget="many2many_tags"` with domain
  `[('id', '!=', id), ('visibility', '=', visibility), ('website_published', '=', website_published)]`.
  The dropdown is empty until **both** form-state conditions are applied
  live on the current record: visibility matches the candidate and
  `website_published` matches. A task that seeds the prereq as
  `members + published=True` requires the agent to flip visibility to
  `members` AND publish BEFORE touching the prereq field — otherwise the
  autocomplete silently yields nothing.
- `slide.channel.is_published` in the backend form uses
  `widget="website_redirect_button"` (navigation-only, same RedirectField
  component as event.event). The backend form CANNOT publish — only
  (a) the frontend `/slides/<slug>` Owl systray Unpublished/Published
  toggle (calls `website_publish_button`) or (b) toggling the list-view
  `is_published` boolean cell.
- `slide.channel._compute_enroll` auto-coerces `enroll='invite'` when
  `visibility=='members'` (backed by a DB CHECK constraint). Writing
  `{visibility: 'members'}` alone is sufficient — do not also write
  `enroll` in the same call unless you want to be explicit.
- `slide.channel.user_id` defaults to `self.env.uid`. Seeds run under
  SUPERUSER_ID (id=1, partner_root / OdooBot), so a `create()` without
  explicit `user_id=admin.id` ends up calling `_action_add_members` on
  the OdooBot partner and enrolling it as an attendee. Fix: pass
  `user_id=admin.id` OR unlink `slide.channel.partner` residue right
  after create; check.py counts exactly the task-added rows otherwise.
- `slide.channel.invite` wizard (opened by the `Add Attendees` /
  `Invite` header buttons) has `_compute_send_email =
  channel_visibility != 'public' or enroll_mode`. The toggle is
  `invisible="enroll_mode or channel_visibility != 'public'"`, so with
  `visibility='members'` (or any enroll_mode=True opening) you CANNOT
  uncheck send_email. The wizard calls `mail.mail.send` and the
  transaction rolls back (no `slide.channel.partner` row persisted) if
  SMTP fails. Same aiosmtpd sink pattern as the discuss invite-by-email
  cookbook applies.
- `slide.channel.partner` list view has `create="0"` — no "New" button.
  The only supported UI path to add attendees is the wizard (forcing
  email). Oracle scripts should `slide.channel.partner.create(...)`
  directly via JSON-RPC; `slide.channel._action_add_members` is
  underscore-prefixed and blocked by `call_kw`'s private-method guard.
- Browser-use failure mode: `many2many_tags` with autocomplete — BU
  often types the term and then moves on without clicking the popover
  option, leaving the m2m empty. Since state_spec usually leaves m2m
  out (noisy diffs), the postcondition check must explicitly assert
  the m2m membership.

---

## mrp_subcontracting — receipt + auto-MO chain

- **Module not in base**: `mrp_subcontracting` AND its auto-install-gated
  bridge `mrp_subcontracting_purchase` are NOT in
  `benchmark/base_modules.txt`. Seed must `button_immediate_install` both
  before creating any subcontract BoM or confirming a subcontracting PO.
- **Phantom "Resupply Subcontractor" picking on PO confirm**:
  `stock.warehouse.subcontracting_to_resupply` defaults to **True**, so
  confirming a subcontracting PO auto-generates TWO pickings sharing the
  same `origin`: the incoming Receipt (`WH/IN/…`) AND an internal
  `Resupply Subcontractor` picking (`WH/RES/…`) that wants to push
  components from WH/Stock → Subcontracting location. If the task
  pre-stocks components directly at the subcontracting location, the
  resupply picking is spurious and breaks `click_list_row(PO_NAME)`
  (matches both rows). Fix: seed
  `env["stock.warehouse"].search([]).write({"subcontracting_to_resupply": False})`.
- **Subcontract BoM wiring**: `mrp.bom.type='subcontract'` (Selection
  extension) + `subcontractor_ids` (m2m `mrp_bom_subcontractor`) are
  both required — view XML makes `subcontractor_ids` required when
  `type='subcontract'`. `_bom_subcontract_find` uses `'parent_of'`
  matching on subcontractor so a child contact still resolves.
- **Subcontracting location resolution**:
  `partner.with_company(env.company).property_stock_subcontractor` with a
  company fallback `env.company.subcontracting_location_id`. Needs
  `stock.group_stock_multi_locations` on admin for the
  Subcontracting location to render in the UI + `stock.group_production_lot`
  for the Detailed Operations popup's `lot_id` columns.
- **Serial-tracked finished → MO splitting**: with `tracking='serial'`
  on the finished subcontracted product and `product_qty>1`, validating
  the receipt triggers `_sync_subcontracting_productions._split_productions`
  → the single initial MO becomes **N done MOs** (one per serial/lot).
  `expected_state.json` must encode the extras with `#dup1`, `#dup2`, …
  entity-key suffixes (the diff engine's collision marker) + `op=create`.
  The first MO stays on its original key with `op=set`.
- **Receipt picking type lot-creation flags**: for the Detailed
  Operations popup's `lot_id` autocomplete to expose a
  `Create "<serial>"` option, the incoming picking type needs BOTH
  `use_create_lots=True` AND `use_existing_lots=True`. Without the
  former, the `lot_name` Char input is hidden; without the latter, the
  `lot_id` autocomplete is hidden.
- **Subcontract move `action_show_details`** returns the
  `mrp_subcontracting_view_stock_move_operations` view (not the vanilla
  stock one) — same button selector
  (`button[name='action_show_details']:visible` on the move row) but the
  popup layout exposes `order_finished_lot_ids` on the move and an
  editable move_line_ids list in the lower half.
- **No user-facing "Record Production" button on the backend receipt**
  form for backend (internal) users. The portal view has a `Register
  components for subcontracted product` button, but the backend shows
  only the `Subcontracting Productions` smart button in the button_box,
  and it's invisible until `move.show_subcontracting_details_visible`
  (`is_subcontract AND move_line_ids AND quantity > 0 AND MO state !=
  cancel`). The canonical flow is: open Details on the move → fill
  move_lines → validate — the smart button is optional drill-down.

---

## pos_restaurant — install on demand, auto-floor, course.fired is the "ready" flag

- `pos_restaurant` is NOT in `benchmark/base_modules.txt`. Seeds must
  `button_immediate_install()` the `pos_restaurant` `ir.module.module`
  row before using `restaurant.floor` / `restaurant.table` /
  `restaurant.order.course` or setting
  `pos.config.module_pos_restaurant=True`. Depends on `point_of_sale`
  (already in base).
- `pos.config._setup_default_floor` fires on both create and write
  whenever `module_pos_restaurant=True`, auto-creating a
  `restaurant.floor` named after the company and a single
  `restaurant.table` with `table_number=1`. To control deterministic
  floor/table identity, seed must: (1) create the config, (2) capture
  `config.floor_ids`, (3) `config.write({"floor_ids": [(5, 0, 0)]})` to
  detach, (4) unlink the orphan tables + floor, (5) create the desired
  `restaurant.floor` / `restaurant.table` and link via
  `pos_config_ids`. Order matters: the floor's `ondelete` guard
  (`_unlink_except_active_pos_session`) blocks unlink while any of its
  `pos_config_ids` has a non-closed session, so do all of this BEFORE
  `env["pos.session"].create({"config_id": config.id})`.
- Odoo 19 Community has **no** `kitchen_done` or explicit `ready` flag
  on `pos.order`. The per-course kitchen-ready signal is
  `restaurant.order.course.fired` (Boolean, default False) with an
  auto-set `fired_date` when `fired` flips True and no date was set.
- Courses are NOT auto-created on line add. They exist only after the
  user clicks the **Course** control button (`this.pos.addCourse()`),
  which wraps existing lines into Course 1 + creates an empty Course 2.
  If no course exists when the Send/Order button is clicked,
  `order.getFirstCourse()` returns undefined and the
  `firstCourse.fired=true` side effect in
  `sendOrderInPreparationUpdateLastChange` is skipped.
- Two UI paths set `course.fired=True`: (a) clicking the primary
  action-pad **Send** button (class `.submit-order`, labelled with the
  per-category count summary) fires the first non-fired course on the
  order via `sendOrderInPreparationUpdateLastChange`; (b) clicking the
  explicit **Fire Course N** button (class `.fire-btn`) which replaces
  the Payment button only when `getCourseToFire()` returns a non-empty
  not-yet-fired course (usually after all in-flight lines have already
  been sent). The `Fired` badge in the course header is the visual
  confirmation (`rounded text-bg-info` span inside `.order-course-name`).
- `pos.order.pos_reference` is auto-generated per run as
  `<pos_config_id>-<pos_session_id>-<nnnnnn>`. Do NOT use it as a
  state-diff `match_key` when oracle and browser-use both create
  orders — the strings diverge and F1 drops to zero on an otherwise
  successful BU run. Use `table_id` (which normalises to the display
  `<floor.name>, <table_number>`, e.g. `"Main Floor, 1"`) as a stable
  cross-run key.
- `restaurant.table._compute_display_name` returns
  `f"{floor.name}, {table_number}"` — NOT `"T<n>"` or a prefix form.
  The kiosk floor-plan tile shows ONLY `table_number` as its label.
- Browser-use calibration: a single-shot run of the open-table +
  split-course + fire-course-1 flow PASSES in ~100s on a clearly
  labelled kiosk UI. Restaurant POS is not by itself a hard pattern;
  harden via split-bill, transfer-merge, non-default course picks,
  guests count, or cash reconciliation with a deliberate mismatch.

---

## website_customer / res.partner customer-reference publish

- `website_customer` is NOT in the base snapshot. Seed must
  `button_immediate_install()` — dependencies pulled transitively are
  `website_crm_partner_assign` and `website_partner`.
- `/customers` controller domain (in
  `addons/website_customer/controllers/main.py`) is
  `[('website_published', '=', True), ('assigned_partner_id', '!=', False)]`.
  A res.partner MUST have BOTH `website_published=True` AND a non-
  empty `assigned_partner_id` ("Implemented by") to render on the
  public list. Seeds that publish but forget `assigned_partner_id`
  will pass check.py for the publish flip but fail the "visible on
  /customers" assertion.
- `/partners/<slug>` (from `website_partner.partners_detail`)
  renders for unpublished partners IFF the visitor has
  `website.group_website_restricted_editor` (admin does). This
  enables the "click Go to Website from the unpublished form, land
  on the preview, then flip the Owl systray toggle" workflow —
  admin can preview-then-publish in one chain without needing to
  publish first to see the page.
- `res.partner.is_published` on the backend form uses
  `widget="website_redirect_button"` (from
  `addons/website_partner/views/res_partner_views.xml`). Like
  `event.event` / `hr.job` / `slide.channel`, this button is
  NAVIGATION-ONLY — it calls `open_website_url` and navigates to
  the `website_url`; it does NOT toggle `is_published`. The button's
  visible text is always "Go to Website" with a red (unpublished)
  or green (published) globe icon; the aria-label / title reflect
  the current state ("Unpublished" / "Published"). Canonical
  Playwright selector:
  ```python
  page.locator(".o_field_website_redirect_button button, "
               ".o_field_widget[name='is_published'] button").first
  ```
- Seed cleanup must null out `assigned_partner_id` back-references
  before unlinking implementer partners, else FK constraints from
  `website_crm_partner_assign` block the unlink:
  ```python
  referring = env["res.partner"].with_context(active_test=False).search([
      ("assigned_partner_id", "in", old_partners.ids),
  ])
  if referring:
      referring.sudo().write({"assigned_partner_id": False})
  old_partners.sudo().unlink()
  ```

---

## stock_landed_costs — module install, picking domain, FIFO categ, two-button flow

- **Not in base snapshot** — seed must `button_immediate_install()` on the
  `stock_landed_costs` module record before referencing the
  `stock.landed.cost` model. Guard downstream seed ops with
  `if "stock.landed.cost" not in env.registry` to survive a partial install.
- `stock.landed.cost.picking_ids` many2many_tags field domain requires
  `move_ids.is_in != False OR move_ids.is_out != False`. `stock.move.is_in`
  (added by `stock_account`) is a stored Boolean that flips True only when
  `move.state == 'done'` and the move is net-incoming. So the seeded
  receipt MUST be validated (`button_validate` with `skip_backorder=True`
  and `move.quantity` + `move.picked=True` pre-set) or the Transfers
  autocomplete silently returns zero rows.
- `stock.landed.cost.get_valuation_lines` skips moves whose
  `product.cost_method` is not in `('fifo', 'average')`. The default
  company `cost_method` is `'standard'`, so a product with no special
  category yields Compute → 0 adjustment lines → Validate raises
  `"Cost and adjustments lines do not match."` Seed a dedicated
  `product.category` with `property_cost_method='fifo'` (and
  `property_valuation='periodic'` to avoid needing stock journal /
  valuation / price-diff accounts — `real_time` requires those three
  on the category or validate crashes at `_create_accounting_entries`).
- `product.template.landed_cost_ok` + `split_method_landed_cost` are
  **invisible** on the product form when `type != 'service'`. They're
  writable via JSON-RPC regardless, but a UI-driven task that
  toggles "Is a Landed Cost" MUST have `type='service'` first.
- **Compute is a footer button**, not a header action. It lives inside
  the Additional Costs tab in the `oe_subtotal_footer` group as
  `<button name="compute_landed_cost" class="float-end btn-secondary"/>`.
  Agents / oracles that target "Validate" via `.o_statusbar_buttons
  button` and never call Compute hit the "Cost and adjustments lines
  do not match" UserError.
- **Validate (`button_validate`) requires a persisted record**. On a
  dirty new form in Odoo 19 Owl, clicking Validate is a no-op. Oracle
  must click `.o_form_button_save` first (if visible), THEN click
  `.o_statusbar_buttons button[name='button_validate']`.
- **DO NOT use `button.o_form_button_create` as a Validate fallback
  selector**. `.o_form_button_create` is the top-bar "New" (plus
  icon) button. Including it in an OR-selector for Validate makes
  Playwright click "New" on the saved record, creating a phantom
  `stock.landed.cost` with `amount_total=0` and poisoning the
  state_diff.
- `stock.landed.cost.lines.onchange_product_id` stamps
  `split_method = product.product_tmpl_id.split_method_landed_cost or
  line.split_method or 'equal'` — so the cost line inherits the
  Freight-product default (e.g. `by_quantity`) on product pick. Tasks
  that assert a specific split_method should pre-seed
  `split_method_landed_cost` on the service product template AND
  assert the cost-line value in `check.py`.
- `compute_landed_cost()` calls
  `AdjustementLines.search([('cost_id','in', self.ids)]).unlink()`
  at the top, so clicking Compute twice is safe — each call rebuilds
  the valuation adjustment lines from scratch.
- URL for the list action is `/odoo/landed-costs`
  (`action.path='landed-costs'`, xmlid `stock_landed_costs.action_stock_landed_cost`).
  Menu path is Inventory > Operations > Adjustments > Landed Costs.

---

## hr_skills_survey is Community-limited: no hr.skill.survey_id

Odoo 19 Community ships `hr_skills_survey` as an auto-install bridge
between `hr_skills` and `survey`, but the Community version does NOT
add a `survey_id` field on `hr.skill`. The bridge only extends:

- `hr.resume.line.survey_id` — Many2one('survey.survey'), **readonly**,
  populated automatically by `survey.user_input._mark_done()` when a
  user submits a passing certification response (see
  `addons/hr_skills_survey/models/survey_user.py`).
- `survey.survey.certification_validity_months` — Integer (months
  validity after passing).

No module in `addons/` declares `_inherit = 'hr.skill'` adding a
survey Many2one — verified via:

```python
"survey_id" in env["hr.skill"]._fields   # False in Community
```

Implications for task authors:

- Tasks of the form "open a skill, pick a certification survey in its
  Certification field" are **Enterprise-only** and should be filed as
  BLOCKED (precedent: row 387
  `hr_skills_survey.link_certification_survey_to_skill`).
- The side-effect path (take a certification survey as admin → resume
  line appears via `_mark_done()`) IS available in Community, but the
  `survey_id` on the resume line is readonly, so any task asserting it
  must drive the change through a full survey-submission flow rather
  than a UI field write.
- Before taking a backlog task that touches `hr.skill` ↔ survey linkage,
  probe `env["hr.skill"]._fields` for `survey_id` (or grep
  `_inherit.*hr\.skill` across addons) and mark Removed if absent.

---

## sale_management — quotation template feature group + auto-populate onchange

- `sale_management.group_sale_order_template` gates BOTH the
  **Sales > Configuration > Quotation Templates** menu AND the
  **Quotation Template** (`sale_order_template_id`) field on the
  `sale.order` form. Seeds that want either surface visible must
  `group.sudo().write({"user_ids": [(4, admin.id)]})`. The Sales
  Settings checkbox labelled "Quotation Templates" just toggles this
  same group.
- Direct action URL for the templates list:
  `/odoo/action-sale_management.sale_order_template_action`.
- `sale.order.template` Lines tab uses the `so_template_line_o2m` widget
  (a `SectionAndNoteListRenderer` extension) over a standard
  `<list editable="bottom">`. Cell field names in the list are
  `product_id`, `name`, `product_uom_qty`, `product_uom_id` — NOT
  `product_template_id` (the `sol_o2m` widget on `sale.order` uses
  `product_template_id` in its list but `sale.order.template` does NOT).
- Setting `sale.order.sale_order_template_id` fires the
  `_onchange_sale_order_template_id` hook which **clears** existing
  `order_line` and recreates one `sale.order.line` per
  `sale.order.template.line` via `_prepare_order_line_values()`. One
  m2o pick fully populates the lines — no per-line data entry needed.
- `sale.order.sale_order_template_id` uses
  `options="{'no_create': True}"` and is
  `readonly="state in ['cancel', 'sale']"`. Quick-create is disabled;
  the template must already exist before the SO form loads.
- `sale.order.template.display_name` is just `name` (NO currency suffix
  like pricelists have). `expected_state.json` entries that target
  `sale.order.sale_order_template_id` use the bare template name.
- `sale.order.template.name` renders inside the `oe_title` H1 block,
  but the field name is still `name` — standard
  `fill_field(page, "name", "...")` works.

---

## stock_sms — delivery SMS feature + post_init hook trap

- `stock_sms` is `auto_install=True` with `depends=[stock, sms]`.
  Neither `sms` nor `stock_sms` is in `benchmark/base_modules.txt`, so
  seeding `sms` alone via `button_immediate_install()` pulls
  `stock_sms` in transitively.
- The feature is a pair of **company-dependent** fields on
  `res.company`: `stock_text_confirmation` (Boolean) and
  `stock_confirmation_type` (Selection, only value `'sms'`). There is
  NO `stock.picking.type.sms_confirmation` field — the SMS delivery
  notification is NOT per-picking-type, it is per-company.
- The Settings path is **Inventory > Configuration > Settings >
  Operations block > Text Confirmation** (setting id
  `stock_text_confirmation` in the view). Action:
  `stock.action_stock_config_settings`.
- `stock_sms.__init__._assign_default_sms_template_picking_id` is a
  **post_init_hook that unconditionally sets
  `res.company.stock_text_confirmation=True`** on every company where
  the field was False, as long as the default SMS template exists
  (which it always does — it's loaded from `data/sms_data.xml`).
  Tasks that want the agent to flip the toggle through the UI MUST
  reset `company.stock_text_confirmation=False` in seed AFTER
  `button_immediate_install` runs, otherwise the Settings step is a
  no-op.
- `res.company.has_received_warning_stock_sms` gates the
  `confirm.stock.sms` warning wizard shown on the FIRST validate after
  the feature is enabled. Reset it to False in seed if you want the
  wizard to appear.
- Warning wizard buttons: **`name='send_sms'`** (*Confirm*, primary,
  highlighted) → sets `has_received_warning_stock_sms=True`, re-invokes
  `button_validate()` which then emits the SMS via
  `_send_confirmation_email` → `_message_sms_with_template` →
  `_notify_thread_by_sms`. **`name='dont_send_sms'`** (*Disable SMS*,
  secondary) → sets `has_received_warning_stock_sms=True` AND
  `stock_text_confirmation=False`, re-invokes validate which proceeds
  without emitting the SMS. This is a natural side-effect-trap
  distractor for medium tasks.
- Playwright selector for the primary button:
  `.modal:visible button[name='send_sms']` (safer than matching
  "Confirm" text — localization-safe + avoids collisions with other
  generic Confirm buttons).

## `res.company` entity_key normalizes to [null] in state_diff

- Even with `state_spec.yaml.res.company.match_key: [name]`, the state
  diff engine emits `"entity_key": [null]` for the singleton main
  company. Root cause: `_extract_entity_key` calls
  `getattr(record, "name", None)`, which on `res.company` comes back
  as `False` / `None` through the instrumentation cursor in some
  snapshot flows (company_dependent / related-field read paths). The
  current workaround in `expected_state.json` is to use
  `"entity_key": [null]` literally — verified against
  `stock_sms.enable_delivery_sms_notification_validate`'s observed
  `state_diff.json`.

---

## project.milestone — gating + embedded action entry point

- `project.milestone` is gated per-project by
  `project.project.allow_milestones` (Boolean, default False on fresh
  `create()`). Seed must explicitly set `allow_milestones=True` or the
  Milestones entry point is hidden AND the per-task `milestone_id` field
  is `invisible="not allow_milestones"` on the task form group.
- Visibility also requires `project.group_project_milestone`. In Odoo 19
  the group is implied by `base.group_user` via
  `addons/project/data/project_demo.xml`, so admin inherits it in a clean
  base snapshot. Seeds for milestone-heavy tasks should still idempotently
  add admin to the group to survive snapshot churn.
- **Entry point is an `ir.embedded.actions` record**
  (`project.project_embedded_action_project_milestones`) whose
  `parent_action_id` is
  `project.act_project_project_2_project_task_all`. It surfaces as a
  **"Milestones" breadcrumb button in the project's task view's Top Menu**,
  NOT as a tab on the `project.project` form. The project card's
  kebab menu on the dashboard also exposes a View > Milestones option.
  Browser-use consistently struggles to discover either path: in the
  calibration run for
  `project.create_milestone_assign_tasks_reach` BU spent 27+ steps
  clicking the wrong menu items before landing on the embedded panel.
- `project.milestone.is_reached` (Boolean, `default=False`,
  `copy=False`): on a record created-and-set-True inside the same task,
  the state-diff engine folds to a single `op: "create"` with
  `norm_value: true`. Partial-failure runs emit
  `op: "create"` with `norm_value: null` (same null-vs-false quirk
  documented for `website_blog.archive`). `expected_state.json` must
  encode `true` for the success case.
- `project.milestone.toggle_is_reached(is_reached)` is the kanban
  checkmark-widget binding; backend list clicks the `is_reached` cell
  directly. Leave `project.milestone.write` + `web_save` + `toggle_is_reached`
  all in `optional_ops`.
- `project.milestone.reached_date` is a `@api.depends('is_reached')`
  stored computed Date — add it to `ignore_fields` in `state_spec.yaml`
  to avoid timezone-sensitive diff noise.
- `project.task.milestone_id` is
  `compute='_compute_milestone_id', store=True, readonly=False` with
  `domain="[('project_id', '=', project_id)]"`. Autocomplete is
  scoped per-project, so cross-project milestone distractors are
  impossible. Writing `project_id` on a task with a milestone pinned
  to the old project silently nulls `milestone_id` via the guard in
  `project.task.write` (see `project_task.py::1219-1233`).
- `match_key: [project_id, name]` on `project.milestone` is the
  correct state-diff key — keying on `name` alone risks collision with
  foreign-project milestones; keying on `project_id` alone can't
  distinguish multiple milestones on the same project.

---

## lunch module — kiosk-style Owl UI + related-name partner rewrite

- **Model naming**: the vendor model is `lunch.supplier` (NOT
  `lunch.vendor`, which does not exist in Odoo 19). The UI label
  reads "Vendor" but every technical reference is `supplier_*`.
  `lunch.product.supplier_id` is a m2o to `lunch.supplier`.
- **Not in base snapshot**: seed must `button_immediate_install()` the
  `lunch` module record. Admin is auto-added to
  `lunch.group_lunch_manager` by the module's security data, so
  Configuration menus render post-install without extra ACL work.
- **`lunch.supplier.name = related('partner_id.name', readonly=False)`**.
  Picking an existing partner from the `partner_id` autocomplete
  *clobbers* whatever the agent typed into the `name` field earlier.
  Typing into `name` writes back to the partner (renaming it). Oracle
  / human flow must pick the partner FIRST, then type the vendor
  name. Seed cleanup should handle both the seeded partner name and
  the final vendor name when releasing the partner, otherwise a
  re-run fails to find the "Bench Cafe Partner" seed row (it got
  renamed to "Bench Cafe").
- **`lunch.supplier.delivery` Selection renders via `o_select_menu`
  widget**, NOT a native `<select>`. The generic `set_selection`
  helper (which calls `select_option(label=...)`) times out. Same
  pattern as `crm.team.alias_contact`. Working:
  ```python
  page.locator(".o_field_widget[name='delivery'] .o_select_menu_toggler").click()
  page.locator(".o_select_menu_menu .o_select_menu_item:has-text('Delivery')").click()
  ```
- **`lunch.supplier` weekday toggles use `widget="week_days"`**
  (`addons/web/static/src/views/widgets/week_days/`). The widget
  renders a 2-row `<table>`: row 1 = `<th>` day labels with
  `data-tooltip` = the day string, row 2 = `<CheckBox>` components
  *without* a `name` attribute. Toggle by matching header text to a
  column index, then click the checkbox in the same column of
  row 2. Default is Mon-Fri only; Sat and Sun are False.
- **`/odoo/lunch` kiosk dashboard**: opens the
  `lunch_product_action_order` kanban with a sidebar
  `LunchDashboard` Owl component.
  `LunchKanbanRenderer.getGroupsOrRecords` returns `[]` when
  `searchModel.lunchState.locationId` is falsy. Seed must set
  `admin.last_lunch_location_id` to the seeded `HQ Office`
  location to avoid a race where the kanban renders empty before
  the `/lunch/infos` RPC resolves the fallback.
- **Clicking a product kanban card** triggers
  `LunchKanbanRecord.onGlobalClick` → bus event `lunch_open_order` →
  `action.doAction({res_model:'lunch.order', views:[[false,'form']],
  target:'new', context:{default_product_id: ...}})`. The resulting
  dialog is a standard `.o_dialog` wrapping the `lunch.order` form
  view. **Click the product name text, NOT the favorite star** in
  the card corner — `is_favorite widget="lunch_is_favorite"` has its
  own click handler that swallows the card-level onGlobalClick.
- **Order dialog footer button visibility**:
  `Add To Cart` has `invisible="order_deadline_passed or
  not display_add_button"`. Both computes fire at form-new time:
  - `order_deadline_passed` for `date=today`, `send_by='phone'`
    supplier = `not supplier.available_today` =
    `not supplier[WEEKDAY_TO_NAME[today.weekday()]]`. If the weekday
    flag for TODAY is off, the button is hidden. Tasks that require
    "order for today" must either enable all 7 days on the supplier
    or pin the test date to a known weekday.
  - `display_add_button` = `get_wallet_balance(user) >= price`.
    `get_wallet_balance` = `sum(cashmoves) +
    res.company.lunch_minimum_threshold`. Seed must set
    `lunch_minimum_threshold >= product.price` so the button is
    visible without requiring the agent to top up a wallet.
- **`lunch.order.add_to_cart()` is a no-op** Python method that
  returns True. The order record is persisted by the form
  controller's `web_save` BEFORE the object method runs. Initial
  state is `'new'`.
- **Two-phase submission**: closing the dialog fires the bus event
  `lunch_update_dashboard` which re-fetches `/lunch/infos` and
  shows the pending line + sidebar **Order Now** button. Clicking
  Order Now POSTs to `/lunch/pay` which calls `action_order()` on
  all `state='new'` lines for the current user today, transitioning
  to `state='ordered'`. This is the ONLY state-transition step —
  forgetting it leaves the order at `new` and the postcondition
  fails.
- **`lunch.product.supplier_id` display_name format**:
  `lunch.supplier._compute_display_name` returns
  `f'{name} {phone}'` when phone is set, else `name`. The state-diff
  engine normalizes m2o to display_name, so `expected_state.json`
  for `lunch.product.supplier_id` must encode
  `"Bench Cafe +1 555 0199"` if the task pins a phone — NOT
  `"Bench Cafe"` alone.
- **Timezone-sensitive `lunch.order.date`**: admin's seeded tz in the
  base snapshot is `Asia/Singapore` (+8h UTC). `fields.Date.
  context_today(admin)` can differ from the backend UTC date by
  1 day depending on when the test runs. `check.py` should accept
  `today`, `today-1d`, `today+1d` as valid date candidates when
  matching the order. (Browser-use failure mode here is separate —
  BU usually never reaches the order step at all.)

---

## sale_timesheet + hr_timesheet — install + timesheet-tab editable o2m quirks

- **Neither `hr_timesheet` nor `sale_timesheet` is in the base snapshot.**
  The `sale_timesheet` bridge depends on `hr_timesheet`; `button_immediate_install`
  on `sale_timesheet` alone pulls `hr_timesheet` in transitively, but installing
  both in order is more robust for test reliability. Wrap each install in
  try/except so a partial install does not abort the seed.
- `product.template.service_policy='delivered_timesheet'` is stored via
  `invoice_policy='delivery' + service_type='timesheet'` (see
  `_get_service_to_general_map` in
  `addons/sale_timesheet/models/product_template.py`). Seeding `service_policy`
  directly works, but writing the underlying two fields is cleaner and survives
  registry reloads.
- **`product.template` has NO `uom_po_id` field in Odoo 19.** The old dual
  sale/purchase UoM split is gone — there's only `uom_id`. Seeds that try to
  write `uom_po_id` raise `ValueError: Invalid field 'uom_po_id' in 'product.template'`.
- `service_tracking='task_in_project'` on the service product causes
  `sale.order.action_confirm` to trigger `_timesheet_service_generation()`
  which auto-creates BOTH a `project.project` and a single `project.task`
  tied to the SO line. The project's `allow_timesheets=True` by default, so
  the Timesheets tab on the generated task is visible immediately.
- **The Tasks smart button on `sale.order` is a COMBINED Projects+Tasks
  button** (one `oe_stat_button` with two `<field>` counts stacked in an
  `o_stat_info` block — see `addons/sale_project/views/sale_order_views.xml`).
  Its `name="action_view_project_ids"` routes to
  `project.act_project_project_2_project_task_all` (tasks list filtered by
  the SO) when `len(project_ids) == 1`. Oracle selector that works:
  `button.oe_stat_button:has-text('Tasks')` — there is no standalone Tasks
  button.
- **`project.task.timesheet_ids` editable-list (`editable="top"`) quirk**:
  adding two rows back-to-back via "Add a line" without an explicit
  `save_form()` between them persists ONLY the SECOND row. The first row's
  in-memory changes are clobbered by the second Add. Oracles (and agents)
  MUST call save (or Ctrl+S) between rows, or fill both rows before a single
  terminal save. Cell selector for the timesheet o2m: the visible columns
  are `date`, `employee_id` (widget=`many2one_avatar_employee`),
  `name` (Description), `unit_amount` (widget=`timesheet_uom` = float_time).
  All other columns in the list XML (`user_id`, `project_id`, `task_id`,
  `company_id`, `readonly_timesheet`) are `column_invisible="True"`.
- `account.analytic.line.unit_amount` uses `widget="timesheet_uom"`. The
  cell input accepts float-time strings like `4:00`, `2:30`, `0.5`. The
  string `4` alone is interpreted as 4.0 hours (no "minutes" magic).
- The Create Invoice wizard's `advance_payment_method` radio on
  `sale.advance.payment.inv` has **three options**: `Regular invoice`
  (default), `Down payment (percentage)`, `Down payment (fixed amount)`.
  Browser-use reliably keeps the default, so this radio alone is NOT a
  hard-tier differentiator — it needs to combine with an upstream
  cross-model chain (timesheets logged on an auto-task, delivered-qty
  gating, etc.). Wizard primary button: `button[name='create_invoices']`
  with text "Create Draft" or "Create Invoice".
- `admin` user is already in `hr_timesheet.group_hr_timesheet_user` after
  installing `hr_timesheet` (the module adds `base.user_admin` to that
  group via its base demo data). A defensive `group.user_ids = [(4, admin.id)]`
  still helps for reliability.
- Browser-use single-shot calibration on this pattern: **PASS in ~183s**
  on the first attempt. The SO -> Tasks smart button -> task form ->
  Timesheets tab -> Add Line flow is well-signposted in Odoo 19, and BU
  does NOT trip on the between-rows save quirk (it appears to navigate
  cells slowly enough that each row commits via implicit blur). To
  re-tier this workflow upward to hard, add: (a) a distractor task on
  the same project that the agent must ignore, (b) require non-default
  employee on one of the rows (e.g. a seeded "Bench Consultant" employee
  vs admin), or (c) gate the Create Invoice on a non-default radio
  (down-payment percentage) rather than the default Regular invoice.

## hr_attendance — public kiosk Owl UI, admin logout redirect, barcode validator

Source tasks: `hr_attendance.clock_in_out_kiosk_mode`,
`hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout`.

- `res.company.attendance_kiosk_mode` is a Selection whose **raw values**
  are `barcode`, `barcode_manual`, `manual` (the Settings UI label
  "Manual Selection" maps to `manual`). Do NOT use `manual_selection`,
  `no_barcode`, or `auto` in seeds — those values don't exist in the
  selection and the write will succeed silently as False but the kiosk
  controller will not render the manual grid.
- To drive the PIN flow you MUST set BOTH
  `company.attendance_kiosk_mode = 'manual'` AND
  `company.attendance_kiosk_use_pin = True`. Without the latter, the
  controller's `manual_selection` JSON-RPC short-circuits without
  requiring a PIN and the kiosk will check the employee in immediately
  on card-click (skipping the numpad screen).
- **Barcode validator** (`hr.employee._verify_barcode`) rejects any
  character outside `[A-Za-z0-9]` and anything longer than 18 chars.
  Seed values like `ATT-001` or `BADGE_42` raise `ValidationError`.
  Use `ATT001`, `BENCH01`, etc.
- **There is no `badge_id` field on `hr.employee` in Odoo 19.** The
  field labelled "Badge ID" in the employee form (Settings tab,
  Attendance/Point of Sale group) is technically `barcode`
  (`addons/hr/models/hr_employee.py:206` — `barcode = fields.Char(
  string="Badge ID", ...)`). Writing `badge_id` in a seed silently
  succeeds as an unknown-key no-op on environments with lax field
  validation, making tests appear to "pass" without setting anything.
  Always `grep -n "badge_id\|barcode" addons/hr/models/hr_employee*.py`
  before building any badge-related task. Source task:
  `hr.generate_employee_card_set_badge_id` (row 425).
- The **Print Badge** button inside the HR Settings tab has
  `invisible="not barcode"` so it is hidden until the barcode field
  has been saved. Oracles/agents that want to click it must complete
  the form save first — clicking it before the write is a no-op
  against an invisible element. For medium-tier tasks that only assert
  the field value, mark the Print Badge click as best-effort.
- The HR "Settings" notebook tab on the employee form has
  `name="hr_settings"` and `string="Settings"` (not "HR Settings") —
  `click_tab(page, "Settings")` is the correct call.
- `attendance_from_systray` on the company must be `False` when the
  intent is to force the kiosk workflow — otherwise the admin navbar
  grows a clock widget that the agent can (and will) click instead of
  the kiosk menu.
- Backend menu item **Attendances → Kiosk Mode** triggers the server
  action `hr_attendance.open_kiosk_url` with path `attendance-kiosk`,
  which calls `res.company._action_open_kiosk_mode()` and returns an
  `ir.actions.act_url` pointing at
  `/hr_attendance/kiosk_mode_menu/<company_id>`. That controller
  **logs the admin out** (via `request.session.logout(keep_db=True)`)
  when the admin has a password, then 302-redirects to
  `/hr_attendance/<attendance_kiosk_key>`. Implication for oracle/agent:
  after the menu click, `/web/session/authenticate` credentials are
  gone and the kiosk page is served via `auth='public'`. Any attempt to
  jump back to `/odoo/...` in the same browser context will force a
  re-login. For checks that must run admin RPC after the flow, prefer
  capturing DB state out-of-band (the eval harness already does this).
- Kiosk DOM landmarks (stable across Odoo 19):
  - Manual-selection grid container: `.o_hr_kiosk_manual_selection`.
  - Employee card (name shown in `h6`):
    `.o_hr_kiosk_manual_selection .card:has(h6:has-text('<name>'))`.
  - PIN pad container: `.o_hr_attendance_pin_pad`.
  - Digit and OK buttons: `.o_hr_attendance_PINbox_button:has-text('<n>')`
    and `...:has-text('OK')`. The numpad layout is rows of 1-2-3, 4-5-6,
    7-8-9, then a C-0-OK row (OK has class `btn-primary`).
  - Greeting card: `.o_hr_attendance_kiosk_card`. After a successful
    check-in/out it auto-returns to main in `kiosk_delay * 1000` ms
    (default 10 s), OR the user can click the bottom
    `.o_hr_kiosk_mode_bottom button:has-text('OK')` to return
    immediately. The latter is more reliable for scripted flows.
- Browser-use single-shot calibration on this pattern: **PASS in ~107s**
  — BU handles the full 2-phase cycle (card → numpad → OK → greet →
  OK → card → numpad → OK) without getting stuck. This makes the
  "public kiosk + PIN + two-phase" flow a **medium tier** difficulty
  in Odoo 19 rather than hard: the UI is very visually distinct
  ("Absent" vs "On site" badges, big circular avatars, large numpad
  buttons) so even naive DOM heuristics pick the right element.
- To re-tier this workflow upward to hard, add: (a) multiple decoy
  employees with similar names in the grid (forces name disambiguation
  without filter UI), (b) barcode mode instead of manual (forces the
  agent to understand it must scan or switch to Manual Selection from
  settings), or (c) a department filter sidebar where the target
  employee is hidden behind a department click.

---

## stock_barcode — Barcode tablet UI is Enterprise-only in Odoo 19

- The warehouse Barcode app (scan-to-receive, scan-to-pack, tablet UI
  with `+ 1` quantity button and Validate tile) ships in the **Enterprise**
  `stock_barcode` addon. Odoo 19 **Community** has ONLY:
  - `addons/barcodes/` — keyboard-event mixin (`BarcodeEventsMixin`)
    that captures Enter-terminated key bursts from USB scanners + bus
    broadcast of `barcode_scanned`; plus the `barcode.nomenclature` /
    `barcode.rule` models for GS1 prefix parsing. **No** warehouse UI.
  - `addons/barcodes_gs1_nomenclature/` — GS1 AI parser extension.
- `grep -rn "stock_barcode" addons/` on `odoo_benchmark` returns only
  i18n strings and one `module_stock_barcode = fields.Boolean("Barcode
  Scanner")` upgrade_boolean on `addons/stock/models/res_config_settings.py:29`
  (ticking it in Inventory → Configuration → Settings asks Odoo to
  install the absent module and fails with "Module not found").
- `/odoo/barcode` is NOT a registered client-action route in this
  checkout — there is no `stock_barcode_action_main_menu`, no
  `BarcodeMainMenu` Owl component, no `BarcodePickingModel` JS class,
  no `receipt_line.js`, no `line_component.js`. Navigating there in a
  Community build lands on the "action not found" 404 screen.
- **Pre-flight for any `stock_barcode.*` task:** run
  ```python
  module = env["ir.module.module"].search(
      [("name", "=", "stock_barcode")], limit=1)
  assert module and module.state == "installed"
  ```
  If False, the task is BLOCKED — ship the standard BLOCKED skeleton
  (seed / oracle / check short-circuit with diagnostics, empty
  expected_state / state_spec / trace_spec, RESULT.md documenting the
  absence). Precedent: `barcodes.receive_product_via_scan_validate`,
  `stock_barcode.receive_via_barcode_scan_validate` (row 401), and all
  other Enterprise-only module blockers (rows 350, 351, 352, 387).
- When scaffolding a fallback task for scanning-like behavior in
  Community, pivot to the backend form view: `stock.picking` list →
  open picking → edit move line `quantity` inline → Validate. This is
  the same data path but exposed via the standard form widget, not a
  tablet UI. File the re-scoped task under `stock.*`, not
  `stock_barcode.*`.
- When the enterprise addon IS vendored, the scanning UI historically
  listens on a hidden `<input class="o_barcode_input">` that is
  positioned off-screen; programmatic scanning via
  `page.keyboard.type("BENCH-A-001"); page.keyboard.press("Enter")`
  drives the same `barcode_scanned` bus event as a physical USB
  scanner. The `+ 1` tile is (as of recent versions)
  `button.o_add_reserved` / `button.o_barcode_line_btn_add_quantity` —
  selector names drift between Odoo versions, always confirm against
  the shipping enterprise source before writing oracle selectors.

---

## account_followup — Follow-up Reports / Customer Statement is Enterprise-only in Odoo 19

- The payment-reminder workflow (Follow-up Reports list, per-customer
  follow-up card with **Send Email** / **Send Letter** / **Schedule
  Activity** header buttons, configurable `account_followup.followup.line`
  levels with per-level email template + delay days, the partner
  `followup_status` / `followup_line_id` / `followup_next_action_date`
  fields, and the `account_followup_manual_reminder` wizard) ships in the
  **Enterprise** `account_followup` addon. Odoo 19 **Community** has NO
  equivalent.
- `grep -rn "account_followup" addons/` on `odoo_benchmark` returns
  **zero** matches — no model, no view, no controller, no client action,
  no i18n string. The `account_followup` source is not even shipped as a
  stub. `ls addons/account_followup/` → "No such file or directory".
- The only follow-up-adjacent Community artefact is the
  `send_invoices_followups` upgrade_boolean at
  `addons/account/views/res_config_settings_views.xml:115`, which
  references `module_snailmail_account` (physical-mail invoicing) — NOT
  a reminder workflow. Ticking it installs `snailmail_account`, which
  adds a "Send by Post" option on invoices but does NOT add any
  per-partner follow-up card, level logic, or reminder email template.
- `/odoo/action-account_followup.*` is NOT a registered route in this
  checkout — there is no `account_followup.followup.report` client
  action, no `action_account_manual_followup` window action.
- **Pre-flight for any `account_followup.*` task:** run
  ```python
  module = env["ir.module.module"].search(
      [("name", "=", "account_followup")], limit=1)
  assert module and module.state == "installed"
  ```
  If False, the task is BLOCKED — ship the standard BLOCKED skeleton
  (seed / oracle / check short-circuit with diagnostics, empty
  expected_state / state_spec / trace_spec, RESULT.md documenting the
  absence). Precedent:
  `account_followup.send_reminder_level_two_customers` (row 404),
  `stock_barcode.receive_via_barcode_scan_validate` (row 401), and all
  other Enterprise-only module blockers (rows 350, 351, 352, 387).
- When scaffolding a fallback task for reminder-like behavior in
  Community, pivot to the invoice chatter: open `account.move` →
  chatter → **Send Message** → compose an email referencing the due
  date. This uses the stock mail chatter path, does NOT escalate a
  level, and does NOT attach invoice PDFs automatically. File the
  re-scoped task under `account.*` or `mail.*`, not `account_followup.*`.

---

## documents — Documents app / Workspaces UI is Enterprise-only in Odoo 19

- The entire Documents app (Kanban of folders, left **Workspaces**
  tree, header **Upload** button with its hidden `<input type='file'>`,
  drag-and-drop intake, right-hand **inspector** side-panel with
  Folder / Tags / Owner / Activities / Versions / Share fields,
  workflow-rules engine, request-document flow, split-PDF flow, and
  the `documents.document` / `documents.folder` / `documents.facet` /
  `documents.tag` / `documents.workflow.rule` models) ships in the
  **Enterprise** `documents` addon. Odoo 19 **Community** has NO
  equivalent.
- `ls addons/documents/` on `odoo_benchmark` → "No such file or
  directory". `ls addons/ | grep -i document` returns only
  `l10n_latam_invoice_document` (unrelated LATAM fiscal document-type
  module).
- `grep -rn "documents.document" addons/` returns only 5 files of
  **soft references** — all of them gate on
  `env.get("documents.document")`, which is the canonical
  optional-Enterprise-integration pattern used by cloud-storage
  bridges and audit-trail linkers:
  - `spreadsheet/static/tests/helpers/data.js` (mock JS record factory)
  - `cloud_storage/models/ir_attachment.py`
  - `cloud_storage_migration/models/ir_attachment.py`
  - `account/tests/test_audit_trail.py`
  - `account/models/ir_attachment.py`
  None of these register the real model — they all early-return when
  the Enterprise model is absent.
- `/odoo/documents` is NOT a registered client action in this
  checkout — there is no `documents_kanban` view, no
  `documents_inspector` Owl component, no `documents_list` view.
- **Pre-flight for any `documents.*` task:** run
  ```python
  module = env["ir.module.module"].search(
      [("name", "=", "documents")], limit=1)
  assert module and module.state == "installed"
  ```
  If False, the task is BLOCKED — ship the standard BLOCKED skeleton
  (seed / oracle / check short-circuit with diagnostics, empty
  expected_state / state_spec / trace_spec, RESULT.md documenting the
  absence). Precedent:
  `documents.upload_document_tag_assign_to_folder` (row 411),
  `account_followup.send_reminder_level_two_customers` (row 404),
  `stock_barcode.receive_via_barcode_scan_validate` (row 401), and all
  other Enterprise-only module blockers (rows 350, 351, 352, 387).
- When scaffolding a fallback task for upload-like behavior in
  Community, pivot to the chatter: open any record (`res.partner`,
  `account.move`, `project.task`, …) → chatter → **attach files**
  paperclip → pick a file. This creates an `ir.attachment` linked to
  the record via `res_model` / `res_id`, but does NOT place the file
  in a Workspace, does NOT allow tag assignment, and does NOT surface
  an Owner field. File the re-scoped task under `mail.*` (e.g.
  `mail.send_email_with_attachment_log_as_note`), NOT `documents.*`.

---

## website_crm contact form: frontend submit -> crm.lead pipeline

- `website_crm` has `auto_install: True` and depends on `website + crm`.
  When both are in the benchmark base, `website_crm` is already installed
  and its `data/ir_model_data.xml` ran a `formbuilder_whitelist` call
  exposing `crm.lead` fields (`contact_name`, `partner_name`,
  `description`, `email_from`, `name`, `phone`, `team_id`, `user_id`,
  `lead_properties`) to the `/website/form/<model>` controller. No extra
  install step is needed in the seed.
- The default `/contactus` page ships with `data-model_name="mail.mail"`
  — submitting it creates a `mail.mail` record, NOT a `crm.lead`. To
  create a lead you must EITHER drive the website builder to switch the
  form action (tour `website_crm_pre_tour` does this via the right-hand
  options panel "Action -> Create an Opportunity") OR seed a separate
  page whose `<form>` arch already has `data-model_name="crm.lead"` plus
  `name=` attributes matching the whitelisted crm.lead fields. The
  latter is the pattern used for `website.submit_contact_form_create_crm_lead`.
- Field-name mapping gotcha: on the default `/contactus` the "Name" input
  is `name="name"` (maps to `crm.lead.name` = subject) and there is NO
  `contact_name` input. For a crm.lead-targeted form the mapping must
  be:
    * Visitor's name  -> `<input name="contact_name">`
    * Subject line    -> `<input name="name">`
    * Company         -> `<input name="partner_name">`
    * Message body    -> `<textarea name="description">`
  Mixing these up silently puts the visitor's name into `crm.lead.name`
  (subject) and leaves contact_name blank.
- The `s_website_form` Owl `Interaction` (see
  `addons/website/static/src/snippets/s_website_form/form.js`) binds a
  `t-on-click.prevent` handler to `.s_website_form_send`, which calls
  `send()` -> POST `/website/form/<model_name>`. It also attaches
  `t-on-submit.prevent` to the `<form>` itself. **Critical for oracle
  scripts:** a plain `page.click(".s_website_form_send")` is intercepted
  synchronously BUT the JS `send()` is async — you MUST wait for the
  redirect or for the POST round-trip. Pattern that works:
  ```python
  with page.expect_navigation(
      url="**/contactus-thank-you**", timeout=25000
  ) as nav:
      page.click("form .s_website_form_send")
  nav.value
  ```
- `form.js` `willStart()` unconditionally calls `recaptcha.loadLibs()`
  unless the `<form>` carries class `s_website_form_no_recaptcha`. If
  the base DB has `ir.config_parameter.recaptcha_private_key` set, the
  submit will try to fetch a token and block. For seeded forms used in
  benchmarks, either:
  * add `s_website_form_no_recaptcha` to the form's class list, AND/OR
  * explicitly clear `recaptcha_private_key` / `recaptcha_public_key`
    config params in the seed (`icp.set_param(...)`).
- `website_crm/controllers/website_form.WebsiteForm._handle_website_form`
  reformats every phone field on `crm.lead` via
  `phone_validation.phone_format(..., force_format='INTERNATIONAL')`
  before insert. Passing `+15555551212` to a US-country form comes out
  as `+1 555-555-1212` (spaces and dash). **Check scripts must normalize
  phone** (strip non-digit/plus chars) before comparing equality.
- `website_crm.insert_record` defaults `values['company_id'] =
  request.website.company_id.id` and `values['lang_id'] =
  res.lang._get_data(code=lang).id` AFTER the form handler. These
  show up as extra create-edits in the state diff — include them in
  `expected_state.json` or add them to `ignore_fields` in `state_spec.yaml`.
- The created `crm.lead.type` defaults to `'opportunity'` in
  Odoo 19 Community (crm.lead `_default_type` returns 'opportunity' when
  `user_has_groups('crm.group_use_lead')` is False — which is the base
  snapshot configuration). If your check expects `type='lead'` you must
  either enable `crm.group_use_lead` in the seed OR accept
  `type='opportunity'` as the expected value.

## hr.leave.type / hr.leave.allocation — Odoo 19 allocation validation lifecycle

From `hr_holidays.request_allocation_approve_self_book_day_off`.

- `hr.leave.type.requires_allocation` is a **Selection**, not Boolean.
  Valid values: `'yes'` / `'no'`. Seeding with `True`/`False` raises
  `ValueError: Wrong value for hr.leave.type.requires_allocation`.
- `hr.leave.type.allocation_validation_type` is a **Selection** with values
  `'no_validation'` / `'manager'` / `'both'` / `'hr'`. The legacy Odoo ≤16
  `'officer'` value no longer exists in Odoo 19 — writing it raises
  `ValueError: Wrong value for hr.leave.type.allocation_validation_type:
  'officer'`. Use `'hr'` for the HR-officer flow, `'manager'` for the
  Time-Off-Responsible flow, or `'both'` if both roles must approve.
- With `allocation_validation_type='hr'` an allocation needs two clicks:
  **Confirm** (draft → `confirm`) then **Approve** (`confirm` → `validate`).
  Many UI paths auto-confirm on create, so a single Approve click is
  usually enough — oracles should defensively call `action_confirm` before
  `action_approve` (confirm on an already-confirmed record is a no-op).
- **Ordering constraint:** a `hr.leave.type` with `requires_allocation='yes'`
  forces the matching `hr.leave` to have a validated allocation covering
  the requested dates BEFORE `action_approve` will succeed; otherwise
  approval raises with "The number of remaining time off is not sufficient
  for this time off type". Tasks that test the allocation → leave flow
  must seed the allocation-requiring type and leave the agent to create
  the allocation first; oracles using RPC must call
  `hr.leave.allocation.action_approve` before `hr.leave.create` + `action_approve`.
- `hr.employee.parent_id` (reporting tree) and `hr.employee.leave_manager_id`
  (who approves time off) are **separate fields**. For admin to approve an
  employee's leaves, seed `leave_manager_id=admin.id`. `parent_id` alone
  does not grant approval authority.

---

## stock.quant Physical Inventory — Apply wizard & mirror quants

### Applying an inventory count creates mirror quants at the virtual `Inventory adjustment` location

Calling `stock.quant.action_apply_inventory` (or the header `Apply All` button
on the Physical Inventory list) does three things:

1. Writes `stock.quant.quantity` on the source quant to equal the new
   `inventory_quantity` (Counted Qty) and resets `inventory_quantity_set=False`.
2. Creates a done `stock.move` with `is_inventory=True` whose source/destination
   is `WH/Stock` and the virtual `Virtual Locations/Inventory adjustment`
   location (`stock.location_inventory`).
3. Creates a mirror `stock.quant` row at the virtual `Inventory adjustment`
   location carrying the move delta.

This means any state-diff oracle tracking `stock.quant` with
`match_key: [product_id, location_id]` will see **extra create edits** for
every adjusted product at `(product, "Inventory adjustment")` — include them
in `expected_state.json` or you will fail Precision.

Sign convention: a downward adjustment (20 → 18) produces a mirror quant with
`quantity = +2` at `Inventory adjustment` (units flowed OUT of WH/Stock into
the virtual bucket). An upward adjustment (15 → 16) produces a mirror quant
with `quantity = -1` at `Inventory adjustment` (units flowed FROM the virtual
bucket into WH/Stock).

```json
{"model": "stock.quant",
 "entity_key": ["Bench Prod A", "Inventory adjustment"],
 "field": "quantity", "op": "create", "norm_value": 2.0}
```

### Counted Quantity column is `inventory_quantity`, NOT `quantity`

On the Physical Inventory list (`action_view_quants` with
`inventory_mode=True`), the editable cell labeled **Counted Quantity** binds
to `stock.quant.inventory_quantity`, not to `quantity`. Selectors:

```
.o_data_row [name="inventory_quantity"]          /* the td / div */
.o_data_row [name="inventory_quantity"] input    /* edit input */
```

Oracles that try to edit the `On Hand Quantity` column (`name="quantity"`)
instead will not trigger an inventory adjustment — `quantity` is a stored
computed that is only writable via `_update_available_quantity` or the Apply
flow.

### Apply flow: Apply All → confirmation dialog → primary Apply/Update Quantities

Clicking `button[name="action_apply_all"]` in the list header opens a small
modal `stock.inventory.adjustment.name` wizard asking for an adjustment
reference. The primary footer button is labeled **Apply** (or **Update
Quantities** in some localizations) — `button[name="action_apply"]` or
`button.btn-primary` inside the `.modal:visible`. If the agent clicks `Save`
without clicking through this dialog, `inventory_quantity_set=True` but
`quantity` is unchanged (the adjustment is staged but not posted).

Selector bundle that works across label variants:

```
.modal:visible button[name="action_apply"]:visible,
.o_dialog:visible button[name="action_apply"]:visible,
.modal:visible button:has-text("Update Quantities"):visible,
.modal:visible button:has-text("Apply"):visible
```

### Postcondition gate: assert `stock.move.is_inventory=True`

Without a `stock.move(is_inventory=True, state=done)` postcondition,
a BU run that edits `stock.quant.quantity` directly via write / web_save
(skipping the Apply flow) can score State-Diff F1=1.0 despite bypassing
the user-visible Apply dialog. Always check:

```python
env["stock.move"].search([
    ("product_id", "=", product.id),
    ("is_inventory", "=", True),
    ("state", "=", "done"),
])
```

and sum signed deltas via `location_dest_id == WH/Stock ? +qty : -qty` to
confirm the Apply path was exercised end-to-end.

### Phantom new-row on inline editable list: recover via Discard

When the agent clicks a `name="inventory_quantity"` cell and types, then
presses Tab/Enter outside of an already-editable cell context, the
Physical Inventory list (and other inline editable list views with
`editable="bottom"`) can spawn a blank new-row at the bottom with all
required fields empty. A subsequent click on `button[name="action_apply_all"]`
then raises a client-side "Missing required fields" error and the Apply
modal never opens.

The reliable recovery is the **Discard** button in the list header
(`button.o_list_button_discard`, label "Discard") which kills the
phantom row and re-enables Apply All. This was observed in a BU
single-shot run on `stock.create_physical_inventory_adjust_two_products`
(row 427): BU clicked Discard after the first failed Apply All, then
re-set the second Counted Quantity and Apply All succeeded. Oracles
that drive this flow programmatically do not hit the bug (focus stays
inside the quant's row), but browser agents routinely do — list this
recovery as an acceptable fallback in task prompts when relevant, and
do NOT include `button.o_list_button_discard` as a forbidden op.

Related side-effect: when the inline list has a phantom new row, the
`Apply All` button may be rendered but **disabled** (greyed). BU's
"wait then click again" loop eventually succeeds once the row is
discarded.

---

## `project.task.date_deadline` — Datetime stored in UTC, typed as a date

`project.task.date_deadline` is `fields.Datetime` (not Date) in Odoo 19:

```
# addons/project/models/project_task.py:183
date_deadline = fields.Datetime(string='Deadline', index=True, tracking=True, copy=False)
```

The form widget renders it as a date-only input, so when the agent types
`06/30/2026` the backend stores `2026-06-30 00:00:00` interpreted in the
CURRENT USER'S timezone and serialized to UTC. With the benchmark admin on
America/Los_Angeles, `06/30/2026` persists as `2026-06-29 16:00:00 UTC`.

For check.py, compare on the admin-local date, not the UTC datetime:

```python
import pytz
tz = pytz.timezone(env.user.tz or "UTC")
actual = pytz.UTC.localize(task.date_deadline).astimezone(tz).date()
assert actual == date(2026, 6, 30)
```

Same approach for any Datetime field the prompt expresses as a date
(`project_todo` notes, event activities, etc.). Never assert
`task.date_deadline == date(...)` directly.

---

## Seeding a second internal user that appears in `user_ids` m2m autocompletes

To make a seeded user pickable on `project.task.user_ids` (and similar
`res.users` m2m fields constrained by `domain=[('share','=',False)]`), the
user must be a full internal user:

```python
group_internal = env.ref("base.group_user")
group_project_user = env.ref("project.group_project_user")
env["res.users"].create({
    "name": "Bench Dev 2",
    "login": "bench_dev_2",
    "password": "bench_dev_2",
    "group_ids": [(6, 0, [group_internal.id, group_project_user.id])],
})
```

A login/password is REQUIRED even when the seed never authenticates as the
user — the form's name_search filters out users with `share=True` (the default
for users without `base.group_user`). Use the `login` slug as the canonical
identifier in check.py (logins are benchmark-owned; display names may collide
with other seeds).

---

## Newly-created records emit `active=True` alongside `name` in the diff

Most Odoo models default `active=True` and the diff engine emits BOTH a
`name` create edit and an `active=True` create edit when a new record is
created (seen on `project.task`, `project.task.type`, `project.tags`, etc.).
Include both in `expected_state.json`:

```json
[
  {"model":"project.task","entity_key":["Fix login bug"],"field":"name","op":"create","norm_value":"Fix login bug"},
  {"model":"project.task","entity_key":["Fix login bug"],"field":"active","op":"create","norm_value":true}
]
```

Missing the `active` edit drops F1 to 0.67 (1 extra, 2 observed, 1 matched
of 1 expected → Precision 0.5, Recall 1.0 → F1 = 0.67). Always run the task
against the oracle once and inspect `state_diff.json` for the full create-row
set.


## account.payment.register wizard on a posted customer invoice

### Header-button label

The invoice form's statusbar button that opens the Register Payment wizard
is labeled **`Pay`**, not "Register Payment". The wizard's **title** is
"Register Payment" but the actionable button the agent/oracle must click
is `<button name="action_register_payment" string="Pay">`. Prompts that
instruct the agent to click "Register Payment" will work because BU tends
to match either; but oracle scripts MUST target the statusbar Pay button:

```python
pay_btn = page.locator(
    ".o_statusbar_buttons button:has-text('Pay'):visible"
)
pay_btn.first.click(force=True)
```

### Wizard footer primary button

The wizard footer has two primary buttons gated on `total_payments_amount`:

- `string="Create Payments"` when `total_payments_amount != 1`
- `string="Create Payment"` when `total_payments_amount == 1`

Both call the same method `action_create_payments`. Target by name, not
by text, to avoid picking "Discard":

```python
modal.locator("button.btn-primary[name='action_create_payments']").first.click()
```

### Default values are already correct for a full payment

On a single posted invoice with no outstanding payments, the wizard's
defaults are:

- `journal_id` → first Bank journal in the company
- `payment_method_line_id` → Manual
- `amount` → `source_amount` (invoice `amount_residual`, e.g. 500.00)
- `payment_date` → today
- `communication` → the invoice's auto-assigned name (e.g. `INV/2026/00001`)

**Consequence for task design:** "open invoice → click Pay → click Create
Payment" is an Accept-Defaults flow and will not fail browser-use (empirically
F1=1.0 single-shot). To make the wizard a real trap you must REQUIRE a
non-default value: partial amount, back-dated `payment_date`, custom
`communication` memo, or a non-default journal (seed two bank journals).

### Post-reconcile state values

After `action_create_payments` on a clean base snapshot:

- `account.move.payment_state` goes **directly to `'paid'`** (not `'in_payment'`)
  because the default Bank journal in `benchmark_base` has **no configured
  `outstanding_account`** — so the payment posts straight to the receivable
  account and the receivable line is reconciled in one step. A task that
  expects `'in_payment'` must seed an outstanding account on the journal.
- `account.payment.state` reports **`'paid'`** (not `'posted'`) once the
  counterpart journal item is fully reconciled. Accept `posted|paid|in_process`
  in `check.py`.

### State-diff: the payment's backing journal entry is visible

Creating an `account.payment` also creates its backing `account.move` with
`move_type='entry'` and an auto-assigned name (e.g. `INV/2026/00001` from
the next Miscellaneous-journal sequence, which can collide numerically with
the invoice's name). If `state_spec.yaml` tracks `account.move` by
`[partner_id, ref]` you will see **five extra create edits** in
`state_diff.json` that must be baked into `expected_state.json`:

```json
{"model":"account.move","entity_key":["Bench Recon Co","INV/2026/00001"],"field":"partner_id","op":"create","norm_value":"Bench Recon Co"},
{"model":"account.move","entity_key":["Bench Recon Co","INV/2026/00001"],"field":"ref","op":"create","norm_value":"INV/2026/00001"},
{"model":"account.move","entity_key":["Bench Recon Co","INV/2026/00001"],"field":"state","op":"create","norm_value":"posted"},
{"model":"account.move","entity_key":["Bench Recon Co","INV/2026/00001"],"field":"move_type","op":"create","norm_value":"entry"},
{"model":"account.move","entity_key":["Bench Recon Co","INV/2026/00001"],"field":"payment_state","op":"create","norm_value":"not_paid"}
```

### Seed cleanup order for prior payment runs

You cannot `unlink()` a posted `account.payment` whose counterpart line is
reconciled. Sequence:

```python
for line in pay.move_id.line_ids.filtered(
    lambda l: l.matched_debit_ids or l.matched_credit_ids
):
    line.remove_move_reconcile()
pay.action_draft()     # state: posted → draft
pay.action_cancel()    # state: draft → cancel (Odoo 19 has this on the payment)
pay.unlink()
```

Forgetting `remove_move_reconcile` before `action_draft` raises
`UserError("You can't modify a posted entry.")` at the reconcile engine.

### Odoo 19 field renames relevant here

- `account.payment.memo` (not `ref`) — prompts and check.py asserting the
  memo must read `payment.memo`.
- The wizard stores the memo in `account.payment.register.communication`
  (Char, `string="Memo"`), which maps to `payment.memo` via
  `_create_payments` at `vals['memo'] = self.communication`.


## product.pricelist — pricelist rule configuration + SO onchange (calibration notes)

Cookbook notes from `sale.configure_pricelist_apply_to_order_line` (row 418,
hard, tier 3). Browser-use passed single-shot (F1=1.0) with a ~8-step
recovery loop — the workflow has traps for humans but BU eventually got
through. Useful reference for anyone building pricelist-adjacent tasks.

### The Pricelists menu is gated by `product.group_product_pricelist`

Without this group enabled, (a) the Sales > Products > Pricelists menu
item is hidden and (b) the `pricelist_id` field on `sale.order` is
hidden. The group must be granted to **both admin AND user_root** in the
seed, not just admin — because some pricelist computations (e.g.
`_get_partner_pricelist_multi` short-circuits to empty if `user_root`
lacks the group) run under root context during ORM writes, which silently
breaks the SO's `_compute_pricelist_id` chain:

```python
pricelist_group = env.ref("product.group_product_pricelist")
pricelist_group.sudo().write({
    "user_ids": [(4, env.ref("base.user_admin").id),
                 (4, env.ref("base.user_root").id)],
})
```

The menu is at **Sales > Products > Pricelists** (NOT Configuration —
common mistake in prompts). The URL path is `/odoo/pricelists` thanks to
`<field name="path">pricelists</field>` on `product.product_pricelist_action2`.

### `item_ids` opens a modal dialog, NOT inline editing

The default `product.pricelist_view` form renders `item_ids` as a
non-editable list (no `editable="bottom"` attribute). Clicking **Add a
line** opens a full `product.pricelist.item` form in an X2Many dialog
with **Save & Close** and **Discard** footer buttons (`o_form_button_save`,
`o_form_button_cancel`). Oracles need to locate the modal after clicking
Add a line:

```python
click_add_a_line(page)
page.wait_for_selector(".modal:visible", timeout=10000)
modal = page.locator(".modal:visible").last
# ... fill fields ...
modal.locator(".modal-footer button.o_form_button_save").first.click()
```

### Two "discount" fields — the classic human + agent trap

The rule form has **two visually-similar Discount inputs** controlled by
the `compute_price` radio:

| `compute_price` | Visible field | Technical field |
|---|---|---|
| `percentage` (radio "Discount") | `<input>` labeled "Discount" + `%` | `percent_price` |
| `formula` (radio "Formula") | `<input>` labeled "Discount" (inside the `pricelist_rule_base` group below) + `%` | `price_discount` |
| `fixed` (default radio "Fixed Price") | `<input>` labeled "Price" | `fixed_price` |

The Formula section (`name="pricelist_rule_base"`) is `invisible` until
the agent clicks the Formula radio. A task that asks for "Formula with 10%"
must spell out that the `price_discount` field is inside the formula
sub-section — not the percentage-price input at the top. Browser-use
correctly picked the Formula radio on the first try but then repeatedly
failed to persist `price_discount=10` through "Save & Close" (~8 retry
loop with "Oops" error dialogs) before it stuck. Oracle fix: focus the
input, `fill("")`, `fill("10")`, `press("Tab")` before clicking Save &
Close so the onchange resolves before save.

### `applied_on='3_global'` is an onchange side-effect, not a direct radio

The visible radio on the rule form is `display_applied_on`, which only
exposes `1_product` and `2_product_category`. "All Products" is not a
radio option — it's what `_onchange_display_applied_on` sets
`applied_on` to when `display_applied_on='1_product'` AND the
`product_tmpl_id` field is left empty:

```python
@api.onchange('display_applied_on')
def _onchange_display_applied_on(self):
    for item in self:
        if not (item.product_tmpl_id or item.categ_id):
            item.update({'applied_on': '3_global'})
```

Prompts should say "leave Apply To on Product (default) and leave the
product field empty" — NOT "select All Products". This is the only way
to hit `applied_on='3_global'` from the UI.

### SO pricelist-driven `price_unit` flow

With the seeded product `Bench Price Item` at `list_price=200` and a rule
`(applied_on='3_global', compute_price='formula', base='list_price',
price_discount=10)`:

1. User sets `sale.order.partner_id = Bench Price Co` — triggers
   `_compute_pricelist_id` which lands on the default pricelist (or the
   partner's property, whichever is set).
2. User sets `sale.order.pricelist_id = Bench 10% Off`.
3. User adds a line with `product_template_id = Bench Price Item`.
4. `sale.order.line._compute_price_unit` fires via the pricelist's
   `_get_product_price_rule` → applies 10% formula → sets
   `price_unit = 200 * (1 - 10/100) = 180.0`.

Test this by asserting `abs(line.price_unit - 180.0) <= 0.01` in
`check.py`. Also clear taxes (`taxes_id=[(5,0,0)]`) at seed time or
`tax_included` variations will skew the expected number.

### Why this task still passed browser-use (calibration note)

Despite the two-stage workflow, the nested "Formula > Discount" trap,
and the modal dialog, browser-use completed the task single-shot in
44 steps / 326s (F1=1.0). To push this into a genuine trap consider:

1. **Distractor pricelists** — seed `Bench 20% Off` + `Bench Fixed 150`
   so name-matching the correct one actually matters.
2. **Chained base** — require `base='pricelist'` + `base_pricelist_id`
   pointing at a second pricelist (two-hop computation).
3. **Tiered rule** — require a second rule row with `min_quantity=10`
   for a volume discount, so the agent must add multiple rules and
   the task validates qty=5 triggers rule A vs qty=15 triggers rule B.

Simple single-rule formula pricelists are "hard-looking but BU-passable".

## `stock.valuation.layer` removed in Odoo 19 — use `stock.move.value` + `product.value`

Odoo 19 dropped the `stock.valuation.layer` model entirely. Code / task
prompts that still reference it will raise `KeyError` from
`env['stock.valuation.layer']`. The replacement surface:

- `stock.move.value` — `fields.Monetary`, per-move cash value set by
  `stock_account.stock_move._set_value()` during `_action_done`. Acts
  as "the" valuation signal for incoming (`is_in=True`) AND outgoing
  (`is_out=True`) moves; negative sign is encoded as `is_out` (value
  itself stays positive).
- `stock.move.is_in` / `is_out` / `is_valued` / `is_dropship` —
  computed Booleans that classify a done move.
- `product.value` — small history model (`addons/stock_account/models/
  product_value.py`) for manual revaluations + lot / standard-price
  updates.
- `stock.move.remaining_qty` / `remaining_value` — carries the old
  FIFO remaining-tail semantics that used to live on SVL.

For MO-close tasks filter via
`stock.move.production_id == mo` (finished) and
`stock.move.raw_material_production_id == mo` (components), NOT via
any SVL query.

## `mrp_account._cal_price` is `cost_method`-gated

`mrp_account/models/mrp_production.py::_cal_price` rolls consumed
component values + workcenter cost + extra_cost into the finished
stock.move's `price_unit` **only** when the finished product's
`cost_method in ('fifo', 'average')`. For `cost_method='standard'`
it short-circuits to `finished_move.price_unit = product.standard_price`
and returns. A common seeding mistake in hard-tier valuation tasks is:

- set finished `standard_price=0` ("cost should come from rollup")
- leave category at default `property_cost_method='standard'`

That combination makes `_cal_price` write 0 to the finished move's
`price_unit`, and `_get_value_from_production` (`value = quantity *
price_unit`) then returns 0, so `stock.move.value=0` on the finished
move and the postcondition fails. Fix: seed
`property_cost_method='average'` (or `'fifo'`) on the category.

## Location `valuation_account_id` still mandatory even for move-value-only checks

`stock_account.stock_move._action_done` unconditionally calls
`_create_account_move()` on the move set. If `_should_create_account_move`
raises (because `location_dest_id.valuation_account_id` and
`location_id.valuation_account_id` are both NULL) the whole
`action_done` aborts, leaving the MO stuck pre-done. Seed MUST set:

- Production location (`usage='production'`) →
  `500100 Cost of Production` (`account_type='expense'`).
- Internal Stock location (`usage='internal'`) →
  `140000 Stock Valuation` (`account_type='asset_current'`, also
  written to `company.account_stock_valuation_id`).
- `company.account_stock_journal_id` → any general journal.

Seed both even when `check.py` only asserts on `stock.move.value`,
because the `account_move` side is an *invariant* of `_action_done`.

---

## Developer mode as a task gate (mail.alias, ir.ui.menu base.group_no_one)

Some Odoo 19 configuration menus — notably **Settings → Technical →
Email → Aliases** (`mail_alias_menu`), **Email Servers**, **Message
Subtypes**, **Database Structure**, and anything else gated by
`groups="base.group_no_one"` — are *hidden by default* even for admin.
They only appear when the client session flag `debug` is truthy. Simply
granting `base.group_no_one` to the user in the seed is **not enough**:

- `res.users.has_group('base.group_no_one')` (see
  `odoo/addons/base/models/res_users.py:1081`) explicitly returns
  `False` unless `request.session.debug` is also truthy. The group is
  described as "Technical Features" but its effective membership is
  gated at request time.
- There is no server-side `ir.config_parameter` or `res.users` write
  that can persist `session.debug = True`. It is a per-browser cookie.

To enable developer mode in a task:

1. **Seed-side (necessary)**: add `base.group_no_one` to the target
   user so they CAN see the menu once the session flag flips.

   ```python
   admin = env.ref("base.user_admin")
   admin.sudo().write({"group_ids": [(4, env.ref("base.group_no_one").id)]})
   ```

2. **Agent-side (required)**: either
   - click **Activate the developer mode** in the Developer Tools
     panel at the bottom of `/odoo/settings` (widget
     `res_config_dev_tool`, defined in
     `addons/web/static/src/webclient/settings_form_view/widgets/
     res_config_dev_tool.xml`), or
   - navigate to a URL with `?debug=1` appended.

   The widget calls
   `router.pushState({ debug: 1 }, { reload: true })`, which triggers
   a **full page reload**. Playwright must
   `wait_for_url("**debug=1**")` AND re-wait for `.o_action_manager`
   after the reload — `_wait_for_ready` alone is not sufficient. The
   `.o_action_manager` re-renders after the reload regardless of
   route; a bare `page.wait_for_load_state('load')` returns too early.

### Three "Activate" links — disambiguate

The Developer Tools panel renders up to three links depending on
current state:

1. "Activate the developer mode"
2. "Activate the developer mode (with assets)"
3. "Activate the developer mode (with tests assets)"

A naive `page.locator("a:has-text('Activate the developer mode')")`
selector matches all three. For normal tasks (plain debug=1) use:

```python
page.locator("#developer_tool a:has-text('Activate the developer mode')") \
    .filter(has_not_text="assets") \
    .filter(has_not_text="tests") \
    .first
```

### mail.alias field-level quirks

- `ir.model._description` for `crm.lead` is literally `"Lead"` (not
  "Lead/Opportunity"). Typing "Lead/Opportunity" in an `alias_model_id`
  many2one autocomplete returns zero real hits and only the quick-create
  variants. Clicking a quick-create entry calls
  `ir.model.name_create(['Lead/Opportunity'])`, spawning a new custom
  model `x_lead_opportunity`. Use the **technical name** (`crm.lead`)
  which uniquely matches via `_rec_names_search = ['name', 'model']`.
- The autocomplete's Create / Search-More entries add the class
  `o_m2o_dropdown_option` directly on the `<li>` (see
  `addons/web/static/src/views/fields/relational_utils.js:489`).
  Playwright's `has_not=page.locator(...)` filters by descendants, NOT
  by a class on the element itself — the reliable filter is CSS's
  `:not(.o_m2o_dropdown_option)` on the same element.
- The generic `mail.alias` form renders `alias_contact` as a native
  `<select>` (so `select_option(label='Everyone')` works) — unlike
  `crm.team.alias_contact` which uses the custom `o_select_menu`
  widget requiring the click-toggler-then-click-item pattern.
- `alias_defaults` is a plain Text field rendered as a `<textarea>`.
  After interacting with the m2o above, a leftover autocomplete
  dropdown frequently covers it and Playwright reports `subtree
  intercepts pointer events`. Dismiss via JS DOM removal + Escape,
  then `click(force=True)` or focus via `el.evaluate('el => el.focus()')`.
- `alias_defaults` is stored as a string; checks should parse with
  `ast.literal_eval` and assert both the keys and their values.
---

## `mail.activity.schedule` chatter wizard (Odoo 19)

- The chatter **Activity** button opens the `mail.activity.schedule`
  TransientModel directly (no pre-dropdown). Default values are:
  `activity_type_id` = the `To-Do` record (`mail.mail_activity_data_todo`,
  stored as the Char name `"To-Do"` with a hyphen — see earlier note at
  §account.move journal entries), `summary` = `activity_type.summary` (empty
  for To-Do), `note` = `activity_type.default_note` (empty), `date_deadline`
  = `today + activity_type.delay_count <delay_unit>` (To-Do's default is
  `+5 days`, NOT today).
- Fields in the wizard form:
  - `activity_type_id` — many2one with domain
    `['|', ('res_model','=',False), ('res_model','=', res_model)]`.
  - `summary` — plain `fields.Char`.
  - `note` — `fields.Html(sanitize_style=True)` rendered as an Owl
    wysiwyg editor (NOT a `<textarea>`). Agents that do a generic
    "type into first visible field" will land on summary. Playwright
    selector: `.o_field_widget[name='note'] .note-editable` or
    `textarea` fallback (see `benchmark.oracle_helpers.schedule_activity`).
  - `date_deadline` — `fields.Date` rendered as a **button-to-input**
    widget. Before first interaction the DOM shows a read-only button
    labelled with the preview date (e.g. `"Apr 24"`). Clicking the
    button flips the node to a visible `<input>` that accepts typed
    dates in the user locale (US admin: `MM/DD/YYYY`). Typing directly
    without clicking the button first will miss the input.
  - `activity_user_id` — many2one, defaults to `env.user`.
- Footer primary button label: **Schedule** (`action_schedule_activities`).
  `_action_schedule_activities` delegates to
  `self._get_applied_on_records().activity_schedule(activity_type_id,
  summary, note, date_deadline, user_id)`, which creates the final
  `mail.activity` row directly.
- Oracle shortcut for tasks that just need the end state: call
  `<model>.activity_schedule(activity_type_id=..., summary=..., note=...,
  date_deadline=...)` via call_kw. The record's model only needs to
  inherit `mail.activity.mixin` (which `res.partner` does).
- check.py patterns for `note` HTML field:
  - Typed plain text becomes `<p>Discuss Q2 plan</p>` after Owl wraps it.
  - Either strip `<p>`/`<br>` tags with a small regex
    (`re.sub(r"<[^>]+>", "", note_html)`) or substring-match the raw
    HTML for the core text (e.g. `"Q2 plan" in note_html`).
  - Do NOT compare `activity.note` to a verbatim HTML string — the
    wrapper varies (`<p>` vs. `<div>` vs. trailing `<br/>`).
- Cleanup ordering for partner-owned activities: unlink
  `mail.activity(res_model='res.partner', res_id in ids)` +
  `mail.message(model='res.partner', res_id in ids)` +
  `ir.attachment(res_model='res.partner', res_id in ids)` BEFORE
  `res.partner.unlink()`, else FK violations on `mail_message.res_id`
  fire. Fallback to `active=False` if unlink still fails.
