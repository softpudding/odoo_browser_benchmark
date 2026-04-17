"""Oracle for hr_expense.create_expense_with_receipt."""

from benchmark.oracle_helpers import (
    fill_field,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    _wait_no_loading,
)


INTERNAL_NOTES = "Q2 client retention dinner - VIP attendee list on file"


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    new_btn = page.locator(
        "button.o_list_button_add:visible, button.o-kanban-button-new:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    if new_btn.count() > 0:
        new_btn.first.click()
    else:
        page.locator("button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Description (name)
    fill_field(page, "name", "Client dinner at Harborview")
    # Category
    set_many2one(page, "product_id", "Client Meals")
    # Total (visible field is total_amount_currency; backend mirrors to total_amount)
    fill_field(page, "total_amount_currency", "185.50")
    # Date
    set_date(page, "date", "05/12/2026")

    # Payment mode radio — click the company option
    # Odoo radio widget renders: <input type="radio" value="company_account">
    company_radio = page.locator(
        ".o_field_widget[name='payment_mode'] input[type='radio'][data-value='company_account'], "
        ".o_field_widget[name='payment_mode'] input[type='radio'] + label:has-text('Company'), "
        ".o_field_widget[name='payment_mode'] label:has-text('Company')"
    ).first
    company_radio.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Vendor many2one (only visible when payment_mode == company_account)
    set_many2one(page, "vendor_id", "Harborview Restaurant Group")

    # Internal notes (description field is a Text, so textarea)
    fill_text_field(page, "description", INTERNAL_NOTES)

    save_btn = page.locator(
        "button.o_form_button_save:visible, "
        ".o_control_panel button[data-tooltip='Save']:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        page.keyboard.press("Control+s")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
