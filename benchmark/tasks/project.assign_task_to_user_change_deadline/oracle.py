"""Oracle for project.assign_task_to_user_change_deadline.

Open 'Bench Assign Project', open task 'Bench Assign Task', add the
existing 'Bench Dev' user to the user_ids m2m, set date_deadline to
06/30/2026, and save.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_for_ready,
    _wait_no_loading,
)


PROJECT_NAME = "Bench Assign Project"
TASK_NAME = "Bench Assign Task"
DEV_NAME = "Bench Dev"
DEADLINE_MMDDYYYY = "06/30/2026"


def _open_task(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(600)

    click_kanban_card(page, PROJECT_NAME)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_kanban_card(page, TASK_NAME)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)


def _add_bench_dev_assignee(page):
    """Add the existing 'Bench Dev' user via the user_ids autocomplete.

    Skip any 'Create "Bench Dev" as new user...' / 'Start typing' /
    'Search more' rows — we must pick the EXISTING user.
    """
    user_input = page.locator(
        ".o_field_widget[name='user_ids'] input"
    ).first
    user_input.click()
    user_input.fill(DEV_NAME)
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
        if DEV_NAME.lower() in low:
            items.nth(i).click()
            picked = True
            break
    if not picked and count > 0:
        # Fallback: first visible item (oracle must not fail silently).
        items.first.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    _open_task(page)

    # 1. Assignee (user_ids m2m) — pick the EXISTING Bench Dev user.
    _add_bench_dev_assignee(page)
    page.wait_for_timeout(300)

    # 2. Deadline (MM/DD/YYYY) — set_date handles Tab + Escape so the
    #    picker popover doesn't eat the save click.
    set_date(page, "date_deadline", DEADLINE_MMDDYYYY)
    page.wait_for_timeout(300)

    # 3. Save.
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
