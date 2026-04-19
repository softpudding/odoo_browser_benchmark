"""Oracle for point_of_sale.refund_previous_order.

Uses JSON-RPC (allowed for oracle scripts only) to bypass the POS kiosk
UI. Finds the seeded prior order (Bench Widget x3, paid 30.00), invokes
pos.order.refund() to generate a draft refund order, then edits the
auto-generated refund line so that only 1 Bench Widget is refunded
(qty = -1, subtotal -10.00). Finally registers a single -10.00 cash
payment via pos.make.payment, leaving the refund order in the paid
state with is_refund=True.
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

            // 1. Locate config + session.
            const configRes = await callKw({
                model: 'pos.config',
                method: 'search_read',
                args: [[['name', '=', 'Bench Refund POS']], ['id', 'pricelist_id']],
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

            // 2. Locate the prior paid order.
            const origRes = await callKw({
                model: 'pos.order',
                method: 'search_read',
                args: [
                    [['pos_reference', '=', 'BENCH-REFUND-01']],
                    ['id', 'name'],
                ],
                kwargs: { limit: 1 },
            });
            if (!origRes.length) {
                throw new Error('Seeded prior order BENCH-REFUND-01 missing');
            }
            const origOrderId = origRes[0].id;

            // 3. Call refund() on the original order. It returns an action
            //    whose res_id is the new draft refund order id.
            const refundAction = await callKw({
                model: 'pos.order',
                method: 'refund',
                args: [[origOrderId]],
                kwargs: {},
            });
            const refundOrderId = refundAction.res_id;
            if (!refundOrderId) {
                throw new Error('refund() did not return a res_id');
            }

            // 4. Inspect the auto-generated refund line (qty -3) and
            //    reduce its qty to -1 so only one Bench Widget is refunded.
            const refundLines = await callKw({
                model: 'pos.order.line',
                method: 'search_read',
                args: [
                    [['order_id', '=', refundOrderId]],
                    ['id', 'qty', 'price_unit'],
                ],
                kwargs: {},
            });
            if (refundLines.length !== 1) {
                throw new Error('Expected exactly 1 refund line, got ' + refundLines.length);
            }
            const refundLineId = refundLines[0].id;

            // Update the refund line: qty -1, subtotals -10.00.
            await callKw({
                model: 'pos.order.line',
                method: 'write',
                args: [[refundLineId], {
                    qty: -1,
                    price_subtotal: -10.0,
                    price_subtotal_incl: -10.0,
                }],
                kwargs: {},
            });

            // 5. Update the refund order's aggregate totals to match the
            //    reduced refund-line qty.
            await callKw({
                model: 'pos.order',
                method: 'write',
                args: [[refundOrderId], {
                    amount_tax: 0.0,
                    amount_total: -10.0,
                    amount_paid: 0.0,
                    amount_return: 0.0,
                }],
                kwargs: {},
            });

            // 6. Register a single -10.00 cash payment.
            const cashRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', '=', 'Bench Refund Cash']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!cashRes.length) {
                throw new Error('Bench Refund Cash payment method missing');
            }
            const paymentContext = { active_id: refundOrderId, active_ids: [refundOrderId] };
            const wizardId = unwrapId(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: -10.0,
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
