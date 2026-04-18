"""Oracle for hr_holidays.request_half_day_morning."""

from benchmark.oracle_helpers import (
    fill_text_field,
    login,
    navigate,
    run_oracle,
    set_many2one,
    _wait_no_loading,
)


def _close_overlays(page):
    """Dismiss any open date picker / popover overlay without discarding form."""
    # Click on a non-interactive label area. Avoid Escape (discards form).
    try:
        lab = page.locator("label:has-text('Day Period')").first
        if lab.count() > 0:
            lab.click(force=True)
            page.wait_for_timeout(200)
            return
    except Exception:
        pass
    # Fallback: click somewhere on the form header.
    try:
        page.locator(".o_form_statusbar, .breadcrumb").first.click(
            position={"x": 5, "y": 5}
        )
    except Exception:
        pass
    page.wait_for_timeout(200)


def _set_select_menu(page, field_name, option_label):
    """Set an Odoo o_select_menu (Selection with widget override) field."""
    _close_overlays(page)
    # Wait until the field is rendered (half-day mode toggled on).
    try:
        page.wait_for_selector(
            f".o_field_widget[name='{field_name}'] input.o_select_menu_input",
            state="visible",
            timeout=10000,
        )
    except Exception:
        pass
    widget = page.locator(f".o_field_widget[name='{field_name}']").first
    widget.locator("input.o_select_menu_input").first.click(force=True)
    page.wait_for_timeout(500)
    page.locator(
        f"ul.o_select_menu_menu li:has-text('{option_label}'), "
        f".o-dropdown--menu .dropdown-item:has-text('{option_label}')"
    ).first.click()
    page.wait_for_timeout(300)


def _fill_daterange(page, field, value):
    """Fill a daterange sub-field identified by data-field attribute."""
    target = page.locator(f"[data-field='{field}']")
    target.first.click()
    page.wait_for_timeout(400)
    inp = page.locator(f"input[data-field='{field}']")
    inp.first.fill("")
    inp.first.type(value)
    # Use Tab instead of Escape — Escape on the form may discard unsaved
    # changes and close the form entirely.
    inp.first.press("Tab")
    page.wait_for_timeout(400)


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    new_btn = page.locator(
        "button.o_list_button_add:visible, button.o-kanban-button-new:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    if new_btn.count() > 0:
        new_btn.first.click()
    else:
        page.locator("button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Select leave type. Seed sets request_unit='half_day' so the form
    # auto-activates half-day mode (single-day range + AM/PM selectors).
    set_many2one(page, "holiday_status_id", "Paid Time Off")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Fill both ends of the daterange with the same date.
    _fill_daterange(page, "request_date_from", "06/15/2026")
    _fill_daterange(page, "request_date_to", "06/15/2026")

    # Set request_date_to_period to Morning. The field uses Odoo's
    # o_select_menu widget: click the toggler input, then click the option.
    _set_select_menu(page, "request_date_to_period", "Morning")

    fill_text_field(page, "name", "Doctor appointment")

    save_btn = page.locator(
        "button.o_form_button_save:visible, "
        ".o_control_panel button[data-tooltip='Save']:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        page.keyboard.press("Control+s")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Dismiss any warning modal.
    ok_btn = page.locator(
        ".modal button.btn-primary:visible, .modal button:has-text('Ok'):visible"
    )
    if ok_btn.count() > 0:
        try:
            ok_btn.first.click()
            page.wait_for_timeout(800)
        except Exception:
            pass
    _wait_no_loading(page)


run_oracle(oracle)
