"""Oracle for project.set_task_priority_urgent_assign_tag.

Open 'Bench Prio Project', open task 'Fix critical bug', click the
priority star (toggle priority '0' -> '1'), add the existing 'Bug' tag,
and save.
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


PROJECT_NAME = "Bench Prio Project"
TASK_NAME = "Fix critical bug"
TAG_NAME = "Bug"


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


def _click_priority_star(page):
    """Click the first priority star to toggle priority '0' -> '1'.

    Odoo 19 renders the priority widget as `.o_field_widget[name='priority']`
    containing one or more `.o_priority_star` anchor/button nodes. Clicking
    a star sets priority to that star's 1-indexed value (star #1 -> '1').
    """
    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star")
    if stars.count() > 0:
        stars.first.click()
        page.wait_for_timeout(400)
        _wait_no_loading(page)
        return

    # Fallback: force-set the priority via the hidden input.
    page.evaluate(
        """
        () => {
            const w = document.querySelector(".o_field_widget[name='priority']");
            if (!w) { return; }
            const input = w.querySelector("input");
            if (!input) { return; }
            input.value = '1';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """
    )
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _add_bug_tag(page):
    """Add the existing 'Bug' tag via the tag_ids many2many autocomplete.

    Skip any "Create 'Bug'" / "Start typing" / "Search more" rows.
    """
    tag_input = page.locator(
        ".o_field_widget[name='tag_ids'] input"
    ).first
    tag_input.click()
    tag_input.fill(TAG_NAME)
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
        if TAG_NAME.lower() in low:
            items.nth(i).click()
            picked = True
            break
    if not picked and count > 0:
        items.first.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    _open_task(page)

    _click_priority_star(page)
    page.wait_for_timeout(200)

    _add_bug_tag(page)
    page.wait_for_timeout(200)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
