"""Oracle for sale_project.confirm_rollout_quote_update_generated_project.

Find quotation with ref ROLL-PROJ-31 (Atlas Retail Group). Confirm it.
Open generated project. Rename tasks and move stages:
  - "Discovery Workshop" -> "Atlas Rollout Kickoff", In Progress
  - "Go-Live Review" -> "Atlas Go-Live Signoff", Done
Set project description to "2 rollout tasks generated from ROLL-PROJ-31".
Return to sales order, change Customer Reference to ROLL-PROJ-31-LIVE.
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

    # Open "Discovery Workshop" task
    task_card = page.locator(
        ".o_kanban_record:has-text('Discovery Workshop'), "
        ".o_list_view .o_data_row:has-text('Discovery Workshop')"
    )
    if task_card.count() > 0:
        task_card.first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        click_list_row(page, "Discovery Workshop")
    page.wait_for_timeout(1000)

    _fill_task_name(page, "Atlas Rollout Kickoff")
    _click_stage_if_exists(page, "In Progress")

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Go back to task list
    breadcrumb = page.locator(".o_breadcrumb .breadcrumb-item a")
    if breadcrumb.count() > 0:
        breadcrumb.first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        page.go_back()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Open "Go-Live Review" task
    task_card = page.locator(
        ".o_kanban_record:has-text('Go-Live Review'), "
        ".o_list_view .o_data_row:has-text('Go-Live Review')"
    )
    if task_card.count() > 0:
        task_card.first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        click_list_row(page, "Go-Live Review")
    page.wait_for_timeout(1000)

    _fill_task_name(page, "Atlas Go-Live Signoff")
    _click_stage_if_exists(page, "Done")

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set project description
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    card = page.locator(".o_kanban_record:has-text('Atlas Retail Group')").first
    kebab = card.locator(
        ".o_kanban_manage_toggle_button, "
        "button.dropdown-toggle, "
        ".o_dropdown_kanban .dropdown-toggle, "
        ".o_kanban_config_button"
    )
    if kebab.count() > 0:
        kebab.first.click()
        page.wait_for_timeout(500)

        settings_link = page.locator(
            ".dropdown-menu a:has-text('Settings'), "
            ".dropdown-menu a:has-text('Edit'), "
            ".o_kanban_manage_section a:has-text('Settings'), "
            ".dropdown-item:has-text('Settings'), "
            ".dropdown-item:has-text('Edit')"
        )
        if settings_link.count() > 0:
            settings_link.first.click()
            page.wait_for_load_state("load")
            _wait_for_ready(page)
        else:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            card.click()
            page.wait_for_load_state("load")
            _wait_for_ready(page)
    else:
        card.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)

    desc_tab = page.locator(".o_notebook .nav-link:has-text('Description')")
    if desc_tab.count() > 0:
        desc_tab.first.click()
        page.wait_for_timeout(500)

    desc_widget = page.locator(".o_field_widget[name='description']").first
    desc_widget.click()
    page.wait_for_timeout(500)

    editable = desc_widget.locator(
        "textarea, .note-editable, .odoo-editor-editable, [contenteditable='true']"
    )
    if editable.count() > 0:
        el = editable.first
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        if tag == "textarea":
            el.fill("2 rollout tasks generated from ROLL-PROJ-31")
        else:
            el.click()
            page.keyboard.press("Control+a")
            page.keyboard.type("2 rollout tasks generated from ROLL-PROJ-31")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Return to the sales order and change Customer Reference
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "ROLL-PROJ-31")
    page.wait_for_timeout(1000)

    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "ROLL-PROJ-31-LIVE")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
