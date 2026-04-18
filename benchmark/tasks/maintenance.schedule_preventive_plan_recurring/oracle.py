"""Oracle for maintenance.schedule_preventive_plan_recurring."""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
)


def _open_equipment(page, name: str) -> None:
    """Open the equipment record by clicking its kanban/list entry."""
    # Try list view first by clicking a row link with the equipment name.
    row = page.locator(
        f".o_data_row:has-text('{name}'), "
        f".o_kanban_record:has-text('{name}')"
    ).first
    row.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def oracle(page):
    login(page)

    # ---- Step 1: edit equipment ----
    navigate(page, "/odoo/maintenance/equipments")
    _wait_no_loading(page)

    _open_equipment(page, "Conveyor Belt CB-7")

    # Click the Maintenance tab.
    page.locator(".o_notebook .nav-link:has-text('Maintenance')").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set Expected Mean Time Between Failure to 120.
    inp = page.locator(".o_field_widget[name='expected_mtbf'] input").first
    inp.click()
    inp.fill("")
    inp.fill("120")
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ---- Step 2: create the preventive request ----
    navigate(page, "/odoo/maintenance-requests")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Title
    page.locator(".o_field_widget[name='name'] input, .o_field_widget[name='name'] textarea").first.click()
    page.locator(".o_field_widget[name='name'] input, .o_field_widget[name='name'] textarea").first.fill("Monthly Belt Inspection")
    page.keyboard.press("Tab")
    page.wait_for_timeout(300)

    # Equipment
    set_many2one(page, "equipment_id", "Conveyor Belt CB-7")

    # Maintenance type radio: select Preventive (non-default).
    preventive_radio = page.locator(
        ".o_field_widget[name='maintenance_type'] input[type='radio'][data-value='preventive'], "
        ".o_field_widget[name='maintenance_type'] input[type='radio'][value='preventive'], "
        ".o_field_widget[name='maintenance_type'] .o_radio_item:has-text('Preventive') input, "
        ".o_field_widget[name='maintenance_type'] label:has-text('Preventive')"
    ).first
    preventive_radio.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Maintenance team
    set_many2one(page, "maintenance_team_id", "Bench Maintenance")

    # Schedule date — datetime field
    sd_widget = page.locator(".o_field_widget[name='schedule_date']").first
    sd_input = sd_widget.locator("input")
    if sd_input.count() == 0 or not sd_input.first.is_visible():
        sd_widget.click()
        page.wait_for_timeout(300)
        sd_input = sd_widget.locator("input")
    sd_input.first.click()
    sd_input.first.fill("")
    sd_input.first.type("05/15/2026 08:00:00")
    sd_input.first.press("Escape")
    page.wait_for_timeout(300)
    page.keyboard.press("Tab")
    page.wait_for_timeout(300)
    # Make sure no datepicker is left open.
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(300)
    _wait_no_loading(page)

    # Enable recurring toggle (only visible when type is preventive).
    rec_toggle = page.locator(
        ".o_field_widget[name='recurring_maintenance'] input[type='checkbox']"
    ).first
    if rec_toggle.count() > 0 and not rec_toggle.is_checked():
        rec_toggle.click()
        page.wait_for_timeout(300)
        _wait_no_loading(page)

    # Set repeat_interval to 30
    rep_input = page.locator(".o_field_widget[name='repeat_interval'] input").first
    if rep_input.count() > 0 and rep_input.is_visible():
        rep_input.click()
        rep_input.fill("")
        rep_input.fill("30")
        rep_input.press("Tab")
        page.wait_for_timeout(300)

    # Set repeat_unit to "days" if it is a select widget.
    unit_select = page.locator(".o_field_widget[name='repeat_unit'] select")
    if unit_select.count() > 0 and unit_select.first.is_visible():
        unit_select.first.select_option(label="days")
        page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
