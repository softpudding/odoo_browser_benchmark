"""Oracle for crm.set_lost_reason_reassign_salesperson."""

from benchmark.oracle_helpers import (
    clear_search_filters,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def _set_salesperson(page, name):
    """Set the user_id field on the opportunity form to `name`. Robust to
    Odoo 19 autocomplete variants, avoids matching 'Create ...' items."""
    widget = page.locator(".o_field_widget[name='user_id']").first
    widget.wait_for(state="visible", timeout=15000)
    inp = widget.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(name)
    page.wait_for_timeout(1000)
    # Exclude the "Create ..." items by requiring the exact name as option text.
    all_options = page.locator(
        ".o-autocomplete--dropdown-menu li:visible, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    )
    picked = False
    seen = []
    for i in range(all_options.count()):
        opt = all_options.nth(i)
        try:
            txt = opt.inner_text().strip()
        except Exception:
            continue
        seen.append(txt)
        # Skip 'Create "X"' / 'Invite "X"' suggestion items; we want an
        # existing user, not a quick-create.
        low = txt.lower()
        if low.startswith("create") or low.startswith("invite"):
            continue
        if name in txt:
            opt.click()
            picked = True
            break
    if not picked:
        raise RuntimeError(
            f"No existing-user autocomplete option containing '{name}' found; "
            f"saw={seen}"
        )
    page.wait_for_timeout(500)
    _wait_no_loading(page)
    current = inp.input_value()
    if name not in current:
        raise RuntimeError(
            f"user_id field shows '{current}', expected to contain '{name}'"
        )


def _dismiss_invite_modal_if_any(page):
    """Odoo's 'Invite teammates' onboarding sometimes pops up after saving a CRM
    record. Dismiss it by clicking Discard so it doesn't intercept later clicks."""
    for _ in range(3):
        invite = page.locator(
            ".modal.show:visible, .modal.d-block:visible"
        ).filter(has_text="Invite teammates")
        if invite.count() == 0:
            return
        discard = invite.first.locator(
            "button:has-text('Discard'), button:has-text('Close'), button.btn-close"
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

    card = page.locator(
        ".o_kanban_view .o_kanban_record:has-text('Acme – Q3 renewal')"
    ).first
    card.wait_for(state="visible", timeout=15000)
    card.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.locator(
        ".o_form_view .o_field_widget[name='user_id']"
    ).first.wait_for(state="visible", timeout=20000)
    page.wait_for_timeout(800)

    _set_salesperson(page, "Mitchell Admin")
    page.wait_for_timeout(500)
    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    _dismiss_invite_modal_if_any(page)

    lost_btn = page.locator(
        ".o_form_statusbar button[name='action_set_lost']:visible, "
        ".o_form_statusbar button:has-text('Lost'):visible"
    ).first
    lost_btn.wait_for(state="visible", timeout=10000)
    lost_btn.click()
    page.wait_for_timeout(1500)

    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10000)

    badge = modal.locator(
        ".o_field_widget[name='lost_reason_id'] .o_selection_badge"
    ).filter(has_text="Too expensive").first
    if badge.count() == 0:
        inp = modal.locator(
            ".o_field_widget[name='lost_reason_id'] input:visible"
        ).first
        inp.click()
        inp.fill("Too expensive")
        page.wait_for_timeout(700)
        page.locator(
            ".o-autocomplete--dropdown-menu li:has-text('Too expensive'):visible, "
            ".o-autocomplete li:has-text('Too expensive'):visible, "
            ".dropdown-menu:visible .dropdown-item:has-text('Too expensive')"
        ).first.click()
    else:
        badge.click()
    page.wait_for_timeout(500)

    confirm = modal.locator(
        "button:has-text('Mark as Lost'), "
        "button:has-text('Confirm'), "
        "button.btn-primary"
    ).first
    confirm.click()
    page.wait_for_timeout(1800)
    _wait_no_loading(page)


run_oracle(oracle)
