"""Oracle for website_hr_recruitment.apply_public_then_schedule_interview."""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    click_kanban_card,
    click_list_row,
    full_url,
    run_oracle,
    DB,
    login,
    navigate,
)


def _schedule_call_activity(page) -> None:
    activity_btn = page.locator(
        "button.o-mail-Chatter-activity:visible, "
        ".o-mail-Chatter button:has-text('Activity'):visible, "
        "button.o_ChatterTopbar_activityBtn:visible"
    ).first
    activity_btn.click()
    page.wait_for_timeout(1200)

    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    call_badge = modal.locator(
        ".o_field_widget[name='activity_type_id'] .o_selection_badge:has-text('Call')"
    )
    if call_badge.count() > 0:
        call_badge.first.click()
        page.wait_for_timeout(300)

    summary_input = modal.locator(".o_field_widget[name='summary'] input").first
    summary_input.wait_for(state="visible", timeout=15000)
    summary_input.click(force=True)
    summary_input.fill("")
    summary_input.fill("Schedule initial interview")
    summary_input.press("Tab")
    page.wait_for_timeout(400)

    deadline_widget = modal.locator(".o_field_widget[name='date_deadline']").first
    deadline_input = deadline_widget.locator("input:visible")
    if deadline_input.count() == 0:
        deadline_widget.locator("button, .o_input").first.click()
        page.wait_for_timeout(400)
        deadline_input = deadline_widget.locator("input:visible")
    deadline_input.first.click(force=True)
    deadline_input.first.fill("")
    deadline_input.first.type("05/28/2026")
    deadline_input.first.press("Tab")
    page.wait_for_timeout(500)
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(300)

    assignee = modal.locator(".o_field_widget[name='activity_user_id'] input").first
    assignee.click(force=True)
    assignee.press("Control+a")
    assignee.press("Backspace")
    assignee.fill("")
    assignee.type("Marc Demo")
    page.wait_for_timeout(800)
    options = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text="Marc Demo")
    if options.count() > 0:
        options.first.click(force=True)
    else:
        assignee.press("ArrowDown")
        assignee.press("Enter")
    page.wait_for_timeout(400)
    assignee.press("Tab")
    page.wait_for_timeout(300)

    modal.locator(
        ".modal-footer button:has-text('Schedule'), "
        ".modal-footer button:has-text('Save'), "
        ".modal-footer button.btn-primary"
    ).first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def oracle(page):
    login(page)

    url = "/jobs"
    if DB:
        url = f"/jobs?db={DB}"
    page.goto(full_url(url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # If we hit a database selector page, select the DB
    db_select = page.locator("select[name='db']")
    if db_select.count() > 0 and db_select.is_visible():
        if DB:
            db_select.select_option(DB)
            page.wait_for_timeout(1000)
        page.goto(full_url(url))
        page.wait_for_load_state("load")
        page.wait_for_timeout(3000)

    job_link = page.locator("a:has-text('Platform Support Analyst')").first
    job_link.wait_for(timeout=10000)
    job_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    apply_btn = page.locator(
        "a:has-text('Apply'), "
        "button:has-text('Apply')"
    ).first
    apply_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    page.locator("input[name='partner_name']").first.fill("Casey Portal")
    page.locator("input[name='email_from']").first.fill("casey.portal@example.com")
    page.locator("input[name='partner_phone']").first.fill("+1 555 0128")
    page.locator("input[name='linkedin_profile']").first.fill(
        "linkedin.com/in/casey-portal"
    )
    page.locator("textarea[name='short_introduction']").first.fill(
        "Public applicant ready for interview scheduling."
    )
    page.locator(".s_website_form_send").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    page.wait_for_selector(
        ".s_website_form_end_message:visible, "
        "span:has-text('Thank'):visible, "
        "div:has-text('submitted'):visible, "
        "div:has-text('Congratulations'):visible",
        timeout=15000,
    )

    navigate(page, "/odoo/recruitment")
    click_kanban_card(page, "Platform Support Analyst")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    click_list_row(page, "Casey Portal")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _schedule_call_activity(page)


run_oracle(oracle)
