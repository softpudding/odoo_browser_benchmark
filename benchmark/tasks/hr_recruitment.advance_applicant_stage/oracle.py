"""Oracle for hr_recruitment.advance_applicant_stage.

Navigate to "Experienced Developer" job, find applicant "Taylor Kim",
move to "First Interview" stage, set appreciation to "In Progress" (1),
and write application summary.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    # Click on the "Experienced Developer" job position
    click_kanban_card(page, "Experienced Developer")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Now in the job's applicant kanban view — find Taylor Kim
    click_kanban_card(page, "Taylor Kim")
    page.wait_for_timeout(500)

    # Set stage to "First Interview" via status bar
    stage_btn = page.locator(
        ".o_statusbar_status button:has-text('First Interview')"
    )
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Set appreciation/priority to "1" (In Progress) — click the first star
    priority_widget = page.locator(".o_field_widget[name='priority']").first
    stars = priority_widget.locator(
        ".o_priority_star, .fa-star, .fa-star-o"
    )
    if stars.count() > 0:
        stars.first.click()
        page.wait_for_timeout(300)

    # Write application summary (applicant_notes is an HTML field)
    desc_field = page.locator(
        ".o_field_widget[name='applicant_notes'] .note-editable, "
        ".o_field_widget[name='applicant_notes'] .odoo-editor-editable, "
        ".o_field_widget[name='applicant_notes'] [contenteditable='true']"
    )
    if desc_field.count() > 0:
        desc_field.first.click()
        page.keyboard.type(
            "Strong technical background. Schedule technical interview next week."
        )
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
