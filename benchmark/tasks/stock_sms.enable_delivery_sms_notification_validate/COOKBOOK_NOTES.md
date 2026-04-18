# Cookbook notes — stock_sms.enable_delivery_sms_notification_validate

Quirks uncovered while building this task. Candidates to fold back into
`benchmark/ODOO19_PATTERNS.md`.

## stock_sms module install + post_init hook resets settings

- `stock_sms` is `auto_install=True` with `depends=[stock, sms]` — installing
  `sms` alone is enough to pull `stock_sms` in. Neither module is in the
  base snapshot, so the seed must `button_immediate_install('sms')` (and
  defensively `stock_sms`).
- `stock_sms.__init__._assign_default_sms_template_picking_id` is a
  **post_init_hook that unconditionally sets
  `res.company.stock_text_confirmation=True`** on every company where the
  field was False, as long as the default SMS template XML record is
  present. Consequence: right after install, the "Text Confirmation"
  setting is already ticked. Tasks that want the user to toggle it must
  reset `company.stock_text_confirmation=False` in the seed **after**
  `button_immediate_install` completes.
- `_reset_sms_text_confirmation` (uninstall hook) wipes the flag off
  companies that had it set — not relevant for our task but worth noting
  if a benchmark later uninstalls and reinstalls.

## Feature lives on res.company, not picking_type_id

- The SMS delivery-notification feature is a pair of company-dependent
  fields on `res.company`: `stock_text_confirmation` (bool) and
  `stock_confirmation_type` (selection, only value `'sms'`). There is NO
  `stock.picking.type.sms_confirmation` field — despite what similar
  patterns (signature on delivery, email confirmation) might suggest.
- The Settings UI path is **Inventory > Configuration > Settings >
  Operations block > Text Confirmation**. Action id
  `stock.action_stock_config_settings`.
- `_get_text_validation('sms')` on the company drives the branch in
  `stock_sms.StockPicking._pre_action_done_hook` and
  `_send_confirmation_email`.

## stock_sms warning wizard fires exactly once per company

- First validate after the feature is enabled triggers
  `stock_sms.confirm.stock.sms` as a modal wizard
  ("You are about to confirm this Delivery Order by SMS Text Message").
  It has two primary buttons:
  - `send_sms` (**Confirm**, primary/highlighted) → sets
    `has_received_warning_stock_sms=True`, then re-invokes
    `picking.button_validate()` — which now flows into
    `_send_confirmation_email` and emits the SMS.
  - `dont_send_sms` (**Disable SMS**, secondary) → sets
    `has_received_warning_stock_sms=True` **and**
    `stock_text_confirmation=False`, then re-invokes validate — which
    proceeds WITHOUT emitting the SMS because the company flag was
    flipped off.
- Once `has_received_warning_stock_sms=True`, subsequent validates skip
  the wizard entirely and emit SMS silently. Tests that need the wizard
  to appear must reset the flag in the seed.
- Oracle selector for the primary button:
  `.modal:visible button[name='send_sms']` (safer than matching
  "Confirm" text because the label is generic).

## sms.sms persists before .send() runs

- Reaffirmed behaviour from `crm_sms.send_sms_to_opportunity`: the
  `sms.sms` record is created inside `_notify_thread_by_sms` with
  `state='outgoing'`, body rendered from the template, number from
  `partner._phone_format`, and `mail_message_id` linking back to the
  document message. **Only after that** is `sms_all.send(...)` called,
  which flips `state` to `error` when IAP has no credits. Check.py must
  assert persistence (body + number + linkage) and **never** on `state`.

## res.company entity_key normalizes to [null] in state_diff

- Even with `match_key: [name]` on `res.company`, the state diff engine
  emits `entity_key: [null]` for the singleton main company. Reason:
  `_extract_entity_key` reads `record.name`, which on `res.company` is
  a related field and comes back as `False`/`None` when the base
  snapshot's default "YourCompany" record is read through the
  instrumentation cursor (likely because of the company_dependent /
  `search([])` path). Expected_state.json must use
  `"entity_key": [null]` literally to match. Could be patched in
  instrumentation to fall back to `partner_id.name`, but the easier
  path for now is to use the observed key.

## Stock picking `origin` is the SO name, not client_order_ref

- Established by `delivery.set_third_party_carrier_print_label` cookbook
  and reconfirmed here: a picking created by confirming a sale.order
  copies the SO's `name` into `origin`. To let the prompt refer to a
  deterministic delivery reference (e.g. S-BENCH-SMS-001), set
  `sale.order.name` directly in `create()` — don't rely on
  `client_order_ref`.
