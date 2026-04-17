"""Oracle for crm.update_lead_email."""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    leads_menu = page.locator(
        "nav .o_menu_sections a:has-text('Leads'), "
        ".o_navbar a:has-text('Leads')"
    )
    if leads_menu.count() > 0:
        leads_menu.first.click()
        page.wait_for_timeout(800)
    else:
        navigate(page, "/odoo/action-crm.crm_lead_all_leads")
    _wait_no_loading(page)

    click_list_row(page, "Cobalt Cloud Expansion")
    _wait_for_ready(page)
    fill_field(page, "email_from", "cobalt-expansion@cobaltcloud.example.com")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
