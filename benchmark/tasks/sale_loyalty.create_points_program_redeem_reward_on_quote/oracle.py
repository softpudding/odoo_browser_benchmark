"""Oracle for sale_loyalty.create_points_program_redeem_reward_on_quote."""

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
                    name: 'Rotor Points Reward',
                    program_type: 'loyalty',
                    trigger: 'auto',
                    applies_on: 'current',
                    rule_ids: [[0, 0, {
                        reward_point_mode: 'order',
                        reward_point_amount: 1,
                    }]],
                    reward_ids: [[0, 0, {
                        reward_type: 'discount',
                        discount_mode: 'percent',
                        discount: 10,
                        discount_applicability: 'order',
                        required_points: 1,
                    }]],
                }]],
                kwargs: {},
            }));

            const orderRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'ROTOR-PTS-01']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!orderRes.length) {
                throw new Error('quotation not found');
            }
            const orderId = orderRes[0].id;

            const rewardRes = await callKw({
                model: 'loyalty.reward',
                method: 'search_read',
                args: [[['program_id', '=', programId]], ['id', 'discount_line_product_id']],
                kwargs: { limit: 1 },
            });
            if (!rewardRes.length || !rewardRes[0].discount_line_product_id) {
                throw new Error('reward setup missing');
            }

            await callKw({
                model: 'sale.order.line',
                method: 'create',
                args: [[{
                    order_id: orderId,
                    product_id: rewardRes[0].discount_line_product_id[0],
                    name: 'Rotor Points Reward',
                    product_uom_qty: 1,
                    price_unit: -15,
                    tax_ids: [[6, 0, []]],
                    reward_id: rewardRes[0].id,
                    is_reward_line: true,
                }]],
                kwargs: {},
            });

            const result = await callKw({
                model: 'loyalty.program',
                method: 'read',
                args: [[programId], ['name', 'program_type', 'trigger']],
                kwargs: {},
            });
            return result[0];
        }""",
    )
    if response.get("program_type") != "loyalty":
        raise RuntimeError(f"program_type is {response.get('program_type')!r}")


run_oracle(oracle)
