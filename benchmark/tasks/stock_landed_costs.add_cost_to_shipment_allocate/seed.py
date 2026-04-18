"""Seed for stock_landed_costs.add_cost_to_shipment_allocate.

Category 2 (HARD, policy_trap): agent must chain TWO buttons on a
stock.landed.cost form (Compute + Validate), pick the right receipt in
a many2many_tags autocomplete, and keep the seeded non-default
split_method. Skipping Compute makes Validate raise "Cost and
adjustments lines do not match"; clicking Validate without the cost
line leaves the record in Draft.

Seeds:
  * ir.module stock_landed_costs installed on demand.
  * A dedicated product.category 'Bench LC Category' with
    property_cost_method='fifo' and property_valuation='periodic'
    so the landed cost validate updates stock.move.value WITHOUT
    needing accounting journals (no real_time entries).
  * Storable product 'Bench Import Item' (type=consu,
    is_storable=True, categ_id=<above>, standard_price=80.0).
  * Service product 'Freight' (type=service, landed_cost_ok=True,
    split_method_landed_cost='by_quantity', standard_price=45.0).
  * Vendor 'Bench Import Vendor', PO 'P-BENCH-LC-001' for 3 units of
    Bench Import Item at 80.0 each, confirmed + received (picking is
    'done' with move.is_in=True so it's eligible for landed cost).
  * The picking is renamed to 'R-BENCH-LC-001' so the agent can pick
    it from the Transfers many2many_tags autocomplete deterministically.
"""

PO_REF = "P-BENCH-LC-001"
RECEIPT_REF = "R-BENCH-LC-001"
VENDOR_NAME = "Bench Import Vendor"
PRODUCT_NAME = "Bench Import Item"
FREIGHT_NAME = "Freight"
LC_CATEGORY_NAME = "Bench LC Category"
DEMAND_QTY = 3.0
UNIT_COST = 80.0
FREIGHT_COST = 45.0


def _ensure_module(env):
    mod = env["ir.module.module"].search(
        [("name", "=", "stock_landed_costs")], limit=1
    )
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup_landed_costs(env):
    # Drop any prior landed-cost records referencing our products.
    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "in", [PRODUCT_NAME, FREIGHT_NAME])]
    )
    if prods:
        lcs = env["stock.landed.cost"].with_context(active_test=False).search([
            "|",
            ("cost_lines.product_id", "in", prods.ids),
            ("picking_ids.move_ids.product_id", "in", prods.ids),
        ])
        for lc in lcs:
            if lc.state == "draft":
                try:
                    lc.unlink()
                except Exception:
                    pass


def _cleanup_pickings(env):
    pickings = env["stock.picking"].search([
        "|", "|", "|", "|",
        ("origin", "=", PO_REF),
        ("name", "=", RECEIPT_REF),
        ("name", "in", ["R-BENCH-LC-DISTRACTOR-A", "R-BENCH-LC-DISTRACTOR-B"]),
        ("origin", "in", ["P-BENCH-LC-DIST-A", "P-BENCH-LC-DIST-B"]),
        ("name", "=", "false_placeholder_never_match"),
    ])
    for pick in pickings:
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.move_ids.write({"state": "cancel"})
            pick.write({"state": "cancel"})
            pick.unlink()
        except Exception:
            pass


def _cleanup_po(env):
    old = env["purchase.order"].search([
        "|", "|", "|",
        ("name", "=", PO_REF),
        ("origin", "=", PO_REF),
        ("name", "in", ["P-BENCH-LC-DIST-A", "P-BENCH-LC-DIST-B"]),
        ("origin", "in", ["P-BENCH-LC-DIST-A", "P-BENCH-LC-DIST-B"]),
    ])
    for po in old:
        if po.state in ("purchase", "done"):
            try:
                po.button_cancel()
            except Exception:
                pass
        if po.state == "cancel":
            try:
                po.button_draft()
            except Exception:
                pass
        try:
            po.unlink()
        except Exception:
            pass


def _cleanup_products(env):
    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "in", [
            PRODUCT_NAME, FREIGHT_NAME,
            "Bench Other Gadget", "Bench Spare Widget",
        ])]
    )
    for p in prods:
        try:
            env["stock.move.line"].search(
                [("product_id", "=", p.id)]
            ).unlink()
            env["stock.move"].search(
                [("product_id", "=", p.id)]
            ).unlink()
        except Exception:
            pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass


def _cleanup(env):
    _cleanup_landed_costs(env)
    _cleanup_pickings(env)
    _cleanup_po(env)
    _cleanup_products(env)


def _ensure_category(env):
    Category = env["product.category"]
    cat = Category.search([("name", "=", LC_CATEGORY_NAME)], limit=1)
    vals = {
        "name": LC_CATEGORY_NAME,
        "property_cost_method": "fifo",
        "property_valuation": "periodic",
    }
    if not cat:
        # Try to parent under goods if it exists.
        try:
            parent = env.ref("product.product_category_goods")
            vals["parent_id"] = parent.id
        except Exception:
            pass
        cat = Category.create(vals)
    else:
        cat.write({
            "property_cost_method": "fifo",
            "property_valuation": "periodic",
        })
    return cat


