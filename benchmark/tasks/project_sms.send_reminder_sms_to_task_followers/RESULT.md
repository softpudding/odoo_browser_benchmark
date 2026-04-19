# project_sms.send_reminder_sms_to_task_followers — result

## Summary

Medium task exercising the `project_sms` auto-install bridge.  The agent
opens the `Bench SMS Project` Tasks list, multi-selects two seeded
reviewer tasks, invokes cog Actions → Send SMS (mass mode), types the
reminder body, and clicks Send now.  Two `sms.sms` rows are created,
one per task, each carrying a distinct seeded phone number.

## Oracle

- **Status:** PASS (strict)
- **StateDiffF1:** 1.0 (4/4 atomic edits matched)
- **Wall clock:** ~29s
- **Postconditions:** 0 failures
- `sms` is installed via `button_immediate_install`; `project_sms` auto-installs.

## Browser-Use

- **Status:** FAIL (strict)
- **StateDiffF1:** 0.5 (precision 0.333, recall 1.0)
- **Wall clock:** 360s (time limit reached, `gave_up=True`)
- **Postconditions:** 0 failures — BU sent SMS to both recipients
  correctly, but kept retrying Send Now after the modal closed, producing
  12 `sms.sms` creates instead of the expected 4 (3× duplication per
  recipient).

## Calibration notes

- **Chatter Send SMS does NOT exist on project.task.** `project_sms` only
  exposes Send SMS via the cog Actions binding
  (`binding_view_types=list,kanban,form`). The user spec's
  "chatter → Send SMS" framing had to be pivoted to the cog Actions path.
- **Mass mode ≠ followers.**  `composition_mode='mass'` on
  `sms.composer` sends one sms.sms per selected record, routing to the
  record's `partner_id` via `_mail_get_partners`. Followers are a
  cosmetic addition here — they exist on the tasks but do NOT receive
  the SMS. To get ≥2 sms.sms rows, the seed creates two tasks with
  distinct partners and the agent multi-selects both.
- **Stage seeding required.**  Tasks without a `stage_id` fall into a
  collapsed "None" group (via `group_expand` on
  `project.task.type`) and disappear from both kanban and list views
  until the group is expanded.  A seeded `Review` stage pinned to the
  project with `fold=False` keeps the tasks visible on first render.
- **US E.164 phones + country_id=base.us** are required for
  `_phone_format` to sanitize the numbers to themselves. A missing
  country or truncated number leaves `sanitized=False` and the
  resulting sms.sms row flips to `state='canceled'`
  `failure_type='sms_number_missing'`; the row still persists so
  check.py works either way, but the prompt UX assumes successful
  sanitization.
- **sms.sms state is IAP-environment-dependent.**  Without IAP
  credentials, `.send()` flips `state` to `error`; `state_spec.yaml`
  puts `state` + `failure_type` in `ignore_fields`.

## Failure mode

BU duplicate-send: the agent clicked Send Now, saw the modal close,
and (not recognizing completion) re-opened the cog menu and re-ran the
Send SMS action one or two more times. Each run added 2 more
`sms.sms` rows with the same entity_key (same number + same body),
which the diff engine counts as extra `create` edits, collapsing
precision from 1.0 to 0.333. Postconditions still pass because
check.py requires `≥2` matching sms rows covering both numbers — it
does not enforce exact count.
