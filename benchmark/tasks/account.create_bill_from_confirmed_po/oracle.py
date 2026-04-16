"""Oracle for account.create_bill_from_confirmed_po.

Open confirmed PO BENCH-BILL-PO, click Create Bill, set bill date to
05/03/2026 and bill reference to MSC-BILL-9921, Confirm the bill.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_status_button,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    search_for,
    set_date,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    # The default /odoo/purchase shows RFQs. Navigate to Purchase Orders list.
    navigate(page, "/odoo/purchase-orders")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Search by partner_ref (hidden column but searchable) to narrow list
    search_for(page, "BENCH-BILL-PO")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # There should be one row after search; select its checkbox
    rows = page.locator(".o_list_view .o_data_row")
    assert rows.count() >= 1, "No rows after searching BENCH-BILL-PO"
    rows.first.locator(
        ".o_list_record_selector input[type='checkbox']"
    ).first.click()
    page.wait_for_timeout(500)

    # Click Create Bills in the list header (appears after selection)
    create_btn = page.locator(
        ".o_list_view button.o_list_button_create_bills, "
        ".o_control_panel button:has-text('Create Bills'):visible, "
        ".o_list_view header button:has-text('Create Bills')"
    ).first
    create_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Set Bill Date and Reference on the draft bill form
    set_date(page, "invoice_date", "05/03/2026")
    page.wait_for_timeout(500)

    fill_field(page, "ref", "MSC-BILL-9921")
    page.wait_for_timeout(500)

    # Confirm the bill
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
