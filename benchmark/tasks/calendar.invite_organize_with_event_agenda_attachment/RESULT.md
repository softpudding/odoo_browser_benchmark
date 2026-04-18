# Result: calendar.invite_organize_with_event_agenda_attachment

| Field | Value |
|---|---|
| Task ID | calendar.invite_organize_with_event_agenda_attachment |
| Difficulty | hard (tier 3) |
| Time / step limits | 480 sec / 300 steps |

## Oracle

- Agent: `oracle` (JSON-RPC via `call_kw` in-page)
- Outcome: **PASS**, F1=1.0, wall-clock 10.8 s
- State-diff: 2 expected edits matched exactly (name + allday on calendar.event)
- Strategy: read admin tz, convert 14:00 local to UTC, create calendar.event
  with `partner_ids` = [Alice, Bob], then `ir.attachment.create` with
  `res_model='calendar.event' res_id=<event>` and base64 agenda.txt bytes.

## Browser-use

- Agent: browser-use (default provider/model)
- Outcome: **FAIL**, F1=0.0 (postcondition failure → score downgraded)
- Wall-clock 82.2 s
- Agent created the calendar.event with name + attendees in draft form but
  **could not upload the agenda file** and **never saved** the event.
- Concrete blocker reported in agent_stdout: browser-use's own sandbox
  rejected the seed-provided file path with
  `File path benchmark/tasks/.../agenda.txt is not available. To fix:
  The user must add this file path to the available_file_paths parameter
  when creating the Agent.` — BU retried 6+ times and gave up.
- Postcondition: `No ir.attachment named 'agenda.txt' linked to calendar
  event id=2; all attachments: ['invitation.ics', 'invitation.ics']` (the
  two invitation.ics rows are the auto-generated calendar invites for the
  two attendees; BU did add the attendees correctly).

## Calibration

Hard, as specified. BU's native file-upload weakness is double-reinforced
in this run: (a) the chatter paperclip triggers a hidden
`<input type="file">` that needs an OS dialog, and (b) browser-use
additionally guards uploads behind an `available_file_paths` allow-list
that the task harness does not pass through. Even a strong LLM-driven
browser agent would need code-level changes to the runner to clear this
task — aligns with the "BU canonical weakness: file uploads" cookbook
note.

## Files

All 9 required task files live in
`benchmark/tasks/calendar.invite_organize_with_event_agenda_attachment/`:
`task.yaml`, `prompt.md`, `seed.py`, `oracle.py`, `check.py`,
`expected_state.json`, `state_spec.yaml`, `trace_spec.yaml`,
`cleanup.py`, plus `seed_artifacts/agenda.txt`.
