"""Cleanup for website_sale.publish_product_shop."""


def cleanup(env):
    env["product.template"].with_context(active_test=False).search(
        [("name", "=", "Bench Gadget Pro")]
    ).unlink()
