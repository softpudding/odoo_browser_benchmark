"""Seed for website_sale.add_product_review_publish.

Category: deep_ui_interaction (MEDIUM).

Creates:
  * A published product.template `Bench Review Item` (is_published=True,
    sale_ok=True, list_price=49.0).
  * Activates the website_sale `product_comment` ir.ui.view
    (active=False by default) so the shop page renders a
    `Customer Reviews` section with the rating popup composer. Without
    this activation the rating UI never appears on the frontend product
    page and the task is unsolvable via the browser.
  * Leaves admin as the session user so the agent can log in with the
    default benchmark credentials.

Agent posts a 4-star review with body `Great product` on the product's
shop page, which triggers the `/mail/message/post` JSON-RPC with
`post_data.rating_value = 4` and creates:

  * a `mail.message` with message_type='comment', subtype_id=mt_comment,
    model='product.template', res_id=<product id>, author_id=<admin partner>,
    body containing `Great product`, plus a non-null rating_id.
  * a `rating.rating` row with rating=4.0, res_model='product.template',
    res_id=<product id>, partner_id=<admin partner>, consumed=True,
    message_id=<mail.message id>.
"""


PRODUCT_NAME = "Bench Review Item"
PRODUCT_PRICE = 49.0
COMMENT_VIEW_KEY = "website_sale.product_comment"


def _cleanup(env):
    # Drop any prior rating.rating rows for the product (cascade via
    # res_model/res_id) and any mail.message rows that were posted on
    # a prior product. We search by name so a re-seed resets state
    # fully (the test assumes exactly zero existing reviews at seed
    # time).
    prior = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if prior:
        env["rating.rating"].sudo().search([
            ("res_model", "=", "product.template"),
            ("res_id", "in", prior.ids),
        ]).unlink()
        env["mail.message"].sudo().search([
            ("model", "=", "product.template"),
            ("res_id", "in", prior.ids),
        ]).unlink()
        prior.unlink()


def setup(env):
    _cleanup(env)

    if "rating.rating" not in env:
        raise RuntimeError(
            "rating.rating model missing — 'rating' / 'portal_rating' must "
            "be installed (they auto-install with website_sale)."
        )

    # Activate the Customer Reviews section view on the product page.
    # The `website_sale.product_comment` view is delivered with
    # active=False and must be flipped to True to render the review
    # UI. We search by key with active_test=False to catch the view
    # even if it was toggled off from a prior run.
    comment_views = env["ir.ui.view"].with_context(active_test=False).search(
        [("key", "=", COMMENT_VIEW_KEY)]
    )
    if not comment_views:
        raise RuntimeError(
            f"Required view {COMMENT_VIEW_KEY!r} is missing — website_sale "
            "is not installed."
        )
    comment_views.write({"active": True})

    # Create the product. is_published=True puts it in /shop without
    # any extra publish step.
    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": PRODUCT_PRICE,
        "is_published": True,
        "website_published": True,
        "description_ecommerce": (
            "<p>A sturdy benchmark item used to exercise the product "
            "review + rating flow on the eCommerce shop.</p>"
        ),
        "taxes_id": [(5, 0, 0)],
    })

    # Sanity: at least one website record (else /shop 404s).
    if not env["website"].search([], limit=1):
        raise RuntimeError("No website record present in DB; cannot run /shop test")
