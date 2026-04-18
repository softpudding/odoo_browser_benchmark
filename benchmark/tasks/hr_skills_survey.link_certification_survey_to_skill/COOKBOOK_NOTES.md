# Cookbook notes — hr_skills_survey.link_certification_survey_to_skill

## Feature availability audit: hr.skill ↔ survey.survey link in Community

Odoo 19 Community ships `hr_skills_survey` as a bridge between
`hr_skills` and `survey`, but the Community version of the bridge does
**NOT** add a `survey_id` field on `hr.skill`. Inspection of
`addons/hr_skills_survey/models/` shows the bridge only:

1. Adds a *readonly* `survey_id` + `expiration_status` on
   `hr.resume.line` — populated automatically by `_mark_done()` when a
   certification submission passes.
2. Adds `certification_validity_months` on `survey.survey`.
3. Extends `survey.user_input._mark_done()` to write `hr.resume.line`
   rows for certification passes.

The "pick a survey to award this skill" UI pattern (an editable
`survey_id` many2one rendered on the `hr.skill` form) is
**Enterprise-only** in this Odoo version. `grep '_inherit.*hr\\.skill'`
across all of `addons/` returns no match — no module in the Community
checkout extends `hr.skill` with a survey Many2one.

### Implications for task authors

- Any task that requires the agent to pick a survey on an `hr.skill`
  (or via a "Certification" field on that form) is **not buildable**
  on Community.
- A workflow-adjacent task ("take a certification survey as admin,
  observe the resume line appear") IS possible in Community, but the
  task becomes a single-actor survey flow rather than a
  configuration-then-certify chain. File it under the `survey` or
  `hr_skills_survey` namespace with a clearly different task_id.
- Before picking any `hr_skills*` task that says "link / attach a
  survey to a skill", confirm with:
  ```python
  "survey_id" in env["hr.skill"]._fields
  ```
  If False, the task is blocked until the enterprise extension is
  vendored.

## Pattern for BLOCKED-task commits (reminder)

Following the precedent set by `appointment.public_booking_reschedule_cancel_portal`
and the Enterprise-only helpdesk/marketing_automation tasks, BLOCKED
tasks ship:

1. `task.yaml` with `metadata.blocked_reason` + `primary_track: false`.
2. `seed.py` / `oracle.py` / `check.py` that short-circuit with clear
   diagnostic `RuntimeError` / list-of-failures messages rather than
   silently passing. Each file should also carry a *commented* sketch
   of the real body so a future agent has a starting point once the
   constraint is lifted.
3. `expected_state.json = []` and `state_spec.yaml: models: {}` and
   empty `trace_spec` lists.
4. A `RESULT.md` recording the blocker evidence + re-enabling steps.
5. STATUS.md row set to `Removed` with `FAIL (feature unavailable)`
   in the oracle column, plus a detailed section at the end.

## Precedent

- `appointment.public_booking_reschedule_cancel_portal` (row 350)
- `helpdesk.team_sla_assign_escalate_close` (row 351)
- `marketing_automation.tag_trigger_drip_campaign` (row 352)

All four (including this task) share the same core shape:
Enterprise-only feature / addon absent in Community, skeleton preserved
for forward compatibility.
