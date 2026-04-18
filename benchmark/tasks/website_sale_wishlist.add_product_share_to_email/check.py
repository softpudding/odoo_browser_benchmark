"""Postcondition checks for website_sale_wishlist.add_product_share_to_email.

Pass criteria:

  * ``Bench Wishlist Item`` still exists, active, published.
  * Exactly ONE ``product.wishlist`` row exists for the admin partner
    referencing the seeded product.
  * The row's website_id matches an installed website.
  * No other admin-owned wishlist rows exist (to ensure the agent did not
    scattershot-heart-click other random products).
"""


PRODUCT_NAME = "Bench Wishlist Item"


def check(env):
    failures = []

    tmpl = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if not tmpl:
        return [f"Product {PRODUCT_NAME!r} is missing"]

    if not tmpl.active:
        failures.append(f"Product {PRODUCT_NAME!r} was archived")
    if not tmpl.is_published:
        failures.append(f"Product {PRODUCT_NAME!r} was unpublished")

    admin = env.ref("base.user_admin")
    variants = tmpl.product_variant_ids

    # Look for admin-owned wishlist rows for any variant of the product.
    wishes = env["product.wishlist"].with_context(active_test=False).sudo().search([
        ("partner_id", "=", admin.partner_id.id),
        ("product_id", "in", variants.ids),
    ])

    if not wishes:
        # Double-check whether the row landed as partner_id=False (public
        # session) — useful signal for diagnostics.
        session_wishes = env["product.wishlist"].with_context(
            active_test=False,
        ).sudo().search([
            ("partner_id", "=", False),
            ("product_id", "in", variants.ids),
        ])
        if session_wishes:
            failures.append(
                f"product.wishlist row exists for {PRODUCT_NAME!r} but partner_id "
                f"is False (public-session ownership); expected admin partner"
            )
        else:
            failures.append(
                f"No product.wishlist row for {PRODUCT_NAME!r} attached to the "
                f"admin partner"
            )
        return failures

    if len(wishes) != 1:
        failures.append(
            f"Expected exactly 1 product.wishlist row for {PRODUCT_NAME!r} + "
            f"admin partner, got {len(wishes)}"
        )

    wish = wishes[0]
    if not wish.active:
        failures.append("product.wishlist row is archived (active=False)")
    if not wish.website_id:
        failures.append("product.wishlist.website_id is unset")

    # No unrelated admin wishlist rows (e.g. agent hearted other products).
    extra = env["product.wishlist"].with_context(active_test=False).sudo().search([
        ("partner_id", "=", admin.partner_id.id),
        ("product_id", "not in", variants.ids),
    ])
    if extra:
        extra_names = sorted({w.product_id.display_name for w in extra})
        failures.append(
            f"Unexpected extra admin wishlist rows: {extra_names}"
        )

    return failures
