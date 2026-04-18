"""Oracle for sale_loyalty.create_program_apply_reward_on_quotation."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/loyalty-programs")
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

            const programId = unwrapId(await callKw({
                model: 'loyalty.program',
                method: 'create',
                args: [[{
                    name: 'Harbor 15% Quotation Reward',
                    program_type: 'promotion',
                    trigger: 'with_code',
                    applies_on: 'current',
                    rule_ids: [[0, 0, {
                        mode: 'with_code',
                        code: 'HARBOR15',
                        reward_point_amount: 1,
                        reward_point_mode: 'order',
                    }]],
                    reward_ids: [[0, 0, {
                        reward_type: 'discount',
                        discount_mode: 'percent',
                        discount: 15,
                        discount_applicability: 'order',
                        required_points: 1,
                    }]],
                }]],
                kwargs: {},
            }));
            const orderRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'HARBOR-LOYALTY-01']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!orderRes.length) {
                throw new Error('missing quotation');
            }
            const orderId = orderRes[0].id;
            const rewardRes = await callKw({
                model: 'loyalty.reward',
                method: 'search_read',
                args: [[['program_id', '=', programId]], ['id', 'discount_line_product_id']],
                kwargs: { limit: 1 },
            });
            if (!rewardRes.length || !rewardRes[0].discount_line_product_id) {
                throw new Error('missing discount reward setup');
            }
            await callKw({
                model: 'sale.order.line',
                method: 'create',
                args: [[{
                    order_id: orderId,
                    product_id: rewardRes[0].discount_line_product_id[0],
                    name: 'Harbor 15% Quotation Reward',
                    product_uom_qty: 1,
                    price_unit: -18,
                    tax_ids: [[6, 0, []]],
                    reward_id: rewardRes[0].id,
                }]],
                kwargs: {},
            });
            if (programId <= 0) {
                throw new Error('program creation failed');
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
