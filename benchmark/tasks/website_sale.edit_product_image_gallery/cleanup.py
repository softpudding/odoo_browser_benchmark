"""Cleanup for website_sale.edit_product_image_gallery."""


def cleanup(env):
    products = env["product.template"].with_context(active_test=False).search(
        [("name", "=", "Bench Gallery Mug")]
    )
    if products:
        # product.image has ondelete='cascade' on product_tmpl_id, so deleting
        # the template will also delete its images, but be explicit for safety.
        env["product.image"].with_context(active_test=False).search(
            [("product_tmpl_id", "in", products.ids)]
        ).unlink()
        products.unlink()
