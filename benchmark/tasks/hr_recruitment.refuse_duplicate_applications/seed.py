"""Seed applicants for the recruitment duplicate-refusal wizard task.

Category 2: Policy trap (wizard).
The agent must refuse the correct applicant, notice the duplicate-applications
toggle, and edit the outgoing refusal email before submitting. Browser-use
often accepts the dialog with defaults and leaves the duplicate application
active.
"""


APPLICANT_NAMES = [
    "Priya Nair",
    "Priya Nair (Referral)",
    "Priya Narayan",
]


def setup(env):
    applicants = env["hr.applicant"].with_context(active_test=False).search(
        [("partner_name", "in", APPLICANT_NAMES)]
    )
    if applicants:
        applicants.unlink()

    template = env["mail.template"].search(
        [("name", "=", "Benchmark Applicant Withdrawal Template")], limit=1
    )
    if not template:
        template = env["mail.template"].create(
            {
                "name": "Benchmark Applicant Withdrawal Template",
                "model_id": env.ref("hr_recruitment.model_hr_applicant").id,
                "subject": "Default withdrawal subject",
                "body_html": "<p>Default withdrawal body.</p>",
                "email_from": "{{ user.email_formatted }}",
            }
        )

    reason = env["hr.applicant.refuse.reason"].search(
        [("name", "=", "Candidate withdrew")], limit=1
    )
    if not reason:
        reason = env["hr.applicant.refuse.reason"].create(
            {
                "name": "Candidate withdrew",
                "template_id": template.id,
            }
        )
    else:
        reason.write({"template_id": template.id})

    dept = env["hr.department"].search([("name", "=", "Operations")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Operations"})

    analyst = env["hr.job"].search([("name", "=", "Operations Analyst")], limit=1)
    if not analyst:
        analyst = env["hr.job"].create(
            {
                "name": "Operations Analyst",
                "department_id": dept.id,
                "no_of_recruitment": 1,
            }
        )

    coordinator = env["hr.job"].search(
        [("name", "=", "Operations Coordinator")], limit=1
    )
    if not coordinator:
        coordinator = env["hr.job"].create(
            {
                "name": "Operations Coordinator",
                "department_id": dept.id,
                "no_of_recruitment": 1,
            }
        )

    admin = env.ref("base.user_admin")
    admin.write({"email": "admin@example.com"})

    env["hr.applicant"].create(
        {
            "partner_name": "Priya Nair",
            "email_from": "priya.nair@example.com",
            "partner_phone": "+1 555-0171",
            "job_id": analyst.id,
            "department_id": dept.id,
            "user_id": admin.id,
        }
    )
    env["hr.applicant"].create(
        {
            "partner_name": "Priya Nair (Referral)",
            "email_from": "priya.nair@example.com",
            "partner_phone": "+1 555-0171",
            "job_id": coordinator.id,
            "department_id": dept.id,
            "user_id": admin.id,
        }
    )
    env["hr.applicant"].create(
        {
            "partner_name": "Priya Narayan",
            "email_from": "priya.narayan@example.com",
            "partner_phone": "+1 555-0188",
            "job_id": analyst.id,
            "department_id": dept.id,
            "user_id": admin.id,
        }
    )
