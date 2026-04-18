"""Oracle for hr_expense.submit_report_for_approval.

Create a new hr.expense line for a Paris hotel stay (250.00 on
03/12/2026), save it, then click Submit to Manager so it transitions
from Draft to Submitted.
"""

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

    fill_field(page, "name", "Hotel in Paris")
    set_many2one(page, "product_id", "Travel & Accommodation")
    set_date(page, "date", "03/12/2026")

    # Odoo 19 uses total_amount_currency as the displayed monetary field.
    total = page.locator(
        ".o_field_widget[name='total_amount_currency'] input:visible"
    )
    if total.count() > 0:
        total.first.click()
        total.first.fill("")
        total.first.fill("250.00")
        total.first.press("Tab")
        page.wait_for_timeout(300)
    else:
        # Fallback: the field may be total_amount.
        alt = page.locator(
            ".o_field_widget[name='total_amount'] input:visible"
        )
        if alt.count() > 0:
            alt.first.click()
            alt.first.fill("")
            alt.first.fill("250.00")
            alt.first.press("Tab")
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
    page.wait_for_timeout(800)

    # Click Submit to Manager (the status-bar button). Some builds label
    # the button simply "Submit". Try each label in order.
    try:
        click_status_button(page, "Submit to Manager")
    except Exception:
        click_status_button(page, "Submit")
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
