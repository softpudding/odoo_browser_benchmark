"""Oracle for project.kanban_drag_task_between_stages.

Open the 'Benchmark Drag Project', then drag the kanban card
'Benchmark Card Alpha' from the 'To Do' column into the 'In Progress'
column.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    drag_to_stage,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


PROJECT_NAME = "Benchmark Drag Project"
CARD_NAME = "Benchmark Card Alpha"
TARGET_STAGE = "In Progress"


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project kanban card -> lands on the project's task kanban
    click_kanban_card(page, PROJECT_NAME)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # If we somehow landed in the form view of the project, switch back to
    # kanban of the tasks. Normally the kanban-card click opens the task
    # board directly.
    if page.locator(".o_kanban_view").count() == 0:
        # Fallback: click the 'Tasks' / Kanban switcher if present.
        kanban_switch = page.locator(
            ".o_control_panel button.o_switch_view.o_kanban, "
            ".o_cp_switch_buttons button:has(i.oi-view-kanban), "
            ".o_cp_switch_buttons button:has(i.fa-th-large)"
        ).first
        if kanban_switch.count() > 0:
            kanban_switch.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)

    # Wait for the kanban columns to be rendered
    page.wait_for_selector(".o_kanban_group", timeout=15000)
    page.wait_for_selector(
        f".o_kanban_record:has-text('{CARD_NAME}')", timeout=15000
    )
    page.wait_for_timeout(500)

    drag_to_stage(page, CARD_NAME, TARGET_STAGE)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
