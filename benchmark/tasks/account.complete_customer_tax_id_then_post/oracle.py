"""Oracle for account.complete_customer_tax_id_then_post.

Open draft invoice VAT-302, read the VAT from narration, set customer Tax ID,
set Customer Reference, and post the invoice.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    fill_field,
    click_breadcrumb,
    click_status_button,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)

    # Go to Invoices list
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the draft invoice with origin VAT-302
    # The origin may not be visible as a column, but click_list_row
    # will use the search bar as fallback
    click_list_row(page, "VAT-302")
    page.wait_for_timeout(1000)

    # Open the customer record from the invoice via the external link button
    external_btn = page.locator(
        ".o_field_widget[name='partner_id'] button.o_external_button, "
        ".o_field_widget[name='partner_id'] .o_external_button"
    ).first
    external_btn.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Set Tax ID to EU3029981
    fill_field(page, "vat", "EU3029981")
    page.wait_for_timeout(500)

    # Save and return to the invoice via breadcrumb
    save_form(page)
    page.wait_for_timeout(500)
    # Navigate back — breadcrumb has the invoice number, click it
    bc_items = page.locator(".o_breadcrumb .breadcrumb-item a")
    # Click the last breadcrumb item before current (the invoice)
    if bc_items.count() >= 1:
        bc_items.last.click()
        page.wait_for_load_state("load")
        _wait_no_loading(page)
        page.wait_for_timeout(1000)

    # Go to Other Info tab and set Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "ref", "VAT-302-CLEAR")
    page.wait_for_timeout(500)

    # Post the invoice
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
