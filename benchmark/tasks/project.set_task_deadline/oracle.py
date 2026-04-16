"""Oracle for project.set_task_deadline.

Open task Design Landing Page Mockup, change deadline to May 20, 2026, save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_kanban_card,
    set_date,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    click_kanban_card(page, "Omega Platform Launch")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    click_kanban_card(page, "Design Landing Page Mockup")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    edit_btn = page.locator(".o_control_panel button:has-text('Edit'):visible, button.o_form_button_edit:visible")
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    set_date(page, "date_deadline", "05/20/2026")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)