"""Shared Playwright helpers for Odoo oracle scripts.

Every oracle.py imports from this module for common UI operations:
login, navigation, form interaction, many2one fields, date pickers, etc.

Environment variables (set by eval.py --agent oracle):
    BENCHMARK_BASE_URL   – e.g. http://127.0.0.1:8069
    BENCHMARK_START_URL  – e.g. /odoo/sales
    BENCHMARK_DB         – database name
    BENCHMARK_LOGIN      – login (default "admin")
    BENCHMARK_PASSWORD   – password (default "admin")
    BENCHMARK_HEADED     – "1" for headed, "" for headless
"""

from __future__ import annotations

import os
import sys
import time
from contextlib import contextmanager
from typing import Any

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    sync_playwright,
)

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

BASE_URL = os.environ.get("BENCHMARK_BASE_URL", "http://127.0.0.1:8069")
START_URL = os.environ.get("BENCHMARK_START_URL", "/odoo")
DB = os.environ.get("BENCHMARK_DB", "")
LOGIN = os.environ.get("BENCHMARK_LOGIN", "admin")
PASSWORD = os.environ.get("BENCHMARK_PASSWORD", "admin")
HEADED = bool(os.environ.get("BENCHMARK_HEADED", "1"))


def full_url(path: str) -> str:
    return f"{BASE_URL.rstrip('/')}{path}"


# ---------------------------------------------------------------------------
# Browser lifecycle
# ---------------------------------------------------------------------------

@contextmanager
def odoo_browser(
    *,
    headed: bool | None = None,
    slow_mo: int = 0,
    timeout: int = 30_000,
):
    """Context manager that yields (page, browser_context).

    Handles login automatically.
    """
    if headed is None:
        headed = HEADED
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed, slow_mo=slow_mo)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        ctx.set_default_timeout(timeout)
        page = ctx.new_page()
        try:
            yield page
        finally:
            ctx.close()
            browser.close()


def login(page: Page, *, login: str = "", password: str = "", db: str = "") -> None:
    """Log in to Odoo via /web/login."""
    _login = login or LOGIN
    _password = password or PASSWORD
    _db = db or DB

    page.goto(full_url("/web/login"))
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector("input[name='login']", timeout=15000)

    # Select DB if the selector is visible
    db_select = page.locator("select[name='db']")
    if db_select.count() > 0 and db_select.is_visible() and _db:
        db_select.select_option(_db)

    page.fill("input[name='login']", _login)
    page.fill("input[name='password']", _password)
    page.click(".oe_login_form button[type='submit'], form[action='/web/login'] button[type='submit']:has-text('Log')")
    page.wait_for_load_state("domcontentloaded")
    # Wait for Odoo web client to be ready
    page.wait_for_selector(".o_action_manager, .o_home_menu", timeout=30000)


def navigate(page: Page, path: str) -> None:
    """Navigate to a path within Odoo."""
    page.goto(full_url(path))
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def _wait_for_ready(page: Page, timeout: int = 15000) -> None:
    """Wait for Odoo action manager to be present and loading to finish."""
    try:
        page.wait_for_selector(".o_action_manager", timeout=timeout)
    except Exception:
        pass
    _wait_no_loading(page)


def _wait_no_loading(page: Page, timeout: int = 10000) -> None:
    """Wait until there are no loading indicators."""
    # Wait for the blockUI / loading overlay to disappear
    try:
        page.wait_for_selector(
            ".o_loading_indicator, .o_blockUI, .modal-backdrop.o_blockUI",
            state="hidden", timeout=timeout,
        )
    except Exception:
        pass
    page.wait_for_timeout(300)


# ---------------------------------------------------------------------------
# List / Kanban view helpers
# ---------------------------------------------------------------------------

def clear_search_filters(page: Page) -> None:
    """Remove all active search facets (e.g. 'My Quotations')."""
    for _ in range(10):
        facets = page.locator(
            ".o_searchview .o_facet_remove, "
            ".o_searchview_facet .o_facet_remove"
        )
        if facets.count() == 0:
            break
        facets.first.click()
        page.wait_for_timeout(500)
    _wait_no_loading(page)


