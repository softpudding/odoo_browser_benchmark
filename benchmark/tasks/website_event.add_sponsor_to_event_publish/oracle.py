"""Oracle for website_event.add_sponsor_to_event_publish.

Two phases:
  1. UI — open the event, click the Sponsors smart button, click New, set
     partner_id + sponsor_type_id on the sponsor form, save.
  2. JSON-RPC bypass — flip is_published on the event via
     event.event.website_publish_button(). The backend form's
     `website_redirect_button` widget only navigates to the frontend preview;
     the publish control is the Owl systray inside the iframe, which is
     fragile under Playwright. JSON-RPC bypass is sanctioned for oracles
     (see ODOO19_PATTERNS.md 'Oracle patterns'); browser-use still solves
     via UI.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_stat_button,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


EVENT_NAME = "Bench Conf 2026"
PARTNER_NAME = "Bench Sponsor Inc"
SPONSOR_LEVEL = "Silver"


def oracle(page):
    # =====================================================================
    # Phase 1 — UI: open event, Sponsors smart button, create sponsor.
    # =====================================================================
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)

    clear_search_filters(page)
    click_list_row(page, EVENT_NAME)
    _wait_for_ready(page)

    # Open the Sponsors smart button.
    click_stat_button(page, "Sponsors")
    _wait_for_ready(page)

    # Click New. The sponsor view defaults to kanban — the New button in the
    # control panel opens the full form in both kanban and list views.
    page.locator(
        "button.o_list_button_add:visible, "
        ".o-kanban-button-new:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first.click()
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Set the Partner many2one.
    set_many2one(page, "partner_id", PARTNER_NAME)

    # Set the Sponsorship Level many2one (field name: sponsor_type_id).
    set_many2one(page, "sponsor_type_id", SPONSOR_LEVEL)

    save_form(page)
    _wait_no_loading(page)

    # =====================================================================
    # Phase 2 — JSON-RPC publish bypass.
    # =====================================================================
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
                args: [[['name', '=', eventName]], ['id', 'is_published']],
                kwargs: { limit: 1 },
            });
            if (!rev.result || !rev.result.length) {
                return 'event not found';
            }
            const ev = rev.result[0];
            if (!ev.is_published) {
                const res = await callKw({
                    model: 'event.event',
                    method: 'website_publish_button',
                    args: [[ev.id]],
                    kwargs: {},
                });
                if (res.error) return 'publish error: ' + JSON.stringify(res.error);
            }
            // Belt-and-suspenders: ensure is_published is true.
            await callKw({
                model: 'event.event',
                method: 'write',
                args: [[ev.id], {is_published: true}],
                kwargs: {},
            });
            return 'ok';
        }""",
        EVENT_NAME,
    )
    if response != "ok":
        raise RuntimeError(f"Publish bypass failed: {response}")


run_oracle(oracle)
