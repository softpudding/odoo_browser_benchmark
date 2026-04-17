"""Oracle for mrp.unbuild_product_partial."""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)

    # Navigate: Operations > Unbuild Orders
    page.locator('.o_menu_sections .dropdown-toggle:has-text("Operations")').first.click()
    page.wait_for_timeout(500)
    page.locator('.dropdown-menu:visible .dropdown-item:has-text("Unbuild Orders")').first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.get_by_role("button", name="New").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    set_many2one(page, "product_id", "Field Controller Kit")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Dismiss any modal that appeared
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        close_btn = modal.last.locator("button:has-text('Close'), .btn-close")
        if close_btn.count() > 0:
            close_btn.first.click()
            page.wait_for_timeout(500)

    # BOM should auto-populate; if not, set it
    bom_val = page.locator('.o_field_widget[name="bom_id"] input').first.input_value()
    if "BOM-FCK-UNBUILD" not in bom_val:
        set_many2one(page, "bom_id", "Field Controller Kit")
        page.wait_for_timeout(500)
        # Dismiss modal again if needed
        modal = page.locator(".modal:visible")
        if modal.count() > 0:
            close_btn = modal.last.locator("button:has-text('Close'), .btn-close")
            if close_btn.count() > 0:
                close_btn.first.click()
                page.wait_for_timeout(500)

    fill_field(page, "product_qty", "2")
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click Unbuild button in the statusbar
    unbuild_btn = page.locator('.o_statusbar_buttons button:has-text("Unbuild"):visible')
    if unbuild_btn.count() > 0:
        unbuild_btn.first.click()
    else:
        page.locator('button:visible:has-text("Validate")').first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Handle any confirmation modal
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        primary = modal.last.locator("button.btn-primary:visible")
        if primary.count() > 0:
            primary.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)


run_oracle(oracle)
