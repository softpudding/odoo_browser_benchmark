"""Seed for mrp.create_bom_confirm_mo.

Category 2 (MEDIUM): Create a BOM with 3 components, then create and confirm
a Manufacturing Order for 10 units. The agent must navigate BOM creation with
multiple component lines and then cross to MO creation.
"""


PRODUCT_NAME = "Bench Assembly Table"
COMPONENTS = [
    ("Table Leg", 4),
    ("Table Top Panel", 1),
    ("Assembly Screw Pack", 2),
]


def setup(env):
    # Cleanup prior runs
    old_mos = env["mrp.production"].search([
        ("product_id.name", "=", PRODUCT_NAME),
    ])
    for mo in old_mos:
        if mo.state == "confirmed":
            mo.action_cancel()
        if mo.state != "cancel":
            try:
                mo.action_cancel()
            except Exception:
                pass
    old_mos.unlink()

    old_boms = env["mrp.bom"].search([
        ("product_tmpl_id.name", "=", PRODUCT_NAME),
    ])
    old_boms.unlink()

    # Create the finished product
    finished = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not finished:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "is_storable": True,
            "list_price": 250.0,
            "standard_price": 120.0,
        })
        finished = tmpl.product_variant_id

    # Create component products
    for comp_name, _qty in COMPONENTS:
        comp = env["product.product"].search(
            [("name", "=", comp_name)], limit=1
        )
        if not comp:
            env["product.template"].create({
                "name": comp_name,
                "type": "consu",
                "is_storable": True,
                "list_price": 10.0,
                "standard_price": 5.0,
            })
