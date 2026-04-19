# hr_recruitment.hire_candidate_refuse_another — Odoo 19 quirks

## There is no "Hire" button on hr.applicant

- `hr.applicant` form header exposes `Create Employee`
  (`name='create_employee_from_applicant'`) and `Refuse`
  (`name='archive_applicant'`). There is NO "Hire" action — the
  hire path is:
  1. Click the `hired_stage=True` pill in the form status bar
     (default Odoo 19 demo: the `Contract Signed` stage — sequence 5
     — has `hired_stage=True`, `fold=True`). Writing `stage_id` to
     that stage fires `_compute_date_closed`, which sets
     `date_closed=fields.Datetime.now()` (see
     `addons/hr_recruitment/models/hr_applicant.py:598-604`).
  2. The conditionally-invisible Create Employee button becomes
     visible because its invisible clause is
     `employee_id or not active or not date_closed`
     (`hr_applicant_views.xml:92-93`).
- `create_employee_from_applicant` is a **two-phase** action: it
  creates an `hr.employee` row (committing immediately), then returns
  `hr.open_view_employee_list` with `res_id=<new employee id>` so the
  browser lands on the employee form. The DB-level `employee_id`
  back-link is populated inside the action via
  `employee.write({'applicant_ids': self.ids})` — no follow-up Save
  is required for the link to persist, but any post-landing edits
  (e.g. `job_title`) do require a `web_save` to be committed.

## Refuse wizard: `applicant.get.refuse.reason`

- Opened by `hr.applicant.archive_applicant` (header button label
  `Refuse`, hotkey `d`). The action returns
  `ir.actions.act_window` with `res_model='applicant.get.refuse.reason'`
  and `target='new'`.
- The wizard form has:
  - `refuse_reason_id` rendered as `widget="selection_badge"`
    `options="{'horizontal': true, 'no_create': True, 'no_open': True}"`
    — each reason is a coloured badge; the agent clicks one.
  - `send_mail` boolean_toggle, computed by `_compute_send_mail` =
    `refuse_reason_id.template_id and not applicant_without_email`.
    A seeded reason with NO `template_id` starts with `send_mail=False`
    (no email composer revealed). To force the "turn off Send Email"
    trap, seed the reason WITH a template
    (e.g. `mail.email_template_data_applicant_refuse`).
  - Footer primary button is **ALSO** labelled `Refuse`
    (`name='action_refuse_reason_apply'`, hotkey `q`). This is a
    subtle trap: the header Refuse clicked by the agent opens a
    wizard whose primary button reads the same word — agents who
    rely on button-label keyword spotting ("Refuse was clicked;
    task done") fail to click the wizard primary button.
- `action_refuse_reason_apply` writes
  `{refuse_reason_id: <reason>, active: False, refuse_date: now()}`
  on the applicant and optionally posts a refusal email if
  `send_mail=True`.

## hired_stage computed field cascade

- Writing `stage_id` to a stage with `hired_stage=True` triggers
  `_compute_date_closed` (`@api.depends('stage_id.hired_stage')`):
  - First time: `applicant.date_closed = fields.Datetime.now()`.
  - Flipping back to a non-hired stage: `applicant.date_closed = False`
    (resets `application_status` from 'hired' back to 'ongoing').
- `application_status` is a non-stored computed Selection:
  `refused` if `refuse_reason_id`, else `archived` if not `active`,
  else `hired` if `date_closed`, else `ongoing`. The form's three
  web_ribbon widgets (`Refused`/`Archived`/`Hired`) toggle off this
  field.

## state_spec / expected_state for the combined hire+refuse task

- match_key `[partner_name, job_id]` normalises cleanly; `partner_name`
  alone collides when the same applicant is on multiple jobs.
- The diff engine emits 4 atomic `op=set` edits for this task:
  - `hr.applicant.stage_id = "Contract Signed"` (Top Candidate)
  - `hr.applicant.employee_id = "Top Candidate"` (Top Candidate;
    m2o normalises to the new employee's display name, which is
    inherited from the applicant's `partner_name`)
  - `hr.applicant.active = null` (Runner Up; False → null)
  - `hr.applicant.refuse_reason_id = "Not a fit"` (Runner Up)
- `date_closed`, `date_last_stage_update`, `refuse_date`,
  `application_status`, `kanban_state`, `last_stage_id` all need to
  be in `ignore_fields` to avoid noise.

## Near-duplicate refuse reasons as a disambiguation trap

- Odoo 19 demo data ships 6 refuse reasons (`Does not fit the job
  requirements`, `Refused by applicant: job fit`, `Job already
  fulfilled`, `Duplicate`, `Spam`, `Refused by applicant: salary`).
- Seeding near-duplicates (`Not a good fit`, `Not a fit - incomplete
  application`) alongside the correct reason (`Not a fit`) creates
  a selection-badge trap: modern BU still picks the correct one
  reliably if the prompt names it exactly, but noise adds friction
  and some weaker agents mis-click.

## Calibration (hard)

- Oracle: PASS in ~29s, F1=1.0 (4/4 atomic edits matched,
  RequiredOpRecall=1.0, 0 forbidden writes).
- BU single-shot: PASS in ~111s, F1=1.0. BU recognised all three
  decision points (Contract Signed pill, Create Employee button,
  Not a fit badge) and correctly edited `job_title` on the
  pre-filled employee form. **Calibration miss** at single sample —
  task is on the easy side of tier-3. To re-harden, seed the
  correct refuse reason WITH a template so `send_mail` defaults to
  True (forcing a toggle-off + composer-subject override), or add
  4+ distractor applicants so finding the two targets is itself a
  navigation challenge.
