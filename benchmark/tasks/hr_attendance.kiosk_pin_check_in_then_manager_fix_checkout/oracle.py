"""Oracle for hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout."""

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


EMPLOYEE_NAME = "Bench Kiosk Worker"
PIN = "2468"
CHECK_OUT_LOCAL = "05/21/2026 01:00:00"


def _open_kiosk(page):
    kiosk_menu = page.locator(
        ".o_menu_sections a:has-text('Kiosk Mode'), "
        ".o_nav_entry:has-text('Kiosk Mode'), "
        ".o_navbar a:has-text('Kiosk Mode')"
    ).first
    kiosk_menu.wait_for(state="visible", timeout=10000)
    kiosk_menu.click()
    page.wait_for_url("**/hr_attendance/**", timeout=20000)
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)


def _kiosk_pin_attempt(page):
    card = page.locator(
        f".o_hr_kiosk_manual_selection .card:has(h6:has-text('{EMPLOYEE_NAME}'))"
    ).first
    card.wait_for(state="visible", timeout=10000)
    card.click()
    page.wait_for_timeout(700)

    for ch in PIN:
        page.locator(
            f".o_hr_attendance_pin_pad .o_hr_attendance_PINbox_button:has-text('{ch}')"
        ).first.click()
        page.wait_for_timeout(150)

    page.locator(
        ".o_hr_attendance_pin_pad .o_hr_attendance_PINbox_button:has-text('OK')"
    ).first.click()
    page.wait_for_timeout(1200)

    error_modal = page.locator(".modal:visible").last
    error_modal.wait_for(state="visible", timeout=10000)
    error_modal.locator("button:has-text('Close')").first.click()
    page.wait_for_timeout(600)


def _open_target_attendance(page):
    navigate(page, "/odoo/attendances")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    group_headers = page.locator("tr.o_group_header")
    group_headers.nth(0).click()
    page.wait_for_timeout(400)
    page.locator("tr.o_group_header").nth(1).click()
    page.wait_for_timeout(700)

    row = page.locator(".o_data_row").filter(has_text=EMPLOYEE_NAME).first
    row.wait_for(state="visible", timeout=10000)
    row.click()
    _wait_no_loading(page)
    page.wait_for_timeout(1000)


def oracle(page):
    login(page)
    navigate(page, "/odoo/attendances")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    _open_kiosk(page)
    _kiosk_pin_attempt(page)

    login(page)
    _open_target_attendance(page)

    check_out = page.locator(".o_field_widget[name='check_out'] input").first
    check_out.click()
    check_out.fill(CHECK_OUT_LOCAL)
    check_out.press("Tab")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
