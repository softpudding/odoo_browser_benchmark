"""Oracle for crm.lead_set_contact_name_email_phone_save.

Opens the seeded lead 'Bench Lead Basic' from the CRM Leads list and
fills Contact Name, Email, and Phone, then saves.
"""

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


TARGET = "Bench Lead Basic"
CONTACT_NAME = "Alice Example"
EMAIL = "alice@example.com"
PHONE = "+1-555-0200"


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Navigate to Leads list (top menu) — fall back to direct action URL.
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
    page.wait_for_timeout(500)

    click_list_row(page, TARGET)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill the three empty char fields.
    fill_field(page, "contact_name", CONTACT_NAME)
    fill_field(page, "email_from", EMAIL)
    fill_field(page, "phone", PHONE)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
