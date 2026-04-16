"""Oracle for crm.update_opportunity_revenue_priority_won."""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    click_list_row(page, "Northwind Renewal Review")
    page.wait_for_timeout(1000)

    fill_field(page, "expected_revenue", "21000")
    page.wait_for_timeout(400)
    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star")
    if stars.count() < 2:
        raise RuntimeError("Priority stars not found on opportunity form")
    stars.nth(1).click()
    page.wait_for_timeout(400)
    save_form(page)
    page.wait_for_timeout(700)

    won_btn = page.locator("button[data-hotkey='w']:visible")
    if won_btn.count() == 0:
        raise RuntimeError("Won button not found on opportunity form")
    won_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
