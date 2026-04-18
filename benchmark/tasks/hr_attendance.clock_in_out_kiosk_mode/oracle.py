"""Oracle for hr_attendance.clock_in_out_kiosk_mode.

Flow:
  1. Login, go to /odoo/attendances.
  2. Click the "Kiosk Mode" sidebar menu item. This triggers a logout and
     redirects to the public kiosk page /hr_attendance/<token>.
  3. In the kiosk manual-selection grid, click the 'Bench Worker' card.
  4. A PIN pad opens. Enter 1234, press OK. Greetings screen appears.
  5. Click OK on the greetings to return to the manual grid.
  6. Click 'Bench Worker' again.
  7. Enter 1234, press OK. Greetings confirms check-out.

Odoo 19 notes:
- attendance_kiosk_mode 'manual' = "Manual Selection" label in settings.
- Employee cards are rendered in .o_hr_kiosk_manual_selection with card h6
  displaying the name.
- Pin pad buttons use selector .o_hr_attendance_PINbox_button and the OK
  button has text 'OK' with class btn-primary.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)

EMPLOYEE_NAME = "Bench Worker"
PIN = "1234"


def _click_employee_card(page, name, timeout=15000):
    card = page.locator(
        f".o_hr_kiosk_manual_selection .card:has(h6:has-text('{name}'))"
    ).first
    card.wait_for(state="visible", timeout=timeout)
    card.click()
    page.wait_for_timeout(800)


def _enter_pin(page, pin):
    page.locator(".o_hr_attendance_pin_pad").first.wait_for(
        state="visible", timeout=10000
    )
    for ch in pin:
        btn = page.locator(
            f".o_hr_attendance_pin_pad .o_hr_attendance_PINbox_button:has-text('{ch}')"
        ).first
        btn.click()
        page.wait_for_timeout(150)
    ok_btn = page.locator(
        ".o_hr_attendance_pin_pad .o_hr_attendance_PINbox_button:has-text('OK')"
    ).first
    ok_btn.click()
    page.wait_for_timeout(1200)


def _wait_for_greeting(page, timeout=15000):
    page.locator(".o_hr_attendance_kiosk_card").first.wait_for(
        state="visible", timeout=timeout
    )


def _return_from_greeting(page):
    # Click the OK button on the greetings card to return immediately.
    btn = page.locator(".o_hr_kiosk_mode_bottom button:has-text('OK')").first
    btn.wait_for(state="visible", timeout=10000)
    btn.click()
    page.wait_for_timeout(800)


def _open_kiosk_from_attendances(page):
    # From /odoo/attendances, click "Kiosk Mode" in the sidebar menu.
    # It triggers a server action that redirects the browser, logging the
    # admin out and opening the public kiosk page.
    kiosk_menu = page.locator(
        ".o_menu_sections a:has-text('Kiosk Mode'), "
        ".o_nav_entry:has-text('Kiosk Mode'), "
        ".o_navbar a:has-text('Kiosk Mode')"
    ).first
    kiosk_menu.wait_for(state="visible", timeout=10000)
    kiosk_menu.click()
    # Wait for the public kiosk page to load.
    page.wait_for_url("**/hr_attendance/**", timeout=20000)
    page.wait_for_load_state("load")
    # Kiosk UI initializes via Owl, give it time.
    page.wait_for_timeout(1500)


def oracle(page):
    login(page)
    navigate(page, "/odoo/attendances")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Step 1: Open kiosk mode (admin gets logged out, redirect to /hr_attendance/<token>)
    _open_kiosk_from_attendances(page)

    # The manual-selection grid should be visible
    page.locator(".o_hr_kiosk_manual_selection").first.wait_for(
        state="visible", timeout=15000
    )

    # Step 2: First cycle — CHECK IN
    _click_employee_card(page, EMPLOYEE_NAME)
    _enter_pin(page, PIN)
    _wait_for_greeting(page)
    _return_from_greeting(page)

    # Back on manual grid
    page.locator(".o_hr_kiosk_manual_selection").first.wait_for(
        state="visible", timeout=15000
    )
    page.wait_for_timeout(800)

    # Step 3: Second cycle — CHECK OUT
    _click_employee_card(page, EMPLOYEE_NAME)
    _enter_pin(page, PIN)
    _wait_for_greeting(page)
    # No need to return — state capture happens directly from DB.


run_oracle(oracle)
