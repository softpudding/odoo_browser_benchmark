"""Oracle for crm.move_opportunity_stage.

Find the "Acme Corporation" opportunity in the CRM pipeline and move it
to the "Qualified" stage via the form's stage selector.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_kanban_card,
    click_button,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Click the "Acme Corporation" kanban card to open the opportunity
    click_kanban_card(page, "Acme Corporation")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Change the stage to "Qualified" using the statusbar/stage selector
    # In Odoo 19 CRM, stages are shown as buttons in the statusbar
    qualified_btn = page.locator(
        ".o_statusbar_status button:has-text('Qualified'):visible, "
        ".o_field_widget[name='stage_id'] .o_arrow_button:has-text('Qualified'):visible, "
        "button.o_statusbar_clickable:has-text('Qualified'):visible"
    )
    if qualified_btn.count() > 0:
        qualified_btn.first.click()
    else:
        # Try clicking the current stage to open the dropdown
        stage_dropdown = page.locator(
            ".o_field_widget[name='stage_id'] .o_statusbar_status, "
            ".o_statusbar_status"
        ).first
        stage_dropdown.click()
        page.wait_for_timeout(500)
        page.locator("button:has-text('Qualified'), .dropdown-item:has-text('Qualified')").first.click()

    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
