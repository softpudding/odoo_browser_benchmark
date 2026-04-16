"""Oracle for sale.set_commitment_date.

Find confirmed SO BENCH-COMMIT-01, cancel it, reset to draft, navigate to
Other Information tab, set Delivery Date to 05/20/2026, then re-confirm.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    click_status_button,
    click_tab,
    set_date,
    modal_click_button,
)

TARGET_REF = "BENCH-COMMIT-01"
DELIVERY_DATE = "05/20/2026"


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Find and open the target sales order
    click_list_row(page, TARGET_REF)
    _wait_for_ready(page)

    # Step 1: Cancel the order — triggers ConfirmationDialog
    click_status_button(page, "Cancel")
    page.wait_for_timeout(800)

    # Confirm the cancellation dialog
    if page.locator(".modal:visible, .o_dialog:visible").count() > 0:
        modal_click_button(page, "Ok")
        page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Step 2: Reset to Draft
    click_status_button(page, "Set to Quotation")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Step 3: Navigate to Other Information tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)

    # Step 4: Set Delivery Date (commitment_date) to 05/20/2026
    set_date(page, "commitment_date", DELIVERY_DATE)
    page.wait_for_timeout(500)

    # Step 5: Confirm the order
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
