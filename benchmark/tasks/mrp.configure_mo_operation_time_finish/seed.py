"""Seed a confirmed MO with a single work order for the configure-and-finish task.

Medium: the agent must open the MO, switch to the Work Orders tab, set the
expected duration to 45 minutes, start the work order, and then mark it as
done. Tests tab navigation + inline field edit + sequential button clicks on
an x2many line.
"""


MO_NAME = "WH/MO/BENCH0001"
PRODUCT_NAME = "Bench Operation Product"
COMPONENT_NAME = "Bench Operation Component"
WORKCENTER_NAME = "Bench Assembly Station"
OPERATION_NAME = "Assembly Station"


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]
    Workcenter = env["mrp.workcenter"]
    RoutingWC = env["mrp.routing.workcenter"]

    # --- Enable Work Orders feature so Operations tab is visible ---
    routings_group = env.ref("mrp.group_mrp_routings")
    admin = env.ref("base.user_admin")
    if routings_group not in admin.group_ids:
        admin.write({"group_ids": [(4, routings_group.id)]})

    # --- Cleanup prior runs ---
    stale_mo = MO.search([("name", "=", MO_NAME)])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
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

    # --- Create workcenter ---
    workcenter = Workcenter.create({
        "name": WORKCENTER_NAME,
        "time_efficiency": 100.0,
    })

    # --- Create finished product + component ---
    finished = Product.create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    component = Product.create({
        "name": COMPONENT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create BOM with one operation ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": component.id,
        "product_qty": 1,
    })
    RoutingWC.create({
        "name": OPERATION_NAME,
        "bom_id": bom.id,
        "workcenter_id": workcenter.id,
        "time_cycle_manual": 10.0,
    })

    # --- Create MO ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 5,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    # Ensure workorder was generated
    assert mo.workorder_ids, "Expected work order was not created by action_confirm()"
