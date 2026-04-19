"""Oracle for hr.generate_employee_card_set_badge_id.

Open 'Bench Worker Badge', switch to the 'Settings' notebook tab (name attr:
hr_settings, label "Settings") and fill the Badge ID (`barcode`) with
`EMPBENCH001`. Save. Best-effort click 'Print Badge' if the button becomes
visible.

Odoo 19 quirks:
- The field is `barcode` (no `badge_id`). Label on the view is "Badge ID".
- `_verify_barcode` only accepts `[A-Za-z0-9]{1,18}` — 'EMPBENCH001' passes.
- "Print Badge" is `invisible="not barcode"` so it only shows AFTER save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    click_tab,
    save_form,
)

EMPLOYEE_NAME = "Bench Worker Badge"
EXPECTED_BADGE = "EMPBENCH001"


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    click_list_row(page, EMPLOYEE_NAME)
    _wait_for_ready(page)

    # Switch to the "Settings" tab (name=hr_settings, string="Settings").
    click_tab(page, "Settings")
    page.wait_for_timeout(600)

    # Fill the Badge ID / barcode field under Attendance/Point of Sale group.
    barcode_input = page.locator(".o_field_widget[name='barcode'] input").first
    barcode_input.wait_for(state="visible", timeout=10000)
    barcode_input.click()
    barcode_input.fill("")
    barcode_input.fill(EXPECTED_BADGE)
    barcode_input.press("Tab")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Best-effort: click the "Print Badge" button if it appeared. Not required.
    try:
        print_btn = page.locator(
            ".o_field_widget[name='barcode'] ~ * button:has-text('Print Badge'),"
            " button:has-text('Print Badge')"
        ).first
        if print_btn.count() > 0 and print_btn.is_visible():
            print_btn.click(timeout=2000)
            page.wait_for_timeout(600)
    except Exception:
        pass


run_oracle(oracle)
