"""Postcondition checks for website_sale.configure_optional_products_add_upsell_to_cart."""


def check(env):
    failures = []

    main_product = env["product.template"].search([("name", "=", "Docking Console")], limit=1)
    optional_product = env["product.template"].search([("name", "=", "Protective Sleeve")], limit=1)
    if not main_product or not optional_product:
        return ["Target products are missing"]

    if main_product.optional_product_ids != optional_product:
        failures.append(
            f"Optional products are {main_product.optional_product_ids.mapped('name')}, expected ['Protective Sleeve']"
        )
    if not optional_product.is_published:
        failures.append("Protective Sleeve is not published to the website")

    orders = env["sale.order"].search([("website_id", "!=", False)])
    matching_orders = orders.filtered(
        lambda order: {"Docking Console", "Protective Sleeve"}.issubset(
            set(order.order_line.mapped("product_template_id.name"))
        )
    )
    if not matching_orders:
        failures.append("No website cart/order contains both Docking Console and Protective Sleeve")

    return failures
