"""Oracle for hr.promote_employee_set_new_job_title_save.

Open 'Bench Promote Me', locate the Job Title char field on the Work
tab (directly below the Job Position many2one), replace 'Analyst' with
'Senior Analyst', and save.

The Job Title field is ``job_title`` (Char) — distinct from the Job
Position many2one ``job_id`` (see
``addons/hr/views/hr_employee_views.xml:161`` and the existing task
``hr.update_employee_job_title`` which targets ``job_id``).
"""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
)

EMPLOYEE_NAME = "Bench Promote Me"
NEW_JOB_TITLE = "Senior Analyst"


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the seeded employee from the kanban/list view.
    click_list_row(page, EMPLOYEE_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill the Job Title char field. It's on the default "Work" tab so
    # no tab switch is needed. ``fill_field`` clears the existing value
    # (``Analyst``) before typing the new one.
    fill_field(page, "job_title", NEW_JOB_TITLE)
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
