"""Oracle for stock_sms.enable_delivery_sms_notification_validate.

Deterministically:
  1. Toggle res.company.stock_text_confirmation=True (Inventory settings).
  2. Open the S-BENCH-SMS-001 delivery picking.
  3. Click Validate. The stock_sms warning wizard opens on first-ever
     SMS-confirmed validate; click its 'Confirm' button (name=send_sms).
  4. The wizard re-invokes button_validate which then flows through
     _send_confirmation_email -> _message_sms_with_template ->
     _notify_thread_by_sms, which creates the sms.sms record.

The settings toggle is done via JSON-RPC write on res.company to sidestep
the Settings form's save/reload dance (which sometimes drops the toggle
state on the first page load because stock_text_confirmation is
company_dependent). The UI path for validate + wizard is exercised so the
stock_sms._pre_action_done_hook code path actually runs.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


SO_NAME = "S-BENCH-SMS-001"


def _enable_sms_confirmation(page):
    """Flip res.company.stock_text_confirmation via JSON-RPC."""
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };
            const sessionRes = await fetch('/web/session/get_session_info', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: {} }),
            });
            const sessionJson = await sessionRes.json();
            const companyId = sessionJson.result && sessionJson.result.user_companies
                ? sessionJson.result.user_companies.current_company
                : (sessionJson.result && sessionJson.result.company_id);
            if (!companyId) {
                throw new Error('no company id from session');
            }
            await callKw({
                model: 'res.company',
                method: 'write',
                args: [[companyId], {
                    stock_text_confirmation: true,
                    stock_confirmation_type: 'sms',
                }],
                kwargs: {},
            });
            return 'ok';
        }"""
    )
    if response != "ok":
        raise RuntimeError(f"settings toggle failed: {response!r}")


def _open_delivery_picking(page):
    # Inventory dashboard: click the Delivery Orders card
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    cards = page.locator(".o_kanban_record:visible")
    opened = False
    for i in range(cards.count()):
        card = cards.nth(i)
        text = card.inner_text()
        if "Delivery Orders" in text or "Delivery Order" in text:
            card.click()
            opened = True
            break
    if not opened:
        page.locator(
            ".o_kanban_record:has-text('Delivery'):visible"
        ).first.click()

    page.wait_for_load_state("load")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Clear any default filter then click the picking
    click_list_row(page, SO_NAME)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _validate_and_confirm_sms(page):
    # Click Validate header button
    validate_btn = page.locator(
        ".o_form_statusbar button[name='button_validate']:visible, "
        ".o_form_statusbar button:has-text('Validate'):visible"
    ).first
    validate_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # stock_sms warning wizard: click 'Confirm' (name=send_sms)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        confirm_btn = modal.last.locator(
            "button[name='send_sms']:visible, "
            "button.btn-primary:has-text('Confirm'):visible, "
            "button:has-text('Confirm'):visible"
        ).first
        confirm_btn.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


def oracle(page):
    login(page)
    _enable_sms_confirmation(page)
    _open_delivery_picking(page)
    _validate_and_confirm_sms(page)


run_oracle(oracle)
