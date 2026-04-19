"""Oracle for event_sale.multi_ticket_checkout_two_attendees.

Playwright UI-based oracle. Walks the real multi-modal flow:

  1. Open Sales -> create a new quotation.
  2. Set the customer (Bench Summit Customer).
  3. Add order line #1 for the Early Bird ticket product.
     Setting a service_tracking=event product triggers the event
     configurator wizard -> pick event + Early Bird ticket, Ok.
  4. Add order line #2 for the VIP ticket product; configurator
     fires again -> pick event + VIP ticket, Ok.
  5. Save the quotation and click Confirm.
  6. On Confirm, Odoo opens the registration editor wizard with TWO
     rows (one per ticket). Fill each row's attendee name + email
     (Alice for Early Bird, Bob for VIP) and click
     Create/Update registrations.
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


EVENT_NAME = "Bench Summit 2026"
TICKET_EARLY = "Early Bird"
TICKET_VIP = "VIP"
PRODUCT_EARLY = "Bench Summit Early Bird Ticket"
PRODUCT_VIP = "Bench Summit VIP Ticket"
PARTNER_NAME = "Bench Summit Customer"

ATTENDEE_EARLY_NAME = "Alice Summit Attendee"
ATTENDEE_EARLY_EMAIL = "alice.summit@example.com"
ATTENDEE_VIP_NAME = "Bob Summit Attendee"
ATTENDEE_VIP_EMAIL = "bob.summit@example.com"


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
    """Fill a field in a specific row of a modal's data table."""
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


def _modal_get_row_ticket(page, row_idx):
    """Read the event_ticket_id cell text for row_idx (for matching Early/VIP)."""
    modal = page.locator(".modal:visible").last
    rows = modal.locator(".o_data_row")
    # Event ticket column might be labeled 'event_ticket_id'
    cell = rows.nth(row_idx).locator(
        "td[name='event_ticket_id'], .o_field_widget[name='event_ticket_id']"
    ).first
    if cell.count() == 0:
        return rows.nth(row_idx).inner_text()
    return cell.inner_text()


def _handle_configurator(page, ticket_name):
    """If the 'Configure an event' wizard is open, fill event + ticket."""
    if page.locator(".modal:visible").count() == 0:
        return
    _modal_set_many2one(page, "event_id", EVENT_NAME)
    _modal_set_many2one(page, "event_ticket_id", ticket_name)

    ok_btn = page.locator(
        ".modal:visible .modal-footer button:has-text('Ok'), "
        ".modal:visible .modal-footer button:has-text('OK'), "
        ".modal:visible .modal-footer button.btn-primary"
    )
    ok_btn.first.click()
    page.wait_for_timeout(1000)
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

    # --------------------------------------------------------------
    # Step 2: Order line #1 - Early Bird Ticket
    # --------------------------------------------------------------
    _click_add_a_line(page)
    page.wait_for_timeout(400)

    set_o2m_many2one(page, 0, "product_template_id", PRODUCT_EARLY)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    _handle_configurator(page, TICKET_EARLY)

    # --------------------------------------------------------------
    # Step 3: Order line #2 - VIP Ticket
    # --------------------------------------------------------------
    # Press Escape to close any residual dropdown/datepicker before
    # adding a fresh line.
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    _wait_no_loading(page)

    _click_add_a_line(page)
    page.wait_for_timeout(400)

    set_o2m_many2one(page, 1, "product_template_id", PRODUCT_VIP)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    _handle_configurator(page, TICKET_VIP)

    # --------------------------------------------------------------
    # Step 4: Save + Confirm
    # --------------------------------------------------------------
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    confirm_btn = page.locator(
        ".o_statusbar_buttons button[name='action_confirm']:visible, "
        ".o_statusbar_buttons button:has-text('Confirm'):visible"
    )
    confirm_btn.first.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # --------------------------------------------------------------
    # Step 5: Registration editor wizard - TWO rows, one per ticket.
    # Match rows to tickets by reading the event_ticket_id cell text.
    # --------------------------------------------------------------
    if page.locator(".modal:visible").count() > 0:
        # Read both rows' ticket labels to decide which is Early / VIP.
        row0_text = _modal_get_row_ticket(page, 0) or ""
        row1_text = _modal_get_row_ticket(page, 1) or ""

        # Default mapping assumes row 0 = Early Bird, row 1 = VIP.
        early_row, vip_row = 0, 1
        if TICKET_VIP in row0_text and TICKET_EARLY in row1_text:
            early_row, vip_row = 1, 0
        elif TICKET_EARLY in row0_text and TICKET_VIP in row1_text:
            early_row, vip_row = 0, 1

        # Fill Early Bird row (Alice).
        _modal_fill_row_field(page, early_row, "name", ATTENDEE_EARLY_NAME)
        _modal_fill_row_field(page, early_row, "email", ATTENDEE_EARLY_EMAIL)
        page.wait_for_timeout(400)

        # Fill VIP row (Bob).
        _modal_fill_row_field(page, vip_row, "name", ATTENDEE_VIP_NAME)
        _modal_fill_row_field(page, vip_row, "email", ATTENDEE_VIP_EMAIL)
        page.wait_for_timeout(400)

        action_btn = page.locator(
            ".modal:visible .modal-footer "
            "button[name='action_make_registration'], "
            ".modal:visible .modal-footer "
            "button:has-text('Create/Update'), "
            ".modal:visible .modal-footer button.btn-primary"
        )
        action_btn.first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
