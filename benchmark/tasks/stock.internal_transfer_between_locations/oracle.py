"""Oracle for stock.internal_transfer_between_locations.

Open the pre-seeded internal transfer (origin BENCH-INT-SHELF-A1),
set done quantity, and validate.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    card = page.locator(
        ".o_kanban_record:has-text('Internal Transfers'):visible"
    ).first
    card.wait_for(state="visible", timeout=15000)
    card.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Clear filters.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    _wait_no_loading(page)

    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "BENCH-INT-SHELF-A1")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    qty_input = page.locator(
        "td[name='quantity'] input:visible, "
        "input[name='quantity']:visible"
    )
    if qty_input.count() > 0:
        qty_input.first.click()
        qty_input.first.fill("5")
        page.keyboard.press("Tab")
        page.wait_for_timeout(400)

    validate_btn = page.locator(
        ".o_form_statusbar button[name='button_validate']:visible, "
        ".o_form_statusbar button:has-text('Validate'):visible"
    ).first
    validate_btn.click()
    page.wait_for_timeout(1500)

    ok = page.locator(
        ".modal button.btn-primary:visible, "
        ".modal button:has-text('Apply'):visible, "
        ".modal button:has-text('OK'):visible"
    )
    if ok.count() > 0:
        try:
            ok.first.click(timeout=2000)
        except Exception:
            pass
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
