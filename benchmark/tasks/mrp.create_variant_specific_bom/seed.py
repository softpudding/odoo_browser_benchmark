"""Seed for mrp.create_variant_specific_bom.

Category: deep_ui_interaction (HARD).

Seeds:
  * A product template 'Bench T-Shirt' with attribute 'Bench Color'
    (values 'Red' and 'Blue') that produces exactly two variants
    'Bench T-Shirt (Red)' and 'Bench T-Shirt (Blue)'.
  * A 'Bench Fabric' component product.
  * NO pre-existing BoM — the agent must create one that applies
    ONLY to the Red variant via the 'Apply on Variants' field.

The agent must:
  1. Create a mrp.bom for product_tmpl_id = Bench T-Shirt.
  2. Set 'Apply on Variants' to the Red variant (product_id =
     Bench T-Shirt (Red) variant id), NOT leave it blank.
  3. Add one Bench Fabric line at qty 1.
  4. Save.
"""

TEMPLATE_NAME = "Bench T-Shirt"
ATTRIBUTE_NAME = "Bench Color"
VALUE_NAMES = ["Red", "Blue"]
COMPONENT_NAME = "Bench Fabric"


def setup(env):
    Template = env["product.template"]
    Product = env["product.product"]
    Attribute = env["product.attribute"]
    AttributeValue = env["product.attribute.value"]
    BOM = env["mrp.bom"]

    # --- Cleanup prior runs --------------------------------------------
    stale_templates = Template.with_context(active_test=False).search([
        ("name", "in", [TEMPLATE_NAME, COMPONENT_NAME]),
    ])
    if stale_templates:
        stale_boms = BOM.search([
            ("product_tmpl_id", "in", stale_templates.ids),
        ])
        try:
            stale_boms.unlink()
        except Exception:
            pass
        try:
            stale_templates.unlink()
        except Exception:
            pass

    # Also cleanup any stale attribute with the same name so we get
    # a clean set of 2 variants.
    stale_attr = Attribute.search([("name", "=", ATTRIBUTE_NAME)])
    if stale_attr:
        try:
            stale_attr.unlink()
        except Exception:
            pass

    # --- Attribute + values --------------------------------------------
    attribute = Attribute.create({
        "name": ATTRIBUTE_NAME,
        "create_variant": "always",
        "display_type": "radio",
    })
    value_recs = AttributeValue
    for name in VALUE_NAMES:
        value_recs |= AttributeValue.create({
            "name": name,
            "attribute_id": attribute.id,
        })

    # --- Component product ---------------------------------------------
    Product.create({
        "name": COMPONENT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Product template with 2 variants ------------------------------
    template = Template.create({
        "name": TEMPLATE_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "attribute_line_ids": [
            (0, 0, {
                "attribute_id": attribute.id,
                "value_ids": [(6, 0, value_recs.ids)],
            }),
        ],
    })

    # Verify we now have exactly 2 variants.
    if len(template.product_variant_ids) != 2:
        raise ValueError(
            f"Expected 2 variants for {TEMPLATE_NAME}, got "
            f"{len(template.product_variant_ids)}"
        )
