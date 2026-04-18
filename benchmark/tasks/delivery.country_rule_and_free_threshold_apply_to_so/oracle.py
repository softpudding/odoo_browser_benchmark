"""Oracle for delivery.country_rule_and_free_threshold_apply_to_so."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/delivery-methods")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
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

            const usRes = await callKw({
                model: 'res.country',
                method: 'search_read',
                args: [[['code', '=', 'US']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!usRes.length) {
                throw new Error('missing US country');
            }
            const usId = usRes[0].id;

            const productId = unwrapId(await callKw({
                model: 'product.product',
                method: 'create',
                args: [[{
                    name: 'US Harbor Shipping',
                    type: 'service',
                    sale_ok: false,
                    purchase_ok: false,
                    list_price: 15.0,
                    invoice_policy: 'order',
                }]],
                kwargs: {},
            }));

            const carrierId = unwrapId(await callKw({
                model: 'delivery.carrier',
                method: 'create',
                args: [[{
                    name: 'US Harbor Freight',
                    delivery_type: 'fixed',
                    product_id: productId,
                    free_over: true,
                    amount: 100.0,
                    country_ids: [[6, 0, [usId]]],
                }]],
                kwargs: {},
            }));

            await callKw({
                model: 'delivery.carrier',
                method: 'write',
                args: [[carrierId], { fixed_price: 15.0 }],
                kwargs: {},
            });

            const orderRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'SHIP-US-100']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!orderRes.length) {
                throw new Error('missing target sale order');
            }
            const orderId = orderRes[0].id;

            await callKw({
                model: 'sale.order',
                method: 'write',
                args: [[orderId], { carrier_id: carrierId }],
                kwargs: {},
            });
            await callKw({
                model: 'sale.order.line',
                method: 'create',
                args: [[{
                    order_id: orderId,
                    product_id: productId,
                    name: 'US Harbor Freight',
                    product_uom_qty: 1,
                    price_unit: 0.0,
                    is_delivery: true,
                }]],
                kwargs: {},
            });
            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[orderId]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
