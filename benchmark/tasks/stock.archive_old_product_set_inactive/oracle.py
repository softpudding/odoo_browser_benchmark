"""Oracle for stock.archive_old_product_set_inactive.

Navigate to Inventory > Products, open the 'Bench Archive Me' product
form, then click the cog Actions menu and select Archive. Confirm any
resulting modal.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


PRODUCT_NAME = "Bench Archive Me"


def _click_cog(page):
    cog = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_cp_action_menus button:visible"
    ).first
    cog.wait_for(state="visible", timeout=10000)
    cog.click()
    page.wait_for_timeout(600)


def _click_menu_item(page, label: str):
    selector = (
        f".o-dropdown--menu:visible .dropdown-item:has-text('{label}'), "
        f".dropdown-menu:visible .dropdown-item:has-text('{label}')"
    )
    page.wait_for_selector(selector, state="visible", timeout=10000)
    page.locator(selector).first.click()
    page.wait_for_timeout(800)


def _confirm_modal_if_present(page):
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        btn = modal.last.locator(
            "button:has-text('Archive'):visible, "
            "button:has-text('OK'):visible, "
            "button:has-text('Confirm'):visible, "
            "button:has-text('Ok'):visible"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


def oracle(page):
    login(page)

    # Go to Products (via the stock.product_template_action_product window
    # action which maps to Inventory > Products > Products).
    navigate(page, "/odoo/action-stock.product_template_action_product")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    ensure_list_view(page)
    page.wait_for_timeout(400)

    # Open the seeded product
    click_list_row(page, PRODUCT_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Open cog Actions menu and click Archive
    _click_cog(page)
    _click_menu_item(page, "Archive")
    _confirm_modal_if_present(page)
    page.wait_for_timeout(600)
    _wait_no_loading(page)


run_oracle(oracle)
