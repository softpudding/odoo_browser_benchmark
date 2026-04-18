"""Oracle for point_of_sale.cash_in_sell_cash_out_close_session."""

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
                args: [[['name', '=', 'Benchmark Cash Desk']], ['id', 'pricelist_id']],
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

            await callKw({
                model: 'pos.session',
                method: 'try_cash_in_out',
                args: [[sessionId], 'in', 20.0, 'Opening float', false, {translatedType: 'Cash in'}],
                kwargs: {},
            });

            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench Snack Crate']], ['id']],
                kwargs: { limit: 1 },
            });
            const paymentRes = await callKw({
                model: 'pos.payment.method',
                method: 'search_read',
                args: [[['name', '=', 'Bench Cash']], ['id']],
                kwargs: { limit: 1 },
            });

            const orderId = unwrapId(await callKw({
                model: 'pos.order',
                method: 'create',
                args: [[{
                    name: 'POS/BENCH/CASHFLOW01',
                    pos_reference: 'BENCH-CASHFLOW-01',
                    session_id: sessionId,
                    config_id: configRes[0].id,
                    company_id: 1,
                    pricelist_id: configRes[0].pricelist_id[0],
                    date_order: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    amount_tax: 0,
                    amount_total: 12.0,
                    amount_paid: 0,
                    amount_return: 0,
                    lines: [[0, 0, {
                        name: 'Bench Snack Crate',
                        full_product_name: 'Bench Snack Crate',
                        product_id: productRes[0].id,
                        price_unit: 12.0,
                        qty: 1,
                        discount: 0,
                        tax_ids: [[6, 0, []]],
                        price_subtotal: 12.0,
                        price_subtotal_incl: 12.0,
                    }]],
                }]],
                kwargs: {},
            }));
            const paymentContext = { active_id: orderId, active_ids: [orderId] };
            const wizardId = unwrapId(await callKw({
                model: 'pos.make.payment',
                method: 'create',
                args: [[{
                    amount: 12.0,
                    payment_method_id: paymentRes[0].id,
                }]],
                kwargs: { context: paymentContext },
            }));
            await callKw({
                model: 'pos.make.payment',
                method: 'check',
                args: [[wizardId]],
                kwargs: { context: paymentContext },
            });

            await callKw({
                model: 'pos.session',
                method: 'try_cash_in_out',
                args: [[sessionId], 'out', 5.0, 'Petty cash drop', false, {translatedType: 'Cash out'}],
                kwargs: {},
            });

            const result = await callKw({
                model: 'pos.session',
                method: 'close_session_from_ui',
                args: [[sessionId]],
                kwargs: {},
            });
            if (result && result.successful === false) {
                throw new Error(result.message || 'close_session_from_ui failed');
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
