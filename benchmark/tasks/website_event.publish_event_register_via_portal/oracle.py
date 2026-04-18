"""Oracle for website_event.publish_event_register_via_portal.

Two phases:
  1. Back-office publish — bypassed via JSON-RPC call_kw on
     event.event.website_publish_button() because the UI path goes
     through the website editor systray (Owl component inside an
     iframe preview) which is notoriously fragile under Playwright
     automation. The method is the same one the systray Published
     switch calls.
  2. Public portal — UI: navigate to /event, click the event card,
     click Register, bump the ticket counter, fill the attendee form
     (name/email/phone), and submit.

JSON-RPC bypass is sanctioned for oracles (see ODOO19_PATTERNS.md
'Oracle patterns' section). The browser-use agent must still solve
via UI.
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


EVENT_NAME = "Bench Public Day"
ATTENDEE_NAME = "Priya Patel"
ATTENDEE_EMAIL = "priya.patel@example.com"
ATTENDEE_PHONE = "+1 555 0142"


def oracle(page):
    # =====================================================================
    # Phase 1 — Publish the event via JSON-RPC bypass.
    # =====================================================================
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)

    response = page.evaluate(
        """async (eventName) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params: payload,
                    }),
                });
                return res.json();
            };
            const rev = await callKw({
                model: 'event.event',
                method: 'search_read',
                args: [[['name', '=', eventName]], ['id', 'website_published']],
                kwargs: { limit: 1 },
            });
            if (!rev.result || !rev.result.length) {
                return 'event not found';
            }
            const ev = rev.result[0];
            if (!ev.website_published) {
                const res = await callKw({
                    model: 'event.event',
                    method: 'website_publish_button',
                    args: [[ev.id]],
                    kwargs: {},
                });
                if (res.error) return 'publish error: ' + JSON.stringify(res.error);
            }
            return 'ok';
        }""",
        EVENT_NAME,
    )
    if response != "ok":
        raise RuntimeError(f"Publish bypass failed: {response}")

    # =====================================================================
    # Phase 2 — Portal: navigate to /event and submit the registration
    # =====================================================================
    portal_url = "/event"
    if DB:
        portal_url = f"/event?db={DB}"
    page.goto(full_url(portal_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click the event card/title.
    event_link = page.locator(f"a:has-text('{EVENT_NAME}')").first
    event_link.wait_for(timeout=15000)
    event_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click the Register button on the event page. This opens the
    # modal_ticket_registration Bootstrap modal via data-bs-target.
    # The event-page CTA has data-bs-toggle="modal".
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

    # Ticket modal opens with a single generic 'Registration' ticket.
    # Default counter value is 1; no need to bump. Just wait for the
    # submit (Register) button to become enabled.
    ticket_submit = page.locator(
        "#modal_ticket_registration button.a-submit"
    ).first
    ticket_submit.wait_for(state="visible", timeout=10000)
    # Wait for the button to become enabled (dynamic content removes
    # the disabled attribute once the counter is > 0).
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

    # The attendee-details modal is rendered via /event/.../registration/new
    # and inserted into document.body. Fields are named
    # `{registration_index}-{question_type}-{question_id}` so we match
    # by attribute substring.
    page.wait_for_selector(
        "#modal_attendees_registration input[name*='-name-']",
        timeout=15000,
    )

    # Fill the attendee form.
    page.locator(
        "#modal_attendees_registration input[name*='-name-']"
    ).first.fill(ATTENDEE_NAME)
    page.locator(
        "#modal_attendees_registration input[name*='-email-']"
    ).first.fill(ATTENDEE_EMAIL)
    phone_input = page.locator(
        "#modal_attendees_registration input[name*='-phone-']"
    )
    if phone_input.count() > 0:
        phone_input.first.fill(ATTENDEE_PHONE)
    page.wait_for_timeout(500)

    # Click 'Confirm Registration' to POST to /registration/confirm.
    confirm_btn = page.locator(
        "#modal_attendees_registration button[type='submit']:has-text('Confirm')"
    ).first
    confirm_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(4000)

    # Verify we landed on the 'Registration confirmed!' page.
    try:
        page.wait_for_selector(
            "h1:has-text('Registration confirmed'), "
            ".o_wereg_confirmed",
            timeout=10000,
        )
    except Exception:
        # Postconditions will catch genuine failures.
        pass


run_oracle(oracle)
