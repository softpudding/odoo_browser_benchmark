"""Oracle for sale.apply_discount_percent_on_sale_order_line.

Open the seeded draft quotation BENCH-DISC for Bench Disc Co and set the
Disc.% field on the FIRST order line (Bench Product A) to 10.0. Save;
do NOT confirm.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


SO_NAME = "BENCH-DISC"
PRODUCT_A = "Bench Product A"


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
                        args: [[['name', '=', 'BENCH-DISC']], ['id']],
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
        raise RuntimeError("Seeded BENCH-DISC sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(600)


def _row_index_for_product(page, product_name):
    """Return the 0-based row index of the data row whose product cell
    text matches `product_name`. Falls back to 0 if not found.
    """
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    count = rows.count()
    for i in range(count):
        try:
            text = rows.nth(i).inner_text(timeout=2000)
        except Exception:
            continue
        if product_name in text:
            return i
    return 0


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_quotation(page)

    # Order Lines is the default-open tab on sale.order; click defensively.
    ol_tab = page.locator(".o_notebook .nav-link:has-text('Order Lines')")
    if ol_tab.count() > 0 and ol_tab.first.is_visible():
        try:
            ol_tab.first.click()
            page.wait_for_timeout(400)
        except Exception:
            pass
    _wait_no_loading(page)

    # Scroll the order lines list into view.
    try:
        page.locator(
            ".o_form_view .o_list_renderer"
        ).first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    except Exception:
        pass

    # Find the Bench Product A row (should be row 0 by seed order, but
    # don't assume).
    row_idx = _row_index_for_product(page, PRODUCT_A)

    # set_o2m_field handles the inline-edit click → fill → Tab commit
    # pattern. The Disc.% column's technical field name is `discount`.
    set_o2m_field(page, row_idx, "discount", "10.0")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Commit any open edit by pressing Escape before saving.
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
