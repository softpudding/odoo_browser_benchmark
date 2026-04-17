"""Postcondition checks for website_sale.configure_variant_publish_product."""


def check(env):
    failures = []
    product = env["product.template"].search([("name", "=", "Field Pack Duffel")], limit=1)
    if not product:
        return ["Product Field Pack Duffel not found"]

    if not product.website_published:
        failures.append("Product is not published on the website")

    line = product.attribute_line_ids.filtered(
        lambda l: l.attribute_id.name == "Bench Size"
    )
    if len(line) != 1:
        failures.append(f"Expected one Bench Size attribute line, found {len(line)}")
        return failures

    value_names = set(line.product_template_value_ids.product_attribute_value_id.mapped("name"))
    if value_names != {"Carry-On", "Weekender"}:
        failures.append(f"Bench Size values are {sorted(value_names)!r}")
    return failures
