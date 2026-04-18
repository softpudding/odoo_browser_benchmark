"""Seed for mrp_subcontracting.receive_subcontracted_product_with_components.

Category (HARD): closed_loop_cross_module.

Creates a subcontracting scenario where:
  * mrp_subcontracting (+ mrp_subcontracting_purchase) is installed.
  * A subcontractor partner 'Bench Subcontractor Inc' exists (with
    supplier_rank=1 so it's also a vendor for purchases).
  * A subcontract BoM for 'Bench Sub Assembly' is defined with two
    components at qty=1 each: 'Bench Sub Part-A' and 'Bench Sub Part-B'.
    The subcontractor is linked on the BoM.
  * The two components are pre-stocked at the subcontractor's
    subcontracting location (enough for 2 assemblies).
  * A confirmed purchase.order 'P-BENCH-SUB-001' exists for 2 units of
    'Bench Sub Assembly' from the subcontractor. Confirming the PO
    auto-generates an incoming receipt (stock.picking) whose single
    move has is_subcontract=True and an auto-created mrp.production
    (state=confirmed).

The agent must Validate the receipt so the subcontract MO closes and
back-flushes the components.

Traps:
  * Agent clicks Validate before setting Done qty — the receipt
    validation errors / creates a no-op backorder and the MO stays
    'confirmed'.
  * Agent navigates to Manufacturing and tries to close the MO
    manually (possible, but not the canonical workflow).
"""

PO_NAME = "P-BENCH-SUB-001"
SUBCONTRACTOR_NAME = "Bench Subcontractor Inc"
FINISHED_NAME = "Bench Sub Assembly"
PART_A = "Bench Sub Part-A"
PART_B = "Bench Sub Part-B"
ORDER_QTY = 2.0


def _install_modules(env):
    for name in ("mrp_subcontracting", "mrp_subcontracting_purchase"):
        mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()


def _cleanup(env):
    # Cancel + unlink any purchase order referencing our name.
    POs = env["purchase.order"].search([("name", "=", PO_NAME)])
    for po in POs:
        try:
            if po.state in ("purchase", "done"):
                po.button_cancel()
        except Exception:
            pass
        # Cancel linked pickings/MOs.
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

    # Orphan pickings still named after our PO.
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

    # Orphan MOs from prior runs (by BoM product).
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

    # Stale BoMs.
    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
    ])
    try:
        boms.unlink()
    except Exception:
        pass

    # Stale move lines / moves / quants for our products.
    env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.quant"].with_context(inventory_mode=True).search([
        ("product_id", "in", prods.ids),
    ]).sudo().unlink()

    # Supplier info.
    env["product.supplierinfo"].search([
        ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
    ]).unlink()

    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass


def _ensure_product(env, name, list_price, storable=True, tracking="none"):
    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "is_storable": storable,
        "tracking": tracking,
        "list_price": list_price,
        "standard_price": list_price * 0.5 if list_price else 0.0,
        "purchase_ok": True,
    })
    return tmpl.product_variant_id


