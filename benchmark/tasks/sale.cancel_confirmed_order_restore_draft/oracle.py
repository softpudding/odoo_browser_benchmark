"""Oracle for sale.cancel_confirmed_order_restore_draft.

Open the confirmed sale.order with client_order_ref BENCH-CANCEL-RESTORE
for Bench Cancel Co, click Cancel in the statusbar, confirm the
"Are you sure?" dialog, then click Set to Quotation (visible only on
cancelled orders) to return state to 'draft'.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _open_order(page):
    """Resolve the SO id via JSON-RPC and navigate to its form view.

    Short-circuits the /odoo/sales list search: the Orders list applies a
    "My Orders" filter by default and `BENCH-CANCEL-RESTORE` is stored in
    `client_order_ref`, not always shown as a visible list column — a
    direct lookup keeps the oracle deterministic.
    """
    so_id = page.evaluate(
        """async () => {
            const res = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'sale.order',
                        method: 'search_read',
                        args: [[['client_order_ref', '=', 'BENCH-CANCEL-RESTORE']], ['id']],
                        kwargs: {},
                    },
                }),
            });
            const json = await res.json();
            if (json.error) throw new Error(json.error.data?.message || json.error.message);
            return json.result.length ? json.result[0].id : null;
        }"""
    )
    if not so_id:
        raise RuntimeError("Seeded BENCH-CANCEL-RESTORE sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(700)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_order(page)

    # --- Click Cancel in the statusbar ---
    # Target button[name='action_cancel'] explicitly: the form also has a
    # breadcrumb discard button that shows "Discard" but some themes label
    # it "Cancel". The statusbar button is the authoritative one.
    cancel_btn = page.locator(
        ".o_statusbar_buttons button[name='action_cancel']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Cancel')"
    ).first
    cancel_btn.wait_for(state="visible", timeout=8000)
    cancel_btn.click()
    page.wait_for_timeout(1200)

    # --- Confirm the native "Are you sure?" dialog ---
    # The button has confirm="Are you sure you want to cancel this order?..."
    # which triggers an Odoo confirm dialog (Dialog component). Click the
    # primary button.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        m = modal.last
        confirm_btn = m.locator(
            ".modal-footer button.btn-primary:visible, "
            ".modal-footer button:has-text('Ok'):visible, "
            ".modal-footer button:has-text('Confirm'):visible"
        ).first
        confirm_btn.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    # Wait for state transition to 'cancel' — statusbar re-renders to show
    # Set to Quotation.
    page.wait_for_selector(
        ".o_statusbar_buttons button[name='action_draft']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Set to Quotation')",
        timeout=10000,
    )
    page.wait_for_timeout(600)

    # --- Click Set to Quotation (action_draft) ---
    draft_btn = page.locator(
        ".o_statusbar_buttons button[name='action_draft']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Set to Quotation')"
    ).first
    draft_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
