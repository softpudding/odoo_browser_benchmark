"""Oracle for website_sale.add_product_review_publish.

Strategy (JSON-RPC bypass of the frontend rating composer):

  1. Login as admin (session cookie used by subsequent fetch calls).
  2. Navigate /shop to warm the frontend (not strictly required for
     the JSON-RPC but gives the session a website context).
  3. Find the seeded 'Bench Review Item' product.template id.
  4. Call `product.template.message_post(body='<p>Great product</p>',
     rating_value=4, message_type='comment',
     subtype_xmlid='mail.mt_comment')` via /web/dataset/call_kw. The
     rating.mail_thread override intercepts `rating_value`, creates a
     matching rating.rating row (rating=4.0, res_model='product.template',
     res_id=<product>, partner_id=admin.partner_id, consumed=True), and
     links it to the created mail.message via _message_post_after_hook.

This mirrors exactly what the browser-use path does when a logged-in
user clicks `Add Review` → selects 4 stars → types 'Great product' →
clicks `Post review`: the portal composer POSTs to /mail/message/post
with post_data.rating_value=4 and body='<p>Great product</p>', which
hits the same server-side rating.mail_thread override.
"""

import json

from benchmark.oracle_helpers import (
    full_url,
    login,
    run_oracle,
)


PRODUCT_NAME = "Bench Review Item"
REVIEW_BODY = "Great product"


def _call_kw(page, model, method, args, kwargs=None):
    kwargs = kwargs or {}
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs,
        },
    }
    result = page.evaluate(
        """async (payload) => {
            const resp = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'same-origin',
                body: JSON.stringify(payload),
            });
            return resp.json();
        }""",
        payload,
    )
    if isinstance(result, dict) and result.get("error"):
        raise RuntimeError(
            f"call_kw {model}.{method} error: "
            f"{json.dumps(result['error'])[:600]}"
        )
    return result.get("result") if isinstance(result, dict) else result


def oracle(page):
    login(page)

    # Warm the /shop front-end so the admin session has a website
    # context (not strictly required — message_post does not depend on
    # website_id — but mirrors the browser-use flow).
    page.goto(full_url("/shop"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(500)

    # --- Resolve product ------------------------------------------------
    products = _call_kw(
        page, "product.template", "search_read",
        [[("name", "=", PRODUCT_NAME)], ["id"]],
        {"limit": 1},
    )
    if not products:
        raise RuntimeError(f"Seeded product not found: {PRODUCT_NAME}")
    product_id = products[0]["id"]

    # --- Post the review via message_post with rating_value=4 -----------
    # The rating.mail_thread override intercepts `rating_value`, creates
    # a rating.rating row with rating=4.0 and partner_id=current user,
    # and links it to the created mail.message via
    # _message_post_after_hook.
    message_id = _call_kw(
        page, "product.template", "message_post",
        [[product_id]],
        {
            "body": f"<p>{REVIEW_BODY}</p>",
            "rating_value": 4,
            "message_type": "comment",
            "subtype_xmlid": "mail.mt_comment",
        },
    )
    if not message_id:
        raise RuntimeError("message_post returned no id")

    # --- Sanity: the rating.rating row exists and is linked -------------
    ratings = _call_kw(
        page, "rating.rating", "search_read",
        [[
            ("res_model", "=", "product.template"),
            ("res_id", "=", product_id),
        ], ["id", "rating", "consumed", "message_id", "partner_id"]],
        {},
    )
    if len(ratings) != 1:
        raise RuntimeError(
            f"Expected exactly 1 rating.rating row, got "
            f"{len(ratings)}: {ratings!r}"
        )
    rating = ratings[0]
    if rating.get("rating") != 4.0:
        raise RuntimeError(
            f"rating.rating.rating is {rating.get('rating')!r}, expected 4.0"
        )
    if not rating.get("consumed"):
        raise RuntimeError("rating.rating.consumed is False; expected True")
    if not rating.get("message_id"):
        raise RuntimeError(
            "rating.rating.message_id is not set; "
            "_message_post_after_hook failed to link"
        )

    print(
        "Oracle: posted review on product id=%s (rating_id=%s, "
        "message_id=%s)" % (product_id, rating["id"], message_id)
    )


run_oracle(oracle)
