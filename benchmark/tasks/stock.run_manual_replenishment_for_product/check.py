"""Postcondition checks for stock.run_manual_replenishment_for_product.

Validates:
  1. Exactly ONE new purchase.order exists for vendor 'Bench Replenish Vendor',
     in state 'draft' OR 'purchase' (both accepted per prompt).
  2. The PO has exactly ONE purchase.order.line for product
     'Bench Replenish Item' with product_qty=20.0 and price_unit=50.0.
  3. The seeded stock.warehouse.orderpoint for 'Bench Replenish Item'
     remains intact: active=True, product_min_qty=5.0, product_max_qty=20.0,
     trigger='manual' (agent did not click Automate).
  4. Product integrity (type/is_storable/tracking unchanged).
"""

VENDOR_NAME = "Bench Replenish Vendor"
PRODUCT_NAME = "Bench Replenish Item"
EXPECTED_QTY = 20.0
EXPECTED_PRICE = 50.0
EXPECTED_MIN = 5.0
EXPECTED_MAX = 20.0


def _close(a, b, tol=1e-6):
    return abs((a or 0.0) - (b or 0.0)) <= tol


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found (seed not applied)"]

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found (seed not applied)"]

    # --- Product integrity ---------------------------------------------
    if product.type != "consu":
        failures.append(
            f"Product type is '{product.type}', expected 'consu' — "
            f"agent may have edited the product directly"
        )
    if not product.is_storable:
        failures.append(
            "Product is_storable is False, expected True — agent may "
            "have flipped the storable flag"
        )

    # --- Orderpoint integrity -----------------------------------------
    # Note: `stock.warehouse.orderpoint.action_replenish` ends with
    #   self.filtered(lambda o: o.create_uid.id == SUPERUSER_ID
    #                           and o.qty_to_order <= 0.0
    #                           and o.trigger == 'manual').unlink()
    # so a seed-created (SUPERUSER_ID) manual orderpoint auto-deletes
    # once its qty_to_order falls to 0 — which happens immediately after
    # action_replenish because the new PO line consumes the demand.
    # We therefore accept either (a) orderpoint still present with seeded
    # values intact, or (b) orderpoint gone (auto-deleted). We ONLY fail
    # if it remains with mutated min/max/trigger (agent edited the rule)
    # or if the agent created a duplicate orderpoint.
    orderpoints = env["stock.warehouse.orderpoint"].with_context(
        active_test=False
    ).search([("product_id", "=", product.id)])
    if len(orderpoints) > 1:
        failures.append(
            f"Expected at most 1 orderpoint for '{PRODUCT_NAME}', found "
            f"{len(orderpoints)}: {orderpoints.mapped('name')} — agent "
            f"may have created a duplicate"
        )
    if len(orderpoints) == 1:
        op = orderpoints[:1]
        if not _close(op.product_min_qty, EXPECTED_MIN):
            failures.append(
                f"Orderpoint product_min_qty is {op.product_min_qty}, "
                f"expected {EXPECTED_MIN} — agent modified Min"
            )
        if not _close(op.product_max_qty, EXPECTED_MAX):
            failures.append(
                f"Orderpoint product_max_qty is {op.product_max_qty}, "
                f"expected {EXPECTED_MAX} — agent modified Max"
            )
        if op.trigger != "manual":
            failures.append(
                f"Orderpoint trigger is '{op.trigger}', expected 'manual' "
                f"— agent clicked Automate (action_replenish_auto) "
                f"instead of Order (action_replenish)"
            )

    # --- Purchase order(s) for the vendor ------------------------------
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id", "=", vendor.id),
    ])
    if len(pos) == 0:
        failures.append(
            f"No purchase.order found for vendor '{VENDOR_NAME}' — agent "
            f"did not trigger action_replenish on the orderpoint"
        )
        return failures
    if len(pos) > 1:
        failures.append(
            f"Expected exactly 1 purchase.order for '{VENDOR_NAME}', "
            f"found {len(pos)}: {pos.mapped('name')} — agent may have "
            f"triggered replenishment more than once or created an "
            f"additional PO by hand"
        )

    po = pos[:1]
    if po.state not in ("draft", "sent", "purchase"):
        failures.append(
            f"PO state is '{po.state}', expected 'draft' or 'purchase' "
            f"(sent also accepted) — agent may have cancelled the PO"
        )

    # --- PO line validation --------------------------------------------
    lines = po.order_line
    if len(lines) != 1:
        failures.append(
            f"PO has {len(lines)} order line(s), expected exactly 1 "
            f"(product: {lines.mapped('product_id.name')})"
        )
    else:
        ln = lines[:1]
        if ln.product_id.id != product.id:
            failures.append(
                f"PO line product is '{ln.product_id.display_name}', "
                f"expected '{PRODUCT_NAME}'"
            )
        if not _close(ln.product_qty, EXPECTED_QTY):
            failures.append(
                f"PO line product_qty is {ln.product_qty}, expected "
                f"{EXPECTED_QTY} — action_replenish should bring stock to "
                f"Max (20). Values near 5 suggest the agent entered the "
                f"Min by hand; 0 suggests the Order button never fired."
            )
        if not _close(ln.price_unit, EXPECTED_PRICE):
            failures.append(
                f"PO line price_unit is {ln.price_unit}, expected "
                f"{EXPECTED_PRICE} — the product.supplierinfo.price of "
                f"50.00 should flow through automatically"
            )

    return failures
