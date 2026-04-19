"""Seed for hr.change_employee_work_schedule.

Easy task: seed an hr.employee 'Bench Sched Me' with the company's
default ``resource_calendar_id`` (Standard 40 hours/week). Also ensure
a part-time ``resource.calendar`` named 'Part Time 20h' exists for the
agent to select.

The agent opens the employee form, switches to the Payroll tab, and
changes the 'Working Hours' m2o (``resource_calendar_id``) from the
default schedule to 'Part Time 20h', then saves.

Odoo 19 notes:
    * ``hr.employee.resource_calendar_id`` is a Many2one to
      ``resource.calendar`` — field label is "Working Hours" (see
      ``addons/hr/models/hr_version.py`` and the Payroll tab in
      ``addons/hr/views/hr_employee_views.xml:353``). The field is
      rendered under the "Schedule" separator on the Payroll tab
      (``groups="hr.group_hr_manager"`` — admin has access).
    * The company-wide default ``Standard 40 hours/week`` schedule is
      seeded by the ``resource`` module itself
      (``addons/resource/data/resource_data.xml``, xmlid
      ``resource.resource_calendar_std``).
    * ``resource.calendar.hours_per_week`` is a stored compute on
      ``attendance_ids`` — we set it via direct write along with
      ``full_time_required_hours`` so both fields read as 20 without
      needing attendance_ids manipulation for this easy task.
"""


EMPLOYEE_NAME = "Bench Sched Me"
WORK_EMAIL = "bench.sched@example.com"
JOB_TITLE = "Operations"
PART_TIME_CALENDAR_NAME = "Part Time 20h"
DEFAULT_CALENDAR_XMLID = "resource.resource_calendar_std"


def _cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()


def _ensure_default_calendar(env):
    """Return the company's Standard 40h calendar."""
    cal = env.ref(DEFAULT_CALENDAR_XMLID, raise_if_not_found=False)
    if cal:
        return cal
    # Fallback — look up by name.
    cal = env["resource.calendar"].search(
        [("name", "ilike", "Standard 40")], limit=1
    )
    if cal:
        return cal
    # Last-resort fallback: company default.
    company = env.company
    return company.resource_calendar_id


def _ensure_part_time_calendar(env):
    """Ensure 'Part Time 20h' resource.calendar exists with 20h/week."""
    cal = env["resource.calendar"].with_context(active_test=False).search(
        [("name", "=", PART_TIME_CALENDAR_NAME)], limit=1
    )
    if not cal:
        cal = env["resource.calendar"].create({
            "name": PART_TIME_CALENDAR_NAME,
            "company_id": env.company.id,
            "tz": env.company.resource_calendar_id.tz or "UTC",
            "hours_per_week": 20.0,
            "full_time_required_hours": 20.0,
        })
    else:
        # Re-activate if some previous run archived it.
        if not cal.active:
            cal.active = True
        # Ensure the targeted numeric invariants regardless of any
        # prior-run attendance tweaks (defensive — this task only
        # checks resource_calendar_id identity, but the task spec asks
        # hours_per_week=20/full_time_required_hours=20).
        cal.write({
            "hours_per_week": 20.0,
            "full_time_required_hours": 20.0,
        })
    return cal


def setup(env):
    _cleanup(env)

    default_cal = _ensure_default_calendar(env)
    _ensure_part_time_calendar(env)

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_title": JOB_TITLE,
        "work_email": WORK_EMAIL,
        "resource_calendar_id": default_cal.id,
    })
