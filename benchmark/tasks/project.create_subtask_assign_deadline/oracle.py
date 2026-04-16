"""Oracle for project.create_subtask_assign_deadline."""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_button_name,
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
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

    click_button_name(page, "action_view_tasks")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_list_row(page, "Prepare onboarding checklist")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_tab(page, "Sub-tasks")
    page.wait_for_timeout(500)

    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "name", "Draft kickoff agenda")
    page.wait_for_timeout(500)
    row = page.locator(".o_form_view .o_list_renderer .o_data_row").nth(0)
    user_cell = row.locator("td[name='user_ids'], .o_field_widget[name='user_ids']").first
    user_cell.click()
    page.wait_for_timeout(300)
    user_input = user_cell.locator("input").first
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

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
