"""Oracle for crm.convert_lead_link_customer_schedule_call."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


TARGET_NAME = "Summit Ridge Support Rollout"
TARGET_CUSTOMER = "Summit Ridge Manufacturing"


def oracle(page):
    login(page)
    navigate(page, "/web#action=crm.crm_lead_all_leads")
    _wait_no_loading(page)

    ensure_list_view(page)
    clear_search_filters(page)
    page.wait_for_timeout(500)
    click_list_row(page, TARGET_NAME)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_button(page, "Convert to Opportunity")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    link_radio = modal.locator("label:has-text('Link to an existing customer')")
    if link_radio.count() > 0:
        link_radio.first.click()
        page.wait_for_timeout(500)

    partner_input = modal.locator(".o_field_widget[name='partner_id'] input").first
    partner_input.fill(TARGET_CUSTOMER)
    page.wait_for_timeout(800)
    page.locator(".dropdown-menu .dropdown-item").filter(has_text=TARGET_CUSTOMER).first.click()
    page.wait_for_timeout(500)

    modal.locator(
        "button:has-text('Create Opportunity'), "
        "button:has-text('Convert'), "
        "button.btn-primary"
    ).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    stage_btn = page.locator(".o_statusbar_status button:has-text('Qualified')")
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
