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

### Event / event_sale

- `event.event.event_ticket_ids` auto-materializes a default "Registration" ticket on create
- `event_sale` is auto-installed when both `event` and `sale` are present; no manual install
- Invoicing a paid registration goes through the Sales app (SO → event configurator wizard)
- The attendee-details wizard pre-fills name/email from the partner; non-default override needed
  if the attendee differs from the buyer
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

## survey.survey + CopyClipboardChar widget

- `survey.survey` has **no `state` field** in Odoo 19. "Ready to share" = `active=True` + `access_mode='public'` + populated `access_token`. Don't query a non-existent state field.
- `widget="CopyClipboardChar"` (e.g. `survey.invite.survey_start_url`) renders as `<span>` in readonly mode, NOT `<input>`. `page.input_value()` will time out. Read via `text_content()` on the field widget div, with input fallback.
- `survey.survey.action_send_survey` returns a `survey.invite` wizard with `default_send_email=False` for public surveys, so closing the wizard has no DB side effect.
