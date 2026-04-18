"""Oracle for website_sale.create_gift_card_apply_in_cart.

Strategy:
  1. Login as admin and use a JSON-RPC `create` to build the gift_card loyalty
     program (uses the gift_card defaults from
     `loyalty.program._program_type_default_values`).
  2. JSON-RPC `create` on `loyalty.card` to mint a single anonymous gift card
     with 50 points (mirrors the Generate Gift Cards wizard).
  3. Navigate to /shop/cart and POST the card's code on the website
     `coupon_code` form (`/shop/pricelist?r=/shop/cart`) to attach the gift-
     card payment line to the seeded €100 cart.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


PROGRAM_NAME = "Spring Gift Card"
GIFT_CARD_VALUE = 50


def oracle(page):
    login(page)

    navigate(page, "/odoo/gift-cards-ewallet")

    code = page.evaluate(
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
            // Use create_from_template to get all proper gift_card defaults
            // (rule with gift_card_product_50, reward = per_point discount, etc.).
            const action = await callKw({
                model: 'loyalty.program',
                method: 'create_from_template',
                args: ['gift_card'],
                kwargs: { context: { menu_type: 'gift_ewallet' } },
            });
            const programId = action && action.res_id;
            if (!programId) {
                throw new Error('create_from_template did not return res_id');
            }
            // Rename the freshly-created program to match the prompt.
            await callKw({
                model: 'loyalty.program',
                method: 'write',
                args: [[programId], { name: payload.programName }],
                kwargs: {},
            });
            // Generate one anonymous gift card with the requested value.
            const cardIds = await callKw({
                model: 'loyalty.card',
                method: 'create',
                args: [[{
                    program_id: programId,
                    points: payload.value,
                    partner_id: false,
                }]],
                kwargs: { context: { loyalty_no_mail: true, action_no_send_mail: true } },
            });
            const cardId = Array.isArray(cardIds) ? cardIds[0] : cardIds;
            const cardData = await callKw({
                model: 'loyalty.card',
                method: 'read',
                args: [[cardId], ['code']],
                kwargs: {},
            });
            return cardData[0].code;
        }""",
        {
            "programName": PROGRAM_NAME,
            "value": GIFT_CARD_VALUE,
        },
    )
    if not code:
        raise RuntimeError(f"Could not generate gift card: {code!r}")

    navigate(page, "/shop/cart")
    page.wait_for_load_state("load")
    page.wait_for_timeout(800)

    apply_status = page.evaluate(
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
        code,
    )
    if apply_status not in (200, 302, 303):
        raise RuntimeError(f"Coupon POST returned status {apply_status}")

    navigate(page, "/shop/cart")
    page.wait_for_load_state("load")
    page.wait_for_timeout(800)


run_oracle(oracle)
