"""Oracle for hr_recruitment.schedule_interview_for_applicant."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    schedule_activity,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    click_kanban_card(page, "Operations Analyst")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    ensure_list_view(page)
    page.wait_for_timeout(800)
    click_list_row(page, "riley.mercer@example.com")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Schedule first interview",
        due_date="06/17/2026",
    )
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
