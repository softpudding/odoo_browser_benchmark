# Cookbook Notes — calendar.configure_meeting_with_location_and_reminder

## New quirks

### 1. `calendar.event.duration` is the reliable end-time handle

In Odoo 19, `calendar.event.stop` is a technical field with
`invisible="1"` on the main form. It is computed from `start + duration`
when the user edits `duration`, or independently when the user edits the
daterange end picker. The `start` field itself uses
`widget="daterange"` with `options="{'end_date_field': 'stop'}"`, so the
end time is exposed via the `.o_daterange_end` pill and a nested
`.o_time_picker_input` inside the opened popover.

Empirically, driving `.o_daterange_end` +
`.o_datetime_picker:visible .o_time_picker_input:nth(1)` with
`click(click_count=3)` / `fill("4:00pm")` / `Tab` is flaky: when the
default stop has already auto-populated to `start + 1h`, Playwright's
fill gets silently dropped and `stop` stays 1 h past `start`. The
calendar create oracles that use this pattern and pass
(e.g. `calendar.invite_external_attendee_by_email`) all happen to have
`duration = 1 h`, so the end time never needs to change and the bug is
hidden.

**Reliable oracle pattern:** write the `duration` field directly as
float_time hh:mm:

```python
duration_input = page.locator('.o_field_widget[name="duration"] input').first
duration_input.click(click_count=3)
duration_input.fill("02:00")
duration_input.press("Tab")
```

This deterministically produces `stop = start + duration` on
`web_save`. Prefer this over poking the daterange end picker whenever
the prompt pins a specific end time.

### 2. `calendar.event.alarm_ids` is many2many_tags with `no_quick_create=True`

On the event form's Options tab, `alarm_ids` renders as
`widget="many2many_tags" options="{'no_quick_create': True}"`. This
means the agent MUST pick an existing `calendar.alarm` record from the
autocomplete dropdown; typing a free-form label does NOT create a new
alarm. Odoo ships seven default alarms in
`calendar/data/calendar_data.xml` covering 15/30 min + 1/2 h
notifications + 1 d notification + 3/6 h email reminders, so "1 hour
before" can always be satisfied by the pre-seeded
`Notification - 1 Hours` record.

Implications for task builders:
- Don't require the agent to "create a new reminder" unless you want a
  gnarly inline-create wizard in the loop.
- The check.py / state_spec should tolerate whichever existing alarm
  the agent picks — assert on `duration_minutes == 60` rather than on
  a specific alarm name or xmlid.
- In `trace_spec.yaml`, put `calendar.alarm.create` / `unlink` in
  `forbidden_ops` to ensure the agent uses the pre-existing records.
