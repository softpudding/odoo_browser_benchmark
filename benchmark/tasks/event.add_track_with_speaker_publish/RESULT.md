# event.add_track_with_speaker_publish

## Oracle

- Result: PASS
- Wall clock: 28.9s
- StateDiffF1: 1.0 (5/5 matching, 0 missing, 0 extra)
- Strict: PASS
- Required ops: satisfied
- Harmful writes: 0

## Browser-Use

- Result: PASS (single-shot)
- Wall clock: 68.6s
- Steps: 11 (1 login, 1 kanban click, 1 Tracks smart button, 1 New, 1 multi-input
  batch for title + date + speaker_name + speaker_email + Save, 1 Published-stage
  click, 1 done)
- StateDiffF1: 1.0 (5/5 matching)
- Strict: PASS
- Postcondition failures: 0
- Harmful writes: 0

BU followed the explicit prompt about clicking the Published stage and
solved the task on the first try. The instruction was deliberately explicit
to meet the "prompt clarity" bar for the benchmark — medium difficulty here
comes from the combination (smart button + sub-resource + multi-tab fields +
stage-driven publish), not from ambiguity.

## Calibration

Target: medium (~60% solve). Actual: BU passed on single-shot. The task is
on the easier side of medium — probably closer to 80%+ solve given the
explicit prompt. Kept at medium because it still covers a nontrivial UI
chain (drill-into-event → smart button → sub-record form → notebook tab →
status-bar stage click) that probes sub-resource + multi-tab handling.

## Task design notes

- `event.track.date` is a Datetime stored in UTC. Admin tz in the benchmark DB
  is UTC+8, so typing `05/15/2026 10:00:00` in the UI stores `2026-05-15
  02:00:00`. check.py asserts the UTC value.
- `website_event` + `website_event_track` are NOT in the base snapshot; the
  seed installs them on demand via `button_immediate_install` (mirrors the
  pattern in `event.publish_event_register_attendee/seed.py`).
- `is_published` is flipped as a computed side-effect of moving the stage to
  one with `is_fully_accessible=True` — see
  `website_event_track/models/event_track.py::_synchronize_with_stage`.
