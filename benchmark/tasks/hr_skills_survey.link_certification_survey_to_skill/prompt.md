# Link a certification survey to a skill (BLOCKED)

> **Note**: This task is BLOCKED because Odoo 19 **Community** does not expose a
> `survey_id` / "Certification" many2one on `hr.skill`. The bridge module
> `hr_skills_survey` in Community only adds a *readonly* `survey_id` on
> `hr.resume.line` (populated automatically by `_mark_done()` when an
> employee takes and passes a certification survey) and a
> `certification_validity_months` Integer on `survey.survey`. There is no
> `hr.skill` extension that lets an admin pick a survey as the skill's
> Certification.
>
> The `hr.skill` → survey picker is an **Enterprise-only** feature that
> is not present in `addons/hr_skills/` or `addons/hr_skills_survey/` on
> this branch (verified: no module declares `_inherit = 'hr.skill'` that
> adds a survey field). The task cannot be executed end-to-end without
> pulling the enterprise-only skill-certification link code into the
> codebase.
>
> The original task intent is preserved below for future re-scoping when
> the enterprise addon becomes available.

You will create a certification survey and link it to an existing skill
record so that passing the survey awards the skill to an employee.

## Phase 1 — Create the certification survey

1. Open the **Surveys** app (`/odoo/surveys`).
2. Create a new survey titled `Bench Python Cert`:
   - **Survey Type**: `Certification`
   - Enable **Scoring** with **Required Score (%)** = `70`
   - Add two scored multiple-choice questions (one correct, two incorrect
     answers each):
     - Q1: `What is the correct way to create a list in Python?`
     - Q2: `Which keyword defines a function in Python?`
3. Save & leave active.

## Phase 2 — Link the survey to the skill

4. Navigate to **Employees → Configuration → Skill Types** and open
   skill type `Programming Languages`.
5. Open the skill row `Python`.
6. In the `Certification` field, pick the `Bench Python Cert` survey
   from the autocomplete.
7. Save the skill.

## Phase 3 — Take the survey and verify skill award

8. On `Bench Python Cert` survey, click **Test** (or take the survey
   as admin), answer both questions correctly, submit.
9. Go back to admin's employee record → **Skills** tab → confirm the
   `Python` skill now has a certification badge / valid-to date.

## Rules

- Do NOT seed/create duplicate skills or surveys.
- The final state must show exactly one `Bench Python Cert` survey,
  linked via `hr.skill.survey_id` to the `Python` skill, and the
  admin employee must have an `hr.employee.skill` row flagged as
  certified.
