"""Cleanup for lunch.create_vendor_product_order_for_today."""

VENDOR_NAME = "Bench Cafe"
PARTNER_NAME = "Bench Cafe Partner"
PRODUCT_NAME = "Veggie Wrap"


def cleanup(env):
    # Orders first (they reference product).
    Order = env["lunch.order"].with_context(active_test=False)
    Order.search([("product_id.name", "=", PRODUCT_NAME)]).unlink()

    # Products before suppliers.
    env["lunch.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    ).unlink()

    env["lunch.supplier"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)]
    ).unlink()

    # Partner last: the vendor form's related ``name`` is readonly=False
    # so picking the partner then typing a new name renames the partner.
    # Try cleanup under both the seeded partner name and the final
    # vendor name.
    for pname in (PARTNER_NAME, VENDOR_NAME):
        partner = env["res.partner"].search([("name", "=", pname)], limit=1)
        if partner and not partner.child_ids:
            try:
                partner.unlink()
            except Exception:
                pass
