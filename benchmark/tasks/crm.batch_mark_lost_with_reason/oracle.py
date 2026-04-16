"""Oracle for crm.batch_mark_lost_with_reason.

Select the two Blue Canyon Power opportunities in list view and use the Mark
Lost wizard with a specific reason and closing note.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


EXPECTED_NOTE = "Budget frozen until Q4 review."


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(1000)
    clear_search_filters(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    rows = page.locator(".o_list_view .o_data_row")
    selected = 0
    targets = {"Blue Canyon Power Renewal", "Blue Canyon Power Expansion"}
    for i in range(rows.count()):
        row = rows.nth(i)
        row_text = row.inner_text()
        if any(target in row_text for target in targets):
            row.locator(".o_list_record_selector input[type='checkbox']").first.click()
            page.wait_for_timeout(300)
            selected += 1
    if selected != 2:
        raise RuntimeError(f"Expected to select 2 rows, selected {selected}")

    actions_btn = page.locator(
        ".o_control_panel .o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_control_panel button:has-text('Action'):visible, "
        ".o_control_panel button:has-text('Actions'):visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(500)

    page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Mark Lost'), "
        ".dropdown-menu:visible .dropdown-item:has-text('Lost')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    modal.locator(
        ".o_field_widget[name='lost_reason_id'] :text('Price too high')"
    ).first.click()
    page.wait_for_timeout(500)

    note = modal.locator(
        ".o_field_widget[name='lost_feedback'] .odoo-editor-editable, "
        ".o_field_widget[name='lost_feedback'] [contenteditable='true']"
    ).first
    note.evaluate(
        """(el, text) => {
            el.innerHTML = '<p>' + text + '</p>';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""",
        EXPECTED_NOTE,
    )
    page.wait_for_timeout(500)

    modal.locator("button:has-text('Mark as Lost')").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
