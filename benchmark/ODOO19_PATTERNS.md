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

---

## website_slides — sections, sequencing, and copy

- `slide.slide.is_category=True` rows ARE the sections of a `slide.channel`; no separate section model.
- `slide.slide.category_id` is **computed** from sequence ordering, NOT writable. To move a lesson, change its `sequence` to fall after that section's marker.
- `slide.slide.copy_data()` resets `sequence=0` on the duplicate (lands at top, uncategorized). Agent must re-sequence/pick section.
- New `is_category` slides default to `slide_category='document'` and `website_published=True` even though they aren't real lessons.
- BU failure mode: asked to "duplicate the lesson via Actions menu", BU tends to land on the COURSE cog menu and duplicate the whole `slide.channel` instead.

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
- `stock.scrap.scrap_qty` defaults to 1.0 — agents often forget to override it. Good calibration trap for hard tier.
- `stock.scrap.production_id` as match_key emits an extra "create" diff row that must be in expected_state.json.
- `stock.scrap.scrap_location_id` defaults to the per-company `Virtual Locations/Scrap` (the auto-created inventory-usage location from `_create_scrap_location`). For a task that requires a custom scrap destination (e.g. `WH/Lost`), seed must create a new `stock.location` with `usage='inventory'` + `location_id=warehouse.view_location_id` so its `complete_name` resolves to `WH/<name>`. Both `scrap_location_id` AND `location_id` fields on the wizard are gated by `groups="stock.group_stock_multi_locations"` — seed must add the admin to that group or the fields are invisible and silently default.
- A validated scrap launched from a `stock.picking` (via `picking_id` in the wizard context) **auto-creates a `stock.move` on the parent picking** (`move._prepare_move_values` sets `picking_id=self.picking_id.id` and `scrap_id=self.id`). Consequence: `picking.move_ids` grows by one after scrap, so `check.py` assertions like `len(picking.move_ids)==1` MUST filter `not m.scrap_id`.

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

---

## product.template / event_product gotchas

- The base snapshot has TWO pre-existing 'Gift Card' product.template records with different list_price. With `match_key: [name]` the diff engine swaps them non-deterministically, emitting phantom `list_price` edits. Fix: extend `match_key: [name, service_tracking, list_price]`.
- `product.template.service_tracking` field is `invisible` in the base product view. `event_sale` (auto-installed) removes the invisible attr, exposing the `event` ('Event Registration') option contributed by `event_product`. No manual install needed for event_sale → event_product.

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
