"""Oracle for website_sale_stock.show_stock_availability_add_to_cart.

Strategy: log in as admin (so the cart is attached to the admin partner),
open /shop, click through to the Bench Limited Stock product page, verify
the stock-availability badge is rendered, bump the quantity to 3, click
Add to cart. JSON-RPC fallback (/shop/cart/add) is used if the UI path
misbehaves.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


TARGET_NAME = "Bench Limited Stock"
EXPECTED_QTY = 3


def oracle(page):
    login(page)

    # 1) Open the shop and click through to the product detail page.
    navigate(page, "/shop")
    page.wait_for_timeout(500)

    # Use the grid link anchored by product name.
    product_link = page.locator(
        f'a.oe_product_image_link:has(h6:has-text("{TARGET_NAME}"))'
    ).first
    if product_link.count() == 0:
        # Fallback: ignore strict tag, just match anchor with text.
        product_link = page.locator(f'a:has-text("{TARGET_NAME}")').first
    product_link.scroll_into_view_if_needed()
    product_link.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(400)

    # 2) Sanity-check that the availability banner is present.
    #    #product_stock_availability wrapper has either out_of_stock_message
    #    or threshold_message inside.  With show_availability=True and
    #    free_qty=5 <= threshold=100, we expect the threshold_message badge.
    banner = page.locator("#product_stock_availability").first
    try:
        banner.wait_for(state="visible", timeout=5000)
    except Exception:
        # Not strictly required for the task to proceed, but log it.
        print("[oracle] stock availability banner not visible within 5s",
              flush=True)

    # 3) Bump the quantity input on the product page to EXPECTED_QTY.
    #    Owl renders the quantity as an <input> inside a field widget
    #    wrapper with class ``css_quantity`` on the product page.
    qty_input = page.locator(
        'input.quantity[name="add_qty"], input[name="add_qty"]'
    ).first
    qty_input.wait_for(state="visible", timeout=5000)
    qty_input.click()
    qty_input.fill(str(EXPECTED_QTY))
    qty_input.press("Tab")
    page.wait_for_timeout(300)

    # 4) Click Add to Cart.  The website_sale template uses
    #    ``#add_to_cart`` as the canonical selector (button type=submit).
    add_btn = page.locator("#add_to_cart").first
    if add_btn.count() == 0:
        add_btn = page.locator(
            "button:has-text('Add to cart'), a:has-text('Add to cart')"
        ).first
    add_btn.scroll_into_view_if_needed()
    add_btn.click()
    page.wait_for_timeout(1500)

    # 5) Dismiss any optional-product upsell modal that might appear.
    close_buttons = page.locator(
        ".modal:visible button[data-bs-dismiss='modal'], "
        ".modal:visible .btn-close, "
        ".modal:visible button:has-text('Proceed to Checkout'), "
        ".modal:visible button:has-text('Continue Shopping')"
    )
    if close_buttons.count() > 0:
        # Prefer Continue Shopping / close, avoid checkout which confirms.
        for i in range(close_buttons.count()):
            btn = close_buttons.nth(i)
            txt = (btn.text_content() or "").strip().lower()
            if "checkout" in txt or "payment" in txt:
                continue
            try:
                btn.click(timeout=2000)
                break
            except Exception:
                continue

    # 6) Navigate to /shop/cart to confirm the cart was materialized.
    navigate(page, "/shop/cart")
    page.wait_for_timeout(500)

    # Verify the cart contains the expected product + quantity via JSON-RPC.
    result = page.evaluate(
        """async (payload) => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const tmplRes = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', payload.name]], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            if (!tmplRes.length) {
                return { status: 'missing_template' };
            }
            const tmplId = tmplRes[0].id;
            const variantId = tmplRes[0].product_variant_id[0];

            const cartRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[
                    ['website_id', '!=', false],
                    ['state', '=', 'draft'],
                    ['order_line.product_template_id', '=', tmplId],
                ], ['id']],
                kwargs: { limit: 1, order: 'write_date desc' },
            });
            if (!cartRes.length) {
                return {
                    status: 'no_cart',
                    tmplId,
                    variantId,
                };
            }
            const orderId = cartRes[0].id;
            const lineRes = await callKw({
                model: 'sale.order.line',
                method: 'search_read',
                args: [[
                    ['order_id', '=', orderId],
                    ['product_template_id', '=', tmplId],
                ], ['product_uom_qty', 'id']],
                kwargs: {},
            });
            return {
                status: 'ok',
                orderId,
                lines: lineRes,
                tmplId,
                variantId,
            };
        }""",
        { "name": TARGET_NAME },
    )

    if result.get("status") != "ok" or not result.get("lines"):
        # Fallback: directly POST /shop/cart/add with qty=3.
        print("[oracle] UI add-to-cart did not persist; falling back "
              f"to /shop/cart/add (state={result!r})", flush=True)
        # Drop any existing stale admin cart first so qty doesn't stack.
        page.evaluate(
            """async () => {
                const callKw = async (params) => {
                    const res = await fetch('/web/dataset/call_kw', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        credentials: 'same-origin',
                        body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                    });
                    const json = await res.json();
                    if (json.error) {
                        throw new Error(json.error.data?.message || json.error.message);
                    }
                    return json.result;
                };
                const userRes = await callKw({
                    model: 'res.users',
                    method: 'search_read',
                    args: [[['login', '=', 'admin']], ['partner_id']],
                    kwargs: { limit: 1 },
                });
                const partnerId = userRes[0].partner_id[0];
                const staleIds = await callKw({
                    model: 'sale.order',
                    method: 'search',
                    args: [[
                        ['partner_id', '=', partnerId],
                        ['website_id', '!=', false],
                        ['state', '=', 'draft'],
                    ]],
                    kwargs: {},
                });
                if (staleIds.length) {
                    await callKw({
                        model: 'sale.order',
                        method: 'unlink',
                        args: [staleIds],
                        kwargs: {},
                    });
                }
            }"""
        )
        page.evaluate(
            """async (payload) => {
                const res = await fetch('/shop/cart/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params: {
                            product_template_id: payload.tmplId,
                            product_id: payload.variantId,
                            quantity: payload.qty,
                        },
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return 'ok';
            }""",
            { "tmplId": result.get("tmplId"), "variantId": result.get("variantId"),
              "qty": EXPECTED_QTY },
        )
        navigate(page, "/shop/cart")
        page.wait_for_timeout(600)


run_oracle(oracle)
