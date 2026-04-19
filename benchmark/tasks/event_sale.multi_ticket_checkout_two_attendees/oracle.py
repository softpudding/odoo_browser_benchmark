"""Oracle for event_sale.multi_ticket_checkout_two_attendees.

Public-portal multi-ticket purchase flow:

  /event -> event card -> Register -> ticket counter modal
    (bump Standard & VIP by +1 each) -> Register submit
    -> attendees modal (fill Alice's row + Bob's row) -> Confirm
    -> /shop/checkout (skipped to /shop/payment if admin has address)
    -> pick Wire Transfer -> Pay now -> /shop/confirmation.

The flow is driven by Playwright; JSON-RPC is not used for the
registration itself so the browser-use agent still has a realistic
reference trace.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
    DB,
)


EVENT_NAME = "Bench Expo 2026"
TICKET_STANDARD = "Standard"
TICKET_VIP = "VIP"
ATTENDEE_STANDARD_NAME = "Alice Standard"
ATTENDEE_STANDARD_EMAIL = "alice@benchexpo.test"
ATTENDEE_VIP_NAME = "Bob VIP"
ATTENDEE_VIP_EMAIL = "bob@benchexpo.test"


def _portal_nav(page, path):
    url = path
    if DB:
        sep = "&" if "?" in path else "?"
        url = f"{path}{sep}db={DB}"
    page.goto(full_url(url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)


def _plus_ticket(page, ticket_name):
    """Click the '+' button for the given ticket row in
    #modal_ticket_registration. The row is selected by its
    `name` attribute which equals the ticket name."""
    row = page.locator(
        f"#modal_ticket_registration .o_wevent_ticket_selector[name='{ticket_name}']"
    ).first
    row.wait_for(state="visible", timeout=10000)
    plus = row.locator("button[data-increment-type='plus']").first
    plus.scroll_into_view_if_needed()
    plus.click()
    page.wait_for_timeout(400)


def _fill_attendee_section(page, section_idx, name, email):
    """Fill the N-th attendee section inside #modal_attendees_registration.

    section_idx is 0-based (counter 1 in the template is index 0)."""
    # All attendee sections are modal-body divs that contain inputs
    # `{counter}-{type}-{qid}`.  We match by the hidden input
    # `{counter}-event_ticket_id` whose counter is the section number.
    counter = section_idx + 1
    name_input = page.locator(
        f"#modal_attendees_registration input[name^='{counter}-name-']"
    ).first
    name_input.wait_for(state="visible", timeout=10000)
    name_input.fill(name)
    email_input = page.locator(
        f"#modal_attendees_registration input[name^='{counter}-email-']"
    ).first
    email_input.fill(email)


def _find_attendee_section_for_ticket(page, ticket_label):
    """Return the counter index (1-based) whose heading mentions ticket_label."""
    headings = page.locator("#modal_attendees_registration h5")
    for i in range(headings.count()):
        text = headings.nth(i).inner_text().strip()
        if ticket_label not in text or "#" not in text:
            continue
        prefix = text.split("-", 1)[0]
        digits = "".join(ch for ch in prefix if ch.isdigit())
        if digits:
            return int(digits)
    return None


def oracle(page):
    # ==================================================================
    # Phase 0 — log in so admin is the cart owner.
    # ==================================================================
    login(page)

    # ==================================================================
    # Phase 1 — navigate to /event and open the event page.
    # ==================================================================
    _portal_nav(page, "/event")

    # Click the event card/title.
    event_link = page.locator(f"a:has-text('{EVENT_NAME}')").first
    event_link.wait_for(state="visible", timeout=15000)
    event_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # ==================================================================
    # Phase 2 — Open Register ticket modal.
    # ==================================================================
    register_btn = page.locator(
        "button[data-bs-toggle='modal'][data-bs-target='#modal_ticket_registration']:visible"
    ).first
    if register_btn.count() == 0:
        register_btn = page.locator(
            "button:has-text('Register'):visible, a:has-text('Register'):visible"
        ).first
    register_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    register_btn.click()
    page.wait_for_timeout(1500)

    # Wait for the ticket modal to render its counters.
    page.wait_for_selector(
        "#modal_ticket_registration .o_wevent_ticket_selector",
        timeout=10000,
    )

    # Bump both counters by 1.
    _plus_ticket(page, TICKET_STANDARD)
    _plus_ticket(page, TICKET_VIP)

    # Submit the ticket modal.
    ticket_submit = page.locator(
        "#modal_ticket_registration button.a-submit"
    ).first
    page.wait_for_function(
        """() => {
            const b = document.querySelector(
                '#modal_ticket_registration button.a-submit'
            );
            return b && !b.disabled;
        }""",
        timeout=10000,
    )
    ticket_submit.click()
    page.wait_for_timeout(2500)

    # ==================================================================
    # Phase 3 — Attendees form.  Figure out which counter goes with which
    # ticket (depends on DB ordering of event_ticket_ids) and fill it.
    # ==================================================================
    page.wait_for_selector(
        "#modal_attendees_registration input[name*='-name-']",
        timeout=15000,
    )

    std_counter = _find_attendee_section_for_ticket(page, TICKET_STANDARD)
    vip_counter = _find_attendee_section_for_ticket(page, TICKET_VIP)

    if not std_counter:
        std_counter = 1
    if not vip_counter:
        vip_counter = 2 if std_counter == 1 else 1

    _fill_attendee_section(page, std_counter - 1, ATTENDEE_STANDARD_NAME, ATTENDEE_STANDARD_EMAIL)
    _fill_attendee_section(page, vip_counter - 1, ATTENDEE_VIP_NAME, ATTENDEE_VIP_EMAIL)

    # Submit the attendees form.  On paid events website_event_sale
    # swaps the button label from 'Confirm Registration' to
    # 'Go to Payment'; accept either by filtering on submit buttons
    # inside the attendees modal and clicking the primary one.
    confirm_btn = page.locator(
        "#modal_attendees_registration button[type='submit'].btn-primary"
    ).last
    confirm_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(4000)

    # ==================================================================
    # Phase 4 — Checkout / Payment.
    # The registration_confirm handler on a paid cart redirects to
    # /shop/checkout?try_skip_step=true; if admin has an address the
    # controller will forward to /shop/payment automatically. If we land
    # on /shop/checkout or /shop/address, click the primary Continue /
    # Confirm button.
    # ==================================================================
    current_url = page.url
    if "/shop/address" in current_url or "/shop/checkout" in current_url:
        # Try to locate the "Save address" / continue button.
        save_btn = page.locator(
            "button:has-text('Save address'):visible, "
            "button:has-text('Confirm'):visible, "
            "button:has-text('Continue'):visible, "
            "button[name='website_sale_main_button']:visible"
        ).first
        if save_btn.count() > 0:
            try:
                save_btn.click()
                page.wait_for_load_state("load")
                page.wait_for_timeout(2500)
            except Exception:
                pass

    # Navigate to /shop/payment explicitly if we didn't land there.
    if "/shop/payment" not in page.url and "/shop/confirmation" not in page.url:
        page.goto(full_url("/shop/payment"))
        page.wait_for_load_state("load")
        page.wait_for_timeout(2000)

    # ==================================================================
    # Phase 5 — Pick Wire Transfer + Pay now.
    # ==================================================================
    if "/shop/confirmation" not in page.url:
        # Click the Wire Transfer payment option radio / card.
        transfer_option = page.locator(
            "input[name='o_payment_radio'][data-payment-option-label='Wire Transfer']"
        ).first
        if transfer_option.count() == 0:
            transfer_option = page.locator(
                "label:has-text('Wire Transfer'):visible, "
                ".o_payment_option_card:has-text('Wire Transfer')"
            ).first
        try:
            transfer_option.scroll_into_view_if_needed()
            transfer_option.click()
            page.wait_for_timeout(800)
        except Exception:
            pass

        # Accept Terms if visible.
        tos = page.locator("input#website_sale_tc_checkbox:visible")
        if tos.count() > 0:
            try:
                tos.check()
            except Exception:
                pass

        pay_btn = page.locator(
            "button[name='o_payment_submit_button']:visible, "
            "button:has-text('Pay now'):visible, "
            "button:has-text('Pay Now'):visible"
        ).first
        pay_btn.scroll_into_view_if_needed()
        pay_btn.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(5000)

    # Phase 6 — wait for confirmation or retry.
    if "/shop/confirmation" not in page.url:
        # Some redirects land on the wire-transfer pending page; follow to
        # confirmation by calling `/shop/payment/validate` directly.
        page.goto(full_url("/shop/payment/validate"))
        page.wait_for_load_state("load")
        page.wait_for_timeout(3000)


run_oracle(oracle)
