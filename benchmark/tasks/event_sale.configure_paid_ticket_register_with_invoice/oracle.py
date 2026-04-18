"""Oracle for event_sale.configure_paid_ticket_register_with_invoice.

Multi-step cross-module workflow:
  events -> add ticket -> sales (new SO) -> configurator wizard ->
  confirm SO -> registration editor wizard -> create invoice wizard.

Final invoice must be left in draft.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_create,
    click_list_row,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


EVENT_NAME = "Spring Dev Summit 2026"
PARTNER_NAME = "Bench Summit Attendee Inc"
PRODUCT_NAME = "Dev Summit Pro Product"
TICKET_NAME = "Professional Pass"
ATTENDEE_NAME = "Berta Attendee"
ATTENDEE_EMAIL = "berta@benchsummit.test"


def _clear_filters(page):
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break


def _switch_to_list(page):
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)


def _click_add_a_line(page):
    add_link = page.locator(
        "a.o_field_x2many_list_row_add:visible, "
        "td.o_field_x2many_list_row_add a:visible"
    )
    add_link.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _modal_set_many2one_in_row(page, row_idx, field_name, search_text):
    modal = page.locator(".modal:visible").last
    rows = modal.locator(".o_data_row")
    cell = rows.nth(row_idx).locator(
        f"td[name='{field_name}'], .o_field_widget[name='{field_name}']"
    ).first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)
    dropdown = page.locator(".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item")
    item = dropdown.filter(has_text=search_text).first
    item.click()
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
    # STEP 1 — Add ticket to event
    # ============================================================
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    _clear_filters(page)
    _switch_to_list(page)
    page.wait_for_timeout(500)

    click_list_row(page, EVENT_NAME)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    click_tab(page, "Tickets")
    page.wait_for_timeout(500)

    _click_add_a_line(page)
    # New row in the event_ticket_ids one2many list.
    set_o2m_many2one(page, 0, "product_id", PRODUCT_NAME)
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "name", TICKET_NAME)
    set_o2m_field(page, 0, "price", "150")
    set_o2m_field(page, 0, "seats_max", "50")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ============================================================
    # STEP 2 — New SO in Sales
    # ============================================================
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    set_many2one(page, "partner_id", PARTNER_NAME)
    page.wait_for_timeout(500)

    # Click the Order Lines tab is usually the default tab; ensure we're there.
    try:
        click_tab(page, "Order Lines")
    except Exception:
        pass
    page.wait_for_timeout(300)

    _click_add_a_line(page)
    page.wait_for_timeout(300)

    # Set the product in the new line. SO lines use product_template_id as
    # the visible field. Setting the product triggers the event configurator
    # wizard.
    set_o2m_many2one(page, 0, "product_template_id", PRODUCT_NAME)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ============================================================
    # STEP 3 — Configurator wizard (event + ticket)
    # ============================================================
    if page.locator(".modal:visible").count() > 0:
        modal = page.locator(".modal:visible").last
        # Set event
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

        # Set ticket
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

        # Click Ok in configurator footer.
        ok_btn = page.locator(
            ".modal:visible .modal-footer button:has-text('Ok'), "
            ".modal:visible .modal-footer button:has-text('OK'), "
            ".modal:visible .modal-footer button.btn-primary"
        )
        ok_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Make sure quantity is 1 (default) — no edit needed.

    # Save the SO first (so Confirm is enabled).
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ============================================================
    # STEP 4 — Confirm SO
    # ============================================================
    confirm_btn = page.locator(
        ".o_statusbar_buttons button[name='action_confirm']:visible, "
        ".o_statusbar_buttons button:has-text('Confirm'):visible"
    )
    confirm_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ============================================================
    # STEP 5 — Registration editor wizard pops up
    # ============================================================
    if page.locator(".modal:visible").count() > 0:
        # The wizard has a one2many list with one row pre-filled with
        # event/ticket — we just need to set name + email.
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

    # ============================================================
    # STEP 6 — Create Invoice (draft only)
    # ============================================================
    # We may have been redirected; ensure we're on the SO. If the SO list
    # is showing, click the SO again. Easiest: navigate back to /odoo/sales
    # and find the SO.
    page.wait_for_timeout(500)

    # Click "Create Invoice" button on the SO (still in scope).
    create_inv_btn = page.locator(
        "button[name='action_invoice_create']:visible, "
        "button[name='_create_invoices']:visible, "
        ".o_statusbar_buttons button:has-text('Create Invoice'):visible, "
        "button:has-text('Create Invoice'):visible"
    )
    if create_inv_btn.count() == 0:
        # Retry by finding the SO via partner search.
        navigate(page, "/odoo/sales")
        _wait_no_loading(page)
        _clear_filters(page)
        click_list_row(page, PARTNER_NAME)
        page.wait_for_timeout(800)
        _wait_no_loading(page)
        create_inv_btn = page.locator(
            ".o_statusbar_buttons button:has-text('Create Invoice'):visible, "
            "button:has-text('Create Invoice'):visible"
        )
    create_inv_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Wizard is open: keep default "Regular invoice" radio.
    # Click "Create Draft Invoice" footer button.
    if page.locator(".modal:visible").count() > 0:
        draft_btn = page.locator(
            ".modal:visible .modal-footer button:has-text('Create Draft Invoice'), "
            ".modal:visible .modal-footer button:has-text('Create Draft'), "
            ".modal:visible .modal-footer button[name='create_invoices'], "
            ".modal:visible .modal-footer button.btn-primary"
        )
        draft_btn.first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)

    # Done — leave invoice in draft.


run_oracle(oracle)
