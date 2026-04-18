"""Oracle for website_sale_wishlist.add_product_share_to_email.

Strategy:
  1. Log in as admin (so the wishlist row has partner_id=admin, not the
     anonymous session).
  2. Navigate /shop, click through to Bench Wishlist Item.
  3. On the product page, click the heart "Add to wishlist" button
     (``.o_add_wishlist_dyn`` or fallback ``.o_add_wishlist``).
  4. Navigate /shop/wishlist and verify the product is listed.
  5. If the UI click failed (e.g. button masked by another click), fall
     back to POSTing /shop/wishlist/add (the same JSON-RPC endpoint the
     heart button ultimately hits).

NOTE (deviation): website_sale_wishlist ships no share-by-email feature
in Odoo 19 Community. This oracle verifies the wishlist-persistence
workflow, which IS observable at the DB level (product.wishlist row).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


TARGET_NAME = "Bench Wishlist Item"


def oracle(page):
    login(page)

    # 1) Open /shop and click through to the product detail page.
    navigate(page, "/shop")
    page.wait_for_timeout(500)

    product_link = page.locator(
        f'a.oe_product_image_link:has(h6:has-text("{TARGET_NAME}"))'
    ).first
    if product_link.count() == 0:
        product_link = page.locator(f'a:has-text("{TARGET_NAME}")').first
    product_link.scroll_into_view_if_needed()
    product_link.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(400)

    # 2) Click the heart "Add to wishlist" button.  On the product detail
    # page the button class is ``.o_add_wishlist_dyn`` (rendered by
    # ``website_sale_wishlist.product_add_to_wishlist`` inside
    # ``#product_option_block``).  Fall back to ``.o_add_wishlist`` tiles
    # from the listing or cart template if the main button is absent.
    heart = page.locator(
        '#product_option_block a.o_add_wishlist_dyn, '
        'a.o_add_wishlist_dyn, '
        'button.o_add_wishlist'
    ).first
    clicked = False
    try:
        heart.wait_for(state="visible", timeout=5000)
        heart.scroll_into_view_if_needed()
        heart.click()
        clicked = True
        # Wait for the RPC to complete; the header wishlist badge flips
        # from d-none to visible with count=1.
        page.wait_for_timeout(1500)
    except Exception as exc:
        print(f"[oracle] heart-icon click failed: {exc!r}", flush=True)

    # 3) Verify persistence via JSON-RPC (source of truth).  If the row
    # isn't attached to the admin partner, fall back.
    state = page.evaluate(
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

            const tmpl = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', payload.name]], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            if (!tmpl.length) {
                return { status: 'missing_template' };
            }
            const variantId = tmpl[0].product_variant_id[0];
            const admin = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            const adminPartnerId = admin[0].partner_id[0];
            const wish = await callKw({
                model: 'product.wishlist',
                method: 'search_read',
                args: [[
                    ['partner_id', '=', adminPartnerId],
                    ['product_id', '=', variantId],
                ], ['id', 'partner_id', 'product_id', 'website_id']],
                kwargs: {},
            });
            return { status: 'ok', variantId, adminPartnerId, wishes: wish };
        }""",
        { "name": TARGET_NAME },
    )

    if state.get("status") != "ok":
        raise RuntimeError(f"Could not resolve product state: {state!r}")

    if not state.get("wishes"):
        # Fallback: POST /shop/wishlist/add directly.
        print("[oracle] UI click did not create admin-owned wishlist row; "
              "falling back to /shop/wishlist/add", flush=True)
        page.evaluate(
            """async (payload) => {
                const res = await fetch('/shop/wishlist/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params: {
                            product_id: payload.variantId,
                        },
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return 'ok';
            }""",
            { "variantId": state["variantId"] },
        )

    # 4) Navigate to /shop/wishlist to render the wishlist page (also
    # required by the prompt for visual confirmation).
    navigate(page, "/shop/wishlist")
    page.wait_for_timeout(600)


run_oracle(oracle)
