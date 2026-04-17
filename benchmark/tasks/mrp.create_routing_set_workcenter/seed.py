"""Seed a BOM with two components and no operations.

The agent must create a new work center AND add an operation on the BOM
that references the newly-created work center. We do NOT seed the
workcenter — that is the agent's job.

Also ensures the admin user has the `mrp.group_mrp_routings` group so the
Operations tab on BOM and the Work Centers configuration menu are visible.
"""


WORKCENTER_NAME = "Benchmark Assembly Station"
PRODUCT_NAME = "Benchmark Frame Assembly"
COMPONENT_NAMES = ["Bench Frame Tube", "Bench Frame Bolt"]


def setup(env):
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]
    Workcenter = env["mrp.workcenter"]

    # --- Enable the Work Orders feature so Operations tab is visible ---
    routings_group = env.ref("mrp.group_mrp_routings")
    admin = env.ref("base.user_admin")
    if routings_group not in admin.group_ids:
        admin.write({"group_ids": [(4, routings_group.id)]})

    # --- Cleanup prior runs ---
    stale_wc = Workcenter.search([("name", "=", WORKCENTER_NAME)])
    if stale_wc:
        # Archive first then unlink (workcenters may have linked data)
        try:
            stale_wc.action_archive()
        except Exception:
            pass
        try:
            stale_wc.unlink()
        except Exception:
            pass

    all_product_names = [PRODUCT_NAME] + COMPONENT_NAMES
    stale_prod = Product.search([("name", "in", all_product_names)])
    if stale_prod:
        stale_bom = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        stale_bom.unlink()
        stale_prod.mapped("product_tmpl_id").unlink()

    # --- Create finished product ---
    finished = Product.create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create components ---
    comp_a = Product.create({
        "name": COMPONENT_NAMES[0],
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_b = Product.create({
        "name": COMPONENT_NAMES[1],
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create BOM with no operations ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({"bom_id": bom.id, "product_id": comp_a.id, "product_qty": 4})
    BOMLine.create({"bom_id": bom.id, "product_id": comp_b.id, "product_qty": 16})
