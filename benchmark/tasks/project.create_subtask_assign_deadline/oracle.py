"""Oracle for project.create_subtask_assign_deadline."""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_list_row,
    click_stat_button,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_list_row(page, "Atlas Implementation Sprint")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_stat_button(page, "Tasks")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_list_row(page, "Prepare onboarding checklist")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_tab(page, "Subtasks")
    page.wait_for_timeout(500)

    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "name", "Draft kickoff agenda")
    page.wait_for_timeout(500)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    subtask_row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row:has-text('Draft kickoff agenda')"
    ).first
    subtask_row.click(force=True)
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    user_input = page.locator(".o_field_widget[name='user_ids'] input").first
    user_input.click()
    user_input.fill("Administrator")
    page.wait_for_timeout(800)
    items = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item"
    )
    for i in range(items.count()):
        txt = items.nth(i).inner_text().strip()
        if "Create" in txt or "create" in txt:
            continue
        if "Administrator" in txt:
            items.nth(i).click()
            break
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    set_date(page, "date_deadline", "05/27/2026")
    page.wait_for_timeout(500)

    stage_btn = page.locator(".o_statusbar_status button:has-text('In Progress')")
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
