"""Oracle for sale_loyalty.buy_x_get_y_reward_in_cart.

Strategy:
  1. Login as admin, open the backend, then JSON-RPC create a 'promotion' loyalty
     program with trigger='auto': the rule requires qty 2 of Bench Widget, and
     the reward is a product reward giving 1 free Bench Gadget.
  2. Navigate to /shop/cart — the website_sale_loyalty cart controller invokes
     _update_programs_and_rewards() and _auto_apply_rewards(), which attaches a
     Bench Gadget reward line at price 0 to the seeded cart.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


PROGRAM_NAME = "Buy 2 Widgets Get 1 Gadget"
BUY_PRODUCT_NAME = "Bench Widget"
REWARD_PRODUCT_NAME = "Bench Gadget"
REWARD_DESCRIPTION = "Free Bench Gadget"


def oracle(page):
    login(page)

    navigate(page, "/odoo/discount-loyalty")

    response = page.evaluate(
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
            const [buyTmpl] = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', payload.buyProductName]], ['product_variant_id']],
                kwargs: { limit: 1 },
            });
            const [rewardTmpl] = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', payload.rewardProductName]], ['product_variant_id']],
                kwargs: { limit: 1 },
            });
            if (!buyTmpl || !rewardTmpl) {
                throw new Error('Seed products not found: buy=' + JSON.stringify(buyTmpl) + ' reward=' + JSON.stringify(rewardTmpl));
            }
            const buyVariantId = Array.isArray(buyTmpl.product_variant_id)
                ? buyTmpl.product_variant_id[0]
                : buyTmpl.product_variant_id;
            const rewardVariantId = Array.isArray(rewardTmpl.product_variant_id)
                ? rewardTmpl.product_variant_id[0]
                : rewardTmpl.product_variant_id;

            const created = await callKw({
                model: 'loyalty.program',
                method: 'create',
                args: [[{
                    name: payload.programName,
                    program_type: 'promotion',
                    applies_on: 'current',
                    trigger: 'auto',
                    rule_ids: [[5, 0, 0], [0, 0, {
                        reward_point_mode: 'order',
                        reward_point_amount: 1,
                        minimum_qty: 2,
                        minimum_amount: 0,
                        product_ids: [[6, 0, [buyVariantId]]],
                    }]],
                    reward_ids: [[5, 0, 0], [0, 0, {
                        reward_type: 'product',
                        reward_product_id: rewardVariantId,
                        reward_product_qty: 1,
                        required_points: 1,
                        description: payload.rewardDescription,
                    }]],
                }]],
                kwargs: {},
            });
            const programId = Array.isArray(created) ? created[0] : created;
            if (!programId) {
                throw new Error('program creation returned no id');
            }
            return programId;
        }""",
        {
            "programName": PROGRAM_NAME,
            "buyProductName": BUY_PRODUCT_NAME,
            "rewardProductName": REWARD_PRODUCT_NAME,
            "rewardDescription": REWARD_DESCRIPTION,
        },
    )
    if not response:
        raise RuntimeError(f"Loyalty program create failed: {response!r}")

    # Hitting /shop/cart triggers _update_programs_and_rewards +
    # _auto_apply_rewards on the seeded cart, which attaches the free Bench
    # Gadget reward line.
    navigate(page, "/shop/cart")
    page.wait_for_load_state("load")
    page.wait_for_timeout(1200)
    # Reload once to guarantee the auto-apply path ran with the freshly
    # created program in-session.
    navigate(page, "/shop/cart")
    page.wait_for_load_state("load")
    page.wait_for_timeout(1200)


run_oracle(oracle)
