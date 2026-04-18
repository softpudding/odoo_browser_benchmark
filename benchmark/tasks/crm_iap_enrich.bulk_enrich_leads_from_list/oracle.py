"""Oracle for crm_iap_enrich.bulk_enrich_leads_from_list.

Flow:
1. Navigate to Leads list action.
2. Switch to list view, clear default filters, search 'Bench Enrich'.
3. Tick exactly three rows (Target Alpha/Bravo/Charlie), skip
   'Already Delta' and 'Manual Echo'.
4. Open Actions dropdown in the control panel and click 'Enrich'.
5. Wait for the server action to finish; dismiss any notification toast.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


TARGET_NAMES = [
    "Bench Enrich Target Alpha",
    "Bench Enrich Target Bravo",
    "Bench Enrich Target Charlie",
]
SKIP_NAMES = [
    "Bench Enrich Already Delta",
    "Bench Enrich Manual Echo",
]
SEARCH_TEXT = "Bench Enrich"


def oracle(page):
    login(page)

    # Leads list action (filter to leads, list view default)
    navigate(page, "/odoo/action-crm.crm_lead_all_leads")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    ensure_list_view(page)
    page.wait_for_timeout(400)

    # Clear default filters (e.g. "Unassigned") so all 5 BENCH-ENRICH
    # leads are visible regardless of salesperson.
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

    # Tick checkboxes on the three target rows. Match by visible text
    # content and avoid the two distractors.
    rows = page.locator(".o_list_view .o_data_row")
    n = rows.count()
    assert n >= 5, f"Expected at least 5 rows after search, got {n}"

    selected = 0
    for i in range(n):
        row = rows.nth(i)
        text = row.inner_text()
        if any(skip in text for skip in SKIP_NAMES):
            continue
        if not any(tgt in text for tgt in TARGET_NAMES):
            continue
        cb = row.locator(".o_list_record_selector input[type='checkbox']")
        if cb.count() > 0:
            cb.first.check()
            selected += 1
    assert selected == 3, f"Expected to select 3 target rows, selected {selected}"
    page.wait_for_timeout(400)

    # Open Actions dropdown in the control panel.
    actions_btn = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_control_panel_actions button:has-text('Actions'):visible, "
        "button[aria-label='Actions']:visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(500)

    # Click the Enrich action menu entry.
    enrich_item = page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Enrich'):visible, "
        "a.dropdown-item:has-text('Enrich'):visible, "
        "span.dropdown-item:has-text('Enrich'):visible"
    ).first
    enrich_item.click()
    page.wait_for_timeout(2500)
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
