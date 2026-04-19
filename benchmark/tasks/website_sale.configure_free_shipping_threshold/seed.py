"""Seed for website_sale.configure_free_shipping_threshold.

Seeds a pre-existing delivery.carrier 'Bench Ship' with:
  - delivery_type='fixed'
  - fixed_price=15.0  (set via the linked service product's list_price, since
    delivery.carrier.fixed_price is stored=compute on product.list_price and
    writes back via its inverse)
  - free_over=False   (the field the agent must flip to True)
  - amount=1000       (Odoo default -- agent must overwrite with 100.00)

Also creates a dedicated service product 'Bench Ship Product' to back the
carrier (carrier.product_id is required). Cleans up prior runs idempotently.
"""


CARRIER_NAME = "Bench Ship"
PRODUCT_NAME = "Bench Ship Product"


def _cleanup(env):
    carriers = env["delivery.carrier"].with_context(active_test=False).search([
        ("name", "=", CARRIER_NAME),
    ])
    if carriers:
        carriers.sudo().write({"active": False})
        env["delivery.price.rule"].with_context(active_test=False).search([
            ("carrier_id", "in", carriers.ids),
        ]).sudo().unlink()
        carriers.sudo().unlink()

    env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "service",
        "sale_ok": False,
        "purchase_ok": False,
        "list_price": 15.0,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],
    })
    product = tmpl.product_variant_id

    carrier = env["delivery.carrier"].create({
        "name": CARRIER_NAME,
        "delivery_type": "fixed",
        "product_id": product.id,
        "fixed_price": 15.0,
        "free_over": False,
        # amount stays at Odoo default (1000) -- the agent must change it.
    })

    # Sanity: the compute-with-inverse on fixed_price writes product.list_price,
    # and reads back product.list_price. Force a known state.
    carrier.product_id.list_price = 15.0
    carrier.invalidate_recordset(["fixed_price"])
    if abs(carrier.fixed_price - 15.0) > 0.01:
        raise RuntimeError(
            f"Seed sanity: fixed_price={carrier.fixed_price}, expected 15.0"
        )
    if carrier.free_over:
        raise RuntimeError("Seed sanity: free_over must start False")
