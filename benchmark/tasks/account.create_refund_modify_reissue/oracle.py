"""Oracle for account.create_refund_modify_reissue.

Open posted invoice for Harborlight Engineering (ref HLE-MOD-01), create a
credit note via "Reverse and Create Invoice", then edit the Technical Audit
line quantity from 8 to 5, set invoice date to 06/10/2026, and confirm.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    click_tab,
    login,
    modal_click_button,
    modal_fill_field,
    modal_set_date,
    navigate,
    run_oracle,
    set_date,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Open the posted invoice by reference
    click_list_row(page, "HLE-MOD-01")
    page.wait_for_timeout(1000)

    # Click Credit Note button
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1000)

    # Fill the reversal wizard
    modal_fill_field(page, "reason", "Quantity correction for project phase 2")
    page.wait_for_timeout(500)

    modal_set_date(page, "date", "04/10/2026")
    page.wait_for_timeout(500)

    # Click "Reverse and Create Invoice" (NOT the default "Reverse" button)
    modal_click_button(page, "Reverse and Create Invoice")
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # We are now on the new draft invoice (copy of original).
    # Go to Invoice Lines tab to edit the Technical Audit quantity
    click_tab(page, "Invoice Lines")
    page.wait_for_timeout(500)

    # Find the Technical Audit row and change quantity from 8 to 5
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    row_count = rows.count()
    if row_count == 0:
        rows = page.locator(".o_list_view .o_data_row")
        row_count = rows.count()

    for i in range(row_count):
        row = rows.nth(i)
        text = row.inner_text()
        if "Technical Audit" in text:
            qty_cell = row.locator("td[name='quantity']").first
            qty_cell.click()
            page.wait_for_timeout(500)
            qty_input = qty_cell.locator("input").first
            qty_input.fill("")
            qty_input.fill("5")
            qty_input.press("Tab")
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
            break

    # Click outside the o2m to deselect, then set the invoice date
    page.locator(".o_form_view .o_form_sheet").first.click(position={"x": 10, "y": 10})
    page.wait_for_timeout(500)

    # Set the invoice date to 06/10/2026 using direct input interaction
    date_widget = page.locator(".o_field_widget[name='invoice_date']").first
    date_widget.scroll_into_view_if_needed()
    date_inp = date_widget.locator("input")
    if date_inp.count() == 0:
        # In Odoo 19, date fields may render as buttons when they have a value
        clickable = date_widget.locator("button, span, div.o_input")
        if clickable.count() > 0:
            clickable.first.click()
            page.wait_for_timeout(500)
        date_inp = date_widget.locator("input")
    if date_inp.count() > 0:
        date_inp.first.click()
        page.wait_for_timeout(300)
        date_inp.first.press("Control+a")
        page.wait_for_timeout(100)
        date_inp.first.type("06/10/2026")
        date_inp.first.press("Tab")
    page.wait_for_timeout(500)
    # Dismiss any datepicker that may still be open
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(300)
    _wait_no_loading(page)

    # Confirm / post the new invoice
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
