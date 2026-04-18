"""Seed for hr_skills_survey.link_certification_survey_to_skill.

BLOCKED TASK — Odoo 19 Community's `hr_skills_survey` bridge does NOT
extend `hr.skill` with a `survey_id` / Certification picker. Inspecting
the addons on the `odoo_benchmark` branch:

  - `hr_skills_survey/models/` contains only:
      * `hr_resume_line.py` — adds a *readonly* `survey_id` that is set
        automatically by `_mark_done()` when a passing submission is
        recorded.
      * `survey_survey.py` — adds `certification_validity_months`.
      * `survey_user.py` — extends `_mark_done()` to write
        `hr.resume.line` rows for certification passes.
  - No module declares `_inherit = 'hr.skill'` with a survey Many2one.

The task spec's "link the survey in its Certification field" on the
skill is therefore Enterprise-only and not reachable in this checkout.

To avoid a silent partial pass (where the agent creates the survey but
cannot complete the skill-link step), this seed raises a clear error
so the eval pipeline records the blocker instead of crashing during
browser interaction.
"""


def setup(env):
    # Detect whether the Enterprise-only survey_id field has been added
    # to `hr.skill`. If it ever becomes available, flip the branch below
    # to run the real seed.
    has_survey_link = "survey_id" in env["hr.skill"]._fields
    if not has_survey_link:
        raise RuntimeError(
            "BLOCKED: Odoo 19 Community `hr_skills_survey` does not add a "
            "`survey_id` field on `hr.skill` (Enterprise-only). Task cannot "
            "be run end-to-end. See STATUS.md row 387 and RESULT.md for the "
            "re-enabling procedure."
        )

    # --- If / when enterprise addon is vendored, fill in the real seed ---
    # The sketch below documents what the real seed would do, kept as a
    # comment so future agents can flesh it out without rediscovering the
    # requirements.
    #
    # admin = env.ref("base.user_admin")
    # # Ensure skill type + skill exist
    # skill_type = env["hr.skill.type"].search(
    #     [("name", "=", "Programming Languages")], limit=1)
    # if not skill_type:
    #     skill_type = env["hr.skill.type"].create({
    #         "name": "Programming Languages",
    #     })
    # skill = env["hr.skill"].search([
    #     ("skill_type_id", "=", skill_type.id),
    #     ("name", "=", "Python"),
    # ], limit=1)
    # if not skill:
    #     skill = env["hr.skill"].create({
    #         "skill_type_id": skill_type.id,
    #         "name": "Python",
    #     })
    # # Ensure there are no stale 'Bench Python Cert' surveys from prior runs.
    # env["survey.survey"].with_context(active_test=False).search(
    #     [("title", "=", "Bench Python Cert")]).unlink()
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "hr.skill.survey_id is available."
    )
