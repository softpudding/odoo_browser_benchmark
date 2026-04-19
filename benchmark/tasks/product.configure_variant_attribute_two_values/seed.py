"""Seed data for product.configure_variant_attribute_two_values.

Creates a clean `Bench Variant Shirt` product.template with no attribute
lines. The task requires the agent to add a `Size` attribute (creating
it inline if absent) with three values (`Small`, `Medium`, `Large`) and
save — saving triggers `_create_variants` and generates three
product.product variants.

Prior-run cleanup: drops the Size attribute and any Bench Variant Shirt
attribute lines so the agent must add them via the UI.
"""

PRODUCT_NAME = "Bench Variant Shirt"
ATTRIBUTE_NAME = "Size"
VALUE_NAMES = ["Small", "Medium", "Large"]


def _cleanup_prior(env):
    """Remove Size attribute + Bench Variant Shirt variants from any
    prior run so the seed is deterministic.

    Order matters: the attribute's product.template.attribute.line rows
    on our template must be dropped before we can unlink the attribute
    itself (or we orphan template value rows)."""
    product = env["product.template"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if product:
        # Drop every attribute line on the template so downstream variants
        # auto-collapse back to the single base variant.
        product.write({"attribute_line_ids": [(5, 0, 0)]})

    attribute = env["product.attribute"].search(
        [("name", "=", ATTRIBUTE_NAME)], limit=1
    )
    if attribute:
        # Remove any product.template.attribute.line rows referencing
        # this attribute on OTHER templates before unlinking the values.
        lines = env["product.template.attribute.line"].search(
            [("attribute_id", "=", attribute.id)]
        )
        if lines:
            lines.unlink()
        # Now safe to drop values + attribute.
        attribute.value_ids.unlink()
        attribute.unlink()


def setup(env):
    _cleanup_prior(env)

    product = env["product.template"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        product = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 39.0,
            "sale_ok": True,
        })
    else:
        product.write({
            "type": "consu",
            "list_price": 39.0,
            "sale_ok": True,
            "attribute_line_ids": [(5, 0, 0)],
            "active": True,
        })

    # Sanity: product has exactly 1 variant (the base) and no attribute lines.
    assert not product.attribute_line_ids, (
        f"seed: {PRODUCT_NAME} still has attribute lines"
    )
    assert len(product.product_variant_ids) == 1, (
        f"seed: expected 1 base variant, got {len(product.product_variant_ids)}"
    )

    env.cr.commit()
