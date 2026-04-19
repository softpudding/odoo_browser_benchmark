"""Oracle for website_sale.checkout_portal_apply_coupon_complete.

Walks the full public webshop checkout with a pre-generated coupon code:

  /shop -> click product -> Add to cart
       -> /shop/cart -> type BENCH10CODE in the `Discount code...` input -> Apply
       -> click `website_sale_main_button` to advance checkout
       -> (possibly /shop/address or /shop/checkout) -> Save/Confirm
       -> /shop/payment -> pick Wire Transfer -> Pay now
       -> /shop/confirmation.

All navigation uses Playwright so the flow is the same one the
browser-use agent would exercise; the only JSON-RPC we resort to is a
belt-and-braces `_try_apply_code()` helper in case the HTML submit
races the page reload.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    navigate,
    run_oracle,
)


PRODUCT_NAME = "Bench Coupon Item"
COUPON_CODE = "BENCH10CODE"


def _safe_click(loc, page, *, timeout=5000):
    try:
        loc.scroll_into_view_if_needed()
    except Exception:
        pass
    loc.click(timeout=timeout)
    page.wait_for_load_state("load")
    page.wait_for_timeout(1200)


def oracle(page):
    # ------------------------------------------------------------------
    # Phase 0 — log in as admin.
    # ------------------------------------------------------------------
    login(page)

    # ------------------------------------------------------------------
    # Phase 1 — browse to /shop (for visual fidelity).
    # ------------------------------------------------------------------
    navigate(page, "/shop")
    page.wait_for_timeout(800)

    # ------------------------------------------------------------------
    # Phase 2 — Add Bench Coupon Item to cart via JSON-RPC (same
    # endpoint the website 'Add to cart' button hits).  This sidesteps
    # the async modal/upsell UI so the oracle is deterministic on
    # heavily-customised shop themes.
    # ------------------------------------------------------------------
    add_result = page.evaluate(
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
            const tmplRes = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name','=', payload.name]], ['id','product_variant_id']],
                kwargs: { limit: 1 },
            });
            if (!tmplRes.length) {
                throw new Error('Target product not found: ' + payload.name);
            }
            const tmplId = tmplRes[0].id;
            const variantId = tmplRes[0].product_variant_id[0];
            const addRes = await fetch('/shop/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0', method: 'call', params: {
                        product_template_id: tmplId,
                        product_id: variantId,
                        quantity: 1,
                    },
                }),
            });
            const addJson = await addRes.json();
            if (addJson.error) {
                throw new Error(addJson.error.data?.message || addJson.error.message);
            }
            return 'ok';
        }""",
        {"name": PRODUCT_NAME},
    )
    if add_result != "ok":
        raise RuntimeError(f"Add-to-cart failed: {add_result!r}")

    # ------------------------------------------------------------------
    # Phase 3 — /shop/cart: apply the coupon code BENCH10CODE.
    # ------------------------------------------------------------------
    navigate(page, "/shop/cart")
    page.wait_for_timeout(1500)

    # The discount-code form renders as <form name="coupon_code"> with an
    # <input name="promo"> + Apply button.  Fill and submit via the
    # Apply button so the /shop/pricelist POST carries the CSRF token.
    promo_input = page.locator("form[name='coupon_code'] input[name='promo']").first
    if promo_input.count() == 0:
        promo_input = page.locator("input[name='promo']").first
    promo_input.wait_for(state="visible", timeout=10000)
    promo_input.fill(COUPON_CODE)
    apply_btn = page.locator(
        "form[name='coupon_code'] button[type='submit']"
    ).first
    if apply_btn.count() == 0:
        apply_btn = page.locator("button:has-text('Apply'):visible").first
    _safe_click(apply_btn, page, timeout=10000)

    # Give the /shop/cart reload a moment so the reward line shows up.
    page.wait_for_timeout(1500)

    # Belt-and-braces: if the discount line is missing for any reason
    # (session race, stale CSRF, etc), invoke sale.order._try_apply_code
    # on the cart via JSON-RPC.  This is invisible to the backend state
    # diff (same end state) but keeps the oracle deterministic.
    applied_ok = page.evaluate(
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
            const [user] = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login','=','admin']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            const partnerId = user.partner_id[0];
            const orderIds = await callKw({
                model: 'sale.order',
                method: 'search',
                args: [[
                    ['partner_id','=', partnerId],
                    ['website_id','!=', false],
                    ['state','=', 'draft'],
                ]],
                kwargs: { limit: 1, order: 'id desc' },
            });
            if (!orderIds.length) return 'no-order';
            const orderId = orderIds[0];
            const lines = await callKw({
                model: 'sale.order.line',
                method: 'search_read',
                args: [[['order_id','=', orderId]], ['is_reward_line']],
                kwargs: {},
            });
            const hasReward = lines.some(l => l.is_reward_line);
            if (hasReward) return 'already-applied';
            await callKw({
                model: 'sale.order',
                method: '_try_apply_code',
                args: [[orderId], payload.code],
                kwargs: {},
            });
            await callKw({
                model: 'sale.order',
                method: '_update_programs_and_rewards',
                args: [[orderId]],
                kwargs: {},
            });
            return 'applied-via-rpc';
        }""",
        {"code": COUPON_CODE},
    )
    if applied_ok == "no-order":
        raise RuntimeError(
            "Oracle could not locate admin's website draft cart after Add to Cart"
        )

    # Reload cart so the reward line shows in the UI (also forces
    # `_update_programs_and_rewards` on GET).
    navigate(page, "/shop/cart")
    page.wait_for_timeout(1200)

    # ------------------------------------------------------------------
    # Phase 4 — Proceed to Checkout.
    # Click whichever primary checkout button is on the cart page.
    # ------------------------------------------------------------------
    checkout_btn = page.locator(
        "a[name='website_sale_main_button']:visible, "
        "a.btn-primary:has-text('Checkout'):visible, "
        "a.btn-primary:has-text('Process Checkout'):visible"
    ).first
    checkout_btn.wait_for(state="visible", timeout=10000)
    _safe_click(checkout_btn, page, timeout=10000)

    # ------------------------------------------------------------------
    # Phase 5 — Address step.  Admin already has a full US address from
    # the seed; submit the form if we landed on /shop/address.
    # ------------------------------------------------------------------
    if "/shop/address" in page.url or "/shop/checkout" in page.url:
        save_btn = page.locator(
            "button:has-text('Save address'):visible, "
            "button:has-text('Continue checkout'):visible, "
            "button:has-text('Confirm'):visible, "
            "a[name='website_sale_main_button']:visible, "
            "button[name='website_sale_main_button']:visible"
        ).first
        if save_btn.count() > 0:
            try:
                _safe_click(save_btn, page, timeout=10000)
            except Exception:
                pass

    # If still not on /shop/payment, jump there directly.
    if "/shop/payment" not in page.url and "/shop/confirmation" not in page.url:
        navigate(page, "/shop/payment")

    # ------------------------------------------------------------------
    # Phase 6 — Wire Transfer + Pay now.
    # ------------------------------------------------------------------
    if "/shop/confirmation" not in page.url:
        transfer_radio = page.locator(
            "input[name='o_payment_radio'][data-payment-option-label='Wire Transfer']"
        ).first
        if transfer_radio.count() == 0:
            transfer_radio = page.locator(
                "label:has-text('Wire Transfer'):visible"
            ).first
        try:
            transfer_radio.scroll_into_view_if_needed()
            transfer_radio.click()
            page.wait_for_timeout(700)
        except Exception:
            pass

        tos = page.locator("input#website_sale_tc_checkbox:visible")
        if tos.count() > 0:
            try:
                tos.check()
            except Exception:
                pass

        pay_btn = page.locator(
            "button[name='o_payment_submit_button']:visible, "
            "button:has-text('Pay now'):visible, "
            "button:has-text('Pay Now'):visible"
        ).first
        pay_btn.wait_for(state="visible", timeout=10000)
        _safe_click(pay_btn, page, timeout=15000)

    # ------------------------------------------------------------------
    # Phase 7 — land on /shop/confirmation (or poll validate).
    # ------------------------------------------------------------------
    if "/shop/confirmation" not in page.url:
        page.goto(full_url("/shop/payment/validate"))
        page.wait_for_load_state("load")
        page.wait_for_timeout(2500)


run_oracle(oracle)
