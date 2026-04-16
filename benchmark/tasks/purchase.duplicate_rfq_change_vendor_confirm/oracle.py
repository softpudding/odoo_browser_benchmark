"""Oracle for purchase.duplicate_rfq_change_vendor_confirm.

Open draft RFQ BENCH-RFQ-DUP, duplicate via Action menu, change vendor
to Pinnacle Hardware, set partner_ref to PH-REISSUE-77, and confirm.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Open source RFQ
    click_list_row(page, "BENCH-RFQ-DUP")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Open cog/Actions menu and click Duplicate
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)
    dup_item = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Duplicate'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Duplicate')"
    ).first
    dup_item.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Swap vendor
    set_many2one(page, "partner_id", "Pinnacle Hardware")
    page.wait_for_timeout(500)

    # Set Vendor Reference (partner_ref) - present on the header
    fill_field(page, "partner_ref", "PH-REISSUE-77")
    page.wait_for_timeout(500)

    # Confirm the duplicate
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
