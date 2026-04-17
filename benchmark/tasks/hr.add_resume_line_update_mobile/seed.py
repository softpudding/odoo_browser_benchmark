"""Seed an employee for the add-resume-line-update-location task.

Category 2 (MEDIUM): the agent must edit an existing employee across two tabs
and use the Resume widget to add one precise entry through the UI modal.
"""

EMPLOYEE_NAME = "Marina Ortega"
LINE_TYPE = "Certification"
RESUME_TITLE = "ISO 27001 Internal Auditor"


def _ensure_location(env, name):
    location = env["hr.work.location"].search([("name", "=", name)], limit=1)
    if not location:
        main_address = env.ref("base.main_partner", raise_if_not_found=False)
        location = env["hr.work.location"].create({
            "name": name,
            "address_id": main_address.id if main_address else env.company.partner_id.id,
            "location_type": "office",
        })
    return location


def _ensure_department(env, name):
    dept = env["hr.department"].search([("name", "=", name)], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": name})
    return dept


def _ensure_job(env, name, department):
    job = env["hr.job"].search([("name", "=", name)], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": name,
            "department_id": department.id,
            "no_of_recruitment": 0,
        })
    return job


def _ensure_line_type(env, name):
    line_type = env["hr.resume.line.type"].search([("name", "=", name)], limit=1)
    if not line_type:
        line_type = env["hr.resume.line.type"].create({
            "name": name,
            "sequence": 20,
            "is_course": False,
        })
    return line_type


def setup(env):
    env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)]).unlink()

    office = _ensure_location(env, "HQ West")
    _ensure_location(env, "Home")
    department = _ensure_department(env, "Operations")
    job = _ensure_job(env, "Support Readiness Lead", department)
    _ensure_line_type(env, LINE_TYPE)

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job.id,
        "department_id": department.id,
        "work_email": "marina.ortega@example.com",
        "work_phone": "+1 503 555 0162",
        "work_location_id": office.id,
    })
