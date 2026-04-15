"""Oracle for account.create_credit_note_and_reconcile.

Open posted invoice for Lakeview Partners (ref CN-TARGET-01), create a credit
note with reason and date, change qty from 18 to 10, and post the credit note.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    click_tab,
    login,
    modal_click_button,
    modal_fill_field,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the posted invoice by its ref
    click_list_row(page, "CN-TARGET-01")
    page.wait_for_timeout(1000)

    # Click Credit Note button (in the statusbar)
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1000)

    # In the credit note wizard, set reason and date
    modal_fill_field(page, "reason", "Partial delivery \u2014 10 units undelivered")
    page.wait_for_timeout(500)

    # Set the credit note date.
    # In Odoo 19, the date field renders as a <button> when it has a default value.
    # Click it to switch to input mode, then type the date.
    modal = page.locator(".modal:visible").last
    date_widget = modal.locator(".o_field_widget[name='date']").first
    date_btn = date_widget.locator("button")
    if date_btn.count() > 0:
        date_btn.first.click()
        page.wait_for_timeout(500)
    date_input = date_widget.locator("input:visible").first
    date_input.fill("04/30/2026")
    date_input.press("Tab")
    page.wait_for_timeout(500)
    # Only dismiss a datepicker if one is still open; a bare Escape would
    # close the modal itself.
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(500)

    # Click Reverse / Create Credit Note
    modal_click_button(page, "Reverse")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # When the credit note date is in the future, Odoo 19 sets auto_post='at_date'
    # which hides the Confirm button. We need to set auto_post to 'No' first.
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)

    auto_post_widget = page.locator(".o_field_widget[name='auto_post']").first
    auto_post_widget.locator(".o_select_menu, .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    options = page.locator(".dropdown-menu:visible .o_select_menu_item, .dropdown-menu:visible .dropdown-item")
    for i in range(options.count()):
        if options.nth(i).inner_text().strip() == "No":
            options.nth(i).click()
            break
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Go back to Invoice Lines tab
    click_tab(page, "Invoice Lines")
    page.wait_for_timeout(500)

    # Now on the draft credit note - edit quantity from 18 to 10
    qty_cell = page.locator(
        ".o_form_view .o_list_renderer .o_data_row td[name='quantity'], "
        ".o_list_view .o_data_row td[name='quantity']"
    ).first
    qty_cell.click()
    page.wait_for_timeout(500)

    qty_input = qty_cell.locator("input").first
    qty_input.fill("")
    qty_input.fill("10")
    qty_input.press("Tab")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Post the credit note
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
