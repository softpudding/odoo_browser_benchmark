"""Oracle for hr_expense.scan_submit_expense_from_mobile_portal.

Drives the "log an expense from My Expenses and submit to manager" flow:

1. Navigate to /odoo/expenses (My Expenses).
2. Click New, pick the Travel - Taxi product, type description,
   override total to 45.00, set date to today.
3. Save.
4. Click the submit/create-report button in the statusbar — depending on
   the exact Odoo 19 configuration this is either 'Submit to Manager' or
   'Create Report' (which auto-submits). We try each in turn.
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
    _wait_for_ready,
)


EXPENSE_NAME = "Airport taxi"
PRODUCT_NAME = "Travel - Taxi"
EXPENSE_DATE = "04/19/2026"


def _override_total(page, value):
    # Try every selector Odoo 19 may use for the total input on hr.expense.
    candidates = [
        ".o_field_widget[name='total_amount_currency'] input",
        ".o_field_widget[name='total_amount'] input",
        "div[name='total_amount_currency'] input",
        "div[name='total_amount'] input",
    ]
    for sel in candidates:
        inp = page.locator(sel)
        if inp.count() == 0:
            continue
        try:
            target = inp.first
            target.scroll_into_view_if_needed()
            target.click()
            # triple-click to select existing content then fill
            target.click(click_count=3)
            target.press("Backspace")
            target.type(value, delay=30)
            target.press("Tab")
            page.wait_for_timeout(700)
            return
        except Exception:
            continue


def _click_any_statusbar_button(page, labels):
    """Click the first visible statusbar button matching any of the labels.

    Returns True if a click happened, False otherwise.
    """
    for label in labels:
        btn = page.locator(
            f".o_statusbar_buttons button:visible:has-text('{label}')"
        )
        if btn.count() > 0:
            try:
                btn.first.click()
                page.wait_for_timeout(1500)
                _wait_no_loading(page)
                return True
            except Exception:
                continue
    return False


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill the product first so the default price/description populate, then
    # override them.
    set_many2one(page, "product_id", PRODUCT_NAME)
    page.wait_for_timeout(500)

    fill_field(page, "name", EXPENSE_NAME)
    page.wait_for_timeout(200)

    set_date(page, "date", EXPENSE_DATE)
    page.wait_for_timeout(200)

    _override_total(page, "45.00")

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Try the Odoo 19 submit flow. Modern Odoo exposes a single 'Create Report'
    # button from the expense form, which on newer versions directly submits.
    # On some versions a 'Submit to Manager' appears instead. After
    # 'Create Report' a sheet/report form may open with its own 'Submit'.
    clicked = _click_any_statusbar_button(
        page,
        ["Submit to Manager", "Submit", "Create Report"],
    )

    # If we landed on a report/sheet form, click Submit on it too.
    if clicked:
        page.wait_for_timeout(1500)
        _click_any_statusbar_button(page, ["Submit to Manager", "Submit"])
        page.wait_for_timeout(800)
        _wait_no_loading(page)


run_oracle(oracle)
