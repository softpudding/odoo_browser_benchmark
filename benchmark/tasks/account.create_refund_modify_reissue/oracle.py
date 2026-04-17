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

    modal_set_date(page, "date", "06/05/2026")
    page.wait_for_timeout(500)

    # Click "Reverse and Create Invoice" (NOT the default "Reverse" button)
    modal_click_button(page, "Reverse and Create Invoice")
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # We are now on the new draft invoice (copy of original).
    # The draft may have auto_post set due to future date; fix if needed.
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)

    auto_post_widget = page.locator(".o_field_widget[name='auto_post']").first
    if auto_post_widget.count() > 0:
        select_trigger = auto_post_widget.locator(
            ".o_select_menu, .dropdown-toggle"
        ).first
        if select_trigger.count() > 0:
            select_trigger.click()
            page.wait_for_timeout(500)
            options = page.locator(
                ".dropdown-menu:visible .o_select_menu_item, "
                ".dropdown-menu:visible .dropdown-item"
            )
            for i in range(options.count()):
                if options.nth(i).inner_text().strip() == "No":
                    options.nth(i).click()
                    break
            page.wait_for_timeout(500)
            _wait_no_loading(page)

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

    # Set the invoice date to 06/10/2026
    set_date(page, "invoice_date", "06/10/2026")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Dismiss any datepicker that may still be open
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(500)

    # Confirm / post the new invoice
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
