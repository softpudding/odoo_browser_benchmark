"""Clean up artifacts from previous runs of
mrp_subcontracting.receive_subcontracted_product_with_components."""

PO_NAME = "P-BENCH-SUB-001"
SUBCONTRACTOR_NAME = "Bench Subcontractor Inc"
FINISHED_NAME = "Bench Sub Assembly"
PART_A = "Bench Sub Part-A"
PART_B = "Bench Sub Part-B"


def cleanup(env):
    POs = env["purchase.order"].search([("name", "=", PO_NAME)])
    for po in POs:
        try:
            if po.state in ("purchase", "done"):
                po.button_cancel()
        except Exception:
            pass
        for pick in po.picking_ids:
            try:
                if pick.state not in ("done", "cancel"):
                    pick.action_cancel()
            except Exception:
                pass
            try:
                pick.move_ids.write({"state": "cancel"})
                pick.write({"state": "cancel"})
                pick.unlink()
            except Exception:
                pass
        try:
            po.unlink()
        except Exception:
            pass

    stray_pickings = env["stock.picking"].search([("origin", "=", PO_NAME)])
    for pick in stray_pickings:
        try:
            if pick.state not in ("done", "cancel"):
                pick.action_cancel()
        except Exception:
            pass
        try:
            pick.move_ids.write({"state": "cancel"})
            pick.write({"state": "cancel"})
            pick.unlink()
        except Exception:
            pass

    prods = env["product.product"].with_context(active_test=False).search([
        ("name", "in", (FINISHED_NAME, PART_A, PART_B)),
    ])

    mos = env["mrp.production"].search([
        ("product_id", "in", prods.ids),
    ])
    for mo in mos:
        try:
            if mo.state not in ("done", "cancel"):
                mo.action_cancel()
        except Exception:
            pass
        try:
            mo.unlink()
        except Exception:
            pass

    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
    ])
    try:
        boms.unlink()
    except Exception:
        pass

    env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.quant"].with_context(inventory_mode=True).search([
        ("product_id", "in", prods.ids),
    ]).sudo().unlink()

    env["product.supplierinfo"].search([
        ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
    ]).unlink()

    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass
