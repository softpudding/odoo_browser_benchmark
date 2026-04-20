"""Seed for website_hr_recruitment.publish_job_set_interview_form_and_archive_old_posting."""

def setup(env):
    for mod_name in ("website_hr_recruitment", "hr_recruitment_survey"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()
    env["hr.job"].with_context(active_test=False).search([("name", "in", ["Warehouse Interview Specialist", "Legacy Support Agent"]) ]).unlink()
    survey = env["survey.survey"].search([("title", "=", "Bench Interview Form")], limit=1)
    if not survey:
        survey = env["survey.survey"].create({"title": "Bench Interview Form", "survey_type": "recruitment"})
    dept = env["hr.department"].search([("name", "=", "Administration")], limit=1) or env["hr.department"].create({"name": "Administration"})
    env["hr.job"].create({"name": "Legacy Support Agent", "department_id": dept.id, "no_of_recruitment": 1, "website_published": True, "is_published": True, "active": True})
