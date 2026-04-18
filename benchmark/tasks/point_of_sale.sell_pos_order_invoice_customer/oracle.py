"""Oracle for point_of_sale.sell_pos_order_invoice_customer.

Uses authenticated JSON-RPC to bypass the POS kiosk UI. Opens the
seeded session if it is still in 'opening_control', creates a pos.order
with one product line at qty 1 (price 50.00), attaches partner Invoice
Iris, sets to_invoice=True, registers a single 50.00 cash payment via
pos.make.payment, then triggers the invoice generation via
pos.order.action_pos_order_invoice (which posts the customer invoice).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/point-of-sale")

    response = page.evaluate(
        """async () => {
            const unwrap = (v) => Array.isArray(v) ? v[0] : v;
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

            const configRes = await callKw({
                model: 'pos.config',
                method: 'search_read',
                args: [
                    [['name', '=', 'Bench Invoice POS']],
                    ['id', 'pricelist_id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!configRes.length) throw new Error('POS config missing');

            const sessionRes = await callKw({
                model: 'pos.session',
                method: 'search_read',
                args: [[['config_id', '=', configRes[0].id]], ['id', 'state']],
                kwargs: { limit: 1 },
            });
            if (!sessionRes.length) throw new Error('POS session missing');
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
                args: [[['name', '=', 'Bench Invoice Item']], ['id']],
                kwargs: { limit: 1 },
            });
            const cashRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', '=', 'Bench Invoice Cash']], ['id']],
                kwargs: { limit: 1 },
            });
            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Invoice Iris']], ['id']],
                kwargs: { limit: 1 },
            });

            const linePayload = [
                [0, 0, {
                    name: 'Bench Invoice Item',
                    full_product_name: 'Bench Invoice Item',
                    product_id: productRes[0].id,
                    price_unit: 50.0,
                    qty: 1,
                    discount: 0,
                    tax_ids: [[6, 0, []]],
                    price_subtotal: 50.0,
                    price_subtotal_incl: 50.0,
                }],
            ];

            const orderId = unwrap(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'Bench Invoice POS - 000001',
                    pos_reference: 'BENCH-INV-01',
                    session_id: sessionId,
                    config_id: configRes[0].id,
                    company_id: 1,
                    partner_id: partnerRes[0].id,
                    pricelist_id: unwrap(configRes[0].pricelist_id) || false,
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 50.0,
                    amount_paid: 0,
                    amount_return: 0,
                    to_invoice: true,
                    lines: linePayload,
                }]],
                kwargs: {},
            }));

            const paymentContext = {
                active_id: orderId,
                active_ids: [orderId],
                generate_pdf: false,
            };
            const wizardId = unwrap(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: 50.0,
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

            // Trigger invoice generation if not already done by the payment flow.
            const orderState = await callKw({
                model: 'pos.order',
                method: 'read',
                args: [[orderId], ['state', 'account_move']],
                kwargs: {},
            });
            if (!orderState[0].account_move) {
                await callKw({
                    model: 'pos.order',
                    method: 'action_pos_order_invoice',
                    args: [[orderId]],
                    kwargs: { context: { generate_pdf: false } },
                });
            }

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
