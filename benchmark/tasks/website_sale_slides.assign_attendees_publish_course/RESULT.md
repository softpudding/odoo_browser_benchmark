ROW: 375
TASK_ID: website_sale_slides.assign_attendees_publish_course
DIFFICULTY: hard
SUMMARY: Set a draft course to Course-Attendees visibility + On-Invitation enroll, publish it via the frontend Owl systray toggle, add a seeded prerequisite course whose dropdown is domain-filtered by matching visibility+published state, and enroll two seeded partners (Alice+Bob) via the Add Attendees email wizard.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## website_sale_slides.assign_attendees_publish_course

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (eLearning), Mail |
| **Workflow** | Open Bench Onboarding (seeded unpublished, visibility=public). Flip visibility to Course Attendees on the Options tab (auto-coerces enroll to On Invitation). Click Go to Website, toggle the admin systray Unpublished/Published to publish. Return to the backend form, then add Bench 101 (seeded published + members) as a prerequisite via the Prerequisites many2many_tags field. Save. Use the header Add Attendees wizard to select Alice Attendee + Bob Attendee, then Send. |
| **Capability tested** | Multi-stage gated UI: the Prerequisites dropdown's domain (`visibility == form.visibility AND website_published == form.website_published`) only yields the target course after BOTH visibility is flipped to 'members' AND the course is published via the frontend Owl systray toggle. Backend form's Go-to-Website button is the `website_redirect_button` widget — navigation only, not a publish toggle. Add Attendees wizard forces `send_email=True` when `visibility != 'public' or enroll_mode`, requiring a real SMTP sink (seeded aiosmtpd). |
| **Notes** | Browser-use typed `Bench 101` into the prereq autocomplete but moved on to Add Attendees without CLICKING the dropdown option, leaving `prerequisite_channel_ids` empty — classic autocomplete-no-commit failure. It correctly handled visibility, publish, wizard send. The task's one explicit calibration trap (domain-filtered prereq needing both visibility AND publish applied first) lands exactly where BU stumbles. Oracle uses JSON-RPC write because running the frontend systray via Playwright is flaky. |
