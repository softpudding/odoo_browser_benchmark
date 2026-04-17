"""Oracle for crm.convert_lead_to_opportunity_simple.

Go to CRM Leads, open the target lead, click Convert to Opportunity,
link to existing Spark Innovations partner, click Create Opportunity.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    modal_set_many2one,
    navigate,
    run_oracle,
    schedule_activity,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    # Leads menu URL in Odoo 19 CRM
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Open Leads via the top navbar; if the option is missing, fall back
    # to the direct URL.
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

    click_list_row(page, "Spark Innovations - Pager SaaS")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    click_status_button(page, "Convert to Opportunity")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Wizard: select "Link to an existing customer" and pick Spark Innovations
    modal = page.locator(".modal:visible").last
    # The action selection defaults to convert; but the Customer section
    # has radio buttons: "Link to an existing customer" and "Create a new
    # customer" (+ sometimes "Do not link").
    link_existing = modal.locator(
        "label:has-text('Link to an existing customer'), "
        "input[data-value='exist']"
    )
    if link_existing.count() > 0:
        link_existing.first.click()
        page.wait_for_timeout(500)
    # Choose the partner
    modal_set_many2one(page, "partner_id", "Spark Innovations")
    page.wait_for_timeout(500)

    # Click Create Opportunity
    modal.locator(
        "button:has-text('Create Opportunity'), "
        "button:has-text('Create opportunity')"
    ).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    qualified_btn = page.locator(
        ".o_statusbar_status button:has-text('Qualified')"
    )
    if qualified_btn.count() > 0:
        qualified_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Confirm rollout timeline",
        due_date="05/15/2026",
    )
    page.wait_for_timeout(800)


run_oracle(oracle)
