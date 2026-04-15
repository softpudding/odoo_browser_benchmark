"""Oracle for crm.merge_duplicate_opportunities_cleanup.

Open CRM list view, select two Northwind Advisory opportunities with
email renewal@northwind.example.com, merge them. On the merged record
set stage Qualified, Expected Revenue 24000. Schedule a Call activity.
"""

from benchmark.oracle_helpers import (
    click_button,
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

    # Switch to list view
    page.locator("button.o_switch_view.o_list:visible, .o_cp_switch_buttons button.o_list:visible").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Select the two Northwind Advisory rows with renewal@northwind.example.com
    # Find rows containing "Northwind" and select their checkboxes
    rows = page.locator(".o_list_view .o_data_row:has-text('Northwind Advisory')")
    count = rows.count()

    selected = 0
    for i in range(count):
        row = rows.nth(i)
        row_text = row.inner_text()
        if "renewal@northwind" in row_text or "Northwind Advisory" in row_text:
            checkbox = row.locator(".o_list_record_selector input[type='checkbox']").first
            checkbox.click()
            page.wait_for_timeout(300)
            selected += 1
            if selected >= 2:
                break

    page.wait_for_timeout(500)

    # Open Action menu and click Merge
    page.locator(".o_control_panel .o_cp_action_menus button:has-text('Action'), .o_control_panel button:has-text('Actions')").first.click()
    page.wait_for_timeout(500)

    page.locator(".dropdown-menu .dropdown-item:has-text('Merge')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # In merge wizard/dialog, confirm the merge
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Merge'), button.btn-primary").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
        _wait_for_ready(page)

    # Now on the merged opportunity form
    # Set stage to Qualified via the status bar
    stage_btn = page.locator(".o_statusbar_status button:has-text('Qualified')").first
    stage_btn.click()
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
