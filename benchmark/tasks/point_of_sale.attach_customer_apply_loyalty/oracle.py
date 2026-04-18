"""Oracle for point_of_sale.attach_customer_apply_loyalty.

Uses JSON-RPC (allowed for oracle scripts only) to bypass the POS kiosk
UI. Opens the seeded session if it is still in 'opening_control', creates
a pos.order with the product line (qty 3 at 20.00 = 60.00), attaches the
seeded loyalty customer, adds a loyalty-funded -6.00 discount reward line
(10% of 60), decrements the loyalty.card balance by 50 points, then
registers a single cash payment of 54.00 through pos.make.payment.
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
                    [['name', '=', 'Bench Loyalty POS']],
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
                args: [[['name', '=', 'Bench POS Item']], ['id']],
                kwargs: { limit: 1 },
            });
            const cashRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', '=', 'Bench Loyalty Cash']], ['id']],
                kwargs: { limit: 1 },
            });
            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Loyal Larry']], ['id']],
                kwargs: { limit: 1 },
            });
            const programRes = await callKw({
                model: 'loyalty.program',
                method: 'search_read',
                args: [[['name', '=', 'Bench Loyalty Program']], ['id']],
                kwargs: { limit: 1 },
            });
            const rewardRes = await callKw({
                model: 'loyalty.reward',
                method: 'search_read',
                args: [
                    [['program_id', '=', programRes[0].id]],
                    ['id', 'description'],
                ],
                kwargs: { limit: 1 },
            });
            const cardRes = await callKw({
                model: 'loyalty.card',
                method: 'search_read',
                args: [
                    [['program_id', '=', programRes[0].id], ['partner_id', '=', partnerRes[0].id]],
                    ['id', 'points'],
                ],
                kwargs: { limit: 1 },
            });
            if (!cardRes.length) {
                throw new Error('loyalty.card for Loyal Larry is missing');
            }

            const linePayload = [
                [0, 0, {
                    name: 'Bench POS Item',
                    full_product_name: 'Bench POS Item',
                    product_id: productRes[0].id,
                    price_unit: 20.0,
                    qty: 3,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 60.0,
                    price_subtotal_incl: 60.0,
                }],
                [0, 0, {
                    name: '10% on your order',
                    full_product_name: '10% on your order',
                    product_id: productRes[0].id,
                    price_unit: -6.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: -6.0,
                    price_subtotal_incl: -6.0,
                    is_reward_line: true,
                    reward_id: rewardRes[0].id,
                    coupon_id: cardRes[0].id,
                    reward_identifier_code: 'LOYALTY-10',
                    points_cost: 50,
                }],
            ];

            const orderId = unwrapId(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'Bench Loyalty POS - 000001',
                    pos_reference: 'BENCH-LOYAL-01',
                    session_id: sessionId,
                    config_id: configRes[0].id,
                    company_id: 1,
                    partner_id: partnerRes[0].id,
                    pricelist_id: unwrapId(configRes[0].pricelist_id) || false,
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 54.0,
                    amount_paid: 0,
                    amount_return: 0,
                    lines: linePayload,
                }]],
                kwargs: {},
            }));

            // Decrement the loyalty card by the redeemed points.
            await callKw({
                model: 'loyalty.card',
                method: 'write',
                args: [[cardRes[0].id], { points: cardRes[0].points - 50 }],
                kwargs: {},
            });

            const paymentContext = { active_id: orderId, active_ids: [orderId] };
            const wizardId = unwrapId(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: 54.0,
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
