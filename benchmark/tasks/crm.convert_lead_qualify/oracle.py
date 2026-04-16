"""Oracle for crm.convert_lead_qualify."""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_button,
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/web#action=crm.crm_lead_all_leads")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(800)
    clear_search_filters(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    click_list_row(page, "ops+netops@silvermaple.example.com")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_button(page, "Convert to Opportunity")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    if modal.count() > 0:
        modal.locator(
            "button:has-text('Create Opportunity'), button.btn-primary"
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


run_oracle(oracle)
