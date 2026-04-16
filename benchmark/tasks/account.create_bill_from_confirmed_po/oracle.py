"""Oracle for account.create_bill_from_confirmed_po.

Open confirmed PO BENCH-BILL-PO, click Create Bill, set bill date to
05/03/2026 and bill reference to MSC-BILL-9921, Confirm the bill.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-BILL-PO")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Click Create Bill in status bar
    click_status_button(page, "Create Bill")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Set Bill Date and Reference
    set_date(page, "invoice_date", "05/03/2026")
    page.wait_for_timeout(500)

    fill_field(page, "ref", "MSC-BILL-9921")
    page.wait_for_timeout(500)

    # Confirm the bill
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
