"""Oracle for project.close_task_change_state_to_done.

Open 'Bench Close Project', open task 'Review document', click the
form-header state widget pill (the `project_task_state_selection`
Odoo 19 widget rendered as `button.o_state_button`), pick 'Done' from the
dropdown, and save.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


PROJECT_NAME = "Bench Close Project"
TASK_NAME = "Review document"
TARGET_STATE_LABEL = "Done"


def _open_task(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_kanban_card(page, PROJECT_NAME)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_kanban_card(page, TASK_NAME)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)


def _click_state_pill_and_pick_done(page):
    """Click the state widget pill on the form header, then pick 'Done'.

    The Odoo 19 `project_task_state_selection` widget renders as a
    `.o_state_button.btn.rounded-pill` button inside
    `.o_field_widget[name='state']` on the form. Clicking it opens a
    Bootstrap-ish Dropdown whose menu is classed both
    `state_selection_field_menu` AND `project_task_state_selection_menu`,
    each option being a `.dropdown-item` whose visible label is the state
    name (In Progress / Changes Requested / Approved / Cancelled / Done).
    """
    # 1. Find the pill. Prefer scoped `.o_field_widget[name='state']`; fall
    #    back to `button.o_state_button` globally (the form-header pill is
    #    visually the only `.o_state_button` on the task form).
    pill = page.locator(
        ".o_field_widget[name='state'] button.o_state_button, "
        ".o_form_view button.o_state_button"
    ).first
    pill.scroll_into_view_if_needed()
    pill.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # 2. Pick 'Done' from the open dropdown menu. Match case-insensitively
    #    and skip any hidden / non-dropdown matches.
    menu_items = page.locator(
        ".state_selection_field_menu:visible .dropdown-item, "
        ".project_task_state_selection_menu:visible .dropdown-item, "
        ".o-dropdown--menu:visible .dropdown-item"
    )
    picked = False
    count = menu_items.count()
    for i in range(count):
        txt = menu_items.nth(i).inner_text().strip()
        if txt.lower() == TARGET_STATE_LABEL.lower():
            menu_items.nth(i).click()
            picked = True
            break
    if not picked:
        # Fallback: any dropdown item with 'Done' substring (but not
        # 'Duplicate', 'Delete', etc.). Exact match first, then fuzzy.
        for i in range(count):
            txt = menu_items.nth(i).inner_text().strip().lower()
            if "done" == txt.split()[0] if txt.split() else False:
                menu_items.nth(i).click()
                picked = True
                break
    if not picked:
        raise RuntimeError(
            f"Oracle: could not find a '{TARGET_STATE_LABEL}' dropdown "
            f"item among {count} menu items"
        )
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    _open_task(page)

    _click_state_pill_and_pick_done(page)
    page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
