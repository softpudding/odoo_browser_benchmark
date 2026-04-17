"""Oracle for mrp.create_mo_consume_produce_done."""

from benchmark.oracle_helpers import (
    click_status_button,
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

    page.get_by_role("button", name="New").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    set_many2one(page, "product_id", "Bench Power Pack")
    set_many2one(page, "bom_id", "BOM-BPP-01")
    fill_field(page, "product_qty", "4")
    save_form(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    for label in ["Produce All", "Mark as Done", "Validate"]:
        btn = page.locator(f"button:visible:has-text('{label}')")
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        primary = modal.locator("button.btn-primary:visible").first
        if primary.count() > 0:
            primary.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)


run_oracle(oracle)
