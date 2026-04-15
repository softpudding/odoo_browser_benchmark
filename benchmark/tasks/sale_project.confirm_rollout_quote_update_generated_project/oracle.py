"""Oracle for sale_project.confirm_rollout_quote_update_generated_project.

Find quotation with ref ROLL-PROJ-31 (Atlas Retail Group). Confirm it.
Open generated project. Rename tasks and move stages:
  - "Discovery Workshop" -> "Atlas Rollout Kickoff", In Progress
  - "Go-Live Review" -> "Atlas Go-Live Signoff", Done
Set project description to "2 rollout tasks generated from ROLL-PROJ-31".
Return to sales order, change Customer Reference to ROLL-PROJ-31-LIVE.
"""

from benchmark.oracle_helpers import (
    click_breadcrumb,
    click_list_row,
    click_stat_button,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the quotation with ref ROLL-PROJ-31
    click_list_row(page, "ROLL-PROJ-31")
    page.wait_for_timeout(1000)

    # Confirm the quotation
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Open the generated project via smart button
    click_stat_button(page, "Project")
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Switch to list view for easier task editing
    list_btn = page.locator("button.o_switch_view.o_list:visible, .o_cp_switch_buttons button.o_list:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Open "Discovery Workshop" task and rename it
    click_list_row(page, "Discovery Workshop")
    page.wait_for_timeout(1000)

    fill_field(page, "name", "Atlas Rollout Kickoff")
    page.wait_for_timeout(500)

    # Move to In Progress stage
    stage_btn = page.locator(".o_statusbar_status button:has-text('In Progress')").first
    stage_btn.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Go back to task list
    click_breadcrumb(page, "Atlas Retail Group")
    page.wait_for_timeout(1000)

    # Open "Go-Live Review" task and rename it
    click_list_row(page, "Go-Live Review")
    page.wait_for_timeout(1000)

    fill_field(page, "name", "Atlas Go-Live Signoff")
    page.wait_for_timeout(500)

    # Move to Done stage
    stage_btn = page.locator(".o_statusbar_status button:has-text('Done')").first
    stage_btn.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set project description - go to project settings
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project settings via kebab menu
    card = page.locator(".o_kanban_record:has-text('Atlas Retail Group')").first
    kebab = card.locator(".o_kanban_manage_toggle_button, button.dropdown-toggle").first
    kebab.click()
    page.wait_for_timeout(500)

    page.locator(".dropdown-menu a:has-text('Settings'), .o_kanban_manage_section a:has-text('Settings')").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    # Click Description tab
    click_tab(page, "Description")
    page.wait_for_timeout(500)

    desc_field = page.locator(
        ".o_field_widget[name='description'] textarea, "
        ".o_field_widget[name='description'] .note-editable, "
        ".o_field_widget[name='description'] .odoo-editor-editable"
    )
    desc_field.first.click()
    desc_field.first.fill("2 rollout tasks generated from ROLL-PROJ-31")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Return to the sales order and change Customer Reference
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Remove filters to see all orders
    filter_tags = page.locator(".o_searchview .o_facet_remove, .o_searchview_facet .o_facet_remove")
    while filter_tags.count() > 0:
        filter_tags.first.click()
        page.wait_for_timeout(500)
        filter_tags = page.locator(".o_searchview .o_facet_remove, .o_searchview_facet .o_facet_remove")
    _wait_no_loading(page)

    click_list_row(page, "ROLL-PROJ-31")
    page.wait_for_timeout(1000)

    # Update Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "ROLL-PROJ-31-LIVE")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
