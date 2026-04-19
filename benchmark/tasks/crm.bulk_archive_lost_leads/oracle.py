"""Oracle for crm.bulk_archive_lost_leads.

Flow:
1. Navigate to the Leads list action.
2. Switch to list view, clear default filters, search "Bench Lost".
3. Tick checkboxes on the three Bench Lost rows (skip Bench Keep 4).
4. Open the cog Actions dropdown and click Archive.
5. Confirm any archive confirmation dialog if one appears.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


TARGET_NAMES = ["Bench Lost 1", "Bench Lost 2", "Bench Lost 3"]
SKIP_NAME = "Bench Keep 4"
SEARCH_TEXT = "Bench Lost"


def oracle(page):
    login(page)

    # Leads list action (filter to leads, list view default).
    navigate(page, "/odoo/action-crm.crm_lead_all_leads")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    ensure_list_view(page)
    page.wait_for_timeout(400)

    # Clear default filters so all four seeded Bench leads are visible
    # regardless of salesperson / to-process state.
    clear_search_filters(page)
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Narrow via search to make row lookup deterministic.
    searchbox = page.locator(".o_searchview_input").first
    searchbox.click()
    searchbox.fill(SEARCH_TEXT)
    page.wait_for_timeout(500)
    searchbox.press("Enter")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    rows = page.locator(".o_list_view .o_data_row")
    n = rows.count()
    assert n >= 3, f"Expected at least 3 rows after search, got {n}"

    selected = 0
    for i in range(n):
        row = rows.nth(i)
        text = row.inner_text()
        if SKIP_NAME in text:
            continue
        if not any(tgt in text for tgt in TARGET_NAMES):
            continue
        cb = row.locator(".o_list_record_selector input[type='checkbox']")
        if cb.count() > 0:
            cb.first.check()
            selected += 1
    assert selected == 3, f"Expected to select 3 target rows, selected {selected}"
    page.wait_for_timeout(400)

    # Open the control-panel Actions (cog) menu.
    actions_btn = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_control_panel_actions button:has-text('Actions'):visible, "
        "button[aria-label='Actions']:visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(500)

    # Click the Archive menu entry.
    archive_item = page.locator(
        ".o-dropdown--menu:visible .dropdown-item:has-text('Archive'), "
        ".dropdown-menu:visible .dropdown-item:has-text('Archive'), "
        "a.dropdown-item:has-text('Archive'):visible, "
        "span.dropdown-item:has-text('Archive'):visible"
    ).first
    archive_item.click()
    page.wait_for_timeout(900)
    _wait_no_loading(page)

    # Confirm any modal if one appears (Archive confirmation).
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        btn = modal.last.locator(
            "button:has-text('Archive'):visible, "
            "button:has-text('OK'):visible, "
            "button:has-text('Confirm'):visible, "
            "button:has-text('Ok'):visible"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)

    # Dismiss any lingering notification toast if present.
    toasts = page.locator(".o_notification:visible, .toast:visible")
    if toasts.count() > 0:
        close_btns = toasts.locator(
            "button.o_notification_close, button.btn-close"
        )
        for i in range(close_btns.count()):
            try:
                close_btns.nth(i).click(timeout=500)
            except Exception:
                pass
    page.wait_for_timeout(400)


run_oracle(oracle)