def ensure_list_view(page: Page) -> None:
    """Switch to list view if not already in list view."""
    list_btn = page.locator(
        "button.o_switch_view.o_list:visible, "
        ".o_cp_switch_buttons button.o_list:visible"
    )
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)


def search_for(page: Page, text: str) -> None:
    """Type text into the search bar and search.

    Tries each autocomplete suggestion until one yields results.
    """
    searchbox = page.locator(".o_searchview_input").first
    searchbox.click()
    searchbox.fill(text)
    page.wait_for_timeout(800)

    # Check autocomplete suggestions
    ac = page.locator(".o_searchview_autocomplete:visible")
    if ac.count() > 0:
        items = ac.first.locator(".o-dropdown-item, .o_menu_item")
        n = items.count()
        for i in range(n):
            item_text = items.nth(i).inner_text().strip()
            if not item_text or "Custom Filter" in item_text:
                continue
            items.nth(i).click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
            rows = page.locator(".o_list_view .o_data_row")
            if rows.count() > 0:
                return
            # No results — remove facet, re-type, try next option
            remove = page.locator(".o_searchview_facet .o_facet_remove")
            if remove.count() > 0:
                remove.last.click()
                page.wait_for_timeout(300)
            searchbox = page.locator(".o_searchview_input").first
            searchbox.click()
            searchbox.fill(text)
            page.wait_for_timeout(800)
            ac = page.locator(".o_searchview_autocomplete:visible")
            if ac.count() == 0:
                break
            items = ac.first.locator(".o-dropdown-item, .o_menu_item")
            n = items.count()

    # Fallback: just press Enter
    searchbox = page.locator(".o_searchview_input").first
    searchbox.click()
    searchbox.fill(text)
    page.wait_for_timeout(500)
    searchbox.press("Enter")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


def click_list_row(page: Page, text: str) -> None:
    """Click a row in a list view that contains the given text.

    Automatically clears search filters, switches to list view, and
    uses the searchbar if the text is not visible in list columns.
    """
    # Wait for the view to load and data to appear
    try:
        page.wait_for_selector(
            ".o_list_view .o_data_row, .o_kanban_view .o_kanban_record, .o_nocontent_help",
            timeout=10000,
        )
    except Exception:
        pass
    page.wait_for_timeout(500)

    # Try to find the row first
    row = page.locator(f".o_list_view .o_data_row:has-text('{text}')")
    if row.count() == 0:
        # Row not found — try clearing filters
        clear_search_filters(page)
        page.wait_for_timeout(1000)

    row = page.locator(f".o_list_view .o_data_row:has-text('{text}')")
    if row.count() == 0:
        # Still not found — try switching to list view
        ensure_list_view(page)
        page.wait_for_timeout(500)

    row = page.locator(f".o_list_view .o_data_row:has-text('{text}')")
    if row.count() == 0:
        # Still not found — search for the text via search bar.
        # After search, the list is filtered but the matching text
        # may not be in a visible column, so click the first result.
        search_for(page, text)
        page.wait_for_timeout(500)
        row = page.locator(".o_list_view .o_data_row")
        if row.count() > 0:
            row.first.click()
            page.wait_for_load_state("load")
            _wait_for_ready(page)
            return

    row = page.locator(f".o_list_view .o_data_row:has-text('{text}')").first
    row.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def click_kanban_card(page: Page, text: str) -> None:
    """Click a kanban card containing the given text."""
    card = page.locator(f".o_kanban_view .o_kanban_record:has-text('{text}')").first
    card.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


# ---------------------------------------------------------------------------
# Form helpers
# ---------------------------------------------------------------------------

