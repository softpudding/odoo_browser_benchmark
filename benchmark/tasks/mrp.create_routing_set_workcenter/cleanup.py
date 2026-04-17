"""Remove artifacts created by seed.py and by the agent."""


WORKCENTER_NAME = "Benchmark Assembly Station"
PRODUCT_NAME = "Benchmark Frame Assembly"
COMPONENT_NAMES = ["Bench Frame Tube", "Bench Frame Bolt"]


def cleanup(env):
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Workcenter = env["mrp.workcenter"]
    RoutingWC = env["mrp.routing.workcenter"]

    # Remove any routing operations pointing at the seeded BOM's product
    all_product_names = [PRODUCT_NAME] + COMPONENT_NAMES
    stale_prod = Product.search([("name", "in", all_product_names)])
    if stale_prod:
        boms = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        if boms:
            RoutingWC.search([("bom_id", "in", boms.ids)]).unlink()
        boms.unlink()
        stale_prod.mapped("product_tmpl_id").unlink()

    # Delete the workcenter (and any orphan routing entries referencing it)
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
