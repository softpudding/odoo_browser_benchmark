"""Postcondition checks for website_sale.add_product_review_publish.

Pass criteria:
  * The seeded product still exists, still published, name unchanged.
  * Exactly ONE rating.rating row on the product with rating=4.0,
    res_model='product.template', res_id=<product>, consumed=True,
    linked to a mail.message whose body contains 'Great product'.
  * The linked mail.message is a public comment (message_type='comment',
    subtype_id = mail.mt_comment).

The check is resilient to HTML wrapping around the review body: both
`<p>Great product</p>` and `Great product` are accepted. It does NOT
gate on partner_id (the active session may be admin or a portal user).
"""


PRODUCT_NAME = "Bench Review Item"
REVIEW_BODY_MARKER = "Great product"
EXPECTED_RATING = 4.0


def check(env):
    failures = []

    products = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if len(products) != 1:
        return [
            f"Expected exactly 1 product named {PRODUCT_NAME!r}, "
            f"found {len(products)}"
        ]

    product = products[0]
    if not product.is_published:
        failures.append(
            f"Product {PRODUCT_NAME!r} is no longer published "
            "(must stay published)"
        )
    if not product.active:
        failures.append(
            f"Product {PRODUCT_NAME!r} was archived (must stay active)"
        )
    if abs(product.list_price - 49.0) > 0.0001:
        failures.append(
            f"Product list_price changed to {product.list_price}; expected 49.0"
        )

    # Verify a rating row on the product template.
    Rating = env["rating.rating"].with_context(active_test=False).sudo()
    ratings = Rating.search([
        ("res_model", "=", "product.template"),
        ("res_id", "=", product.id),
    ])
    if len(ratings) != 1:
        failures.append(
            f"Expected exactly 1 rating.rating row on the product, "
            f"got {len(ratings)}"
        )
        return failures

    rating = ratings[0]
    if abs(rating.rating - EXPECTED_RATING) > 0.0001:
        failures.append(
            f"rating.rating.rating is {rating.rating!r}, "
            f"expected {EXPECTED_RATING}"
        )
    if not rating.consumed:
        failures.append(
            "rating.rating.consumed is False; a posted review should be "
            "consumed=True"
        )
    if not rating.message_id:
        failures.append(
            "rating.rating.message_id is not set; the rating row must "
            "be linked to the mail.message comment"
        )

    # Verify the linked mail.message has the expected body + flags.
    msg = rating.message_id
    if msg:
        body_text = (msg.body or "").strip()
        if REVIEW_BODY_MARKER not in body_text:
            failures.append(
                f"Linked mail.message body does not contain "
                f"{REVIEW_BODY_MARKER!r}; got body={body_text[:160]!r}"
            )
        if msg.message_type != "comment":
            failures.append(
                f"mail.message.message_type is {msg.message_type!r}, "
                "expected 'comment'"
            )
        mt_comment = env.ref("mail.mt_comment")
        if msg.subtype_id != mt_comment:
            failures.append(
                f"mail.message.subtype_id is {msg.subtype_id.name!r}, "
                f"expected 'mail.mt_comment'"
            )
        if msg.model != "product.template":
            failures.append(
                f"mail.message.model is {msg.model!r}, "
                "expected 'product.template'"
            )
        if msg.res_id != product.id:
            failures.append(
                f"mail.message.res_id is {msg.res_id}, "
                f"expected {product.id}"
            )

    return failures
