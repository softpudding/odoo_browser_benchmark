"""Oracle for crm.create_opportunity_set_close_date_priority."""

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


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    fill_field(page, "name", "Vertex Renewal Expansion")
    page.wait_for_timeout(300)
    set_many2one(page, "partner_id", "Azure Interior")
    page.wait_for_timeout(400)
    fill_field(page, "expected_revenue", "42000")
    page.wait_for_timeout(300)
    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star")
    if stars.count() >= 3:
        stars.nth(2).click()
        page.wait_for_timeout(300)
    set_date(page, "date_deadline", "05/20/2026")
    page.wait_for_timeout(400)
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
