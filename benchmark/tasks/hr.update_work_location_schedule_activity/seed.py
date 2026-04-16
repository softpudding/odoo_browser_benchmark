"""Seed an employee for the update-work-location-schedule-activity task.

Category 2 (MEDIUM): update one main-form field, switch to the Work
Information tab for a second edit, save, and then schedule a chatter activity.
"""

EMPLOYEE_NAME = "Avery Collins"
ACTIVITY_SUMMARY = "Confirm home office setup"


def _ensure_location(env, name, location_type, street):
    address = env["res.partner"].search([("name", "=", f"{name} Address")], limit=1)
    if not address:
        address = env["res.partner"].create({
            "name": f"{name} Address",
            "street": street,
            "city": "San Francisco",
            "country_id": env.ref("base.us").id,
        })

    location = env["hr.work.location"].search([("name", "=", name)], limit=1)
    if location:
        location.write({
            "location_type": location_type,
            "address_id": address.id,
        })
        return location

    return env["hr.work.location"].create({
        "name": name,
        "location_type": location_type,
        "address_id": address.id,
    })


def setup(env):
    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)])
    if employee:
        env["mail.activity"].search([
            ("res_model", "=", "hr.employee"),
            ("res_id", "in", employee.ids),
        ]).unlink()
        employee.unlink()

    home = _ensure_location(env, "Home", "home", "55 Remote Lane")
    hq = _ensure_location(env, "Headquarters", "office", "100 Market Street")

    dept = env["hr.department"].search([("name", "=", "Customer Success")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Customer Success"})

    job = env["hr.job"].search([("name", "=", "Customer Success Manager")], limit=1)
    if not job:
        job = env["hr.job"].create({
            "name": "Customer Success Manager",
            "department_id": dept.id,
        })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job.id,
        "department_id": dept.id,
        "work_email": "avery.collins@company.com",
        "work_phone": "+1 415 555 0101",
        "work_location_id": hq.id,
    })
