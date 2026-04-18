# Cookbook notes — crm_sms.send_sms_to_opportunity

Quirks discovered while building this task. Fold back into
`benchmark/ODOO19_PATTERNS.md` when similar tasks come up.

## sms / crm_sms module install

- Neither `sms` nor `crm_sms` is in the base snapshot (grep
  `base_modules.txt`).  Seed must `button_immediate_install` both in
  order. `crm_sms` depends on `crm` (in base) and `sms`.

## crm.lead cog Actions — "Send SMS"

- `crm_sms` binds `sms.composer` to `crm.lead` via
  `binding_model_id` + `binding_view_types="form"` (and `list,kanban`
  for the mass-send variant). That binding surfaces as a **cog
  Actions menu item** on the opportunity form (`.o_cp_action_menus`),
  NOT as a header button.
- List/kanban header also gets a direct `SMS` button injected by
  `crm_sms.crm_case_tree_view_oppor`, but that path uses
  `composition_mode='mass'` with `mass_keep_log=True` — a different
  flow than the single-record `comment` mode targeted here.

## sms.composer single-recipient flow

- Opened from form cog: `composition_mode='comment'`,
  `comment_single_recipient=True`.  The dialog renders a "To" line
  with `recipient_single_number_itf` (editable) + a Message textarea
  with `widget="sms_widget"`.
- **Send button is disabled until `recipient_single_valid=True`**.
  Validity depends on `_phone_format` succeeding — a malformed
  number (e.g. `+15551234`, too short for US) keeps the button
  disabled.  Seed must use a fully-formed E.164 (`+16175551234`) and
  ensure the partner's `country_id` is set so the sanitizer
  resolves.

## sms.sms side effect

- Clicking Send invokes `action_send_sms` →
  `_action_send_sms_comment_single` →
  `record._message_sms(body, ...)` → `message_post(message_type='sms',
  ...)` → `_notify_thread_by_sms` creates the `sms.sms` record
  **before** `.send()` is called.
- Therefore the diff shows `sms.sms` as a create with
  `body`, `number`, `mail_message_id` populated regardless of IAP
  success.  The subsequent `.send()` on a machine without an IAP
  account flips `state` from `'outgoing'` to `'error'`.
- Check.py should assert persistence (body + number + linkage to
  `mail.message` on the crm.lead) and IGNORE `state` — the transport
  outcome is environment-dependent.  Put `state` in
  `ignore_fields` in `state_spec.yaml`.

## Message widget for SMS body

- `sms_widget` renders as `<textarea>` inside
  `.o_field_widget[name='body']`.  `page.locator('textarea')`
  targets it; `fill` followed by `type` works.  No rich editor, no
  iframe.
