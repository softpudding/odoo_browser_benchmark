"""Oracle for project.complete_project_stage_reach_done_percent.

Open 'Bench Progress Project', then drag each of the three task cards
(Task A, Task B, Task C) from the 'To Do' kanban column into the 'Done'
kanban column.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    drag_to_stage,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


PROJECT_NAME = "Bench Progress Project"
TASK_NAMES = ["Task A", "Task B", "Task C"]
TARGET_STAGE = "Done"


def _open_project_kanban(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_kanban_card(page, PROJECT_NAME)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Fallback: if we're not in kanban view, click the kanban switcher.
    if page.locator(".o_kanban_view").count() == 0:
        kanban_switch = page.locator(
            ".o_control_panel button.o_switch_view.o_kanban, "
            ".o_cp_switch_buttons button:has(i.oi-view-kanban), "
            ".o_cp_switch_buttons button:has(i.fa-th-large)"
        ).first
        if kanban_switch.count() > 0:
            kanban_switch.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)

    page.wait_for_selector(".o_kanban_group", timeout=15000)
    page.wait_for_timeout(500)


def oracle(page):
    _open_project_kanban(page)

    # Drag each card one-by-one. project.task has no "Change Stage" bulk
    # action (ODOO19_PATTERNS.md L984-996), so each card must be dragged
    # individually. The kanban auto-saves stage_id on drop via web_save.
    for tname in TASK_NAMES:
        # Ensure the card is still in the DOM before dragging.
        page.wait_for_selector(
            f".o_kanban_record:has-text('{tname}')",
            timeout=15000,
        )
        drag_to_stage(page, tname, TARGET_STAGE)
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Give the server a moment to persist the last web_save.
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
