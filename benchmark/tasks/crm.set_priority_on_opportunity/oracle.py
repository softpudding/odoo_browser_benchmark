"""Oracle for crm.set_priority_on_opportunity."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Find and open the opportunity
    click_list_row(page, "Beacon Analytics Deal")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Click on the 2nd star to set Important priority
    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star")
    stars.nth(1).click()
    page.wait_for_timeout(500)

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
