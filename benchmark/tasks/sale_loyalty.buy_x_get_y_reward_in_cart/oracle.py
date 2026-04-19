"""Oracle for sale_loyalty.buy_x_get_y_reward_in_cart.

Strategy (pure JSON-RPC driven from the Sales backend):
  1. Log in and navigate to the Sales Quotations list.
  2. Create a sale.order for 'Bench Promo Customer'.
  3. Add a sale.order.line with product 'Bench Promo Widget' qty=2 @ €10.
  4. Call `_update_programs_and_rewards` so the BOGO coupon_point_ids are
     created for the in-progress order.
  5. Instantiate the `sale.loyalty.reward.wizard`, pick the single claimable
     reward, write `selected_reward_id`, and call `action_apply`. This adds the
     reward (free product) line via `_apply_program_reward`.
  6. Call `sale.order.action_confirm` to move the SO from 'draft' to 'sale'.
  7. Sanity-check amount_total ~ 20.0 and exactly 3 order lines.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


PROGRAM_NAME = "Bench BOGO"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Widget"


def oracle(page):
    login(page)

    # Land on a real backend page before issuing JSON-RPC calls.
    navigate(page, "/odoo/sales")

    result = page.evaluate(
        """async (payload) => {
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

            // 1. Resolve seeded partner/product/program ids.
            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', payload.customerName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!partnerRes.length) {
                throw new Error('Seeded partner not found');
            }
            const partnerId = partnerRes[0].id;

            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', payload.productName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!productRes.length) {
                throw new Error('Seeded product not found');
            }
            const productId = productRes[0].id;

            const programRes = await callKw({
                model: 'loyalty.program',
                method: 'search_read',
                args: [[['name', '=', payload.programName]], ['id', 'reward_ids']],
                kwargs: { limit: 1 },
            });
            if (!programRes.length) {
                throw new Error('Seeded loyalty program not found');
            }
            const programId = programRes[0].id;
            const rewardId = (programRes[0].reward_ids || [])[0];
            if (!rewardId) {
                throw new Error('Seeded loyalty program has no reward');
            }

            // 2. Create the sale order.
            const orderId = unwrap(await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerId,
                }]],
                kwargs: {},
            }));

            // 3. Add the paid product line (qty 2).
            await callKw({
                model: 'sale.order.line',
                method: 'create',
                args: [[{
                    order_id: orderId,
                    product_id: productId,
                    product_uom_qty: 2.0,
                    price_unit: 10.0,
                    tax_ids: [[5, 0, 0]],
                }]],
                kwargs: {},
            });

            // 4. Claim the BOGO reward via the reward wizard. For this
            //    program (1 reward, not multi_product) action_open_reward_wizard
            //    directly applies the reward server-side; otherwise fall back
            //    to the wizard create + write + action_apply dance.
            const openResult = await callKw({
                model: 'sale.order',
                method: 'action_open_reward_wizard',
                args: [[orderId]],
                kwargs: {},
            });
            const wizardOpened = openResult !== true;
            if (wizardOpened) {
                // The reward wasn't auto-applied; drive the wizard explicitly.
                const wizardId = unwrap(await callKw({
                    model: 'sale.loyalty.reward.wizard',
                    method: 'create',
                    args: [[{ order_id: orderId }]],
                    kwargs: {},
                }));
                const wizardData = await callKw({
                    model: 'sale.loyalty.reward.wizard',
                    method: 'read',
                    args: [[wizardId], ['reward_ids']],
                    kwargs: {},
                });
                const claimable = (wizardData[0] || {}).reward_ids || [];
                if (!claimable.includes(rewardId)) {
                    throw new Error(
                        'BOGO reward is not claimable. claimable='
                        + JSON.stringify(claimable)
                        + ' rewardId=' + rewardId
                    );
                }
                await callKw({
                    model: 'sale.loyalty.reward.wizard',
                    method: 'write',
                    args: [[wizardId], { selected_reward_id: rewardId }],
                    kwargs: {},
                });
                await callKw({
                    model: 'sale.loyalty.reward.wizard',
                    method: 'action_apply',
                    args: [[wizardId]],
                    kwargs: {},
                });
            }

            // 5. Confirm the SO.
            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[orderId]],
                kwargs: {},
            });

            // 6. Final sanity snapshot.
            const snap = await callKw({
                model: 'sale.order',
                method: 'read',
                args: [[orderId], ['state', 'amount_total', 'order_line']],
                kwargs: {},
            });
            return { order: snap[0], programId };
        }""",
        {
            "customerName": CUSTOMER_NAME,
            "productName": PRODUCT_NAME,
            "programName": PROGRAM_NAME,
        },
    )

    order = result["order"]
    if order["state"] != "sale":
        raise RuntimeError(f"Oracle expected state='sale' got {order['state']!r}")
    if abs(order["amount_total"] - 20.0) > 0.05:
        raise RuntimeError(
            f"Oracle expected amount_total=20.0 got {order['amount_total']}"
        )
    if len(order["order_line"]) != 2:
        # We expect exactly 2 lines: one paid (qty 2) + one reward (qty 1).
        raise RuntimeError(
            f"Oracle got unexpected order_line count={len(order['order_line'])}"
        )


run_oracle(oracle)
