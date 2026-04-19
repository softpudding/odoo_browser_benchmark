"""Postcondition checks for mrp.create_variant_specific_bom.

Validates:
  * Exactly one mrp.bom exists for the Bench T-Shirt product template.
  * That BoM's product_id is set to the Bench T-Shirt (Red) variant
    (NOT False, which would mean 'applies to all variants').
  * BoM type='normal' and product_qty=1.0.
  * Exactly one bom_line exists for Bench Fabric at qty 1.
  * The Bench T-Shirt template still has its two variants.
"""

TEMPLATE_NAME = "Bench T-Shirt"
ATTRIBUTE_NAME = "Bench Color"
RED_VALUE = "Red"
BLUE_VALUE = "Blue"
COMPONENT_NAME = "Bench Fabric"


def check(env):
    failures = []

    template = env["product.template"].search(
        [("name", "=", TEMPLATE_NAME)], limit=1
    )
    if not template:
        return [f"Template '{TEMPLATE_NAME}' missing after run"]

    if len(template.product_variant_ids) != 2:
        failures.append(
            f"Template '{TEMPLATE_NAME}' has "
            f"{len(template.product_variant_ids)} variants, expected 2"
        )

    # Resolve Red/Blue variants.
    red_variant = env["product.product"].search([
        ("product_tmpl_id", "=", template.id),
        ("product_template_variant_value_ids.name", "=", RED_VALUE),
    ], limit=1)
    blue_variant = env["product.product"].search([
        ("product_tmpl_id", "=", template.id),
        ("product_template_variant_value_ids.name", "=", BLUE_VALUE),
    ], limit=1)
    if not red_variant:
        failures.append(f"Red variant of '{TEMPLATE_NAME}' missing")
    if not blue_variant:
        failures.append(f"Blue variant of '{TEMPLATE_NAME}' missing")

    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "=", template.id),
    ])
    if not boms:
        return failures + [
            f"No mrp.bom for '{TEMPLATE_NAME}' — the task requires "
            f"creating one for the Red variant"
        ]
    if len(boms) > 1:
        failures.append(
            f"Expected exactly 1 BoM for '{TEMPLATE_NAME}', found "
            f"{len(boms)}"
        )

    bom = boms[0]

    if not bom.product_id:
        failures.append(
            f"BoM for '{TEMPLATE_NAME}' has no Apply-on-Variants set "
            f"(product_id is False). The BoM must apply to the Red "
            f"variant only, not to every variant."
        )
    elif red_variant and bom.product_id.id != red_variant.id:
        failures.append(
            f"BoM product_id is '{bom.product_id.display_name}', "
            f"expected '{red_variant.display_name}' (Red variant)"
        )

    if bom.type != "normal":
        failures.append(
            f"BoM type is '{bom.type}', expected 'normal' (Manufacture this Product)"
        )

    if abs((bom.product_qty or 0.0) - 1.0) > 1e-6:
        failures.append(
            f"BoM product_qty is {bom.product_qty}, expected 1.0"
        )

    if len(bom.bom_line_ids) != 1:
        failures.append(
            f"BoM has {len(bom.bom_line_ids)} component lines, expected exactly 1"
        )
    else:
        line = bom.bom_line_ids[0]
        if not line.product_id or line.product_id.name != COMPONENT_NAME:
            failures.append(
                f"BoM component is '{line.product_id.display_name}', "
                f"expected '{COMPONENT_NAME}'"
            )
        if abs((line.product_qty or 0.0) - 1.0) > 1e-6:
            failures.append(
                f"BoM component qty is {line.product_qty}, expected 1.0"
            )

    return failures
