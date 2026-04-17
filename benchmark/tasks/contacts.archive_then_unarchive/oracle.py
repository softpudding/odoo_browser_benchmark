"""Oracle for contacts.archive_then_unarchive.

Archive Wilder Ferris via the Action menu, toggle the Archived filter,
open Talon Vega, and unarchive him via the Action menu.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


ACTIVE_NAME = "Wilder Ferris (Bench-Archive-01)"
ARCHIVED_NAME = "Talon Vega (Bench-Archive-02)"


def _switch_to_list(page):
    list_switch = page.locator(
        ".o_switch_view.o_list:visible, "
        "button[data-tooltip='List']:visible, "
        ".o_cp_switch_buttons button:has-text('List')"
    ).first
    if list_switch.count() > 0:
        list_switch.click()
        _wait_no_loading(page)
        page.wait_for_timeout(500)


def _click_cog(page):
    # The Actions cog button lives in the control panel action-menus area.
    cog = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_cp_action_menus button:visible"
    ).first
    cog.wait_for(state="visible", timeout=10000)
    cog.click()
    page.wait_for_timeout(600)


def _click_menu_item(page, label: str):
    selector = (
        f".o-dropdown--menu:visible .dropdown-item:has-text('{label}'), "
        f".dropdown-menu:visible .dropdown-item:has-text('{label}')"
    )
    page.wait_for_selector(selector, state="visible", timeout=10000)
    page.locator(selector).first.click()
    page.wait_for_timeout(800)


def _confirm_modal_if_present(page, label: str):
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        btn = modal.last.locator(
            f"button:has-text('{label}'), "
            "button:has-text('OK'), "
            "button:has-text('Confirm')"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(800)


def _action_menu(page, label: str):
    _click_cog(page)
    _click_menu_item(page, label)
    _confirm_modal_if_present(page, label)
    _wait_no_loading(page)


def _toggle_archived_filter(page):
    toggler = page.locator(".o_searchview_dropdown_toggler:visible").first
    toggler.click()
    page.wait_for_timeout(500)
    archived = page.locator(
        ".o_search_bar_menu .o_filter_menu .o_menu_item:has-text('Archived'), "
        ".o-dropdown--menu:visible .o_menu_item:has-text('Archived')"
    ).first
    archived.click()
    page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    _switch_to_list(page)

    # --- Step 1: Archive Wilder Ferris ---
    click_list_row(page, ACTIVE_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _action_menu(page, "Archive")
    page.wait_for_timeout(800)

    # --- Step 2: Go back, toggle Archived filter, unarchive Talon Vega ---
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    _switch_to_list(page)
    _toggle_archived_filter(page)
    page.wait_for_timeout(800)

    # Archived filter is applied; click the name cell of Talon's row to
    # open the form (clicking an edge cell can miss the row target).
    page.wait_for_selector(
        f".o_list_view .o_data_row:has-text('{ARCHIVED_NAME}')",
        state="visible",
        timeout=10000,
    )
    row = page.locator(
        f".o_list_view .o_data_row:has-text('{ARCHIVED_NAME}')"
    ).first
    name_cell = row.locator(
        f"td.o_data_cell:has-text('{ARCHIVED_NAME}')"
    ).first
    if name_cell.count() > 0:
        name_cell.click()
    else:
        row.click()
    page.wait_for_selector(".o_form_view", state="visible", timeout=10000)
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _action_menu(page, "Unarchive")
    page.wait_for_timeout(800)


run_oracle(oracle)
