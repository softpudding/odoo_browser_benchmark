"""Oracle for hr_expense.create_expense_report_submit."""

from benchmark.oracle_helpers import (
    click_create,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)

    click_create(page)
    _wait_for_ready(page)

    fill_field(page, "name", "Summit hotel stay")
    set_many2one(page, "product_id", "Hotel Stay")
    set_date(page, "date", "07/02/2026")
    total = page.locator(".o_field_widget[name='total_amount_currency'] input:visible")
    if total.count() > 0:
        total.first.click()
        total.first.fill("")
        total.first.fill("245.00")
        total.first.press("Tab")
        page.wait_for_timeout(300)
    quantity = page.locator(".o_field_widget[name='quantity'] input:visible")
    if quantity.count() > 0:
        quantity.first.click()
        quantity.first.fill("")
        quantity.first.fill("1")
        quantity.first.press("Tab")
        page.wait_for_timeout(300)

    save_form(page)
    _wait_no_loading(page)

    click_status_button(page, "Submit")
    _wait_no_loading(page)


run_oracle(oracle)
