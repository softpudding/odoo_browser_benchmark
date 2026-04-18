"""Oracle for point_of_sale.attach_customer_mid_sale.

Uses JSON-RPC (allowed for oracle scripts only) to bypass the POS kiosk
UI. Opens the seeded session if it is still in 'opening_control', creates
a pos.order with one line of 'Bench Easy POS Item' (qty 1 at 15.00),
attaches the seeded customer, then registers a single cash payment of
15.00 through pos.make.payment.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/point-of-sale")

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

            const configRes = await callKw({
                model: 'pos.config',
                method: 'search_read',
                args: [
                    [['name', '=', 'Bench Easy POS']],
                    ['id', 'pricelist_id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!configRes.length) {
                throw new Error('POS config missing');
            }
            const sessionRes = await callKw({
                model: 'pos.session',
                method: 'search_read',
                args: [[['config_id', '=', configRes[0].id]], ['id', 'state']],
                kwargs: { limit: 1 },
            });
            if (!sessionRes.length) {
                throw new Error('POS session missing');
            }
            const sessionId = sessionRes[0].id;
            if (sessionRes[0].state === 'opening_control') {
                await callKw({
                    model: 'pos.session',
                    method: 'set_opening_control',
                    args: [[sessionId], 0, ''],
                    kwargs: {},
                });
            }

            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench Easy POS Item']], ['id']],
                kwargs: { limit: 1 },
            });
            const cashRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', '=', 'Bench Easy Cash']], ['id']],
                kwargs: { limit: 1 },
            });
            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Bench POS Easy Customer']], ['id']],
                kwargs: { limit: 1 },
            });

            const linePayload = [
                [0, 0, {
                    name: 'Bench Easy POS Item',
                    full_product_name: 'Bench Easy POS Item',
                    product_id: productRes[0].id,
                    price_unit: 15.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 15.0,
                    price_subtotal_incl: 15.0,
                }],
            ];

            const orderId = unwrapId(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'Bench Easy POS - 000001',
                    pos_reference: 'BENCH-EASY-01',
                    session_id: sessionId,
                    config_id: configRes[0].id,
                    company_id: 1,
                    partner_id: partnerRes[0].id,
                    pricelist_id: unwrapId(configRes[0].pricelist_id) || false,
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 15.0,
                    amount_paid: 0,
                    amount_return: 0,
                    lines: linePayload,
                }]],
                kwargs: {},
            }));

            const paymentContext = { active_id: orderId, active_ids: [orderId] };
            const wizardId = unwrapId(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: 15.0,
                    payment_method_id: cashRes[0].id,
                }]],
                kwargs: { context: paymentContext },
            }));
            await callKw({
                model: 'pos.make.payment',
                method: 'check',
                args: [[wizardId]],
                kwargs: { context: paymentContext },
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
