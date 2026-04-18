# crm_sms.send_sms_to_opportunity — result

## Summary

Medium task. The agent opens the 'Bench Hot Lead' opportunity, accesses the cog Actions menu, launches the Send SMS wizard, fills the body text, and clicks Send.

## Oracle

- **Status:** PASS (strict)
- **StateDiffF1:** 1.0
- **Wall clock:** ~21s
- Required modules (`sms`, `crm_sms`) installed via `button_immediate_install` in seed.

## Browser-Use

- **Status:** PASS (strict)
- **StateDiffF1:** 1.0
- **Wall clock:** ~79s

## Calibration notes

- SMS sending calls IAP and fails (no credits), marking `sms.sms.state='error'`. The `sms.sms` record persists with `body`, `number`, `mail_message_id` set; only the transport state reflects the IAP failure. `state_spec.yaml` puts `state` in `ignore_fields` so the diff engine ignores outgoing/error distinctions and only asserts create-with-body-and-number.
- `+16175551234` (valid US E.164) is used instead of the spec's truncated `+15551234` so that `_phone_format` produces a valid sanitized number and the wizard's Send button becomes enabled (`recipient_single_valid=True`).
- No IAP monkeypatch required — the task validates the wizard's document-posting side effect (sms.sms + mail.message create), which occurs before `send()` is called.

## Failure mode

None observed in one run; both agents complete. Kept as a medium coverage task for the `crm_sms` bridge module + cog Actions pattern.
