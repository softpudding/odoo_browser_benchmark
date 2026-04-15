"""Oracle for account.complete_customer_tax_id_then_post.

Open draft invoice VAT-302, read the VAT from narration, navigate to the
customer record, set Tax ID, return via breadcrumb, set Customer Reference,
and post the invoice.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    fill_field,
    click_breadcrumb,
    click_status_button,
    login,
    navigate,
    open_many2one_record,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)

    # Go to Invoices list
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the draft invoice with origin VAT-302
    click_list_row(page, "VAT-302")
    page.wait_for_timeout(1000)

    # Navigate to the customer record.
    # In Odoo 19 form view, partner_id is a many2one that shows as a link.
    # open_many2one_record tries multiple strategies: <a> link, external button, etc.
    # If the standard helper fails, fall back to clicking the partner name directly.
    widget = page.locator(".o_field_widget[name='partner_id']").first

    # Strategy 1: Look for the link (a tag) in the widget
    link = widget.locator("a")
    if link.count() > 0 and link.first.is_visible():
        link.first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        # Strategy 2: Try the helper which checks more selectors
        try:
            open_many2one_record(page, "partner_id")
        except Exception:
            # Strategy 3: Click the input to focus it, then look for external button
            inp = widget.locator("input").first
            inp.click()
            page.wait_for_timeout(500)
            ext_btn = widget.locator("button, .fa-external-link, a.o_external_button, .o_external_button")
            if ext_btn.count() > 0:
                ext_btn.first.click()
                page.wait_for_load_state("load")
                _wait_for_ready(page)
            else:
                # Strategy 4: Use the URL-based navigation
                # Read the partner name and navigate via URL
                partner_text = widget.inner_text().strip()
                # Navigate directly to the partner form by searching
                navigate(page, "/odoo/contacts")
                _wait_no_loading(page)
                click_list_row(page, partner_text)

    page.wait_for_timeout(1000)

    # Set Tax ID to EU3029981
    fill_field(page, "vat", "EU3029981")
    page.wait_for_timeout(500)

    # Save and return to the invoice via breadcrumb
    save_form(page)
    page.wait_for_timeout(500)
    # Navigate back via breadcrumb — click the last breadcrumb link (the invoice)
    bc_items = page.locator(".o_breadcrumb .breadcrumb-item a")
    if bc_items.count() >= 1:
        bc_items.last.click()
        page.wait_for_load_state("load")
        _wait_no_loading(page)
        page.wait_for_timeout(1000)
    else:
        # If no breadcrumb, go back to invoices and re-open
        page.go_back()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
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