def click_button(page: Page, text: str, *, exact: bool = False) -> None:
    """Click a visible button by its text content."""
    btn = page.locator(f"button:visible").filter(has_text=text)
    if exact:
        btn = page.locator("button:visible").get_by_text(text, exact=True)
    btn.first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def click_button_name(page: Page, name: str) -> None:
    """Click a button by its name attribute (Odoo action buttons)."""
    page.click(f"button[name='{name}']")
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def click_stat_button(page: Page, text: str) -> None:
    """Click a stat button on a form view."""
    btn = page.locator(f".oe_stat_button:has-text('{text}')").first
    btn.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def click_tab(page: Page, tab_name: str) -> None:
    """Click a notebook tab by its label text."""
    page.locator(f".o_notebook .nav-link:has-text('{tab_name}')").first.click()
    page.wait_for_timeout(500)


def fill_field(page: Page, field_name: str, value: str) -> None:
    """Fill an input field identified by its technical name."""
    selector = f".o_field_widget[name='{field_name}'] input"
    inp = page.locator(selector).first
    inp.click()
    inp.fill("")
    inp.fill(value)
    # Press Tab to trigger onchange
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def fill_text_field(page: Page, field_name: str, value: str) -> None:
    """Fill a textarea field."""
    selector = f".o_field_widget[name='{field_name}'] textarea"
    inp = page.locator(selector).first
    inp.click()
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)


def set_many2one(page: Page, field_name: str, search_text: str) -> None:
    """Set a many2one field by searching and selecting from dropdown."""
    selector = f".o_field_widget[name='{field_name}'] input"
    inp = page.locator(selector).first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)
    # Click the dropdown item
    dropdown = page.locator(".o_field_widget .dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item")
    item = dropdown.filter(has_text=search_text).first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def set_many2one_dialog(page: Page, field_name: str, search_text: str) -> None:
    """Set a many2one field, handling the case where a dialog opens for selection."""
    selector = f".o_field_widget[name='{field_name}'] input"
    inp = page.locator(selector).first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)

    # Try dropdown first
    dropdown = page.locator(".o_field_widget .dropdown-menu .dropdown-item")
    item = dropdown.filter(has_text=search_text)
    if item.count() > 0:
        item.first.click()
    else:
        # Click "Search More..." if available
        search_more = dropdown.filter(has_text="Search More")
        if search_more.count() > 0:
            search_more.first.click()
            page.wait_for_timeout(500)
            # Select from dialog list
            page.locator(f".modal .o_data_row:has-text('{search_text}')").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def set_selection(page: Page, field_name: str, value: str) -> None:
    """Set a selection field by its visible value text."""
    page.locator(f".o_field_widget[name='{field_name}'] select").select_option(label=value)
    page.wait_for_timeout(300)


def set_boolean(page: Page, field_name: str, checked: bool) -> None:
    """Set a boolean checkbox field."""
    cb = page.locator(f".o_field_widget[name='{field_name}'] input[type='checkbox']").first
    if cb.is_checked() != checked:
        cb.click()
    page.wait_for_timeout(300)


def set_date(page: Page, field_name: str, date_str: str) -> None:
    """Set a date field. date_str should be in MM/DD/YYYY format."""
    widget = page.locator(f".o_field_widget[name='{field_name}']").first
    inp = widget.locator("input")
    if inp.count() > 0 and inp.first.is_visible():
        inp.first.click()
        inp.first.fill("")
        inp.first.type(date_str)
        inp.first.press("Tab")
    else:
        # Odoo daterange button style: click the button to open picker
        btn = widget.locator("button, .o_input").first
        btn.click()
        page.wait_for_timeout(500)
        # A datepicker popover opens - type the date into its input
        dp_input = page.locator(".o_datetime_picker input:visible, .o_daterange_picker input:visible, .bootstrap-datetimepicker-widget input:visible")
        if dp_input.count() > 0:
            dp_input.first.fill("")
            dp_input.first.type(date_str)
            dp_input.first.press("Enter")
        else:
            # Try clicking the button and using keyboard
            btn.click(click_count=3)
            page.keyboard.type(date_str)
            page.keyboard.press("Tab")
    page.wait_for_timeout(500)
    # Close any datepicker that may be open
    try:
        page.press("body", "Escape")
    except Exception:
        pass
    _wait_no_loading(page)


