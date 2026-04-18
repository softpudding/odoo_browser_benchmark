"""Seed for website_hr_recruitment.apply_public_then_schedule_interview."""


JOB_NAME = "Platform Support Analyst"
DEPARTMENT_NAME = "Operations"
APPLICANT_NAME = "Casey Portal"
APPLICANT_EMAIL = "casey.portal@example.com"
MARC_LOGIN = "marc.demo"
MARC_NAME = "Marc Demo"


def setup(env):
    old_apps = env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ])
    if old_apps:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", old_apps.ids),
        ]).unlink()
        old_apps.unlink()

    department = env["hr.department"].search([("name", "=", DEPARTMENT_NAME)], limit=1)
    if not department:
        department = env["hr.department"].create({"name": DEPARTMENT_NAME})

    marc = env["res.users"].search([("login", "=", MARC_LOGIN)], limit=1)
    if not marc:
        marc = env["res.users"].create({
            "name": MARC_NAME,
            "login": MARC_LOGIN,
            "password": MARC_LOGIN,
            "group_ids": [(4, env.ref("hr_recruitment.group_hr_recruitment_user").id)],
        })
    else:
        marc.write({"name": MARC_NAME})

    job = env["hr.job"].with_context(active_test=False).search([("name", "=", JOB_NAME)], limit=1)
    if job:
        if not job.active:
            job.active = True
        job.write({
            "department_id": department.id,
            "is_published": True,
        })
    else:
        env["hr.job"].create({
            "name": JOB_NAME,
            "is_published": True,
            "department_id": department.id,
            "no_of_recruitment": 1,
        })
