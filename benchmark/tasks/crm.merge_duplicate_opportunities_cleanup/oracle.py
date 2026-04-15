"""Oracle for crm.merge_duplicate_opportunities_cleanup.

Open CRM list view, select two Northwind Advisory opportunities with
email renewal@northwind.example.com, merge them. On the merged record
set stage Qualified, Expected Revenue 24000. Schedule a Call activity.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_button,
    ensure_list_view,
    fill_field,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Switch to list view — CRM defaults to kanban
    ensure_list_view(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Clear any default filters (like "My Pipeline")
    clear_search_filters(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Select the two Northwind Advisory rows with renewal@northwind.example.com
    # Find rows containing "Northwind" and select their checkboxes
    rows = page.locator(".o_list_view .o_data_row")
    count = rows.count()

    selected = 0
    for i in range(count):
        row = rows.nth(i)
        row_text = row.inner_text()
        if "Northwind Advisory" in row_text:
            checkbox = row.locator(".o_list_record_selector input[type='checkbox']").first
            checkbox.click()
            page.wait_for_timeout(300)
            selected += 1
            if selected >= 2:
                break

    page.wait_for_timeout(500)

    # Open Action menu and click Merge
    # In Odoo 19, the Actions dropdown in list view may use different selectors
    actions_btn = page.locator(
        ".o_control_panel .o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_control_panel button:has-text('Actions'):visible, "
        ".o_control_panel button:has-text('Action'):visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(500)

    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Merge')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # In merge wizard/dialog, confirm the merge
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # Look for merge button - may be "Merge" or a primary button
        merge_btn = modal.last.locator(
            "button:has-text('Merge'), button.btn-primary"
        ).first
        merge_btn.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
        _wait_for_ready(page)

    # After merge, we should be on the merged opportunity form
    # If we're back on the list view, click the merged record
    form = page.locator(".o_form_view")
    if form.count() == 0:
        page.wait_for_timeout(1000)
        _wait_for_ready(page)
        # If still on list, click the Northwind record
        if form.count() == 0:
            row = page.locator(".o_list_view .o_data_row:has-text('Northwind')").first
            row.click()
            page.wait_for_load_state("load")
            _wait_for_ready(page)

    # Set stage to Qualified via the status bar
    stage_btn = page.locator(".o_statusbar_status button:has-text('Qualified')")
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Set expected revenue
    fill_field(page, "expected_revenue", "24000")
    page.wait_for_timeout(500)

    # Save before scheduling activity
    save_form(page)
    page.wait_for_timeout(500)

    # Schedule Call activity
    schedule_activity(
        page,
        activity_type="Call",
        summary="Northwind duplicate cleanup",
        due_date="05/08/2026",
    )


run_oracle(oracle)
