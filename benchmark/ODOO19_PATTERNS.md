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

---

## POS / pos_discount

- `pos_discount` is NOT in the base snapshot — seed must `button_immediate_install()` on demand.
- To enable Discount button: `pos.config.module_pos_discount=True`, `iface_discount=True`, `discount_pc=<float>`, `discount_product_id` (data record `pos_discount.product_product_consumable`).
- UI: Discount button lives inside the **Actions popup** (ellipsis `more-btn`), not the top bar. In Odoo 19 `control_buttons.xml` moves secondary actions (Pricelist, Refund, Fiscal position, Discount, etc.) into ControlButtonsPopup.
- Oracle pattern: prefer JSON-RPC `call_kw` over UI-driven POS oracle — `o_technical_modal` sometimes stays in DOM and intercepts pointer events.

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
