"""Oracle for sale.cancel_quotation_log_reason.

Open draft quotation BENCH-CANCEL-01, post log note with the reason,
then click Cancel. Confirm any dialog.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


EXPECTED_NOTE = (
    "Customer withdrew RFP. Cancelling to remove from active pipeline."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-CANCEL-01")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Post log note
    chatter = page.locator("#chatter, .o-mail-Chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.get_by_role("tab", name="Log note").click()
    page.wait_for_timeout(500)
    composer = chatter.locator(".o-mail-Chatter-composer").first
    composer.fill(EXPECTED_NOTE)
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Log").click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Click Cancel — may be in status bar or Action menu
    cancel_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Cancel'), "
        ".o_control_panel button:visible:has-text('Cancel')"
    ).first
    if cancel_btn.count() > 0:
        cancel_btn.click()
    else:
        # Fall back to Action menu Cancel
        cog = page.locator(
            ".o_cp_action_menus button:visible, "
            ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible"
        ).first
        cog.click()
        page.wait_for_timeout(300)
        page.locator(
            ".dropdown-menu:visible .dropdown-item:has-text('Cancel'), "
            ".o-dropdown--menu:visible .dropdown-item:has-text('Cancel')"
        ).first.click()
    page.wait_for_timeout(800)

    # Confirmation dialog — click OK/Cancel inside modal
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), "
            "button:has-text('OK'), "
            "button:has-text('Confirm'), "
            "button:has-text('Cancel')"
        ).last.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
