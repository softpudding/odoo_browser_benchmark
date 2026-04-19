"""Oracle for sale.edit_existing_quotation_add_optional_product.

Open the seeded draft quotation BENCH-ADD-LINE for Bench Add Co and
append a second order line (Bench Extra Item, qty=4) via the default
**Add a product** footer link. Save (do NOT confirm).
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


SO_NAME = "BENCH-ADD-LINE"
PRODUCT_EXTRA = "Bench Extra Item"


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
                        args: [[['name', '=', 'BENCH-ADD-LINE']], ['id']],
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
        raise RuntimeError("Seeded BENCH-ADD-LINE sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(600)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_quotation(page)

    # Order Lines tab is the default on sale.order; click defensively.
    ol_tab = page.locator(".o_notebook .nav-link:has-text('Order Lines')")
    if ol_tab.count() > 0 and ol_tab.first.is_visible():
        try:
            ol_tab.first.click()
            page.wait_for_timeout(400)
        except Exception:
            pass
    _wait_no_loading(page)

    # Scroll the order-lines list into view.
    try:
        page.locator(
            ".o_form_view .o_list_renderer"
        ).first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    except Exception:
        pass

    # Click "Add a product" (the leftmost / default footer link).
    # `click_add_a_line` prefers the link whose text contains "product",
    # which is exactly what we want here.
    click_add_a_line(page)
    page.wait_for_timeout(700)
    _wait_no_loading(page)

    # The new row is the 2nd row (index 1). The sol_o2m widget exposes
    # the product cell as `product_template_id`, NOT `product_id`
    # (documented in create_quotation_with_customer_pricelist cookbook).
    set_o2m_many2one(page, 1, "product_template_id", PRODUCT_EXTRA)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Set qty to 4 on the same new row. Setting product first causes an
    # onchange that sets qty to 1 (default) and price_unit to list_price.
    set_o2m_field(page, 1, "product_uom_qty", "4")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Commit any open edit by pressing Escape before saving.
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
