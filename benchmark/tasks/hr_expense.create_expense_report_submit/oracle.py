"""Oracle for hr_expense.create_expense_report_submit.

Create an expense "Hotel stay - Berlin conference" for 385.00,
then submit it for approval.
"""

from benchmark.oracle_helpers import (
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    click_create(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Set description
    fill_field(page, "name", "Hotel stay - Berlin conference")
    page.wait_for_timeout(300)

    # Set product/category (required field)
    try:
        set_many2one(page, "product_id", "Travel")
    except Exception:
        # Try any expensable product
        inp = page.locator(".o_field_widget[name='product_id'] input").first
        inp.click()
        page.wait_for_timeout(800)
        # Click first dropdown item
        dropdown = page.locator(
            ".dropdown-menu .dropdown-item:visible"
        )
        if dropdown.count() > 0:
            dropdown.first.click()
        page.wait_for_timeout(500)
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Set total amount (visible when product has no cost)
    total_field = page.locator(
        ".o_field_widget[name='total_amount_currency'] input:visible"
    )
    if total_field.count() > 0:
        total_field.first.click()
        total_field.first.fill("")
        total_field.first.fill("385")
        total_field.first.press("Tab")
    else:
        fill_field(page, "total_amount", "385")
    page.wait_for_timeout(300)
    _wait_no_loading(page)

    # Set expense date
    set_date(page, "date", "06/15/2026")
    page.wait_for_timeout(300)

    # Save the expense
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Submit for approval
    submit_btn = page.locator(
        ".o_statusbar_buttons button[name='action_submit']:visible, "
        ".o_statusbar_buttons button:has-text('Submit'):visible, "
        "button[name='action_submit']:visible, "
        "button:has-text('Submit Report'):visible, "
        "button:has-text('Create Report'):visible"
    ).first
    submit_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        ok_btn = modal.last.locator(
            "button:has-text('Submit'), "
            "button:has-text('Ok'), "
            "button.btn-primary"
        )
        if ok_btn.count() > 0:
            ok_btn.first.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)


run_oracle(oracle)
