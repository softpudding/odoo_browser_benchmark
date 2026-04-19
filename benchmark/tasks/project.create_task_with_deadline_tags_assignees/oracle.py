"""Oracle for project.create_task_with_deadline_tags_assignees.

Open 'Bench Tag Proj', click New on the task kanban, then fill in a new
project.task with name 'Fix login bug', date_deadline 06/30/2026, tag_ids =
{urgent, backend}, user_ids = {Administrator, Bench Dev 2}, and save.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_for_ready,
    _wait_no_loading,
)


PROJECT_NAME = "Bench Tag Proj"
TASK_NAME = "Fix login bug"
DEADLINE_MMDDYYYY = "06/30/2026"
TAG_NAMES = ["urgent", "backend"]
ASSIGNEE_QUERIES = [
    # Pairs of (search_text, recognizable_substring_in_option).
    ("Mitchell Admin", "Mitchell Admin"),
    ("Bench Dev 2", "Bench Dev 2"),
]


def _open_project(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    click_kanban_card(page, PROJECT_NAME)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)


def _click_new_task(page):
    # The control-panel 'New' on a grouped kanban view opens an inline
    # quick-create input in the first column; to get the full form view we
    # prefer pressing 'New' in list view. Here we use the top-left 'New'
    # button which — on the task kanban — opens a quick-create row in
    # column #1 (Triage / Inbox / etc.). That row only has a Title input, so
    # we type the title, save the row, then OPEN the task to set the other
    # fields via the form.
    #
    # Simpler & deterministic: switch to list view, click 'New' → opens the
    # form directly.
    list_switch = page.locator(
        "button.o_switch_view.o_list:visible, "
        ".o_cp_switch_buttons button.o_list:visible"
    )
    if list_switch.count() > 0:
        list_switch.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(900)
    _wait_for_ready(page)


def _ensure_form_view_open(page):
    """If 'New' created an inline row instead of a form, fill title, save,
    then click the row to open the form."""
    form = page.locator(".o_form_view").first
    if form.count() > 0 and form.is_visible():
        return

    # Inline quick-create row — type title + Enter, then open the row.
    name_input = page.locator(
        ".o_selected_row .o_field_widget[name='name'] input, "
        ".o_selected_row .o_field_widget[name='name'] textarea, "
        ".o_selected_row input[name='display_name'], "
        ".o_list_view .o_selected_row input"
    ).first
    name_input.click()
    name_input.fill(TASK_NAME)
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    _wait_no_loading(page)
    # Open the newly-created row
    row = page.locator(
        f".o_data_row:has-text('{TASK_NAME}')"
    ).first
    row.click()
    page.wait_for_timeout(800)
    _wait_for_ready(page)


def _fill_tags(page):
    for tag in TAG_NAMES:
        tag_input = page.locator(
            ".o_field_widget[name='tag_ids'] input"
        ).first
        tag_input.click()
        tag_input.fill(tag)
        page.wait_for_timeout(700)
        # Pick the existing tag (avoid 'Create "xxx"' quick-create entries).
        items = page.locator(
            ".o-autocomplete--dropdown-menu:visible "
            ".o-autocomplete--dropdown-item, "
            ".dropdown-menu:visible .dropdown-item"
        )
        picked = False
        count = items.count()
        for i in range(count):
            txt = items.nth(i).inner_text().strip()
            low = txt.lower()
            if "create" in low or "start typing" in low or "search more" in low:
                continue
            if tag.lower() in low:
                items.nth(i).click()
                picked = True
                break
        if not picked and count > 0:
            items.first.click()
        page.wait_for_timeout(400)
        _wait_no_loading(page)


def _fill_assignees(page):
    for query, recognizable in ASSIGNEE_QUERIES:
        user_input = page.locator(
            ".o_field_widget[name='user_ids'] input"
        ).first
        user_input.click()
        user_input.fill(query)
        page.wait_for_timeout(700)
        items = page.locator(
            ".o-autocomplete--dropdown-menu:visible "
            ".o-autocomplete--dropdown-item, "
            ".dropdown-menu:visible .dropdown-item"
        )
        picked = False
        count = items.count()
        for i in range(count):
            txt = items.nth(i).inner_text().strip()
            low = txt.lower()
            if "create" in low or "start typing" in low or "search more" in low:
                continue
            if recognizable.lower() in low:
                items.nth(i).click()
                picked = True
                break
        if not picked and count > 0:
            items.first.click()
        page.wait_for_timeout(400)
        _wait_no_loading(page)


def oracle(page):
    _open_project(page)
    _click_new_task(page)
    _ensure_form_view_open(page)

    # 1. Task title (form textarea widget; safe to re-fill in case inline
    #    quick-create already put it).
    fill_text_field(page, "name", TASK_NAME)
    page.wait_for_timeout(300)

    # 2. Deadline (MM/DD/YYYY format). set_date handles Tab + Escape.
    set_date(page, "date_deadline", DEADLINE_MMDDYYYY)
    page.wait_for_timeout(300)

    # 3. Tags.
    _fill_tags(page)

    # 4. Assignees.
    _fill_assignees(page)

    # 5. Save.
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
