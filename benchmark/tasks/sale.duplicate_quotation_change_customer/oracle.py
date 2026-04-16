"""Oracle for sale.duplicate_quotation_change_customer.

Open draft quotation BENCH-DUP-01, duplicate via Action menu, change the
copy's customer to Summit Ventures, set customer reference to
SV-DUP-2026, save as draft.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the source quotation
    click_list_row(page, "BENCH-DUP-01")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Open the cog/Actions menu and click Duplicate
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

    # Change customer to Summit Ventures
    set_many2one(page, "partner_id", "Summit Ventures")
    page.wait_for_timeout(500)

    # Customer Reference is on the Other Info tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "SV-DUP-2026")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
