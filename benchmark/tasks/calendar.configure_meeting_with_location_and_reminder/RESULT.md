# calendar.configure_meeting_with_location_and_reminder — Result

## Task

Medium calendar task: agent creates `calendar.event` 'Quarterly Review' on
2026-06-10 14:00-16:00 (admin tz), sets `location` = 'Conference Room B, Floor 3',
adds two seeded internal users (Alice Attendee + Bob Attendee) via the
`partner_ids` many2many_tags autocomplete, switches to the Options tab, and
picks the pre-existing `Notification - 1 Hours` alarm via the `alarm_ids`
many2many_tags.

## Oracle

- Result: **PASS**  (F1 = 1.0, wall_clock ~28 s, 3/3 matching diff edits).
- Key trick: the `stop` datetime widget is an `invisible="1"` mirror of
  `start` computed from `duration`; typing into the `.o_daterange_end` time
  picker was flaky (end time stayed 1 h past start). The clean fix is to
  write `duration` = `02:00` directly into the `float_time` widget at
  `.o_field_widget[name="duration"] input`. That deterministically sets
  stop = start + 2 h on save.

## Browser-Use

- Result: **PASS**  (F1 = 1.0, wall_clock ~89 s, 0 postcondition failures, single-shot).
- BU found the calendar, clicked New, filled name / date / times / location,
  added Alice + Bob via the attendees autocomplete, switched to Options,
  selected `Notification - 1 Hours` from the Reminders autocomplete, and
  saved.
- Task sits solidly at tier 2 medium: BU handled the multi-field form +
  notebook-tab switch + two different many2many_tags pickers without
  hallucinating or hitting a wizard trap.

## Calibration

- Originally calibrated as a medium because the many2many_tags for
  `alarm_ids` has `no_quick_create=True`: the agent MUST pick an existing
  alarm (typing a free-form duration doesn't create anything). BU handled
  this correctly on first shot.
- Duration field trick meant the oracle went from 0 -> 1 after one fix.
- BU single-shot PASS matches the expected medium-tier behavior: form fields
  + tabs + existing-tag pickers are BU's strong suit; the only BU trap that
  could apply here (create-a-new-alarm) is explicitly not required.

## Cookbook quirks discovered

1. `calendar.event.duration` (`float_time` widget, visible on the main form
   next to the daterange) is the most reliable way to set the end time in an
   oracle. Typing into `.o_daterange_end` -> `.o_time_picker_input[1]` works
   for 1 h defaults but unreliably overrides pre-filled stop values.
2. `alarm_ids` lives on the Options tab only; it is `many2many_tags` with
   `no_quick_create=True`. Pre-seeded data records (e.g. `Notification - 1
   Hours`) are expected match targets.
