"""Cleanup for mrp.unbuild_finished_goods_to_recover_components."""

MO_NAME = "WH/MO/UNBLD-001"
FINISHED = "Benchmark Recoverable Widget"
COMP_A = "Recovery Component A"
COMP_B = "Recovery Component B"


def cleanup(env):
    unbuilds = env["mrp.unbuild"].search([("mo_id.name", "=", MO_NAME)])
    unbuilds.unlink()

    mos = env["mrp.production"].search([("name", "=", MO_NAME)])
    for mo in mos:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    mos.unlink()

    products = env["product.product"].search([
        ("name", "in", [FINISHED, COMP_A, COMP_B]),
    ])
    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids),
    ])
    boms.unlink()
    products.mapped("product_tmpl_id").unlink()
