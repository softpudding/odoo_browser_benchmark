"""Oracle for sale_project.confirm_quote_and_update_generated_project.

Find quotation with ref SERV-PROJ-17 (Bluebird Labs). Confirm it.
Open generated project. Rename tasks and move stages:
  - "Implementation stream" -> "Bluebird Sprint Kickoff", In Progress
  - "Training stream" -> "Bluebird Training Review", Done
Set project description to "2 service tasks generated from SERV-PROJ-17".
Return to sales order, change Customer Reference to SERV-PROJ-17-LIVE.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
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


def _fill_task_name(page, value):
    """Fill the task name field which uses widget='text' (textarea)."""
    widget = page.locator(".o_field_widget[name='name']").first
    widget.click()
    page.wait_for_timeout(500)

    inp = widget.locator("textarea.o_input, textarea, input")
    if inp.count() > 0 and inp.first.is_visible():
        inp.first.click()
        inp.first.fill("")
        inp.first.fill(value)
        inp.first.press("Tab")
    else:
        # Select all text and replace
        widget.click(click_count=3)
        page.wait_for_timeout(200)
        page.keyboard.press("Control+a")
        page.keyboard.type(value)
        page.keyboard.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _click_stage_if_exists(page, stage_name):
    """Try to click a stage button in the statusbar. Returns True if found."""
    btn = page.locator(
        f".o_statusbar_status button:has-text('{stage_name}'), "
        f".o_statusbar_status .o_arrow_button:has-text('{stage_name}')"
    )
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)
        return True
    return False


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the quotation with ref SERV-PROJ-17
    click_list_row(page, "SERV-PROJ-17")
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

    # We are now in the project's task kanban/list view.
    # Open "Implementation stream" task - try kanban card or list row
    task_card = page.locator(
        ".o_kanban_record:has-text('Implementation stream'), "
        ".o_list_view .o_data_row:has-text('Implementation stream')"
    )
    if task_card.count() > 0:
        task_card.first.click(force=True)
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        click_list_row(page, "Implementation stream")
    page.wait_for_timeout(1000)

    _fill_task_name(page, "Bluebird Sprint Kickoff")
    _click_stage_if_exists(page, "In Progress")

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Go back to task list via breadcrumb (click the last breadcrumb = Tasks)
    breadcrumb = page.locator(".o_breadcrumb .breadcrumb-item a")
    if breadcrumb.count() > 0:
        breadcrumb.last.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        page.go_back()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Open "Training stream" task
    task_card = page.locator(
        ".o_kanban_record:has-text('Training stream'), "
        ".o_list_view .o_data_row:has-text('Training stream')"
    )
    if task_card.count() > 0:
        task_card.first.click(force=True)
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        click_list_row(page, "Training stream")
    page.wait_for_timeout(1000)

    _fill_task_name(page, "Bluebird Training Review")
    _click_stage_if_exists(page, "Done")

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set project description via project settings
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project settings via kebab/dropdown menu on kanban card
    card = page.locator(".o_kanban_record:has-text('Bluebird Labs')").first
    # Hover the card to reveal the kebab menu button (hidden until hover)
    card.hover()
    page.wait_for_timeout(500)
    kebab = card.locator(".o_dropdown_kanban .dropdown-toggle")
    if kebab.count() > 0 and kebab.first.is_visible():
        kebab.first.click()
        page.wait_for_timeout(500)

        settings_link = page.locator(
            ".dropdown-menu .dropdown-item:has-text('Settings'), "
            ".dropdown-item:has-text('Settings')"
        )
        if settings_link.count() > 0:
            settings_link.first.click()
            page.wait_for_load_state("load")
            _wait_for_ready(page)
        else:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            card.click(force=True)
            page.wait_for_load_state("load")
            _wait_for_ready(page)
    else:
        card.click(force=True)
        page.wait_for_load_state("load")
        _wait_for_ready(page)

    # Now we should be on the project form. Look for Description tab.
    desc_tab = page.locator(".o_notebook .nav-link:has-text('Description')")
    if desc_tab.count() > 0:
        desc_tab.first.click()
        page.wait_for_timeout(500)

    # Set project description
    desc_widget = page.locator(".o_field_widget[name='description']").first
    desc_widget.click()
    page.wait_for_timeout(500)

    # Find the editable element
    editable = desc_widget.locator(
        "textarea, .note-editable, .odoo-editor-editable, [contenteditable='true']"
    )
    if editable.count() > 0:
        el = editable.first
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        if tag == "textarea":
            el.fill("2 service tasks generated from SERV-PROJ-17")
        else:
            el.click()
            page.keyboard.press("Control+a")
            page.keyboard.type("2 service tasks generated from SERV-PROJ-17")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Return to the sales order and change Customer Reference
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "SERV-PROJ-17")
    page.wait_for_timeout(1000)

    # Update Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "SERV-PROJ-17-LIVE")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
