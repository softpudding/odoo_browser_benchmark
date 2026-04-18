"""Oracle for event_sale.add_seat_limited_ticket_register_until_full.

Workflow:
  1. Open the event 'Spring Q2 Workshop'.
  2. On the Tickets tab, add a 'VIP Seat' ticket with seats_max=5,
     price=200.
  3. Save the event.
  4. Navigate into the event's Attendees view (smart button) and
     register five attendees VIP-1..VIP-5 one at a time, each on the
     VIP Seat ticket.
  5. Attempt to register VIP-6 — Odoo must raise a ValidationError
     because the ticket is sold out. Discard the draft.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_list_row,
    click_stat_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    _wait_for_ready,
    _wait_no_loading,
)


EVENT_NAME = "Spring Q2 Workshop"
TICKET_NAME = "VIP Seat"
ATTENDEES = [f"VIP-{i}" for i in range(1, 6)]
FORBIDDEN = "VIP-6"


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


def _open_event(page):
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    _clear_filters(page)
    _switch_to_list(page)
    page.wait_for_timeout(500)
    click_list_row(page, EVENT_NAME)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _open_attendees(page):
    """Click the Attendees stat button on the event form."""
    try:
        click_stat_button(page, "Attendees")
    except Exception:
        stat = page.locator(
            "button.oe_stat_button:has-text('Attendees'):visible, "
            ".oe_stat_button:has-text('Attendees'):visible"
        )
        if stat.count() > 0:
            stat.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _new_registration(page, name, expect_block=False):
    """Click New, fill ticket+name, save. Returns True if save succeeded."""
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Set the event ticket many2one. Note: in Odoo 19 the field name
    # on event.registration is 'event_ticket_id'.
    set_many2one(page, "event_ticket_id", TICKET_NAME)
    page.wait_for_timeout(400)

    # Fill name.
    fill_field(page, "name", name)
    page.wait_for_timeout(300)

    # Save — but for VIP-6, the ValidationError raises a modal instead
    # of saving. Catch it and discard.
    save_btn = page.locator(
        ".o_form_button_save:visible, "
        "button.o_form_button_save:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    page.wait_for_timeout(1500)

    # Did an error dialog appear?
    err_modal = page.locator(
        ".modal:visible .modal-title:has-text('Validation Error'), "
        ".modal:visible .modal-title:has-text('Error'), "
        ".modal:visible .modal-body:has-text('not enough seats')"
    )
    if err_modal.count() > 0:
        # Close the dialog (Ok / Close button).
        ok_btn = page.locator(
            ".modal:visible .modal-footer button:has-text('Ok'), "
            ".modal:visible .modal-footer button:has-text('Close'), "
            ".modal:visible .modal-footer button.btn-primary, "
            ".modal:visible button.btn-close"
        )
        ok_btn.first.click()
        page.wait_for_timeout(500)

        # Discard the unsaved draft via breadcrumb back to event.
        discard_btn = page.locator(
            "button.o_form_button_cancel:visible, "
            ".o_control_panel button:has-text('Discard'):visible"
        )
        if discard_btn.count() > 0:
            discard_btn.first.click()
            page.wait_for_timeout(500)
        return False

    _wait_no_loading(page)
    return True


def oracle(page):
    # ============================================================
    # STEP 1 — Add VIP Seat ticket on the event
    # ============================================================
    login(page)
    _open_event(page)

    click_tab(page, "Tickets")
    page.wait_for_timeout(500)

    _click_add_a_line(page)
    set_o2m_field(page, 0, "name", TICKET_NAME)
    set_o2m_field(page, 0, "price", "200")
    set_o2m_field(page, 0, "seats_max", "5")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ============================================================
    # STEP 2 — Register VIP-1..VIP-5 one at a time.
    # After each save we navigate back to the event and re-open
    # Attendees, mimicking the prompt's loop.
    # ============================================================
    for name in ATTENDEES:
        # Re-open the event so the smart-button counter is fresh.
        _open_event(page)
        _open_attendees(page)
        ok = _new_registration(page, name, expect_block=False)
        if not ok:
            raise RuntimeError(
                f"Could not save registration {name} (unexpected block)"
            )

    # ============================================================
    # STEP 3 — Attempt VIP-6, expect block.
    # ============================================================
    _open_event(page)
    _open_attendees(page)
    blocked = _new_registration(page, FORBIDDEN, expect_block=True)
    if blocked:
        raise RuntimeError(
            "VIP-6 was saved unexpectedly — the seats_max constraint "
            "did not block the 6th attendee."
        )


run_oracle(oracle)
