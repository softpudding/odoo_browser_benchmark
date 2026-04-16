"""Oracle for crm.batch_mark_lost_with_reason.

Create a new lost reason, then batch-select the two target opportunities and
use the Mark Lost wizard with that exact reason and note.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_create,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


EXPECTED_REASON = "Deferred to FY27 budget"
EXPECTED_NOTE = "Budget release moved to the FY27 planning cycle."


def _open_lost_reasons(page):
    config = page.locator("a, button").filter(has_text="Configuration")
    if config.count() > 0:
        config.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)
    pipeline = page.locator("a, button").filter(has_text="Pipeline")
    if pipeline.count() > 0:
        pipeline.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)
    lost_reasons = page.locator("a, button, span").filter(has_text="Lost Reasons")
    lost_reasons.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    _open_lost_reasons(page)
    click_create(page)
    page.wait_for_timeout(800)
    fill_field(page, "name", EXPECTED_REASON)
    page.wait_for_timeout(500)
    save_btn = page.locator("button.o_form_button_save:visible, button:has-text('Save'):visible")
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

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
        ".o_field_selection_badge[name='lost_reason_id'] .o_selection_badge, "
        ".o_field_widget[name='lost_reason_id'] .o_selection_badge"
    ).filter(has_text=EXPECTED_REASON).first.click()
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
