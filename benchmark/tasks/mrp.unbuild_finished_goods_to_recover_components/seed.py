"""Seed for mrp.unbuild_finished_goods_to_recover_components.

Creates a completed MO 'WH/MO/UNBLD-001' for Benchmark Recoverable
Widget (3 units produced). Task: create and validate an unbuild order
for that MO.
"""

MO_NAME = "WH/MO/UNBLD-001"
FINISHED = "Benchmark Recoverable Widget"
COMP_A = "Recovery Component A"
COMP_B = "Recovery Component B"


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Unbuild = env["mrp.unbuild"]

    # Cleanup prior runs.
    stale_unbuild = Unbuild.search([("mo_id.name", "=", MO_NAME)])
    for u in stale_unbuild:
        if u.state == "done":
            # Cannot easily revert an unbuild; unlink will fail. Leave it.
            pass
    stale_unbuild.unlink()

    stale_mo = MO.search([("name", "=", MO_NAME)])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    stale_mo.unlink()

    stale_prod = Product.search([("name", "in", [FINISHED, COMP_A, COMP_B])])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_a = Product.create({
        "name": COMP_A,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_b = Product.create({
        "name": COMP_B,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": comp_a.id, "product_qty": 2}),
            (0, 0, {"product_id": comp_b.id, "product_qty": 1}),
        ],
    })

    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 3,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    # Mark as produced by setting qty_producing = 3 and calling button_mark_done.
    mo.qty_producing = 3
    try:
        mo.button_mark_done()
    except Exception:
        # Some Odoo variants require action_assign + action_produce instead;
        # fall back to that if needed.
        try:
            mo.action_assign()
            mo.button_mark_done()
        except Exception:
            pass
