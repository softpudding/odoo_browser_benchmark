# hr_holidays.request_time_off_with_attachment - Odoo 19 quirks

## Hard-tier anchor: chatter paperclip + hr.leave

The difficulty of this task is NOT the dates or the type selection — it is
the file upload via the hidden `<input type=file>` behind the chatter
paperclip (`button[aria-label='Attach files']`) on the saved
`hr.leave` form. This pattern is a known-hard anchor because:

1. **Browser-use cannot drive a native OS file-picker** reliably. If BU
   clicks the visible paperclip, a native Chromium file dialog opens
   that BU cannot close; the task effectively stalls.
2. **The benchmark runner does NOT pass `available_file_paths`** to BU's
   Agent kwargs, so even a BU fork that knows about `set_input_files`
   cannot whitelist the PDF path.
3. The Playwright oracle sidesteps this entirely via an
   `ir.attachment.create` RPC with `res_model='hr.leave'` and
   `res_id=<leave_id>`, which is equivalent to what the chatter upload
   does server-side (no `mail.message` needed — `hr.leave`'s chatter
   renders any attachment with the same `res_model/res_id` under its
   attachment pane).

Oracle pattern (JS, via page.evaluate):

```js
await callKw('ir.attachment', 'create', [[{
    name: 'BENCH-JUST.pdf',
    res_model: 'hr.leave',
    res_id: leaveId,
    type: 'binary',
    mimetype: 'application/pdf',
    datas: pdfBase64,
}]], {});
```

If you need to emulate the chatter paperclip flow end-to-end (e.g. for a
half-UI-half-RPC oracle), see `mail.send_email_with_attachment_log_as_note`'s
cookbook — it uses `res_model='mail.compose.message', res_id=0` and
`message_post(attachment_ids=[...])` instead, but that migration only
happens on `mail.thread.message_post` (partner chatter). For
`hr.leave` the direct `res_model='hr.leave', res_id=<id>` pattern works.

## `Paid Leave` type seed: requires_allocation=False

Odoo 19 ships a `Paid Leave` leave type in some demo data configurations
but not others; the benchmark base snapshot doesn't always have it
active. Always seed it explicitly:

```python
leave_type = env["hr.leave.type"].search([("name", "=", "Paid Leave")], limit=1)
vals = {
    "name": "Paid Leave",
    "requires_allocation": False,          # fields.Boolean — not Selection!
    "leave_validation_type": "hr",
    "request_unit": "day",
    "time_type": "leave",
}
if leave_type:
    leave_type.write(vals)
else:
    leave_type = env["hr.leave.type"].create(vals)
```

`requires_allocation=False` lets the agent skip the allocation-first
workflow entirely. This is DIFFERENT from `hr_holidays.request_leave_with_attachment`'s
medium variant which uses `Annual Leave` + `requires_allocation=True`
and has to pre-seed a 20-day allocation — here we remove that dependency
to keep the task laser-focused on the attachment step.

See `hr_holidays.request_sick_leave_approve_self`'s cookbook for the
definitive note that `requires_allocation` is `fields.Boolean`
(`addons/hr_holidays/models/hr_leave_type.py:88`), NOT the `"yes"/"no"`
Selection claimed by `request_allocation_approve_self_book_day_off`'s
cookbook. Pass `False`/`True` — strings coerce but booleans are safer.

## Dates: Wed/Thu for a clean 2.0 number_of_days

`hr.leave.number_of_days` is computed against the employee's resource
calendar (default = Mon-Fri). We pick **2026-07-01 (Wed)** -> **2026-07-02
(Thu)** so the assert is a clean 2.0. A weekend-adjacent pick (e.g.
2026-07-03 Fri -> 2026-07-06 Mon) would straddle the weekend and yield
`number_of_days=2.0` as well (Fri+Mon both working) but with a
confusing 3-day calendar span — avoid such ranges so the prompt reads
naturally.

If you change the dates, also update:
- `prompt.md` date strings
- `seed.py` (only if you want to be defensive about working-day count)
- `oracle.py`'s `request_date_from` / `request_date_to` payload
- `check.py` `EXPECTED_FROM` / `EXPECTED_TO` / `EXPECTED_DAYS`

## state='confirm' vs 'validate' — do NOT approve

Unlike the sibling `hr_holidays.request_sick_leave_approve_self` task,
this prompt explicitly forbids approving the request. Agents that take
the approve action after saving corrupt the final state. The check
accepts `state in {'confirm','validate1','validate'}` defensively (so
one misguided approve click isn't a cascading failure on all the
other gates) but the state-diff `expected_state.json` pins
`"state": "confirm"`, so a validate-state agent still tanks F1.

## Attachment filename matters: BENCH-JUST.pdf

The check gates on exact filename `BENCH-JUST.pdf` (case-insensitive
via `.strip().lower()`). Agents that upload a renamed copy, paste
bytes into the description, or use a different extension fail the
attachment check. This is distinct from the medium sibling
(`request_leave_with_attachment`) which uses `leave_justification.pdf`.

## BU failure mode (observed single-shot calibration)

355s wall-clock run, F1=0.0, 5 postcondition failures:

- **3 Paid Leave records** created (the seeded snapshot had 0; BU spun
  a save-refuse-save-refuse loop, triggering our
  `forbidden_ops: hr.leave.action_refuse` gate once).
- **Wrong dates** (`2026-07-10`/`2026-07-11` instead of
  `2026-07-01`/`2026-07-02`) — BU misread the prompt's "July 1, 2026 →
  July 2, 2026" or fat-fingered the date widget.
- **number_of_days = 1.0** on the surviving leaves (single-day pick).
- **No ir.attachment** on any hr.leave record. BU never drove the
  chatter paperclip.

The combination of date-widget entry + chatter paperclip is the
two-failure-mode anchor that keeps this task reliably in tier 3
territory.

## File layout

```
hr_holidays.request_time_off_with_attachment/
├── task.yaml                # 420s / 220 steps / tier 3 / primary_track
├── prompt.md                # Exact dates + exact filename + chatter-paperclip instruction
├── seed.py                  # Creates Paid Leave type, admin emp, PDF on disk, idempotent cleanup
├── oracle.py                # RPC-only flow (hr.leave + ir.attachment)
├── check.py                 # Gates on 1 leave + dates + days + attachment filename + bytes
├── cleanup.py               # Reverses seed (drops leave, attachments, type cleared opportunistically)
├── expected_state.json      # 4 atomic create edits (match_key ["Mitchell Admin", "Paid Leave"])
├── state_spec.yaml          # Tracks hr.leave only — match_key [employee_id, holiday_status_id]
├── trace_spec.yaml          # required=[], forbidden=unlink/refuse/cancel
└── seed_artifacts/
    └── BENCH-JUST.pdf       # 322 bytes — minimal valid PDF the agent uploads
```
