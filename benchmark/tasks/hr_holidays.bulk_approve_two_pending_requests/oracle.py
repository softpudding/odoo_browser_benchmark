"""Oracle for hr_holidays.bulk_approve_two_pending_requests.

Navigate to the manager approval dashboard, switch to list view, clear
default filters so all pending leaves are visible, tick the checkboxes for
Eve Pending's 'Family vacation' and Frank Pending's 'Wedding attendance',
and click the bulk Approve button that appears in the list selection-actions
bar.

The bulk Approve is a custom MultiRecordViewButton on the hr.leave list view
(see addons/hr_holidays/static/src/views/list/holidays_list_controller.*).
When one or more rows are selected, an Approve button appears in the list
control-panel-selection-actions slot — clicking it calls action_approve on
all eligible selected leaves at once.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


TARGET_DESCRIPTIONS = {"Family vacation", "Wedding attendance"}


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Switch to list view (this view has js_class hr_holidays_payslip_list
    # with bulk Approve / Refuse buttons in the selection-actions slot).
    ensure_list_view(page)
    page.wait_for_timeout(500)

    # Remove default search facets so Alice/Eve/Frank + distractors are all visible.
    clear_search_filters(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # The list view hides the "Description" / name column by default (it's
    # `optional="hidden"`). Open the optional-columns dropdown and enable the
    # Description column so we can match rows by the leave description.
    opt_btn = page.locator(
        ".o_list_view .o_optional_columns_dropdown_toggle:visible"
    )
    if opt_btn.count() > 0:
        opt_btn.first.click()
        page.wait_for_timeout(400)
        items = page.locator(".dropdown-menu:visible .dropdown-item")
        for i in range(items.count()):
            try:
                lbl = items.nth(i).inner_text().strip()
            except Exception:
                continue
            if "Description" in lbl:
                cb = items.nth(i).locator("input[type='checkbox']")
                if cb.count() > 0 and not cb.first.is_checked():
                    items.nth(i).click()
                    page.wait_for_timeout(300)
                break
        page.press("body", "Escape")
        page.wait_for_timeout(300)
    _wait_no_loading(page)

    # Tick checkboxes on Eve's and Frank's rows. Match by employee name
    # (e.g. "Eve Pending") since that is always visible.
    rows = page.locator(".o_list_view .o_data_row")
    selected = 0
    targets_by_employee = {"Eve Pending", "Frank Pending"}
    picked_employees = set()
    for i in range(rows.count()):
        row = rows.nth(i)
        try:
            row_text = row.inner_text()
        except Exception:
            continue
        for emp in targets_by_employee:
            if emp in row_text and emp not in picked_employees:
                # Ensure we don't tick a non-confirm row (distractors).
                if ("To Approve" not in row_text
                        and "Approved" in row_text):
                    continue
                row.locator(
                    ".o_list_record_selector input[type='checkbox']"
                ).first.click()
                page.wait_for_timeout(250)
                selected += 1
                picked_employees.add(emp)
                break

    if selected != 2:
        raise RuntimeError(
            f"Oracle: expected to tick exactly 2 rows (Eve + Frank), ticked {selected}. "
            f"Picked={picked_employees}"
        )

    # Click the bulk Approve button in the selection-actions bar.
    # After a selection, the header buttons (Approve/Refuse) render in the
    # control-panel selection-actions slot alongside the record-count badge.
    approve_btn = page.locator(
        ".o_control_panel button[name='action_approve']:visible, "
        ".o_list_selection_box ~ * button[name='action_approve']:visible, "
        ".o_cp_action_menus button[name='action_approve']:visible"
    )
    if approve_btn.count() == 0:
        # Fall back to any visible Approve header button.
        approve_btn = page.locator(
            ".o_control_panel button:has-text('Approve'):visible"
        )
    approve_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
