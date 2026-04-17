"""Oracle for project.update_task_priority."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_kanban_card(page, "Astra Feature Rollout")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_kanban_card(page, "Validate release notes")
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    edit_btn = page.locator(
        "button.o_form_button_edit:visible, "
        ".o_control_panel button:has-text('Edit'):visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        _wait_no_loading(page)

    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star")
    if stars.count() > 0:
        # 1 star = Important
        stars.nth(0).click()
        page.wait_for_timeout(400)
    else:
        page.evaluate("""
            () => {
                const input = document.querySelector(".o_field_widget[name='priority'] input");
                if (!input) {
                    return;
                }
                input.value = '1';
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
