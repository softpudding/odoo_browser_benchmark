"""Oracle for crm.qualify_lead_and_prepare_quote.

Find lead "Northwind Advisory Platform Rollout", convert to opportunity
linked to "Northwind Advisory East", move to Qualified, set revenue and
tag, schedule activity, create draft quotation with customer ref and
expiration.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_button,
    click_kanban_card,
    click_list_row,
    click_tab,
    fill_field,
    login,
    modal_click_button,
    modal_set_many2one,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    set_date,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Switch to list view to find the lead
    page.locator("button.o_switch_view.o_list:visible, .o_cp_switch_buttons button.o_list:visible").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click on the lead "Northwind Advisory Platform Rollout"
    click_list_row(page, "Northwind Advisory Platform Rollout")
    page.wait_for_timeout(1000)

    # Convert to opportunity
    click_button(page, "Convert to Opportunity")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # In the conversion modal, link to customer "Northwind Advisory East"
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal_set_many2one(page, "partner_id", "Northwind Advisory East")
        page.wait_for_timeout(500)

        # Confirm conversion
        modal.last.locator("button:has-text('Create Opportunity'), button:has-text('Convert'), button.btn-primary").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
        _wait_for_ready(page)

    # Move to Qualified stage via status bar
    stage_btn = page.locator(".o_statusbar_status button:has-text('Qualified')").first
    stage_btn.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set expected revenue
    fill_field(page, "expected_revenue", "24000")
    page.wait_for_timeout(500)

    # Add tag "Executive Review"
    add_many2many_tag(page, "tag_ids", "Executive Review")
    page.wait_for_timeout(500)

    # Save before scheduling activity
    save_form(page)
    page.wait_for_timeout(500)

    # Schedule Call activity
    schedule_activity(
        page,
        activity_type="Call",
        summary="Northwind discovery handoff",
        due_date="05/06/2026",
    )

    # Create quotation from the opportunity
    click_button(page, "New Quotation")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Set Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "CRM-HANDOFF-24")
    page.wait_for_timeout(500)

    # Set Expiration date
    set_date(page, "validity_date", "05/20/2026")
    page.wait_for_timeout(500)

    # Save as draft (do not confirm)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
