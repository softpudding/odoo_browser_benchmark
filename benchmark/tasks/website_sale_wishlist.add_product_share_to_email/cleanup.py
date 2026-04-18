"""Cleanup for website_sale_wishlist.add_product_share_to_email."""


PRODUCT_NAME = "Bench Wishlist Item"


def cleanup(env):
    admin = env.ref("base.user_admin")

    tmpl = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if tmpl:
        variants = tmpl.product_variant_ids
        if variants:
            env["product.wishlist"].with_context(active_test=False).sudo().search(
                [("product_id", "in", variants.ids)]
            ).unlink()
        tmpl.sudo().unlink()

    # Blanket clear admin-owned wishlist rows from any prior run.
    env["product.wishlist"].with_context(active_test=False).sudo().search(
        [("partner_id", "=", admin.partner_id.id)]
    ).unlink()
