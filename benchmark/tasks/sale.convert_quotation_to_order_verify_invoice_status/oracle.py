"""Oracle for sale.convert_quotation_to_order_verify_invoice_status.

Open the seeded draft quotation BENCH-CONFIRM for Bench Confirm Co and
click the Confirm button in the status bar to flip the state from
'draft' (Quotation) to 'sale' (Sales Order).
"""

from benchmark.oracle_helpers import (
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


SO_NAME = "BENCH-CONFIRM"


def _open_quotation(page):
    """Resolve the seeded SO id via JSON-RPC and navigate to the form."""
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
                        args: [[['name', '=', 'BENCH-CONFIRM']], ['id']],
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
        raise RuntimeError("Seeded BENCH-CONFIRM sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(600)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_quotation(page)

    # Single-click Confirm in the header status bar.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any confirmation dialog (rare for a simple draft SO with a
    # consu product & no credit limit, but safe to dismiss defensively).
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        try:
            modal.last.locator(
                "button:has-text('Ok'), button:has-text('Confirm'), button.btn-primary"
            ).first.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
        except Exception:
            pass


run_oracle(oracle)
