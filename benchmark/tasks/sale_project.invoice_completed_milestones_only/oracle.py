"""Oracle for sale_project.invoice_completed_milestones_only.

The 4 milestones are pre-seeded with M1+M2 reached. The agent only needs to:
  1. Open SO S-BENCH-MS-002
  2. Click Create Invoice
  3. Keep "Regular invoice" radio selected
  4. Click Create Draft / Create Invoice in the wizard
The wizard auto-fills quantity=2 because qty_delivered=2 (M1+M2 of 4).
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


SO_REF = "S-BENCH-MS-002"


def oracle(page):
    login(page)

    # Open Sales app and find the SO.
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, SO_REF)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Click Create Invoice (statusbar action).
    try:
        click_status_button(page, "Create Invoice")
    except Exception:
        page.locator(
            "button:visible:has-text('Create Invoice')"
        ).first.click()
        page.wait_for_load_state("load")
        _wait_no_loading(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Wizard appears; ensure "Regular invoice" radio is selected.
    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    regular = modal.locator(
        ".o_field_widget[name='advance_payment_method'] "
        ".o_selection_badge:has-text('Regular invoice'), "
        ".o_field_widget[name='advance_payment_method'] "
        "label:has-text('Regular invoice'), "
        ".o_field_widget[name='advance_payment_method'] "
        ".o_radio_item:has-text('Regular invoice')"
    )
    if regular.count() > 0:
        try:
            regular.first.click()
            page.wait_for_timeout(500)
            _wait_no_loading(page)
        except Exception:
            pass

    # Click Create button (do NOT change qty -- it's auto-filled to 2).
    create_btn = modal.locator(
        "button[name='create_invoices'], "
        "button:has-text('Create Draft'), "
        "button:has-text('Create Invoice')"
    )
    create_btn.first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)


run_oracle(oracle)
