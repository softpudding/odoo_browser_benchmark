"""Cleanup for hr_skills_survey.link_certification_survey_to_skill.

BLOCKED TASK — hr.skill has no survey_id in this Community checkout, so
there is nothing to clean up. The guard below turns this into a no-op
that stays safe if the field ever becomes available without the rest of
the task being fleshed out.
"""


def cleanup(env):
    if "survey_id" not in env["hr.skill"]._fields:
        return

    # Once the enterprise extension is available, cleanup would look like:
    #
    # skills = env["hr.skill"].search([("name", "=", "Python")])
    # skills.write({"survey_id": False})
    # if "survey.survey" in env.registry:
    #     env["survey.survey"].with_context(active_test=False).search(
    #         [("title", "=", "Bench Python Cert")]).unlink()
