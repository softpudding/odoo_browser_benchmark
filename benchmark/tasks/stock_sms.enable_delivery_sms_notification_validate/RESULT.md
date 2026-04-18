# stock_sms.enable_delivery_sms_notification_validate — result

## Summary

Medium task. The agent toggles the **Text Confirmation** setting in
Inventory > Configuration > Settings (res.company.stock_text_confirmation),
then opens the pending S-BENCH-SMS-001 delivery, clicks **Validate**, and
confirms the stock_sms warning wizard. This chain fires
`_send_confirmation_email -> _message_sms_with_template -> _notify_thread_by_sms`,
which persists an `sms.sms` record keyed to the customer's sanitized
E.164 phone.

## Oracle

- **Status:** PASS (strict)
- **StateDiffF1:** 1.0
- **Precision / Recall:** 1.0 / 1.0
- **Wall clock:** ~23 s
- Required modules (`sms`, `stock_sms`) installed via
  `button_immediate_install` in seed (`stock_sms` is `auto_install=True`
  with `depends=[stock, sms]`).

## Browser-Use

- **Status:** PASS (strict)
- **StateDiffF1:** 1.0
- **Precision / Recall:** 1.0 / 1.0
- **Wall clock:** ~114 s

## Calibration notes

- `stock_sms`'s `post_init_hook` (`_assign_default_sms_template_picking_id`)
  flips `res.company.stock_text_confirmation=True` automatically on install.
  The seed explicitly resets it back to `False` after install so the
  agent has a real setting to toggle (otherwise the task would be
  trivially solvable by just clicking Validate).
- `has_received_warning_stock_sms` is also reset to `False` so the
  stock_sms warning wizard appears on first validate; the agent has to
  choose **Confirm** (the non-default, less-prominent "Disable SMS"
  button is a dedicated distractor for the side-effect trap).
- Customer phone `+16175551234` uses a valid US E.164 format paired with
  `country_id=base.us` so `_phone_format` sanitizes it cleanly —
  matching the exact pattern established by
  `crm_sms.send_sms_to_opportunity`.
- `sms.sms.state` flips from `outgoing` to `error` when IAP has no
  credits. `state` is in `state_spec.yaml.ignore_fields`; `check.py`
  validates persistence (body contains `S-BENCH-SMS-001`, number
  matches phone, mail_message_id links back to the picking) and
  deliberately does not assert on `state`.

## Difficulty framing

Medium side_effect_trap: the agent must both configure a setting
(Inventory > Settings > Operations > Text Confirmation) AND complete a
second wizard (SMS confirmation dialog on Validate) with a non-default
button label ("Confirm" vs "Disable SMS"). Browser-use navigates this
reliably at F1=1.0 in ~2 min; the task contributes SMS/stock bridge
coverage without being a guaranteed failure case.

## Failure mode

None observed across oracle + browser-use runs. The stock_sms warning
wizard's secondary button (**Disable SMS**) sets
`stock_text_confirmation=False` on its own company, which would fail the
check.py company assertion — but browser-use correctly picks the
highlighted primary button.
