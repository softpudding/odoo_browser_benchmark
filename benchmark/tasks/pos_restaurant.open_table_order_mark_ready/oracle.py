"""Oracle for pos_restaurant.open_table_order_mark_ready.

Uses JSON-RPC (allowed for oracle scripts only) to bypass the heavily
customized restaurant POS kiosk UI. Opens the seeded session if it is
still in 'opening_control', then creates a pos.order linked to table T1
with two order lines (Starter Salad x1, Main Steak x1). A
restaurant.order.course is created with fired=True to represent the
kitchen 'ready' state -- the same side effect produced in the UI by
clicking the 'Send / Order' action-pad button after splitting the order
into two courses. The order stays in 'draft' (no payment).
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
                    [['name', '=', 'Bench Restaurant']],
                    ['id', 'pricelist_id', 'floor_ids'],
                ],
                kwargs: { limit: 1 },
            });
            if (!configRes.length) {
                throw new Error('POS config missing');
            }
            const configId = configRes[0].id;

            const sessionRes = await callKw({
                model: 'pos.session',
                method: 'search_read',
                args: [[['config_id', '=', configId]], ['id', 'state']],
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

            const tableRes = await callKw({
                model: 'restaurant.table',
                method: 'search_read',
                args: [
                    [['floor_id.pos_config_ids', '=', configId], ['table_number', '=', 1]],
                    ['id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!tableRes.length) {
                throw new Error('Table T1 missing');
            }
            const tableId = tableRes[0].id;

            const starterRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Starter Salad']], ['id']],
                kwargs: { limit: 1 },
            });
            const mainRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Main Steak']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!starterRes.length || !mainRes.length) {
                throw new Error('Seeded products missing');
            }

            const linePayload = [
                [0, 0, {
                    name: 'Starter Salad',
                    full_product_name: 'Starter Salad',
                    product_id: starterRes[0].id,
                    price_unit: 15.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 15.0,
                    price_subtotal_incl: 15.0,
                }],
                [0, 0, {
                    name: 'Main Steak',
                    full_product_name: 'Main Steak',
                    product_id: mainRes[0].id,
                    price_unit: 20.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 20.0,
                    price_subtotal_incl: 20.0,
                }],
            ];

            const orderId = unwrapId(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'Bench Restaurant - T1 - 000001',
                    pos_reference: 'BENCH-RESTO-T1-01',
                    session_id: sessionId,
                    config_id: configId,
                    company_id: 1,
                    table_id: tableId,
                    customer_count: 2,
                    state: 'draft',
                    pricelist_id: unwrapId(configRes[0].pricelist_id) || false,
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 35.0,
                    amount_paid: 0,
                    amount_return: 0,
                    lines: linePayload,
                }]],
                kwargs: {},
            }));

            // Create Course 1 (fired = True -> kitchen 'ready' state), and
            // attach the first order line to it so the course is considered
            // non-empty by restaurant.order.course cleaners.
            const orderLines = await callKw({
                model: 'pos.order.line',
                method: 'search_read',
                args: [[['order_id', '=', orderId]], ['id', 'product_id']],
                kwargs: { order: 'id asc' },
            });
            const starterLineId = orderLines.find(
                (l) => unwrapId(l.product_id) === starterRes[0].id
            )?.id;
            const mainLineId = orderLines.find(
                (l) => unwrapId(l.product_id) === mainRes[0].id
            )?.id;

            const course1Id = unwrapId(await callKw({
                model: 'restaurant.order.course',
                method: 'create',
                args: [[{
                    order_id: orderId,
                    index: 1,
                    fired: true,
                }]],
                kwargs: {},
            }));
            if (starterLineId) {
                await callKw({
                    model: 'pos.order.line',
                    method: 'write',
                    args: [[starterLineId], { course_id: course1Id }],
                    kwargs: {},
                });
            }

            // Course 2 (not fired) contains the Main Steak -- this is the
            // state the UI would produce after the agent clicks 'Course'
            // between items and then 'Send' to fire the first course only.
            const course2Id = unwrapId(await callKw({
                model: 'restaurant.order.course',
                method: 'create',
                args: [[{
                    order_id: orderId,
                    index: 2,
                    fired: false,
                }]],
                kwargs: {},
            }));
            if (mainLineId) {
                await callKw({
                    model: 'pos.order.line',
                    method: 'write',
                    args: [[mainLineId], { course_id: course2Id }],
                    kwargs: {},
                });
            }

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
