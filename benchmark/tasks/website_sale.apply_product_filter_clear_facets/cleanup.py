"""Cleanup for website_sale.apply_product_filter_clear_facets."""


PRODUCT_NAMES = [
    "Bench Gadget Mini",
    "Bench Gadget Plus",
    "Bench Gadget Pro",
    "Bench Widget Tiny",
    "Bench Widget Max",
]
CATEGORY_NAMES = ["Gadgets", "Widgets"]


def cleanup(env):
    # Drop any website draft cart that references our seeded products.
    product_ids = env["product.template"].with_context(active_test=False).search(
        [("name", "in", PRODUCT_NAMES)]
    ).ids
    if product_ids:
        env["sale.order"].with_context(active_test=False).search([
            ("website_id", "!=", False),
            ("state", "=", "draft"),
            ("order_line.product_template_id", "in", product_ids),
        ]).sudo().unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", PRODUCT_NAMES),
    ]).sudo().unlink()
    env["product.public.category"].with_context(active_test=False).search([
        ("name", "in", CATEGORY_NAMES),
    ]).sudo().unlink()
