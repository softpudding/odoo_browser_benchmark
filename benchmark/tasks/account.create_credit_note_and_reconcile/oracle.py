"""Oracle for account.create_credit_note_and_reconcile.

Open posted invoice for Lakeview Partners (ref CN-TARGET-01), create a credit
note with reason and date, change qty from 18 to 10, and post the credit note.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    modal_click_button,
    modal_fill_field,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the posted invoice by its origin ref
    click_list_row(page, "CN-TARGET-01")
    page.wait_for_timeout(1000)

    # Click Credit Note button (in the statusbar)
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1000)

    # In the credit note wizard, set reason and date
    modal_fill_field(page, "reason", "Partial delivery — 10 units undelivered")
    page.wait_for_timeout(500)

    # Set the credit note date
    modal = page.locator(".modal:visible").last
    date_input = modal.locator(".o_field_widget[name='date'] input").first
    date_input.click()
    date_input.fill("")
    date_input.type("04/30/2026")
    date_input.press("Tab")
    page.wait_for_timeout(500)

    # Click Reverse / Create Credit Note
    modal_click_button(page, "Reverse")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Now on the draft credit note - edit quantity from 18 to 10
    qty_cell = page.locator(".o_list_view .o_data_row td[name='quantity']").first
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
