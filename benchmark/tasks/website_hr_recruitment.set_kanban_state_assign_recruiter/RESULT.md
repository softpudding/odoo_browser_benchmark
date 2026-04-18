ROW: 305
TASK_ID: website_hr_recruitment.set_kanban_state_assign_recruiter
DIFFICULTY: medium
SUMMARY: Open seeded applicant Diana Recruit, flip kanban_state ball to 'Ready for Next Stage', set Recruiter, post Log note.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## website_hr_recruitment.set_kanban_state_assign_recruiter

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment (hr_recruitment) |
| **Workflow** | Open the seeded applicant 'Diana Recruit' (linked to job 'Senior QA Engineer'). Click the small kanban_state status ball at the top of the form and pick 'Ready for Next Stage'. Set the Recruiter many2one to 'Recruiter Bob'. Post an internal Log note 'Phone screen done.' in the chatter. Save. |
| **Capability tested** | Three-part edit on a recruitment form: state-selection ball widget + many2one autocomplete + internal Log-note vs public Send-message distinction. |
| **Notes** | Browser-use solved on the first run (F1=1.0, all postconditions pass) in 147 s. The kanban_state ball turned out to be findable via its dropdown and the agent correctly chose 'Log note' instead of 'Send message'. Calibration: this task lands closer to easy than medium for current browser-use. The state_diff covers kanban_state + user_id; the chatter note is asserted only via check.py and the agent posted it correctly as an internal note. |
