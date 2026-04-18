"""Oracle for hr_holidays.request_half_day_morning.

Open Time Off, create a new request with Paid Time Off, enable Half Day,
set date 2026-06-15, pick Morning period for both start and end so the
half-day stays within the morning, fill description, save.
"""

from benchmark.oracle_helpers import (
    fill_text_field,
    login,
    navigate,
    run_oracle,
    set_many2one,
    _wait_no_loading,
)


def _fill_daterange(page, field, value):
    """Fill a daterange sub-field identified by data-field attribute."""
    target = page.locator(f"[data-field='{field}']")
    target.first.click()
    page.wait_for_timeout(400)
    inp = page.locator(f"input[data-field='{field}']")
    inp.first.fill("")
    inp.first.type(value)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)


def _set_period(page, field_name, value):
    """Set a selection field like request_date_*_period to 'am' or 'pm'.
    Covers the Odoo 19 variants: <select>, selection badge, or autocomplete."""
    label_text = "Morning" if value == "am" else "Afternoon"
    # Search in both o_field_widget[name] and div[name] + the entire DOM.
    candidates = [
        f".o_field_widget[name='{field_name}']",
        f"div[name='{field_name}']",
        f"[name='{field_name}']",
    ]
    for sel_prefix in candidates:
        scope = page.locator(sel_prefix).first
        if scope.count() == 0:
            continue
        # <select>
        sel = scope.locator("select")
        if sel.count() > 0:
            sel.first.select_option(value=value)
            return
        # Selection badge (radio-style)
        badge = scope.locator(".o_selection_badge").filter(has_text=label_text)
        if badge.count() > 0:
            badge.first.click()
            return
        # Autocomplete input
        inp = scope.locator("input")
        if inp.count() > 0:
            inp.first.click()
            inp.first.fill(label_text)
            page.wait_for_timeout(500)
            opt = page.locator(
                ".o-autocomplete--dropdown-menu li:visible, "
                ".dropdown-menu:visible .dropdown-item"
            ).filter(has_text=label_text).first
            if opt.count() > 0:
                opt.click()
                return
    raise RuntimeError(f"Could not set {field_name}={value!r}")


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    new_btn = page.locator(
        "button.o_list_button_add:visible, button.o-kanban-button-new:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible, "
        "button:has-text('New Time Off'):visible, "
        "button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    set_many2one(page, "holiday_status_id", "Paid Time Off")
    page.wait_for_timeout(500)

    # Half day toggle — seed makes Paid Time Off's request_unit='half_day' so
    # the form defaults request_unit_half=True, but explicitly enable it in
    # case any other default wins.
    try:
        cb = page.locator("input[name='request_unit_half']").first
        if cb.count() > 0 and not cb.is_checked():
            cb.check(force=True)
    except Exception:
        pass
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    _fill_daterange(page, "request_date_from", "06/15/2026")
    # request_date_to is marked invisible in the form but backs the daterange
    # widget end. Try to set it via the widget; if not reachable, fall back.
    try:
        _fill_daterange(page, "request_date_to", "06/15/2026")
    except Exception:
        pass
    page.wait_for_timeout(500)

    # Ensure both period selectors are Morning (am) so duration is 0.5.
    try:
        _set_period(page, "request_date_from_period", "am")
    except Exception:
        pass
    try:
        _set_period(page, "request_date_to_period", "am")
    except Exception:
        pass

    fill_text_field(page, "name", "Doctor appointment")

    save_btn = page.locator(
        "button.o_form_button_save:visible, "
        ".o_control_panel button[data-tooltip='Save']:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        page.keyboard.press("Control+s")
    page.wait_for_timeout(2500)
    _wait_no_loading(page)


run_oracle(oracle)
