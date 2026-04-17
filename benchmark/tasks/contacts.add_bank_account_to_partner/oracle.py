"""Oracle for contacts.add_bank_account_to_partner."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

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

    # Search for partner.
    search = page.locator(".o_searchview input:visible").first
    search.click()
    search.fill("Benchmark IBAN Supplier Ltd")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    _wait_no_loading(page)

    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "Benchmark IBAN Supplier Ltd")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Go to Accounting tab.
    try:
        click_tab(page, "Accounting")
    except Exception:
        tab = page.locator("a.nav-link:has-text('Accounting'):visible")
        if tab.count() > 0:
            tab.first.click()
    page.wait_for_timeout(500)

    # Click "Add a line" in Bank Accounts.
    add_line = page.locator(
        "div[name='bank_ids'] a:has-text('Add a line'), "
        "div[name='bank_ids'] button:has-text('Add a line'), "
        ".o_field_x2many[name='bank_ids'] a.o_field_x2many_list_row_add"
    ).first
    add_line.wait_for(state="visible", timeout=15000)
    add_line.click()
    page.wait_for_timeout(500)

    # Fill the IBAN in the acc_number cell of the new row.
    acc_input = page.locator(
        "tr.o_selected_row td[name='acc_number'] input, "
        "td[name='acc_number'] input:visible"
    ).first
    acc_input.wait_for(state="visible", timeout=10000)
    acc_input.click()
    acc_input.fill("GB82 WEST 1234 5698 7654 32")
    page.keyboard.press("Tab")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
