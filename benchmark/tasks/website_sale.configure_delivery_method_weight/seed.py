"""Seed for website_sale.configure_delivery_method_weight.

No pre-existing delivery.carrier named 'Bench Weight Shipping' — the agent
must create it from scratch on the Delivery Methods list. We do seed a
dedicated service product ('Bench Delivery Product') that the agent can
select as the carrier's Delivery Product. We leave Odoo's demo carriers
untouched so the agent has to explicitly click New and fill fields.

Cleans up any prior 'Bench Weight Shipping' carrier + its pricing rules
from earlier runs.
"""


CARRIER_NAME = "Bench Weight Shipping"
DELIVERY_PRODUCT_NAME = "Bench Delivery Product"


def _cleanup(env):
    carriers = env["delivery.carrier"].with_context(active_test=False).search([
        ("name", "=", CARRIER_NAME),
    ])
    if carriers:
        # Unpublish first so related website bindings don't block unlink
        carriers.sudo().write({"active": False})
        # Remove price rules tied to them (ondelete cascade should handle it,
        # but be defensive for older snapshots).
        env["delivery.price.rule"].with_context(active_test=False).search([
            ("carrier_id", "in", carriers.ids),
        ]).sudo().unlink()
        carriers.sudo().unlink()

    env["product.template"].with_context(active_test=False).search([
        ("name", "=", DELIVERY_PRODUCT_NAME),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    # Seed a dedicated service product so the carrier form's Delivery Product
    # field has a clean, unambiguous match. Odoo's own default is also fine;
    # we just want *something* deterministic the agent can pick.
    env["product.template"].create({
        "name": DELIVERY_PRODUCT_NAME,
        "type": "service",
        "sale_ok": False,
        "purchase_ok": False,
        "list_price": 0.0,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],
    })

    # Sanity: make sure the carrier doesn't already exist (post-cleanup).
    existing = env["delivery.carrier"].with_context(active_test=False).search(
        [("name", "=", CARRIER_NAME)]
    )
    if existing:
        raise RuntimeError(
            f"Seed sanity failed: '{CARRIER_NAME}' still exists after cleanup"
        )
