"""Postcondition checks for product.configure_variant_attribute_two_values.

Verifies:
  * product.attribute 'Size' exists with exactly Small/Medium/Large values.
  * product.template 'Bench Variant Shirt' has exactly one
    product.template.attribute.line whose attribute is 'Size' and whose
    value_ids are exactly {Small, Medium, Large}.
  * The onchange / save auto-generated exactly 3 product.product variants
    for that template.
"""


PRODUCT_NAME = "Bench Variant Shirt"
ATTRIBUTE_NAME = "Size"
EXPECTED_VALUES = {"Small", "Medium", "Large"}


def check(env):
    failures = []

    product = env["product.template"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product {PRODUCT_NAME!r} not found"]

    attribute = env["product.attribute"].search(
        [("name", "=", ATTRIBUTE_NAME)], limit=1
    )
    if not attribute:
        failures.append(f"Attribute {ATTRIBUTE_NAME!r} was not created")
        return failures

    # Attribute must expose at least the three required values (agent may
    # have added extras by mistake — we flag that separately).
    attribute_value_names = set(attribute.value_ids.mapped("name"))
    missing = EXPECTED_VALUES - attribute_value_names
    if missing:
        failures.append(
            f"Attribute 'Size' is missing values {sorted(missing)!r}; "
            f"has {sorted(attribute_value_names)!r}"
        )
    extra_attr_values = attribute_value_names - EXPECTED_VALUES
    if extra_attr_values:
        failures.append(
            f"Attribute 'Size' has unexpected extra values "
            f"{sorted(extra_attr_values)!r}"
        )

    # Product attribute lines: exactly one Size line.
    size_lines = product.attribute_line_ids.filtered(
        lambda l: l.attribute_id.id == attribute.id
    )
    other_lines = product.attribute_line_ids - size_lines
    if other_lines:
        failures.append(
            "Product has extra attribute lines: "
            f"{other_lines.attribute_id.mapped('name')!r}"
        )
    if len(size_lines) != 1:
        failures.append(
            f"Expected 1 Size attribute line, found {len(size_lines)}"
        )
        return failures

    line_value_names = set(size_lines.value_ids.mapped("name"))
    if line_value_names != EXPECTED_VALUES:
        failures.append(
            f"Size line values are {sorted(line_value_names)!r}, "
            f"expected {sorted(EXPECTED_VALUES)!r}"
        )

    # Variants: product.template should have spawned exactly 3 product.product.
    variants = product.product_variant_ids
    if len(variants) != 3:
        failures.append(
            f"Expected 3 variants auto-generated, found {len(variants)}"
        )
    else:
        ptav_names = set()
        for variant in variants:
            vals = variant.product_template_variant_value_ids.mapped(
                "product_attribute_value_id.name"
            )
            if len(vals) != 1:
                failures.append(
                    f"Variant {variant.display_name!r} has unexpected "
                    f"attribute value combo {vals!r}"
                )
            else:
                ptav_names.add(vals[0])
        if ptav_names != EXPECTED_VALUES:
            failures.append(
                f"Variant attribute values set is {sorted(ptav_names)!r}, "
                f"expected {sorted(EXPECTED_VALUES)!r}"
            )

    return failures
