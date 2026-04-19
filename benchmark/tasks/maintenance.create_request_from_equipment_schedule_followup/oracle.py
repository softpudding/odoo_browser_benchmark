"""Oracle for maintenance.create_request_from_equipment_schedule_followup."""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_create,
    click_list_row,
    click_stat_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
)


EQUIPMENT_NAME = "Forklift FL-88"
REQUEST_NAME = "Inspect Forklift Battery Cooling"


def _open_equipment(page, name: str) -> None:
    record = page.locator(
        f".o_list_view .o_data_row:has-text('{name}'), "
        f".o_kanban_view .o_kanban_record:has-text('{name}')"
    ).first
    record.wait_for(state="visible", timeout=15000)
    record.click(force=True)
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def _open_requests_from_equipment(page) -> None:
    for label in ("Requests", "Maintenance Requests"):
        try:
            click_stat_button(page, label)
            return
        except Exception:
            continue
    navigate(page, "/odoo/maintenance-requests")


def _schedule_todo_activity(page) -> None:
    activity_btn = page.locator(
        "button.o-mail-Chatter-activity:visible, "
        ".o-mail-Chatter button:has-text('Activities'):visible, "
        ".o-mail-Chatter button:has-text('Activity'):visible, "
        "button:has-text('Schedule Activity'):visible, "
        "button.o_ChatterTopbar_activityBtn:visible"
    ).first
    activity_btn.click()
    page.wait_for_timeout(1200)

    schedule_link = page.locator(
        "button:has-text('Schedule an activity'), "
        "a:has-text('Schedule an activity')"
    )
    if schedule_link.count() > 0 and page.locator(".modal:visible").count() == 0:
        schedule_link.first.click()
        page.wait_for_timeout(800)

    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    summary_input = modal.locator(".o_field_widget[name='summary'] input").first
    summary_input.wait_for(state="visible", timeout=15000)
    summary_input.click(force=True)
    summary_input.fill("")
    summary_input.fill("Review cooling test report")
    summary_input.press("Tab")
    page.wait_for_timeout(400)

    for field_name in ("user_id", "activity_user_id"):
        assignee = page.locator(f".modal:visible .o_field_widget[name='{field_name}'] input")
        if assignee.count() > 0 and assignee.first.is_visible():
            assignee.first.click(force=True)
            assignee.first.fill("")
            assignee.first.type("Marc Demo")
            page.wait_for_timeout(800)
            page.locator(
                ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
            ).filter(has_text="Marc Demo").first.click(force=True)
            page.wait_for_timeout(400)
            break

    deadline_widget = modal.locator(".o_field_widget[name='date_deadline']").first
    deadline_input = deadline_widget.locator("input:visible")
    if deadline_input.count() == 0:
        trigger = deadline_widget.locator("button, input, .o_input").first
        trigger.click()
        page.wait_for_timeout(400)
        deadline_input = deadline_widget.locator("input:visible")
    deadline_input.first.click(force=True)
    deadline_input.first.fill("")
    deadline_input.first.type("05/23/2026")
    deadline_input.first.press("Tab")
    page.wait_for_timeout(500)
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(300)

    modal.locator(
        ".modal-footer button:has-text('Schedule Activity'), "
        ".modal-footer button:has-text('Schedule'), "
        ".modal-footer button:has-text('Save'), "
        ".modal-footer button.btn-primary"
    ).first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def oracle(page):
    login(page)

    navigate(page, "/odoo/maintenance/equipments")
    _wait_no_loading(page)
    _open_equipment(page, EQUIPMENT_NAME)
    _open_requests_from_equipment(page)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    fill_field(page, "name", REQUEST_NAME)
    set_many2one(page, "equipment_id", EQUIPMENT_NAME)
    set_many2one(page, "maintenance_team_id", "Bench Maintenance")
    set_many2one(page, "user_id", "Marc Demo")

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    navigate(page, "/odoo/maintenance-requests")
    click_list_row(page, REQUEST_NAME)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    _schedule_todo_activity(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
