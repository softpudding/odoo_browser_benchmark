"""Oracle for point_of_sale.apply_fixed_discount_before_payment.

Uses JSON-RPC (allowed for oracle scripts only) to bypass the POS
kiosk UI. Opens the seeded session, creates a pos.order with the two
product lines (Item A qty 1 @ 20.00, Item B qty 1 @ 15.00) and a
-5.00 global-discount line using the configured discount_product,
then records a single cash payment of 30.00 through pos.make.payment.
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
                    [['name', '=', 'Bench POS']],
                    ['id', 'pricelist_id', 'discount_product_id'],
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

            const productARes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench POS Item A']], ['id']],
                kwargs: { limit: 1 },
            });
            const productBRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench POS Item B']], ['id']],
                kwargs: { limit: 1 },
            });
            const cashRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', '=', 'Bench Cash']], ['id']],
                kwargs: { limit: 1 },
            });
            const discountProductId = unwrapId(configRes[0].discount_product_id);
            if (!discountProductId) {
                throw new Error('discount_product_id is not configured on the POS config');
            }

            const linePayload = [
                [0, 0, {
                    name: 'Bench POS Item A',
                    full_product_name: 'Bench POS Item A',
                    product_id: productARes[0].id,
                    price_unit: 20.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 20.0,
                    price_subtotal_incl: 20.0,
                }],
                [0, 0, {
                    name: 'Bench POS Item B',
                    full_product_name: 'Bench POS Item B',
                    product_id: productBRes[0].id,
                    price_unit: 15.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 15.0,
                    price_subtotal_incl: 15.0,
                }],
                [0, 0, {
                    name: 'Discount 14.29%',
                    full_product_name: 'Discount',
                    product_id: discountProductId,
                    price_unit: -5.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: -5.0,
                    price_subtotal_incl: -5.0,
                }],
            ];

            const orderId = unwrapId(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'Bench POS - 000001',
                    pos_reference: 'BENCH-FIXEDDISC-01',
                    session_id: sessionId,
                    config_id: configRes[0].id,
                    company_id: 1,
                    pricelist_id: unwrapId(configRes[0].pricelist_id) || false,
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 30.0,
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
                    amount: 30.0,
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
