"""Oracle for website_sale.add_optional_at_cart_remove_main_keep_optional.

Strategy:
  1. Login as admin.
  2. Use a JSON-RPC call to find Bench Camera and Bench Tripod product
     variants and the website id, then create a draft website sale.order
     for the admin partner with both lines (this is the post-state of
     "Add to Cart + accept upsell" without driving the website widget,
     which is fragile inside Playwright on /shop).
  3. Then call sale.order.line.unlink on the Bench Camera line to mimic
     the agent's per-line trash click on /shop/cart -- preserving the
     orphaned Bench Tripod line in the same cart.

This proves the task is solvable: the resulting state is exactly what
check.py expects.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo")

    response = page.evaluate(
        """async () => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params,
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const main = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Bench Camera']], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            const opt = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Bench Tripod']], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            const website = await callKw({
                model: 'website',
                method: 'search_read',
                args: [[], ['id', 'company_id']],
                kwargs: { limit: 1 },
            });
            const userRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            if (!main.length || !opt.length || !website.length || !userRes.length) {
                throw new Error('seed entities missing');
            }
            const partnerId = userRes[0].partner_id[0];
            const websiteId = website[0].id;
            const mainVariantId = main[0].product_variant_id[0];
            const optVariantId = opt[0].product_variant_id[0];

            // Drop any pre-existing draft website cart for admin to keep
            // entity counts deterministic.
            const oldOrders = await callKw({
                model: 'sale.order',
                method: 'search',
                args: [[
                    ['partner_id', '=', partnerId],
                    ['website_id', '!=', false],
                    ['state', '=', 'draft'],
                ]],
                kwargs: {},
            });
            if (oldOrders.length) {
                await callKw({
                    model: 'sale.order',
                    method: 'unlink',
                    args: [oldOrders],
                    kwargs: {},
                });
            }

            // Create the cart with both lines (the post-add-to-cart state).
            const orderId = await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerId,
                    website_id: websiteId,
                    client_order_ref: 'BENCH-OPT-ORPHAN-01',
                    order_line: [
                        [0, 0, {
                            product_id: mainVariantId,
                            product_uom_qty: 1,
                            price_unit: 320.0,
                            name: 'Bench Camera',
                            tax_ids: [[5, 0, 0]],
                        }],
                        [0, 0, {
                            product_id: optVariantId,
                            product_uom_qty: 1,
                            price_unit: 75.0,
                            name: 'Bench Tripod',
                            tax_ids: [[5, 0, 0]],
                        }],
                    ],
                }]],
                kwargs: {},
            });
            const newOrderId = Array.isArray(orderId) ? orderId[0] : orderId;

            // Now mimic the agent's "click trash on Bench Camera line"
            // by unlinking only that line, leaving Bench Tripod orphaned.
            const lines = await callKw({
                model: 'sale.order.line',
                method: 'search_read',
                args: [[
                    ['order_id', '=', newOrderId],
                    ['product_id', '=', mainVariantId],
                ], ['id']],
                kwargs: {},
            });
            if (!lines.length) {
                throw new Error('Bench Camera line not found on new cart');
            }
            await callKw({
                model: 'sale.order.line',
                method: 'unlink',
                args: [lines.map(l => l.id)],
                kwargs: {},
            });

            return 'ok';
        }"""
    )
    if response != "ok":
        raise RuntimeError(f"oracle JSON-RPC failed: {response!r}")


run_oracle(oracle)
