"""Oracle for crm.set_lost_reason_reassign_salesperson."""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "Acme – Q3 renewal")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    # Wait for the form to fully render user_id field.
    page.locator(
        ".o_field_widget[name='user_id']"
    ).first.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(500)

    # Reassign salesperson.
    set_many2one(page, "user_id", "Mitchell Admin")
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Lost button.
    lost_btn = page.locator(
        ".o_form_statusbar button[name='action_set_lost']:visible, "
        ".o_form_statusbar button:has-text('Lost'):visible"
    ).first
    lost_btn.click()
    page.wait_for_timeout(800)

    # Modal: pick lost reason and confirm.
    reason_input = page.locator(
        ".modal .o_field_widget[name='lost_reason_id'] input:visible"
    ).first
    reason_input.click()
    reason_input.fill("Too expensive")
    page.wait_for_timeout(600)
    opt = page.locator(
        ".o-autocomplete--dropdown-menu li:has-text('Too expensive'):visible, "
        ".o-autocomplete li:has-text('Too expensive'):visible"
    ).first
    try:
        opt.click(timeout=3000)
    except Exception:
        pass

    confirm = page.locator(
        ".modal button.btn-primary:visible, "
        ".modal button:has-text('Mark as Lost'):visible, "
        ".modal button:has-text('Confirm'):visible"
    ).first
    confirm.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
