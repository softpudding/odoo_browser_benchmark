"""Oracle for delivery.configure_fixed_rate_carrier_confirm_sale."""

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

            const serviceProductId = unwrapId(await callKw({
                model: 'product.product',
                method: 'create',
                args: [[{
                    name: 'Harbor Flat Freight Service',
                    type: 'service',
                    sale_ok: false,
                    purchase_ok: false,
                    list_price: 18.5,
                }]],
                kwargs: {},
            }));
            const carrierId = unwrapId(await callKw({
                model: 'delivery.carrier',
                method: 'create',
                args: [[{
                    name: 'Harbor Flat Freight',
                    delivery_type: 'fixed',
                    product_id: serviceProductId,
                    fixed_price: 18.5,
                }]],
                kwargs: {},
            }));
            const orderRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'HARBOR-SHIP-01']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!orderRes.length) {
                throw new Error('missing sale order');
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
                    product_id: serviceProductId,
                    name: 'Harbor Flat Freight',
                    product_uom_qty: 1,
                    price_unit: 18.5,
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
