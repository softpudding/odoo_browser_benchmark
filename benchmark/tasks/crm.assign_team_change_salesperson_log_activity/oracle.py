"""Oracle for crm.assign_team_change_salesperson_log_activity.

Opens 'Bench Big Deal' opportunity, switches Sales Team to 'Channel', switches
Salesperson to 'Sara Sales', saves, then schedules a Call activity for
2026-06-10 with summary 'Discovery call'.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_tab,
    clear_search_filters,
    login,
    modal_fill_field,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    _wait_no_loading,
)


def _set_m2o_exact(page, field_name, value):
    """Set a many2one in the form to exactly `value`.

    Uses explicit autocomplete option matching, avoiding 'Create ...' quick
    add items.
    """
    widget = page.locator(f".o_field_widget[name='{field_name}']").first
    widget.wait_for(state="visible", timeout=15000)
    inp = widget.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    page.wait_for_timeout(1000)

    options = page.locator(
        ".o-autocomplete--dropdown-menu li:visible, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    )
    picked = False
    seen = []
    for i in range(options.count()):
        opt = options.nth(i)
        try:
            txt = opt.inner_text().strip()
        except Exception:
            continue
        seen.append(txt)
        low = txt.lower()
        if low.startswith("create") or low.startswith("invite"):
            continue
        if value in txt:
            opt.click()
            picked = True
            break
    if not picked:
        raise RuntimeError(
            f"No autocomplete option containing '{value}' found for "
            f"field '{field_name}'. Saw: {seen}"
        )
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _dismiss_invite_modal_if_any(page):
    """Dismiss the 'Invite teammates' onboarding modal if it appears."""
    for _ in range(3):
        invite = page.locator(
            ".modal.show:visible, .modal.d-block:visible"
        ).filter(has_text="Invite teammates")
        if invite.count() == 0:
            return
        discard = invite.first.locator(
            "button:has-text('Discard'), "
            "button:has-text('Close'), "
            "button.btn-close"
        ).first
        try:
            discard.click(timeout=3000)
        except Exception:
            page.keyboard.press("Escape")
        page.wait_for_timeout(600)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    clear_search_filters(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    click_kanban_card(page, "Bench Big Deal")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Wait for form to render
    page.locator(
        ".o_form_view .o_field_widget[name='user_id']"
    ).first.wait_for(state="visible", timeout=20000)
    page.wait_for_timeout(800)

    # 1. Change Salesperson to Sara Sales (visible at top of form)
    _set_m2o_exact(page, "user_id", "Sara Sales")

    # 2. Switch to "Contacts" notebook tab to access team_id
    click_tab(page, "Contacts")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # 3. Change Sales Team to Channel (in Ownership group of Contacts tab)
    _set_m2o_exact(page, "team_id", "Channel")

    # 4. Save the form
    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    _dismiss_invite_modal_if_any(page)

    # 4. Schedule a Call activity (date + summary)
    schedule_activity(
        page,
        activity_type="Call",
        summary="Discovery call",
        due_date="06/10/2026",
    )
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
