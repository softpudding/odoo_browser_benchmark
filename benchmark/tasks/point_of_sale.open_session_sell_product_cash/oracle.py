"""Oracle for point_of_sale.open_session_sell_product_cash."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/point-of-sale")
    _wait_no_loading(page)

    card = page.locator(".o_kanban_record, .o_pos_config_kanban").filter(
        has_text="Benchmark Counter"
    ).first
    card.locator("button:has-text('Open Register'), a:has-text('Open Register')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(4000)

    opening_modal = page.locator("div[role='dialog']:has-text('Opening Control')").first
    if opening_modal.count() > 0:
        opening_cash = opening_modal.locator("input:visible").first
        if opening_cash.count() > 0:
            opening_cash.click()
            opening_cash.fill("0")
            opening_cash.press("Tab")
        open_button = opening_modal.locator("button:has-text('Open Register')").first
        page.wait_for_timeout(1000)
        open_button.click()
        opening_modal.wait_for(state="hidden", timeout=15000)
        page.wait_for_timeout(3000)

    page.locator(
        "article[role='button']:has-text('Counter Snack Box'), "
        ".product:has-text('Counter Snack Box'), .product-card:has-text('Counter Snack Box')"
    ).first.click(force=True)
    page.wait_for_timeout(1000)

    page.locator(
        "button.pay-order-button, .actionpad .pay, .pay-button, .btn-switchpane.pay-button, "
        "button:has-text('Pay'), button:has-text('Payment')"
    ).first.click()
    page.wait_for_timeout(1500)

    cash_button = page.locator(
        ".paymentmethod:has-text('Cash'), .payment-method:has-text('Cash'), button:has-text('Cash')"
    )
    if cash_button.count() > 0:
        cash_button.first.click()
        page.wait_for_timeout(500)

    page.locator("button.validation-button.next, .payment-screen .next").first.click()
    page.wait_for_timeout(3000)


run_oracle(oracle)
