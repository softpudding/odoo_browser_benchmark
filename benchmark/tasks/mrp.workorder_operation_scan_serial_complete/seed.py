"""Seed for mrp.workorder_operation_scan_serial_complete.

Category (HARD): deep_ui_interaction — tests whether the agent can drive
a work-order lifecycle AND override the default-reserved serial number
on a serial-tracked component before finishing the work order and
marking the manufacturing order done.

Pre-seeded entities:
  - 'Bench Assembly Kit' — finished consu/storable product (tracking='none').
  - 'Bench Serial Part' — component consu/storable product, tracking='serial'.
  - stock.lot rows SN-A, SN-B, SN-C, SN-D for 'Bench Serial Part', each with
    1.0 on hand at WH/Stock.
  - mrp.workcenter 'WC-01'.
  - mrp.bom for 'Bench Assembly Kit' (normal, qty=1) with 1x 'Bench Serial
    Part' and a single operation 'Final Assembly' on WC-01.
  - mrp.production 'MO-BENCH-WO' in state='confirmed' with qty=1. After
    action_confirm, exactly ONE serial will have been reserved (typically
    SN-A because it's the first lot by id). The agent's job is to change
    that reservation to SN-B — NOT leave the default.
  - Admin is granted mrp.group_mrp_routings so the Work Orders tab renders.

Why four serials? A naive agent might pick the first entry in the
serial picker (SN-A) or the last (SN-D). The required serial (SN-B) is
sandwiched between distractors — picking the default, first, or last
all fail. Only reading the prompt and picking 'SN-B' explicitly works.

Seed invariants:
  - MO state == 'confirmed'
  - len(mo.workorder_ids) == 1 and workorder_ids[0].state in ('ready','waiting','pending')
  - mo has exactly one serial-tracked component (Bench Serial Part)
  - stock.lot of names SN-A/SN-B/SN-C/SN-D each have qty_available == 1 at WH/Stock
  - The agent has NOT yet consumed any lot.
"""


FINISHED_NAME = "Bench Assembly Kit"
COMPONENT_NAME = "Bench Serial Part"
MO_NAME = "MO-BENCH-WO"
WORKCENTER_NAME = "WC-01"
OPERATION_NAME = "Final Assembly"
SERIAL_NAMES = ["SN-A", "SN-B", "SN-C", "SN-D"]


def _cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Lot = env["stock.lot"]
    Workcenter = env["mrp.workcenter"]

    # MOs first — cancel if active, then unlink.
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

    # Unlink lots for our serial component (they'll fail if linked to done
    # moves, which shouldn't happen after MO cleanup).
    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", [FINISHED_NAME, COMPONENT_NAME]),
    ])
    stale_lots = Lot.search([
        ("product_id", "in", stale_prod.ids),
    ])
    # Zero out any residual quants first so lot unlink succeeds.
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

    # BoMs + products.
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    # Workcenter.
    stale_wc = Workcenter.search([("name", "=", WORKCENTER_NAME)])
    stale_wc.unlink()


def setup(env):
    # Grant admin the routings group so Work Orders tab is visible and
    # operations can be edited on the BoM.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "mrp.group_mrp_routings",
        "stock.group_production_lot",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})

    _cleanup(env)

    Product = env["product.product"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Lot = env["stock.lot"]
    Workcenter = env["mrp.workcenter"]
    MO = env["mrp.production"]

    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id

    # --- Products ---
    finished = Product.create({
        "name": FINISHED_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    component = Product.create({
        "name": COMPONENT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "serial",
    })

    # --- Workcenter ---
    workcenter = Workcenter.create({
        "name": WORKCENTER_NAME,
        "resource_calendar_id": env.ref("resource.resource_calendar_std").id,
        "time_start": 0.0,
        "time_stop": 0.0,
    })

    # --- BoM with a single operation on WC-01 ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1.0,
        "type": "normal",
        "consumption": "flexible",
        "operation_ids": [(0, 0, {
            "name": OPERATION_NAME,
            "workcenter_id": workcenter.id,
            "time_cycle_manual": 10.0,
        })],
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": component.id,
        "product_qty": 1.0,
    })

    # --- Serial lots: SN-A, SN-B, SN-C, SN-D (each with 1.0 on hand) ---
    # Create lots in this deterministic order so SN-A has the lowest id
    # (= reserved first by FIFO). We want SN-A to be the default and
    # SN-B to be the correct pick.
    lot_by_name = {}
    for name in SERIAL_NAMES:
        lot = Lot.create({
            "name": name,
            "product_id": component.id,
            "company_id": env.company.id,
        })
        lot_by_name[name] = lot
        env["stock.quant"]._update_available_quantity(
            component, stock_loc, 1.0, lot_id=lot,
        )

    # --- MO: confirmed with 1 workorder on WC-01 ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 1.0,
        "bom_id": bom.id,
    })
    mo.action_confirm()

    # Seed invariants.
    if mo.state != "confirmed":
        raise RuntimeError(
            f"Seed invariant failed: MO state is {mo.state!r}, expected 'confirmed'"
        )
    if len(mo.workorder_ids) != 1:
        raise RuntimeError(
            f"Seed invariant failed: expected 1 workorder, got {len(mo.workorder_ids)}"
        )

    # Verify all 4 serials still have 1.0 on hand (quantity, not
    # "available" — action_confirm reserves one of them so its
    # available == 0, but quantity on hand is still 1.0).
    for name in SERIAL_NAMES:
        quants = env["stock.quant"].search([
            ("product_id", "=", component.id),
            ("lot_id", "=", lot_by_name[name].id),
            ("location_id", "=", stock_loc.id),
        ])
        on_hand = sum(quants.mapped("quantity"))
        if abs(on_hand - 1.0) > 1e-6:
            raise RuntimeError(
                f"Seed invariant failed: serial {name!r} has on_hand={on_hand}, expected 1.0"
            )
