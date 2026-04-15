"""Oracle for hr_recruitment.new_applicant_schedule_interview.

Open Recruitment app, click "Senior Backend Developer" job, create a new
applicant Elena Vasquez with contact details, recruiter, and expected salary.
Then schedule a Call activity for the first technical interview.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_create,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    # Click the "Senior Backend Developer" job card to see its applicants
    click_kanban_card(page, "Senior Backend Developer")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click New to create a new applicant
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Fill applicant fields
    fill_field(page, "partner_name", "Elena Vasquez")
    page.wait_for_timeout(500)

    fill_field(page, "email_from", "elena.vasquez@example.com")
    page.wait_for_timeout(500)

    fill_field(page, "partner_phone", "+1 555-0142")
    page.wait_for_timeout(500)

    # Set recruiter
    set_many2one(page, "user_id", "Marc Demo")
    page.wait_for_timeout(500)

    # Go to Details tab and set expected salary
    click_tab(page, "Details")
    page.wait_for_timeout(500)

    fill_field(page, "salary_expected", "85000")
    page.wait_for_timeout(500)

    # Save the applicant
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Schedule Call activity
    schedule_activity(
        page,
        activity_type="Call",
        summary="First technical interview",
        due_date="05/01/2026",
        assigned_to="Marc Demo",
    )


run_oracle(oracle)
