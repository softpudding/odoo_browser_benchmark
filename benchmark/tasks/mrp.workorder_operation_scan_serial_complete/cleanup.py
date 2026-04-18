"""Cleanup for mrp.workorder_operation_scan_serial_complete."""


MO_NAME = "MO-BENCH-WO"
FINISHED_NAME = "Bench Assembly Kit"
COMPONENT_NAME = "Bench Serial Part"
WORKCENTER_NAME = "WC-01"


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Lot = env["stock.lot"]
    Workcenter = env["mrp.workcenter"]

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

    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", [FINISHED_NAME, COMPONENT_NAME]),
    ])
    stale_lots = Lot.search([
        ("product_id", "in", stale_prod.ids),
    ])
    stale_quants = env["stock.quant"].search([
        ("lot_id", "in", stale_lots.ids),
    ])
    for q in stale_quants:
        try:
            q.with_context(inventory_mode=True).write({"inventory_quantity": 0.0})
            q.action_apply_inventory()
        except Exception:
            pass
    try:
        stale_lots.unlink()
    except Exception:
        pass

    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    stale_wc = Workcenter.search([("name", "=", WORKCENTER_NAME)])
    stale_wc.unlink()
