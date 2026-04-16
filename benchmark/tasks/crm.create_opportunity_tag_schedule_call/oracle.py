"""Oracle for crm.create_opportunity_tag_schedule_call."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
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

    save_form(page)
    page.wait_for_timeout(500)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    click_kanban_card(page, "Vertex Renewal Expansion")
    page.wait_for_timeout(500)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Review renewal options",
        due_date="05/13/2026",
    )
    page.wait_for_timeout(500)


run_oracle(oracle)