def setup(env):
    _install_modules(env)
    _cleanup(env)

    admin = env.ref("base.user_admin")
    # Grant admin multi-locations + production_lot groups so the subcontract
    # location / per-line Details popup render correctly.
    for xmlid in (
        "stock.group_stock_multi_locations",
        "stock.group_production_lot",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})

    # Disable "Resupply Subcontractors" on every warehouse. The default is
    # True, which makes confirming a subcontracting PO auto-generate a
    # secondary `Resupply Subcontractor` internal picking that moves
    # components from WH/Stock to the subcontracting location. Our task
    # pre-stocks components directly AT the subcontracting location, so
    # there's no need (and no stock) for a resupply picking — disabling it
    # keeps the receipt as the sole picking tied to the PO.
    warehouses = env["stock.warehouse"].search([])
    warehouses.write({"subcontracting_to_resupply": False})

    # Ensure the incoming (Receipts) picking type allows on-the-fly lot
    # creation so the Detailed Operations popup exposes a Create
    # autocomplete entry when the agent types a brand-new serial number.
    picking_types = env["stock.picking.type"].search([
        ("code", "=", "incoming"),
    ])
    picking_types.write({
        "use_create_lots": True,
        "use_existing_lots": True,
    })

    # --- Subcontractor partner (also a vendor) ---
    subcontractor = env["res.partner"].search(
        [("name", "=", SUBCONTRACTOR_NAME)], limit=1,
    )
    if not subcontractor:
        subcontractor = env["res.partner"].create({
            "name": SUBCONTRACTOR_NAME,
            "email": "orders@bench-subcontractor.example",
            "supplier_rank": 1,
            "company_type": "company",
        })
    else:
        subcontractor.write({"supplier_rank": max(subcontractor.supplier_rank, 1)})

    # --- Products ---
    # Finished product is SERIAL-tracked so the agent MUST open the
    # Detailed Operations popup and enter two distinct serial numbers
    # (one per produced unit) before Validate. Components untracked.
    finished = _ensure_product(env, FINISHED_NAME, list_price=500.0, tracking="serial")
    part_a = _ensure_product(env, PART_A, list_price=20.0)
    part_b = _ensure_product(env, PART_B, list_price=35.0)

    # --- Supplierinfo so the PO line picks the subcontractor as seller ---
    env["product.supplierinfo"].create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "partner_id": subcontractor.id,
        "price": 180.0,
        "min_qty": 1.0,
    })

    # --- BoM: type=subcontract, with subcontractor linked ---
    bom = env["mrp.bom"].create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1.0,
        "type": "subcontract",
        "subcontractor_ids": [(6, 0, [subcontractor.id])],
    })
    env["mrp.bom.line"].create({
        "bom_id": bom.id,
        "product_id": part_a.id,
        "product_qty": 1.0,
    })
    env["mrp.bom.line"].create({
        "bom_id": bom.id,
        "product_id": part_b.id,
        "product_qty": 1.0,
    })

    # --- Pre-stock components at the subcontractor's subcontracting location ---
    # (Without this, validation would leave the subcontractor with negative
    # quantities, which is allowed but makes the "back-flush 4 components"
    # invariant unverifiable. Seeding +qty at the subcontracting location
    # gives a clean +qty -> 0 diff on validation.)
    sub_loc = subcontractor.with_company(env.company).property_stock_subcontractor \
        or env.company.subcontracting_location_id
    if not sub_loc:
        raise RuntimeError("No subcontracting location resolved for the subcontractor partner.")
    # 2 of each; BoM consumes 1 of each per finished unit, qty=2.
    env["stock.quant"]._update_available_quantity(part_a, sub_loc, 2.0)
    env["stock.quant"]._update_available_quantity(part_b, sub_loc, 2.0)

    # --- Confirmed Purchase Order ---
    po = env["purchase.order"].create({
        "name": PO_NAME,
        "partner_id": subcontractor.id,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": finished.id,
        "product_qty": ORDER_QTY,
        "price_unit": 180.0,
        "tax_ids": [(5, 0, 0)],
    })
    po.button_confirm()

    # --- Sanity: a picking should have been generated ---
    if not po.picking_ids:
        raise RuntimeError(
            "Seed invariant failed: PO confirmed but no incoming picking generated."
        )
    picking = po.picking_ids[0]
    if picking.state not in ("assigned", "confirmed"):
        raise RuntimeError(
            f"Seed invariant failed: picking state is {picking.state!r}, expected 'assigned'."
        )

    # --- Sanity: an auto-created subcontract MO should exist in state='confirmed' ---
    mo = env["mrp.production"].search([
        ("bom_id", "=", bom.id),
        ("subcontractor_id", "=", subcontractor.id),
    ], limit=1)
    if not mo:
        raise RuntimeError(
            "Seed invariant failed: no subcontract MO auto-created for the receipt."
        )
    if mo.state != "confirmed":
        raise RuntimeError(
            f"Seed invariant failed: subcontract MO state is {mo.state!r}, expected 'confirmed'."
        )