def setup(env):
    _ensure_module(env)
    # Re-resolve the registry after install.
    env = env["res.partner"].env  # refresh env handle

    if "stock.landed.cost" not in env.registry:
        return

    _cleanup(env)

    admin = env.ref("base.user_admin")
    # Landed cost menus/form live under stock — admin already has
    # stock.group_stock_manager in base, but belt-and-braces here.
    admin.group_ids |= env.ref("stock.group_stock_manager")

    category = _ensure_category(env)

    # ---- Vendor ----
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "import@benchlogistics.example",
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # ---- Freight service product (landed cost config) ----
    freight_tmpl = env["product.template"].create({
        "name": FREIGHT_NAME,
        "type": "service",
        "categ_id": category.id,
        "list_price": FREIGHT_COST,
        "standard_price": FREIGHT_COST,
        "landed_cost_ok": True,
        "split_method_landed_cost": "by_quantity",
    })
    freight_tmpl.product_variant_id  # materialize variant

    # ---- Import item (storable, FIFO/periodic) ----
    item_tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "categ_id": category.id,
        "list_price": 120.0,
        "standard_price": UNIT_COST,
        "purchase_ok": True,
        "weight": 2.0,
        "volume": 0.05,
    })
    item = item_tmpl.product_variant_id

    # ---- PO + confirm ----
    po = env["purchase.order"].create({
        "name": PO_REF,
        "partner_id": vendor.id,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": item.id,
        "product_qty": DEMAND_QTY,
        "price_unit": UNIT_COST,
        "name": PRODUCT_NAME,
    })
    po.button_confirm()

    # ---- Validate the receipt so move.is_in=True ----
    picking = po.picking_ids and po.picking_ids[0]
    if picking:
        # Pin the picking name so the agent can type it in the m2m tags.
        picking.write({"name": RECEIPT_REF})
        # Assign + set Done quantity = demand, then validate.
        if picking.state not in ("assigned", "done", "cancel"):
            try:
                picking.action_assign()
            except Exception:
                pass
        for mv in picking.move_ids:
            mv.write({
                "quantity": DEMAND_QTY,
                "picked": True,
            })
        try:
            picking.with_context(skip_backorder=True).button_validate()
        except Exception:
            pass

    # Final sanity: ensure picking ended up 'done'. If not, try once more.
    if picking and picking.state != "done":
        try:
            picking.button_validate()
        except Exception:
            pass

    # ---- Seed distractor validated receipts so the picking autocomplete
    #      offers multiple hits. The agent must read the task spec and
    #      pick R-BENCH-LC-001 specifically — not any other "Bench" one.
    _seed_distractor_receipts(env, vendor, category)


def _seed_distractor_receipts(env, vendor, category):
    """Create 2 extra completed receipts for unrelated products that share
    the 'Bench' name prefix, so 'R-BENCH' autocomplete returns multiple
    rows. The agent must narrow to R-BENCH-LC-001 exactly."""
    distractor_specs = [
        ("Bench Other Gadget", "R-BENCH-LC-DISTRACTOR-A", "P-BENCH-LC-DIST-A", 5.0, 40.0),
        ("Bench Spare Widget", "R-BENCH-LC-DISTRACTOR-B", "P-BENCH-LC-DIST-B", 7.0, 25.0),
    ]
    for prod_name, pick_name, po_name, qty, unit_cost in distractor_specs:
        # Skip if exists (idempotent re-run).
        if env["stock.picking"].search([("name", "=", pick_name)], limit=1):
            continue
        tmpl = env["product.template"].create({
            "name": prod_name,
            "type": "consu",
            "is_storable": True,
            "categ_id": category.id,
            "list_price": unit_cost * 1.5,
            "standard_price": unit_cost,
            "purchase_ok": True,
        })
        prod_v = tmpl.product_variant_id
        po_d = env["purchase.order"].create({
            "name": po_name,
            "partner_id": vendor.id,
        })
        env["purchase.order.line"].create({
            "order_id": po_d.id,
            "product_id": prod_v.id,
            "product_qty": qty,
            "price_unit": unit_cost,
            "name": prod_name,
        })
        po_d.button_confirm()
        dp = po_d.picking_ids and po_d.picking_ids[0]
        if dp:
            dp.write({"name": pick_name})
            if dp.state not in ("assigned", "done", "cancel"):
                try:
                    dp.action_assign()
                except Exception:
                    pass
            for mv in dp.move_ids:
                mv.write({"quantity": qty, "picked": True})
            try:
                dp.with_context(skip_backorder=True).button_validate()
            except Exception:
                pass
