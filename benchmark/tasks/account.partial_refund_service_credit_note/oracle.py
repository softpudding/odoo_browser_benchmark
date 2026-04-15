"""Oracle for account.partial_refund_service_credit_note.

Open posted invoice for Greenfield Manufacturing (ref CN-SERVICE-01), create a
credit note, delete the Onsite Training line, set Warehouse Audit qty to 1,
and post.
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
    click_list_row(page, "CN-SERVICE-01")
    page.wait_for_timeout(1000)

    # Click Credit Note button
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1000)

    # In the wizard, set reason and date
    modal_fill_field(page, "reason", "Warehouse Audit session canceled")
    page.wait_for_timeout(500)

    modal = page.locator(".modal:visible").last
    date_input = modal.locator(".o_field_widget[name='date'] input").first
    date_input.click()
    date_input.fill("")
    date_input.type("05/05/2026")
    date_input.press("Tab")
    page.wait_for_timeout(500)

    # Click Reverse
    modal_click_button(page, "Reverse")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Now on the draft credit note with two lines:
    # Line 0: Warehouse Audit (qty 2)
    # Line 1: Onsite Training (qty 1)
    # We need to delete Onsite Training and set Warehouse Audit qty to 1.

    # Delete the Onsite Training line - click the trash icon on that row
    rows = page.locator(".o_list_view .o_data_row")
    row_count = rows.count()

    for i in range(row_count):
        row = rows.nth(i)
        text = row.inner_text()
        if "Onsite Training" in text:
            delete_btn = row.locator(".o_list_record_remove, .fa-trash-o, .o_list_record_delete").first
            delete_btn.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
            break

    # Now set Warehouse Audit qty to 1
    qty_cell = page.locator(".o_list_view .o_data_row td[name='quantity']").first
    qty_cell.click()
    page.wait_for_timeout(500)

    qty_input = qty_cell.locator("input").first
    qty_input.fill("")
    qty_input.fill("1")
    qty_input.press("Tab")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Post the credit note
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
