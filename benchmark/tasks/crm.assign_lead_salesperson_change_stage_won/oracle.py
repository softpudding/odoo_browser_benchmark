"""Oracle for crm.assign_lead_salesperson_change_stage_won.

Opens 'Bench Big Deal', sets Salesperson to 'Bench Rep', saves, then clicks
the Won status-bar button.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    clear_search_filters,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


TARGET = "Bench Big Deal"
REP_NAME = "Bench Rep"


def _set_m2o_exact(page, field_name, value):
    """Set a many2one in the form to exactly `value`.

    Types into the input, waits for autocomplete, and clicks the matching
    option (skipping 'Create...' / 'Invite...' quick actions).
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


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    click_kanban_card(page, TARGET)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Wait for form
    page.locator(
        ".o_form_view .o_field_widget[name='user_id']"
    ).first.wait_for(state="visible", timeout=20000)
    page.wait_for_timeout(500)

    # 1. Set Salesperson to Bench Rep
    _set_m2o_exact(page, "user_id", REP_NAME)

    # 2. Save the form so the assignment is persisted before the Won action
    try:
        save_form(page)
    except Exception:
        pass
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # 3. Click the Won status-bar button
    won_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Won'), "
        "button[name='action_set_won_rainbowman']:visible, "
        "button[name='action_set_won']:visible"
    ).first
    won_btn.wait_for(state="visible", timeout=15000)
    won_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # rainbowman / any auto save settle
    page.wait_for_timeout(800)


run_oracle(oracle)
