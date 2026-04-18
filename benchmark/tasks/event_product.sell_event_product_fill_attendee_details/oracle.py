"""Oracle for event_product.sell_event_product_fill_attendee_details.

Sales workflow:
  sales -> new SO -> pick customer -> add Bench Summit Ticket line ->
  event configurator wizard (event + ticket) -> save -> confirm ->
  registration editor wizard (fill Name + Email) -> submit.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


EVENT_NAME = "Bench Summit"
PARTNER_NAME = "Bench Attendee Co"
PRODUCT_NAME = "Bench Summit Ticket"
TICKET_NAME = "Standard Pass"
ATTENDEE_NAME = "Alice Attendee"
ATTENDEE_EMAIL = "alice@bench.test"


def _click_add_a_line(page):
    add_link = page.locator(
        "a.o_field_x2many_list_row_add:visible, "
        "td.o_field_x2many_list_row_add a:visible"
    )
    add_link.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _modal_fill_field_in_row(page, row_idx, field_name, value):
    modal = page.locator(".modal:visible").last
    rows = modal.locator(".o_data_row")
    cell = rows.nth(row_idx).locator(
        f"td[name='{field_name}'], .o_field_widget[name='{field_name}']"
    ).first
    cell.click()
    page.wait_for_timeout(200)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(300)
    _wait_no_loading(page)


def oracle(page):
    # ============================================================
    # STEP 1 — New quotation in Sales
    # ============================================================
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    set_many2one(page, "partner_id", PARTNER_NAME)
    page.wait_for_timeout(500)

    # Default tab is Order Lines; make sure.
    try:
        click_tab(page, "Order Lines")
    except Exception:
        pass
    page.wait_for_timeout(300)

    _click_add_a_line(page)
    page.wait_for_timeout(300)

    # Set the product on the new line; triggers event configurator wizard.
    set_o2m_many2one(page, 0, "product_template_id", PRODUCT_NAME)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ============================================================
    # STEP 2 — Event configurator wizard
    # ============================================================
    if page.locator(".modal:visible").count() > 0:
        modal = page.locator(".modal:visible").last
        # Event field.
        evt_inp = modal.locator(
            ".o_field_widget[name='event_id'] input"
        ).first
        evt_inp.click()
        evt_inp.fill("")
        evt_inp.fill(EVENT_NAME)
        page.wait_for_timeout(800)
        page.locator(".dropdown-menu .dropdown-item").filter(
            has_text=EVENT_NAME
        ).first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

        # Ticket field.
        tk_inp = modal.locator(
            ".o_field_widget[name='event_ticket_id'] input"
        ).first
        tk_inp.click()
        tk_inp.fill("")
        tk_inp.fill(TICKET_NAME)
        page.wait_for_timeout(800)
        page.locator(".dropdown-menu .dropdown-item").filter(
            has_text=TICKET_NAME
        ).first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

        # Ok footer button.
        ok_btn = page.locator(
            ".modal:visible .modal-footer button:has-text('Ok'), "
            ".modal:visible .modal-footer button:has-text('OK'), "
            ".modal:visible .modal-footer button.btn-primary"
        )
        ok_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Save SO first so Confirm becomes enabled.
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ============================================================
    # STEP 3 — Confirm the SO
    # ============================================================
    confirm_btn = page.locator(
        ".o_statusbar_buttons button[name='action_confirm']:visible, "
        ".o_statusbar_buttons button:has-text('Confirm'):visible"
    )
    confirm_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ============================================================
    # STEP 4 — Registration editor wizard
    # ============================================================
    if page.locator(".modal:visible").count() > 0:
        _modal_fill_field_in_row(page, 0, "name", ATTENDEE_NAME)
        _modal_fill_field_in_row(page, 0, "email", ATTENDEE_EMAIL)
        page.wait_for_timeout(500)

        action_btn = page.locator(
            ".modal:visible .modal-footer button[name='action_make_registration'], "
            ".modal:visible .modal-footer button:has-text('Create/Update'), "
            ".modal:visible .modal-footer button.btn-primary"
        )
        action_btn.first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
