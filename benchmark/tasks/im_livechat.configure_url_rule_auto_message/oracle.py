"""Oracle for im_livechat.configure_url_rule_auto_message.

The Live Chat kanban opens the discuss-channel session view by default;
to reach the configuration form (with the Rules tab) we open the
kanban card menu and click "Configure Channel".
"""

from benchmark.oracle_helpers import (
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def _open_website_support_form(page):
    """Open the Website Support channel form via the kanban dropdown."""
    card = page.locator(
        ".o_kanban_view .o_kanban_record:has-text('Website Support')"
    ).first
    card.scroll_into_view_if_needed()
    card.hover()
    page.wait_for_timeout(300)

    # Click the per-card menu toggle (3-dots).
    menu_btn = card.locator(
        ".o_dropdown_kanban button, "
        "button[title='Dropdown menu'], "
        "button:has(.oi-ellipsis-v)"
    )
    menu_btn.first.click(force=True)
    page.wait_for_timeout(400)

    # Click "Configure Channel" dropdown item.
    page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Configure Channel'), "
        ".dropdown-menu .dropdown-item:has-text('Configure Channel')"
    ).first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/livechat")
    _wait_no_loading(page)

    _open_website_support_form(page)

    # Switch to the "Rules" tab.
    click_tab(page, "Rules")
    page.wait_for_timeout(500)

    # Click "Add a line" inside the rule_ids one2many list.
    rule_field = page.locator(".o_field_widget[name='rule_ids']").first
    add_link = rule_field.locator(
        "a.o_field_x2many_list_row_add, td.o_field_x2many_list_row_add a"
    )
    if add_link.count() == 0:
        # Fall back to any visible "Add a line" link.
        add_link = page.locator(
            "a.o_field_x2many_list_row_add:visible, "
            "td.o_field_x2many_list_row_add a:visible"
        )
    add_link.first.click()
    page.wait_for_timeout(800)

    # The rule's own form view opens as a modal dialog.
    page.wait_for_selector(".modal:visible", timeout=5000)
    modal = page.locator(".modal:visible").last

    # Select the "Open automatically" radio (action = auto_popup).
    action_widget = modal.locator(".o_field_widget[name='action']").first
    radio = action_widget.locator("input[type='radio'][data-value='auto_popup']")
    if radio.count() == 0:
        radio = action_widget.locator("input[type='radio'][value='auto_popup']")
    if radio.count() > 0:
        radio.first.click(force=True)
    else:
        action_widget.locator("label").filter(has_text="Open automatically").first.click()
    page.wait_for_timeout(500)

    # Fill the auto popup timer (Time to Open).
    timer_widget = modal.locator(".o_field_widget[name='auto_popup_timer']").first
    timer_input = timer_widget.locator("input").first
    timer_input.click()
    timer_input.fill("")
    timer_input.fill("5")
    timer_input.press("Tab")
    page.wait_for_timeout(300)

    # Fill URL Regex.
    regex_widget = modal.locator(".o_field_widget[name='regex_url']").first
    regex_input = regex_widget.locator("input").first
    regex_input.click()
    regex_input.fill("")
    regex_input.fill("/contact")
    regex_input.press("Tab")
    page.wait_for_timeout(300)

    # Save the rule modal ("Save & Close" / "Save").
    save_btn = modal.locator(
        ".modal-footer button:has-text('Save & Close'), "
        ".modal-footer button:has-text('Save'), "
        ".modal-footer button.btn-primary"
    ).first
    save_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Save the parent channel form so the new rule is persisted.
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
