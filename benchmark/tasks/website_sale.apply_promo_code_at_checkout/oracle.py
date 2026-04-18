"""Oracle for website_sale.apply_promo_code_at_checkout.

Strategy:
  1. Log in as admin and navigate to the Discounts & Loyalty list.
  2. Via JSON-RPC `create` on `loyalty.program`, build a promo_code program
     with explicit rule (code=BENCH10, mode=with_code) and reward (10% off,
     discount_applicability='order').
  3. Navigate to the Sales Quotations list, open the seeded SO-BENCH-001, and
     call `_try_apply_code('BENCH10')` on the order via JSON-RPC to attach the
     discount reward line.
  4. Final sanity: read the order total and assert it's ~90.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


PROGRAM_NAME = "Bench Promo 10%"
PROMO_CODE = "BENCH10"
ORDER_REF = "SO-BENCH-001"


def oracle(page):
    login(page)

    # Open the Discounts & Loyalty backend list so the oracle lands somewhere
    # realistic before issuing RPCs.
    navigate(page, "/odoo/discount-loyalty")

    program_id = page.evaluate(
        """async (payload) => {
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
            const ids = await callKw({
                model: 'loyalty.program',
                method: 'create',
                args: [[{
                    name: payload.programName,
                    program_type: 'promo_code',
                    trigger: 'with_code',
                    applies_on: 'current',
                    rule_ids: [[5, 0, 0], [0, 0, {
                        mode: 'with_code',
                        code: payload.code,
                        minimum_qty: 0,
                    }]],
                    reward_ids: [[5, 0, 0], [0, 0, {
                        reward_type: 'discount',
                        discount: 10,
                        discount_mode: 'percent',
                        discount_applicability: 'order',
                        required_points: 1,
                    }]],
                }]],
                kwargs: {},
            });
            return Array.isArray(ids) ? ids[0] : ids;
        }""",
        {
            "programName": PROGRAM_NAME,
            "code": PROMO_CODE,
        },
    )
    if not program_id:
        raise RuntimeError("Could not create loyalty.program")

    # Now open the Sales quotations list and navigate to the seeded SO.
    navigate(page, "/odoo/sales")

    apply_result = page.evaluate(
        """async (payload) => {
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
            const orderIds = await callKw({
                model: 'sale.order',
                method: 'search',
                args: [[['client_order_ref', '=', payload.orderRef]]],
                kwargs: { limit: 1 },
            });
            if (!orderIds || orderIds.length === 0) {
                throw new Error('Seeded order not found');
            }
            const orderId = orderIds[0];

            // Use the Apply Coupon wizard (the standard UI path) to apply the
            // code. The wizard's action_apply internally calls the private
            // _try_apply_code and then returns an action pointing at the
            // reward-selection wizard.
            const couponWizIds = await callKw({
                model: 'sale.loyalty.coupon.wizard',
                method: 'create',
                args: [[{ order_id: orderId, coupon_code: payload.code }]],
                kwargs: {},
            });
            const couponWizId = Array.isArray(couponWizIds)
                ? couponWizIds[0]
                : couponWizIds;
            const couponAction = await callKw({
                model: 'sale.loyalty.coupon.wizard',
                method: 'action_apply',
                args: [[couponWizId]],
                kwargs: {},
            });

            // The coupon wizard returns an action for the reward-selection
            // wizard. We need to instantiate it, pick the single claimable
            // reward, and call action_apply on it.
            const rewardIds = await callKw({
                model: 'sale.loyalty.reward.wizard',
                method: 'create',
                args: [[{ order_id: orderId }]],
                kwargs: {},
            });
            const rewardWizId = Array.isArray(rewardIds) ? rewardIds[0] : rewardIds;
            const rewardWizData = await callKw({
                model: 'sale.loyalty.reward.wizard',
                method: 'read',
                args: [[rewardWizId], ['reward_ids']],
                kwargs: {},
            });
            const claimable = rewardWizData[0].reward_ids || [];
            if (claimable.length === 0) {
                throw new Error('No claimable rewards after applying code');
            }
            await callKw({
                model: 'sale.loyalty.reward.wizard',
                method: 'write',
                args: [[rewardWizId], { selected_reward_id: claimable[0] }],
                kwargs: {},
            });
            await callKw({
                model: 'sale.loyalty.reward.wizard',
                method: 'action_apply',
                args: [[rewardWizId]],
                kwargs: {},
            });

            const totalData = await callKw({
                model: 'sale.order',
                method: 'read',
                args: [[orderId], ['amount_total', 'amount_untaxed']],
                kwargs: {},
            });
            return { order: totalData[0] };
        }""",
        {
            "orderRef": ORDER_REF,
            "code": PROMO_CODE,
        },
    )

    order_total = apply_result["order"]["amount_total"]
    if abs(order_total - 90.0) > 0.05:
        raise RuntimeError(
            f"Oracle post-apply total is {order_total}, expected 90.0"
        )


run_oracle(oracle)
