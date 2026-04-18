"""Oracle for website_sale.apply_product_filter_clear_facets.

Strategy (URL-driven, since the dual-handle price slider is fragile in
Playwright):

  1. Login as admin (so the cart is attached to the admin partner).
  2. Navigate /shop -> click Gadgets category (URL becomes
     /shop/category/gadgets-<id>).
  3. Navigate the same URL with ?max_price=100 appended (shows only
     Gadget Mini + Gadget Plus).
  4. Navigate /shop?max_price=100 to drop the category segment while
     keeping the price filter (shows Gadget Mini, Gadget Plus and
     Widget Tiny - 3 products).
  5. Clean up any stale admin cart, then call /shop/cart/add with the
     Bench Widget Tiny variant id and quantity 1 - the same JSON-RPC
     endpoint the website ``Add to Cart`` button hits.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


TARGET_NAME = "Bench Widget Tiny"
GADGETS_CATEGORY = "Gadgets"


def oracle(page):
    login(page)

    # Step 1: /shop
    navigate(page, "/shop")
    page.wait_for_timeout(500)

    # Step 2: resolve category id and navigate to its filtered URL.
    gadgets_id = page.evaluate(
        """async (name) => {
            const res = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0', method: 'call', params: {
                        model: 'product.public.category',
                        method: 'search_read',
                        args: [[['name', '=', name]], ['id']],
                        kwargs: { limit: 1 },
                    },
                }),
            });
            const json = await res.json();
            if (json.error) {
                throw new Error(json.error.data?.message || json.error.message);
            }
            return json.result[0]?.id;
        }""",
        GADGETS_CATEGORY,
    )
    if not gadgets_id:
        raise RuntimeError(f"Category {GADGETS_CATEGORY!r} not found")

    navigate(page, f"/shop/category/{gadgets_id}")
    page.wait_for_timeout(500)

    # Step 3: add the max_price query param while keeping category.
    navigate(page, f"/shop/category/{gadgets_id}?max_price=100")
    page.wait_for_timeout(500)

    # Step 4: drop the category path segment but keep ?max_price=100.
    navigate(page, "/shop?max_price=100")
    page.wait_for_timeout(500)

    # Step 5: drop stale admin carts, then hit /shop/cart/add for Bench
    # Widget Tiny.
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

            const tmplRes = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', payload.name]], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            if (!tmplRes.length) {
                throw new Error('Target product not found: ' + payload.name);
            }
            const tmplId = tmplRes[0].id;
            const variantId = tmplRes[0].product_variant_id[0];

            const addRes = await fetch('/shop/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0', method: 'call', params: {
                        product_template_id: tmplId,
                        product_id: variantId,
                        quantity: 1,
                    },
                }),
            });
            const addJson = await addRes.json();
            if (addJson.error) {
                throw new Error(addJson.error.data?.message || addJson.error.message);
            }
            return 'ok';
        }""",
        { "name": TARGET_NAME },
    )
    if result != "ok":
        raise RuntimeError(f"Add-to-cart failed: {result!r}")

    # Navigate to /shop/cart so the cart is materialized/refreshed.
    navigate(page, "/shop/cart")
    page.wait_for_timeout(500)


run_oracle(oracle)
