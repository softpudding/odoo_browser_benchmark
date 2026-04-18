"""Clean up artifacts created by seed.py and by the agent."""


MO_NAME = "WH/MO/BENCH0001"
PRODUCT_NAME = "Bench Operation Product"
COMPONENT_NAME = "Bench Operation Component"
WORKCENTER_NAME = "Bench Assembly Station"


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Workcenter = env["mrp.workcenter"]
    RoutingWC = env["mrp.routing.workcenter"]
    Workorder = env["mrp.workorder"]

    stale_mo = MO.search([("name", "=", MO_NAME)])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    # Delete any dangling workorders (should cascade, but be safe)
    if stale_mo:
        Workorder.search([("production_id", "in", stale_mo.ids)]).unlink()
    stale_mo.unlink()

    stale_prod = Product.search([
        ("name", "in", [PRODUCT_NAME, COMPONENT_NAME]),
    ])
    if stale_prod:
        boms = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        if boms:
            RoutingWC.search([("bom_id", "in", boms.ids)]).unlink()
        boms.unlink()
        stale_prod.mapped("product_tmpl_id").unlink()

    stale_wc = Workcenter.search([("name", "=", WORKCENTER_NAME)])
    if stale_wc:
        RoutingWC.search([("workcenter_id", "in", stale_wc.ids)]).unlink()
        try:
            stale_wc.action_archive()
        except Exception:
            pass
        try:
            stale_wc.unlink()
        except Exception:
            pass
