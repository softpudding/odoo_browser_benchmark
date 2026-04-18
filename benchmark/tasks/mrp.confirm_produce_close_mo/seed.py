"""Seed a DRAFT manufacturing order for the confirm-produce-close task.

Category: deep_ui_interaction (HARD).

The agent must take a draft MO for 10 Office Desks, click Confirm
(draft -> confirmed), then click Produce All (confirmed -> done)
and accept the confirmation wizard. Capability tested: two-step
status-bar workflow plus wizard handling, without reducing the
production quantity or creating a backorder.
"""


MO_NAME = "WH/MO/BENCH-DESK-001"
FINISHED_NAME = "Office Desk"
COMPONENTS = [
    # (name, product_qty per 1 finished)
    ("Desk Top", 1.0),
    ("Desk Leg", 4.0),
    ("Cable Tray", 1.0),
]


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]

    # --- Cleanup prior runs ---
    stale_mo = MO.search([
        "|",
        ("name", "=", MO_NAME),
        ("name", "=like", MO_NAME + "-%"),
    ])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    stale_mo.unlink()

    cleanup_names = [FINISHED_NAME] + [n for n, _ in COMPONENTS]
    stale_prod = Product.search([("name", "in", cleanup_names)])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    # --- Create finished product ---
    finished = Product.create({
        "name": FINISHED_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create component products ---
    components = {}
    for name, _qty in COMPONENTS:
        components[name] = Product.create({
            "name": name,
            "type": "consu",
            "is_storable": True,
            "tracking": "none",
        })

    # --- Create BoM: 1 Office Desk = 1 Top + 4 Legs + 1 Cable Tray ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    for name, qty in COMPONENTS:
        BOMLine.create({
            "bom_id": bom.id,
            "product_id": components[name].id,
            "product_qty": qty,
        })

    # --- Create a DRAFT MO (NO action_confirm here — oracle must click it) ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 10,
        "bom_id": bom.id,
    })
    # Sanity check: stay in draft. If Odoo auto-confirmed, force back.
    if mo.state != "draft":
        raise RuntimeError(
            f"Seed invariant failed: MO is in state {mo.state}, expected 'draft'"
        )
