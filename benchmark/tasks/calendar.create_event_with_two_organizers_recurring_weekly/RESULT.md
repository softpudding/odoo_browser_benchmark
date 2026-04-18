ROW: 312
TASK_ID: calendar.create_event_with_two_organizers_recurring_weekly
DIFFICULTY: medium
SUMMARY: Create recurring weekly (Mondays, until 2026-12-31) calendar event with two attendees and Discuss videocall link.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## calendar.create_event_with_two_organizers_recurring_weekly

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Calendar |
| **Workflow** | Create a new timed calendar event "Weekly Standup" on 2026-06-01 09:00-09:30, invite Alice Admin and Bob Test, enable weekly recurrence on Mondays ending on 2026-12-31 (End date, not count), and generate the Discuss videocall link so `videocall_location` becomes `/calendar/join_videocall/<token>`. Save via breadcrumb (calendar form auto-saves). |
| **Capability tested** | Combined UI interaction over the calendar form Options tab: recurrence dialog (weekly weekday toggles + end_type=end_date date picker), many2many attendees, and the Discuss "Generate meeting URL" one-click button. |
| **Notes** | `calendar.event.set_discuss_videocall_location` is a dummy server method — the actual URL is populated frontend-side; oracle must either click the UI button or craft the `/calendar/join_videocall/<token>` URL and write it with `access_token` directly. BU missed both the 09:00 AM time (picked 01:00) and the Monday-only weekday toggle (left Saturday on). Date ≥30 days out rules out today-coincidence. |