def set_datetime(page: Page, field_name: str, datetime_str: str) -> None:
    """Set a datetime field. datetime_str in 'MM/DD/YYYY HH:MM:SS' format."""
    selector = f".o_field_widget[name='{field_name}'] input"
    inp = page.locator(selector).first
    inp.click()
    inp.fill("")
    inp.type(datetime_str)
    inp.press("Tab")
    page.wait_for_timeout(500)
    try:
        page.press("body", "Escape")
    except Exception:
        pass
    _wait_no_loading(page)


def add_many2many_tag(page: Page, field_name: str, tag_text: str) -> None:
    """Add a tag to a many2many_tags field."""
    selector = f".o_field_widget[name='{field_name}'] input"
    inp = page.locator(selector).first
    inp.click()
    inp.fill(tag_text)
    page.wait_for_timeout(800)
    dropdown = page.locator(".o_field_widget .dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item")
    item = dropdown.filter(has_text=tag_text).first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def remove_many2many_tag(page: Page, field_name: str, tag_text: str) -> None:
    """Remove a tag from a many2many_tags field."""
    tag = page.locator(f".o_field_widget[name='{field_name}'] .badge:has-text('{tag_text}') .o_delete").first
    tag.click()
    page.wait_for_timeout(300)


# ---------------------------------------------------------------------------
# Inline tree (one2many) editing
# ---------------------------------------------------------------------------

def click_add_a_line(page: Page) -> None:
    """Click 'Add a line' / 'Add a product' in a one2many field."""
    add_link = page.locator(
        "a.o_field_x2many_list_row_add:visible, "
        "td.o_field_x2many_list_row_add a:visible"
    )
    # Prefer "Add a product" if available, else first "Add a ..." link
    product_link = add_link.filter(has_text="product")
    if product_link.count() > 0:
        product_link.first.click()
    else:
        add_link.first.click()
    page.wait_for_timeout(500)


def set_o2m_field(page: Page, row_index: int, field_name: str, value: str) -> None:
    """Set a field value in a one2many row (0-indexed)."""
    row = page.locator(f".o_list_view .o_data_row").nth(row_index)
    cell = row.locator(f"td[name='{field_name}'], .o_field_widget[name='{field_name}']").first
    cell.click()
    page.wait_for_timeout(300)

    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def set_o2m_many2one(page: Page, row_index: int, field_name: str, search_text: str) -> None:
    """Set a many2one field within a one2many row."""
    row = page.locator(f".o_list_view .o_data_row").nth(row_index)
    cell = row.locator(f"td[name='{field_name}'], .o_field_widget[name='{field_name}']").first
    cell.click()
    page.wait_for_timeout(300)

    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)

    dropdown = page.locator(".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item")
    item = dropdown.filter(has_text=search_text).first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Save / discard / breadcrumbs
# ---------------------------------------------------------------------------

def save_form(page: Page) -> None:
    """Click the form save button (cloud icon or 'Save' text)."""
    # Odoo 17/18 uses a save button in the control panel
    save_btn = page.locator(".o_form_button_save:visible, button.o_form_button_save:visible")
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        # Try clicking the floppy-disk/cloud icon button
        save_btn = page.locator(".o_control_panel button:has-text('Save'):visible")
        if save_btn.count() > 0:
            save_btn.first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def discard_form(page: Page) -> None:
    """Click the discard button."""
    page.locator("button.o_form_button_cancel:visible, .o_control_panel button:has-text('Discard'):visible").first.click()
    page.wait_for_timeout(500)


def click_breadcrumb(page: Page, text: str) -> None:
    """Click a breadcrumb link by text."""
    page.locator(f".o_breadcrumb .breadcrumb-item a:has-text('{text}')").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def click_create(page: Page) -> None:
    """Click the 'New' button to create a new record."""
    page.locator("button.o_list_button_add:visible, .o_control_panel button:has-text('New'):visible").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Modal / Dialog helpers
# ---------------------------------------------------------------------------

