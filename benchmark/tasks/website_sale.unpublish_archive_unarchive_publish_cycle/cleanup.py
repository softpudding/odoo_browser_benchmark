"""Cleanup for website_sale.unpublish_archive_unarchive_publish_cycle."""


PRODUCT_NAME = "Bench Cycle Gadget"


def cleanup(env):
    Product = env["product.template"].with_context(active_test=False)
    Product.search([("name", "=", PRODUCT_NAME)]).unlink()
