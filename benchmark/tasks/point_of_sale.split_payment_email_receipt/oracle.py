"""Oracle for point_of_sale.split_payment_email_receipt."""

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
                args: [[['name', '=', 'Benchmark Bistro']], ['id', 'pricelist_id']],
                kwargs: { limit: 1 },
            });
            const sessionRes = await callKw({
                model: 'pos.session',
                method: 'search_read',
                args: [[['config_id', '=', configRes[0].id]], ['id', 'state']],
                kwargs: { limit: 1 },
            });
            if (!configRes.length || !sessionRes.length) {
                throw new Error('missing POS setup');
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
                args: [[['name', '=', 'Harbor Granola Box']], ['id']],
                kwargs: { limit: 1 },
            });
            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Harbor Receipt Customer']], ['id']],
                kwargs: { limit: 1 },
            });
            const paymentMethodRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', 'in', ['Bench Cash', 'Bench Card']]], ['id', 'name']],
                kwargs: {},
            });
            const paymentIds = Object.fromEntries(paymentMethodRes.map((pm) => [pm.name, pm.id]));

            const orderId = unwrapId(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'POS/BENCH/SPLIT01',
                    pos_reference: 'BENCH-SPLIT-01',
                    session_id: sessionId,
                    config_id: configRes[0].id,
                    company_id: 1,
                    partner_id: partnerRes[0].id,
                    pricelist_id: configRes[0].pricelist_id[0],
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 9.6,
                    amount_paid: 0,
                    amount_return: 0,
                    lines: [[0, 0, {
                        name: 'Harbor Granola Box',
                        full_product_name: 'Harbor Granola Box',
                        product_id: productRes[0].id,
                        price_unit: 9.6,
                        qty: 1,
                        discount: 0,
                        tax_ids: [[6, 0, []]],
                        price_subtotal: 9.6,
                        price_subtotal_incl: 9.6,
                    }]],
                }]],
                kwargs: {},
            }));
            const paymentContext = { active_id: orderId, active_ids: [orderId] };
            const cashWizardId = unwrapId(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: 5.0,
                    payment_method_id: paymentIds['Bench Cash'],
                }]],
                kwargs: { context: paymentContext },
            }));
            await callKw({
                model: 'pos.make.payment',
                method: 'check',
                args: [[cashWizardId]],
                kwargs: { context: paymentContext },
            });
            const cardWizardId = unwrapId(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: 4.6,
                    payment_method_id: paymentIds['Bench Card'],
                }]],
                kwargs: { context: paymentContext },
            }));
            await callKw({
                model: 'pos.make.payment',
                method: 'check',
                args: [[cardWizardId]],
                kwargs: { context: paymentContext },
            });
            await callKw({
                model: 'pos.order',
                method: 'action_send_receipt',
                args: [[orderId], 'harbor.receipts@example.com', btoa('fake-jpeg-ticket'), false],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
