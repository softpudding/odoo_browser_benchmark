from benchmark.oracle_helpers import (
    login, navigate, clear_search_filters, click_create, fill_field,
    set_many2one, set_date, click_tab, click_add_a_line,
    set_o2m_many2one, set_o2m_field, save_form, click_status_button,
    click_button, modal_click_button, modal_fill_field, modal_set_selection,
    _wait_no_loading, run_oracle,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear default "My Quotations" filter
    clear_search_filters(page)
    page.wait_for_timeout(500)

    # Create new quotation
    click_create(page)
    page.wait_for_timeout(1000)

    # Set customer
    set_many2one(page, "partner_id", "Ridgeline Automation")
    page.wait_for_timeout(1000)

    # Set expiration date
    set_date(page, "validity_date", "06/15/2026")
    page.wait_for_timeout(500)

    # Go to Other Info tab to set customer reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "RA-DP-2026")
    page.wait_for_timeout(500)

    # Go back to Order Lines tab to add products
    click_tab(page, "Order Lines")
    page.wait_for_timeout(500)

    # Add first product line: Modular Conveyor Belt x5 @$1200
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_template_id", "Modular Conveyor Belt")
    page.wait_for_timeout(1000)
    set_o2m_field(page, 0, "product_uom_qty", "5")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "1200")
    page.wait_for_timeout(500)

    # Add second product line: Safety Light Curtain x10 @$350
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_template_id", "Safety Light Curtain")
    page.wait_for_timeout(1000)
    set_o2m_field(page, 1, "product_uom_qty", "10")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "350")
    page.wait_for_timeout(500)

    # Confirm the quotation (turns it into a sales order)
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)

    # Click "Create Invoice" button on the sales order
    click_status_button(page, "Create Invoice")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # In the wizard, select "Down payment (percentage)" — rendered as radio widget
    modal = page.locator(".modal:visible").last
    # Click the radio label for "Down payment (percentage)"
    radio_label = modal.locator(
        ".o_field_widget[name='advance_payment_method'] "
        ".o_selection_badge:has-text('Down payment (percentage)'), "
        ".o_field_widget[name='advance_payment_method'] "
        "label:has-text('Down payment (percentage)'), "
        ".o_field_widget[name='advance_payment_method'] "
        ".o_radio_item:has-text('Down payment (percentage)')"
    )
    radio_label.first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Set the down payment percentage to 30
    modal_fill_field(page, "amount", "30")
    page.wait_for_timeout(500)

    # Click "Create Draft" in the wizard (button text is "Create Draft")
    modal_click_button(page, "Create Draft")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Now on the draft invoice - set the invoice date
    # The invoice_date field in Odoo 19 may render as a button initially
    date_widget = page.locator(".o_field_widget[name='invoice_date']").first
    date_widget.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    # Try clicking any button/span to activate the input
    clickable = date_widget.locator("button, span, .o_input")
    if clickable.count() > 0 and date_widget.locator("input:visible").count() == 0:
        clickable.first.click()
        page.wait_for_timeout(500)
    inp = date_widget.locator("input").first
    inp.click()
    inp.fill("")
    inp.type("06/01/2026")
    inp.press("Tab")
    page.wait_for_timeout(500)
    # Close datepicker if open
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Confirm the invoice
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
