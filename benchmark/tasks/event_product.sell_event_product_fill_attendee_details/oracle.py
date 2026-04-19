"""Oracle for event_product.sell_event_product_fill_attendee_details.

Playwright UI-based oracle. Walks the real multi-modal flow:

  1. Open Sales → create a new quotation.
  2. Set the customer (Bench Attendee Customer).
  3. Add an order line for the Bench Standard Ticket product. Setting a
     service_tracking=event product triggers the event configurator
     wizard.
  4. In the configurator, pick Bench Festival 2026 / Standard, click Ok.
  5. Save the quotation and click Confirm.
  6. On Confirm, Odoo opens the registration editor wizard — fill the
     attendee name + email for the single pre-created row and click
     Create/Update registrations to close it.
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
    _wait_for_ready,
    _wait_no_loading,
)


EVENT_NAME = "Bench Festival 2026"
TICKET_NAME = "Standard"
PRODUCT_NAME = "Bench Standard Ticket"
PARTNER_NAME = "Bench Attendee Customer"
ATTENDEE_NAME = "Bench Attendee Name"
ATTENDEE_EMAIL = "bench.attendee@example.com"


def _click_add_a_line(page):
    add_link = page.locator(
        "a.o_field_x2many_list_row_add:visible, "
        "td.o_field_x2many_list_row_add a:visible"
    )
    add_link.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _modal_set_many2one(page, field_name, search_text):
    modal = page.locator(".modal:visible").last
    inp = modal.locator(
        f".o_field_widget[name='{field_name}'] input"
    ).first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)
    item = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text=search_text).first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _modal_fill_row_field(page, row_idx, field_name, value):
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
    login(page)

    # --------------------------------------------------------------
    # Step 1: new quotation in Sales
    # --------------------------------------------------------------
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(500)
    _wait_for_ready(page)

    # Customer
    set_many2one(page, "partner_id", PARTNER_NAME)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Make sure we're on the Order Lines tab (default) then add a line
    try:
        click_tab(page, "Order Lines")
    except Exception:
        pass
    page.wait_for_timeout(300)

    _click_add_a_line(page)
    page.wait_for_timeout(400)

    # Setting an event-tracked product on a SO line opens the
    # "Configure an event" wizard.
    set_o2m_many2one(
        page, 0, "product_template_id", PRODUCT_NAME
    )
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # --------------------------------------------------------------
    # Step 2: Configure an event wizard
    # --------------------------------------------------------------
    if page.locator(".modal:visible").count() > 0:
        _modal_set_many2one(page, "event_id", EVENT_NAME)
        _modal_set_many2one(page, "event_ticket_id", TICKET_NAME)

        ok_btn = page.locator(
            ".modal:visible .modal-footer button:has-text('Ok'), "
            ".modal:visible .modal-footer button:has-text('OK'), "
            ".modal:visible .modal-footer button.btn-primary"
        )
        ok_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Quantity stays at default 1. Save then confirm.
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --------------------------------------------------------------
    # Step 3: Confirm the SO
    # --------------------------------------------------------------
    confirm_btn = page.locator(
        ".o_statusbar_buttons button[name='action_confirm']:visible, "
        ".o_statusbar_buttons button:has-text('Confirm'):visible"
    )
    confirm_btn.first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # --------------------------------------------------------------
    # Step 4: Registration editor wizard — fill name + email
    # --------------------------------------------------------------
    if page.locator(".modal:visible").count() > 0:
        _modal_fill_row_field(page, 0, "name", ATTENDEE_NAME)
        _modal_fill_row_field(page, 0, "email", ATTENDEE_EMAIL)
        page.wait_for_timeout(500)

        action_btn = page.locator(
            ".modal:visible .modal-footer "
            "button[name='action_make_registration'], "
            ".modal:visible .modal-footer "
            "button:has-text('Create/Update'), "
            ".modal:visible .modal-footer button.btn-primary"
        )
        action_btn.first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
