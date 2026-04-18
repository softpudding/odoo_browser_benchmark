"""Seed for product_expiry.receive_lot_set_expiry_date.

Category: deep_ui_interaction (MEDIUM).

Installs product_expiry (not in base snapshot), creates a lot-tracked
perishable product 'Bench Perishable' with use_expiration_date=True and
expiration_time=30, plus a CONFIRMED receipt for 10 units with the done
quantity pre-filled. The agent's only remaining work is to:
  (a) create the lot on the fly with name BP-LOT-001 inside the
      Detailed Operations popup,
  (b) navigate to the stock.lot form via the internal-link arrow on
      lot_id and set explicit expiration_date (today+60) + removal_date
      (today+55),
  (c) save the lot / popup, and
  (d) Validate the receipt.

The medium difficulty comes from the popup-inside-popup navigation
(move.Detailed Operations → stock.lot form → back) plus the datetime
widget interaction. A naive agent will create the lot and validate
without ever opening the lot form, leaving expiration_date at the
30-day template default.
"""

PRODUCT_NAME = "Bench Perishable"
RECEIPT_ORIGIN = "BENCH-PERISH-RCV-01"
DEMAND_QTY = 10.0
LOT_NAME = "BP-LOT-001"


def _ensure_product_expiry(env):
    mod = env["ir.module.module"].search(
        [("name", "=", "product_expiry")], limit=1
    )
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup(env):
    for pick in env["stock.picking"].search(
        [("origin", "=", RECEIPT_ORIGIN)]
    ):
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.unlink()
        except Exception:
            pass

    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    env["stock.move.line"].search(
        [("product_id", "in", prods.ids)]
    ).unlink()
    env["stock.move"].search(
        [("product_id", "in", prods.ids)]
    ).unlink()
    env["stock.lot"].search(
        [("product_id", "in", prods.ids)]
    ).unlink()
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass

    # Any orphan lot sharing our target name.
    stale = env["stock.lot"].search([("name", "=", LOT_NAME)])
    if stale:
        try:
            stale.unlink()
        except Exception:
            pass


def setup(env):
    _ensure_product_expiry(env)
    if "product.template" not in env.registry:
        return
    if not hasattr(env["product.template"], "use_expiration_date"):
        # product_expiry not loaded — nothing else to do.
        return

    _cleanup(env)

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_production_lot")
    admin.group_ids |= env.ref("stock.group_stock_manager")

    # Ensure Receipts picking type allows on-the-fly lot creation AND
    # lookup of existing lots — so the agent sees the m2o widget with
    # 'Create "BP-LOT-001"' autocomplete + internal-link arrow.
    picking_type = env["stock.picking.type"].search(
        [("code", "=", "incoming")], limit=1
    )
    picking_type.write({
        "use_create_lots": True,
        "use_existing_lots": True,
    })

    location_supplier = env.ref("stock.stock_location_suppliers")
    location_stock = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location_stock:
        location_stock = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )

    # Lot-tracked perishable product.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "lot",
        "list_price": 12.5,
        "standard_price": 6.0,
        "use_expiration_date": True,
        "expiration_time": 30,
        "use_time": 20,
        "removal_time": 5,
        "alert_time": 10,
    })
    product = tmpl.product_variant_id

    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
        "origin": RECEIPT_ORIGIN,
    })
    env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": DEMAND_QTY,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
    })

    picking.action_confirm()
    picking.action_assign()

    # Pre-fill the done quantity so the agent's only remaining work
    # is the lot + expiration-date dance + Validate.
    for ml in picking.move_line_ids:
        ml.quantity = DEMAND_QTY
