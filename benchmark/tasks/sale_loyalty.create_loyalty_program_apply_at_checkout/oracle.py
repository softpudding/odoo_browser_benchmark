"""Oracle for sale_loyalty.create_loyalty_program_apply_at_checkout.

Strategy:
  1. Login as admin and use a JSON-RPC call to create the loyalty program
     ('promo_code' type, single 10% order-discount reward, code SPRING10,
     minimum purchase 150, reward description "Spring Sale Discount").
  2. Navigate to /shop/cart and POST the SPRING10 code on the website
     `coupon_code` form to attach the discount line to the seeded cart.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


PROGRAM_NAME = "Spring 10% Discount"
CODE = "SPRING10"
REWARD_DESCRIPTION = "Spring Sale Discount"
MIN_PURCHASE = 150


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
            const created = await callKw({
                model: 'loyalty.program',
                method: 'create',
                args: [[{
                    name: payload.programName,
                    program_type: 'promo_code',
                    applies_on: 'current',
                    trigger: 'with_code',
                    rule_ids: [[5, 0, 0], [0, 0, {
                        mode: 'with_code',
                        code: payload.code,
                        minimum_qty: 0,
                        minimum_amount: payload.minPurchase,
                    }]],
                    reward_ids: [[5, 0, 0], [0, 0, {
                        reward_type: 'discount',
                        discount: 10,
                        discount_mode: 'percent',
                        discount_applicability: 'order',
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
            "code": CODE,
            "minPurchase": MIN_PURCHASE,
            "rewardDescription": REWARD_DESCRIPTION,
        },
    )
    if not response:
        raise RuntimeError(f"Loyalty program create failed: {response!r}")

    navigate(page, "/shop/cart")
    page.wait_for_load_state("load")
    page.wait_for_timeout(800)

    apply_result = page.evaluate(
        """async (code) => {
            const tokenInput = document.querySelector(
                "form[name='coupon_code'] input[name='csrf_token']"
            );
            const token = tokenInput ? tokenInput.value : '';
            const body = new URLSearchParams();
            body.set('promo', code);
            if (token) body.set('csrf_token', token);
            const res = await fetch('/shop/pricelist?r=/shop/cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                credentials: 'same-origin',
                body: body.toString(),
            });
            return res.status;
        }""",
        CODE,
    )
    if apply_result not in (200, 302, 303):
        raise RuntimeError(f"Coupon POST returned status {apply_result}")

    navigate(page, "/shop/cart")
    page.wait_for_load_state("load")
    page.wait_for_timeout(800)


run_oracle(oracle)