def modal_click_button(page: Page, text: str) -> None:
    """Click a button inside a visible modal/dialog."""
    modal = page.locator(".modal:visible").last
    modal.locator(f"button:has-text('{text}')").first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def modal_fill_field(page: Page, field_name: str, value: str) -> None:
    """Fill a field inside the currently open modal."""
    modal = page.locator(".modal:visible").last
    inp = modal.locator(f".o_field_widget[name='{field_name}'] input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)


def modal_set_many2one(page: Page, field_name: str, search_text: str) -> None:
    """Set a many2one in the current modal."""
    modal = page.locator(".modal:visible").last
    inp = modal.locator(f".o_field_widget[name='{field_name}'] input").first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)
    dropdown = page.locator(".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item")
    item = dropdown.filter(has_text=search_text).first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def modal_set_selection(page: Page, field_name: str, value: str) -> None:
    """Set a selection field in the current modal."""
    modal = page.locator(".modal:visible").last
    modal.locator(f".o_field_widget[name='{field_name}'] select").select_option(label=value)
    page.wait_for_timeout(300)


# ---------------------------------------------------------------------------
# Status bar
# ---------------------------------------------------------------------------

def click_status_button(page: Page, status_text: str) -> None:
    """Click a status bar button (e.g., 'Confirm', 'Send by Email')."""
    btn = page.locator(f".o_statusbar_buttons button:visible:has-text('{status_text}')").first
    btn.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Chatter / Activity
# ---------------------------------------------------------------------------

def schedule_activity(
    page: Page,
    *,
    activity_type: str = "",
    summary: str = "",
    due_date: str = "",
    assigned_to: str = "",
    note: str = "",
) -> None:
    """Schedule an activity via the chatter."""
    # Click the activity button in chatter — try multiple selectors
    activity_btn = page.locator(
        ".o_ChatterTopbar button:has-text('Activities'), "
        ".o-mail-Chatter button:has-text('Activities'), "
        ".o_Chatter button:has-text('Activities'), "
        "button:has-text('Schedule Activity'), "
        "button.o_ChatterTopbar_activityBtn"
    ).first
    activity_btn.click()
    page.wait_for_timeout(1000)

    # Click 'Schedule an activity' link/button if a dropdown appeared
    schedule_link = page.locator(
        "button:has-text('Schedule an activity'), "
        "a:has-text('Schedule an activity'), "
        ".o_activity_btn:has-text('Schedule')"
    )
    if schedule_link.count() > 0:
        schedule_link.first.click()
        page.wait_for_timeout(500)

    modal = page.locator(".modal:visible").last

    if activity_type:
        modal_set_many2one(page, "activity_type_id", activity_type)

    if summary:
        modal_fill_field(page, "summary", summary)

    if due_date:
        inp = modal.locator(".o_field_widget[name='date_deadline'] input").first
        inp.click()
        inp.fill("")
        inp.type(due_date)
        inp.press("Tab")
        page.wait_for_timeout(500)

    if assigned_to:
        modal_set_many2one(page, "user_id", assigned_to)

    if note:
        # Note field is usually a textarea or HTML field
        note_field = modal.locator(".o_field_widget[name='note'] textarea, .o_field_widget[name='note'] .note-editable")
        if note_field.count() > 0:
            note_field.first.click()
            note_field.first.fill(note)

    # Click Schedule
    modal.locator("button:has-text('Schedule')").first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Kanban stage helpers
# ---------------------------------------------------------------------------

def drag_to_stage(page: Page, card_text: str, stage_name: str) -> None:
    """Drag a kanban card to a different stage column."""
    card = page.locator(f".o_kanban_record:has-text('{card_text}')").first
    target_col = page.locator(f".o_kanban_group:has(.o_column_title:has-text('{stage_name}'))").first
    card.drag_to(target_col)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Convenience runner
# ---------------------------------------------------------------------------

def run_oracle(fn) -> None:
    """Run an oracle function with standard setup.

    Usage in oracle.py:
        from benchmark.oracle_helpers import *
        def oracle(page):
            login(page)
            navigate(page, "/odoo/sales")
            ...
        run_oracle(oracle)
    """
    with odoo_browser() as page:
        try:
            fn(page)
            print("Oracle: PASS")
            sys.exit(0)
        except Exception as exc:
            print(f"Oracle: FAIL - {exc}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
