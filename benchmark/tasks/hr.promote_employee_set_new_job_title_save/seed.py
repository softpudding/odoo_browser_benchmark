"""Seed for hr.promote_employee_set_new_job_title_save.

Easy task: seed an hr.employee named 'Bench Promote Me' with
``job_title='Analyst'``. The agent opens the employee form and changes
the Job Title *char field* (not the Job Position many2one) to
'Senior Analyst'.

Notes on Odoo 19 hr.employee:
    * ``hr.employee.job_title`` is a free-text ``Char`` field (see
      ``addons/hr/models/hr_employee.py``). It is distinct from
      ``hr.employee.job_id`` (many2one to ``hr.job`` — the "Job
      Position" field). The existing task
      ``hr.update_employee_job_title`` *despite its name* actually
      edits the ``job_id`` many2one; this new task intentionally
      targets the ``job_title`` char field instead.
    * In the form view (``addons/hr/views/hr_employee_views.xml:161``)
      ``job_title`` is rendered on the default "Work" tab just below
      "Job Position". Label shown in the UI is "Job Title".
"""

EMPLOYEE_NAME = "Bench Promote Me"
OLD_JOB_TITLE = "Analyst"
NEW_JOB_TITLE = "Senior Analyst"
WORK_EMAIL = "bench.promote@example.com"


def _cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()


def setup(env):
    _cleanup(env)

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_title": OLD_JOB_TITLE,
        "work_email": WORK_EMAIL,
    })
