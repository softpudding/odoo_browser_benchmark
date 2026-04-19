"""Oracle for account.reconcile_customer_payment_against_invoice.

Open the posted invoice INV/BENCH/RECON for Bench Recon Co, click
Register Payment in the header, and in the account.payment.register
wizard click the primary "Create Payment" button (defaults: amount 500,
Bank journal, Manual payment method, today's date).
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Open the posted invoice
    click_list_row(page, "INV/BENCH/RECON")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Click Pay in the header (Register Payment) to open the wizard.
    # Use a direct locator so we pick the statusbar Pay button not a text match.
    pay_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Pay'):visible"
    )
    pay_btn.first.click(force=True)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(1000)

    # In the wizard, defaults should already be:
    #   amount=500.00, journal=Bank, payment_method=Manual,
    #   payment_date=today, memo=invoice name.
    # We just need to click the primary "Create Payment" button.
    modal = page.locator(".modal:visible").last
    create_btn = modal.locator(
        "button.btn-primary[name='action_create_payments']"
    ).first
    if create_btn.count() == 0:
        # Fallback: exact-text match to avoid picking Discard.
        buttons = modal.locator("footer button")
        for i in range(buttons.count()):
            b = buttons.nth(i)
            text = b.inner_text().strip()
            if text in ("Create Payment", "Create Payments"):
                create_btn = b
                break
    create_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)


run_oracle(oracle)
