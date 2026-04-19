"""Cleanup for mrp.create_variant_specific_bom."""

TEMPLATE_NAME = "Bench T-Shirt"
ATTRIBUTE_NAME = "Bench Color"
COMPONENT_NAME = "Bench Fabric"


def cleanup(env):
    Template = env["product.template"]
    BOM = env["mrp.bom"]
    Attribute = env["product.attribute"]

    templates = Template.with_context(active_test=False).search([
        ("name", "in", [TEMPLATE_NAME, COMPONENT_NAME]),
    ])

    if templates:
        boms = BOM.search([("product_tmpl_id", "in", templates.ids)])
        try:
            boms.unlink()
        except Exception:
            pass
        try:
            templates.unlink()
        except Exception:
            pass

    attrs = Attribute.search([("name", "=", ATTRIBUTE_NAME)])
    if attrs:
        try:
            attrs.unlink()
        except Exception:
            pass
