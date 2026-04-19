"""Cleanup for product.configure_variant_attribute_two_values."""


PRODUCT_NAME = "Bench Variant Shirt"
ATTRIBUTE_NAME = "Size"


def cleanup(env):
    product = env["product.template"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if product:
        product.write({"attribute_line_ids": [(5, 0, 0)]})

    attribute = env["product.attribute"].search(
        [("name", "=", ATTRIBUTE_NAME)], limit=1
    )
    if attribute:
        lines = env["product.template.attribute.line"].search(
            [("attribute_id", "=", attribute.id)]
        )
        if lines:
            lines.unlink()
        attribute.value_ids.unlink()
        attribute.unlink()
