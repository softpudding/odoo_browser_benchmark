"""Oracle for project.create_kanban_stage_reorder_drag.

Open the 'Bench Project A' kanban (grouped by stage), use the 'Add column'
quick-create to add a new stage 'Backlog Review', then drag the column
header leftward so 'Backlog Review' ends up between 'Triage' and
'In Progress' (position #2).
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


PROJECT_NAME = "Bench Project A"
NEW_STAGE = "Backlog Review"
TARGET_BEFORE = "In Progress"   # new stage must end up immediately left of this


def _open_project_kanban(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, PROJECT_NAME)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Make sure we're on the task kanban view. The default view for a
    # project card is the grouped-by-stage kanban of its tasks.
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


def _create_new_stage(page, stage_name: str) -> None:
    """Click the folded '+ / Add column' quick-create, type name, confirm."""
    # The quick-create lives at the right edge. When folded it shows the
    # chevron button with aria-label='Add column' (the container has the
    # CLASS `o_quick_create_folded` on the `.o_column_quick_create` div
    # itself; when unfolded the class becomes `o_quick_create_unfolded`).
    quick = page.locator(".o_column_quick_create").first
    quick.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    is_folded = quick.evaluate(
        "(el) => el.classList.contains('o_quick_create_folded')"
    )
    if is_folded:
        # Click the chevron button to unfold the stage-name input.
        unfold_btn = quick.locator(
            "button.o_quick_create_button, "
            "button:has(i.fa-angle-double-right)"
        ).first
        unfold_btn.click()
        page.wait_for_timeout(600)

    # Type name into the quick-create input and confirm.
    quick_input = quick.locator("input[type='text']").first
    quick_input.wait_for(state="visible", timeout=5000)
    quick_input.click()
    quick_input.fill(stage_name)
    page.wait_for_timeout(300)

    add_btn = quick.locator("button.o_kanban_add").first
    if add_btn.count() > 0:
        add_btn.click()
    else:
        quick_input.press("Enter")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Wait for the new column to appear on the board.
    page.wait_for_selector(
        f".o_kanban_group .o_column_title:has-text('{stage_name}')",
        timeout=10000,
    )
    page.wait_for_timeout(500)


def _drag_column_before(page, moved_name: str, anchor_name: str) -> None:
    """Drag column named `moved_name` so its drop position is immediately
    to the LEFT of the column named `anchor_name`.

    The kanban column drag handle is the `.o_column_title` inside
    the `.o_kanban_header` of a `.o_group_draggable` `.o_kanban_group`.
    """
    moved_col = page.locator(
        f".o_kanban_group:has(.o_column_title:has-text('{moved_name}'))"
    ).first
    anchor_col = page.locator(
        f".o_kanban_group:has(.o_column_title:has-text('{anchor_name}'))"
    ).first

    moved_col.wait_for(state="visible", timeout=10000)
    anchor_col.wait_for(state="visible", timeout=10000)
    moved_col.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    moved_handle = moved_col.locator(".o_column_title").first
    anchor_handle = anchor_col.locator(".o_column_title").first

    start = moved_handle.bounding_box()
    end = anchor_handle.bounding_box()
    if not start or not end:
        raise RuntimeError(
            "Could not get bounding boxes for kanban column drag-reorder."
        )

    start_x = start["x"] + start["width"] / 2
    start_y = start["y"] + start["height"] / 2
    # Aim for just to the LEFT of the anchor column title so the drop
    # inserts BEFORE it.
    end_x = end["x"] + 4
    end_y = end["y"] + end["height"] / 2

    page.mouse.move(start_x, start_y)
    page.wait_for_timeout(120)
    page.mouse.down()
    page.wait_for_timeout(160)
    # Tiny nudge to fire dragstart.
    page.mouse.move(start_x - 6, start_y + 4, steps=3)
    page.wait_for_timeout(80)

    steps = 28
    for i in range(1, steps + 1):
        x = start_x + (end_x - start_x) * (i / steps)
        y = start_y + (end_y - start_y) * (i / steps)
        page.mouse.move(x, y, steps=2)
        page.wait_for_timeout(20)

    # Hover the left edge of the anchor column briefly to trigger insertion
    # before it, then release.
    page.mouse.move(end_x, end_y, steps=5)
    page.wait_for_timeout(250)
    page.mouse.up()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def oracle(page):
    _open_project_kanban(page)
    _create_new_stage(page, NEW_STAGE)
    _drag_column_before(page, NEW_STAGE, TARGET_BEFORE)

    # Give the server a moment to persist web_resequence.
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
