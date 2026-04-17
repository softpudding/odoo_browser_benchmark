"""Oracle for calendar.invite_external_attendee_by_email.

Create a calendar event "Benchmark Strategy Sync" on 2026-05-14 10:00-11:00
and add `vendor.partner@example.com` as an attendee via the "Create ..."
quick-create option in the Attendees m2m_tags autocomplete (no existing
partner has this email — Odoo will create one on-the-fly).
"""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


EXTERNAL_EMAIL = "vendor.partner@example.com"


def _quickcreate_external_attendee(page, email):
    """Type an email into the Attendees m2m field and select the
    "Create ..." option in the dropdown. In Odoo 19's calendar form the
    attendees widget is configured with `no_quick_create: True`, so this
    opens a simple partner form dialog (name pre-filled with the typed
    value, `email` required). We then fill `email` with the actual
    address and save the dialog.
    """
    # Focus the attendees input
    selector = '.o_field_widget[name="partner_ids"] input'
    inp = page.locator(selector).first
    inp.click()
    inp.fill("")
    inp.type(email, delay=30)
    page.wait_for_timeout(1200)

    # Candidate selectors for the "Create ..." dropdown item.
    candidates = [
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item",
        ".dropdown-menu:visible .dropdown-item",
        ".ui-autocomplete:visible .ui-menu-item",
    ]
    clicked = False
    # First pass: prefer plain "Create ..." (no edit). In Odoo 19 calendar
    # the attendees widget has no_quick_create=True so only "Create and
    # edit..." is offered — handle both in a single pass.
    for sel in candidates:
        items = page.locator(sel)
        n = items.count()
        best_idx = -1
        fallback_idx = -1
        for i in range(n):
            try:
                txt = items.nth(i).inner_text().strip()
            except Exception:
                continue
            low = txt.lower()
            if low.startswith("create") and "edit" not in low:
                best_idx = i
                break
            if low.startswith("create") and fallback_idx < 0:
                fallback_idx = i
        if best_idx >= 0:
            items.nth(best_idx).click()
            clicked = True
            break
        if fallback_idx >= 0:
            items.nth(fallback_idx).click()
            clicked = True
            break

    if not clicked:
        raise RuntimeError(
            "Could not find a 'Create ...' quick-create option in the "
            "Attendees dropdown."
        )

    # A simple partner form dialog opens with name pre-filled with the
    # typed email. Fill email and save.
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(600)
    modal = page.locator(".modal:visible").last

    email_inp = modal.locator('.o_field_widget[name="email"] input').first
    email_inp.click()
    email_inp.fill("")
    email_inp.fill(email)
    email_inp.press("Tab")
    page.wait_for_timeout(300)

    # Save & Close the dialog
    save_btn = modal.locator(
        ".modal-footer button:has-text('Save & Close'), "
        ".modal-footer button:has-text('Save and Close'), "
        ".modal-footer button:has-text('Save'), "
        ".modal-footer button.btn-primary"
    )
    save_btn.first.click()

    # Wait for the modal to close
    try:
        page.wait_for_selector(".modal:visible", state="hidden", timeout=10000)
    except Exception:
        pass
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Open a new event form
    page.locator(
        '.o_control_panel button:has-text("New"):visible'
    ).first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Title
    fill_field(page, "name", "Benchmark Strategy Sync")
    page.wait_for_timeout(500)

    # Start = 2026-05-14 10:00 AM
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("05/14/2026 10:00:00 AM")
    start_input.press("Tab")
    page.wait_for_timeout(600)
    if page.locator(".o_datetime_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # Stop = 2026-05-14 11:00 AM via the daterange end picker
    stop_btn = page.locator(".o_daterange_end").first
    stop_btn.click()
    page.wait_for_timeout(800)
    time_inputs = page.locator(
        ".o_datetime_picker:visible .o_time_picker_input"
    )
    if time_inputs.count() >= 2:
        end_time_input = time_inputs.nth(1)
        end_time_input.click(click_count=3)
        end_time_input.fill("11:00am")
        end_time_input.press("Tab")
        page.wait_for_timeout(400)
    if page.locator(".o_datetime_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # Attendee via external-email quick-create
    _quickcreate_external_attendee(page, EXTERNAL_EMAIL)

    # Save via breadcrumb navigation
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)


run_oracle(oracle)
