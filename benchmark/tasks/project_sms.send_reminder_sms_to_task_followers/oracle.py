"""Oracle for project_sms.send_reminder_sms_to_task_followers.

Flow:
  1. Navigate to /odoo/project.
  2. Click the 'Bench SMS Project' kanban card (opens the project's
     tasks kanban).
  3. Switch to list view.
  4. Tick the checkboxes on both reviewer task rows.
  5. Open the cog Actions menu and click 'Send SMS'.
  6. Fill the body with 'Reminder: please review by EOD'.
  7. Click 'Send now' (mass mode secondary button, name=action_send_sms_mass_now).

Notes:
- project_sms binds sms.composer to project.task with
  composition_mode='mass' by default (view xml default_composition_mode='mass'
  + default_mass_keep_log=True). Mass mode creates ONE sms.sms per
  selected record, pulling the number from partner_id via
  _sms_get_recipients_info.
- The composer dialog renders the body via widget='sms_widget' which is a
  plain <textarea>. No rich editor.
- 'Send now' button is `name='action_send_sms_mass_now'`. 'Put in queue'
  is `name='action_send_sms'` in mass mode. The check inspects the
  persisted sms.sms records regardless of which button is used, but the
  prompt asks for Send now to match the UX described.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


SMS_BODY = "Reminder: please review by EOD"
TASK_A_NAME = "Urgent Review Request — Reviewer A"
TASK_B_NAME = "Urgent Review Request — Reviewer B"
PROJECT_NAME = "Bench SMS Project"


def _open_project_tasks(page):
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    # The Projects kanban uses <kanban action="action_view_tasks" type="object">,
    # so clicking anywhere on the card invokes action_view_tasks → tasks action.
    card = page.locator(
        f".o_kanban_view .o_kanban_record:has-text({PROJECT_NAME!r})"
    ).first
    card.wait_for(state="visible", timeout=15000)
    card.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)
    # Wait until we leave the project kanban and land on the tasks view.
    # The tasks action uses view_mode kanban,list,form,calendar,pivot,graph,activity
    # so by default we land in a task kanban (not the project kanban).
    page.wait_for_selector(
        ".o_action_manager .o_kanban_view.o_task_kanban, "
        ".o_action_manager .o_kanban_view[class*='project_task'], "
        ".o_action_manager .o_list_view .o_list_table, "
        ".o_action .o_kanban_view, .o_action .o_list_view",
        timeout=15000,
    )
    page.wait_for_timeout(800)


def _switch_to_list(page):
    """Click the list-view button in the view switcher if available."""
    # Try a broader set of selectors for the list switch button.
    btn = page.locator(
        "button.o_switch_view.o_list, "
        ".o_cp_switch_buttons button.o_list, "
        "button[data-tooltip='List'], "
        "button.o_switch_view[aria-label='List'], "
        "button[data-tooltip='list']"
    )
    if btn.count() > 0:
        try:
            btn.first.click(force=True)
        except Exception:
            pass
        page.wait_for_timeout(700)
        _wait_no_loading(page)
    # Wait for list view (either data row or empty-list table).
    page.wait_for_selector(
        ".o_list_view, .o_list_renderer",
        timeout=15000,
    )
    page.wait_for_timeout(600)
    # Wait specifically for a data row
    page.wait_for_selector(
        ".o_list_view .o_data_row",
        timeout=15000,
    )
    page.wait_for_timeout(400)


def _tick_row_checkbox(page, text: str) -> None:
    """Tick the leftmost record checkbox on a list row matching text."""
    # Use partial-match fallback in case em-dash substring is flaky:
    # the suffix "Reviewer A" / "Reviewer B" is unique across seeded rows.
    suffix = text.split("—")[-1].strip() if "—" in text else text
    row = page.locator(
        f".o_list_view .o_data_row:has-text({suffix!r})"
    ).first
    row.wait_for(state="visible", timeout=10000)
    checkbox = row.locator(
        ".o_list_record_selector input[type='checkbox'], "
        "td.o_list_record_selector input[type='checkbox']"
    ).first
    checkbox.check()
    page.wait_for_timeout(200)


def _open_cog_menu(page):
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(400)


def _click_send_sms_menu_item(page):
    item = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Send SMS'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Send SMS')"
    ).first
    item.click()
    page.wait_for_timeout(700)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(400)


def _fill_sms_body(page, body: str):
    modal = page.locator(".modal:visible").last
    body_field = modal.locator(
        ".o_field_widget[name='body'] textarea:visible"
    ).first
    body_field.click()
    body_field.fill("")
    body_field.type(body)
    page.wait_for_timeout(300)


def _click_send_now(page):
    modal = page.locator(".modal:visible").last
    # Mass mode secondary button: 'Send now' (name=action_send_sms_mass_now)
    send_btn = modal.locator(
        ".modal-footer button[name='action_send_sms_mass_now']:not([disabled]):visible, "
        ".modal-footer button:has-text('Send now'):not([disabled]):visible"
    ).first
    send_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    _open_project_tasks(page)
    _switch_to_list(page)

    _tick_row_checkbox(page, TASK_A_NAME)
    _tick_row_checkbox(page, TASK_B_NAME)

    _open_cog_menu(page)
    _click_send_sms_menu_item(page)

    _fill_sms_body(page, SMS_BODY)
    _click_send_now(page)


run_oracle(oracle)
