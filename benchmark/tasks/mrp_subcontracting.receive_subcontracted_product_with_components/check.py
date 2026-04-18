"""Postcondition checks for
mrp_subcontracting.receive_subcontracted_product_with_components.

Validates:
  1. The receipt for PO P-BENCH-SUB-001 is in state='done'.
  2. The subcontract move on the receipt carries exactly 2
     stock.move.line rows, each with quantity==1 and a distinct
     stock.lot named BSA-2026-01 / BSA-2026-02 on Bench Sub Assembly.
  3. The auto-created subcontract mrp.production records for
     Bench Sub Assembly (subcontractor = Bench Subcontractor Inc)
     total product_qty == 2.0 and are ALL state='done'.
  4. At the subcontractor's subcontracting location, the stock.quant
     for Bench Sub Part-A and Bench Sub Part-B each decreased by 2.0
     (from +2 -> 0).
  5. stock.lot records exist for both serials.
"""

PO_NAME = "P-BENCH-SUB-001"
SUBCONTRACTOR_NAME = "Bench Subcontractor Inc"
FINISHED_NAME = "Bench Sub Assembly"
PART_A = "Bench Sub Part-A"
PART_B = "Bench Sub Part-B"
ORDER_QTY = 2.0
EXPECTED_SERIALS = {"BSA-2026-01", "BSA-2026-02"}


def check(env):
    failures = []

    # ------------------------------------------------------------------
    # 1. Receipt state
    # ------------------------------------------------------------------
    po = env["purchase.order"].search([("name", "=", PO_NAME)], limit=1)
    if not po:
        return [f"Purchase order '{PO_NAME}' not found"]
    if not po.picking_ids:
        return [f"No picking linked to purchase order '{PO_NAME}'"]

    receipts = po.picking_ids.filtered(
        lambda p: p.picking_type_id.code == "incoming"
    )
    if not receipts:
        return [f"No incoming picking linked to '{PO_NAME}'"]
    receipt = receipts[0]
    if receipt.state != "done":
        failures.append(
            f"Receipt state is '{receipt.state}', expected 'done'"
        )

    # ------------------------------------------------------------------
    # 2. Serial move lines on the subcontract move
    # ------------------------------------------------------------------
    sub_moves = receipt.move_ids.filtered(lambda m: m.is_subcontract)
    if not sub_moves:
        failures.append(
            "Receipt has no subcontract move (is_subcontract=True)."
        )
    else:
        total_done = sum(sub_moves.mapped("quantity"))
        if abs(total_done - ORDER_QTY) > 0.001:
            failures.append(
                f"Receipt subcontract move total Done qty is {total_done}, "
                f"expected {ORDER_QTY}"
            )

        mls = sub_moves.mapped("move_line_ids")
        real_mls = mls.filtered(lambda ml: ml.quantity > 0)
        if len(real_mls) != 2:
            failures.append(
                f"Expected 2 move_lines (qty>0) for Bench Sub Assembly, "
                f"found {len(real_mls)} — agent may have merged both "
                f"serials into a single move_line (qty=2 on one row)"
            )
        else:
            qtys = sorted(ml.quantity for ml in real_mls)
            if not all(abs(q - 1.0) < 0.001 for q in qtys):
                failures.append(
                    f"Move line quantities are {qtys}, expected [1.0, 1.0]"
                )

        lot_names = set()
        for ml in mls:
            if ml.lot_id:
                lot_names.add(ml.lot_id.name)
        missing = EXPECTED_SERIALS - lot_names
        extra = lot_names - EXPECTED_SERIALS
        if missing:
            failures.append(
                f"Missing serials on receipt move_lines: {sorted(missing)} "
                f"(found {sorted(lot_names)})"
            )
        if extra:
            failures.append(
                f"Unexpected serials on receipt move_lines: {sorted(extra)}"
            )

    # ------------------------------------------------------------------
    # 3. Subcontract MO done
    # ------------------------------------------------------------------
    subcontractor = env["res.partner"].search(
        [("name", "=", SUBCONTRACTOR_NAME)], limit=1,
    )
    if not subcontractor:
        return failures + [f"Subcontractor '{SUBCONTRACTOR_NAME}' missing"]

    finished = env["product.product"].search(
        [("name", "=", FINISHED_NAME)], limit=1,
    )
    if not finished:
        return failures + [f"Finished product '{FINISHED_NAME}' missing"]

    mos = env["mrp.production"].search([
        ("subcontractor_id", "=", subcontractor.id),
        ("product_id", "=", finished.id),
    ])
    if not mos:
        failures.append(
            "No subcontract mrp.production auto-created for "
            f"'{FINISHED_NAME}' by '{SUBCONTRACTOR_NAME}'"
        )
    else:
        non_done = mos.filtered(lambda m: m.state != "done")
        if non_done:
            failures.append(
                f"Subcontract MO(s) not all 'done': "
                f"states={sorted(set(mos.mapped('state')))}"
            )
        total_produced = sum(
            mos.filtered(lambda m: m.state == "done").mapped("product_qty")
        )
        if abs(total_produced - ORDER_QTY) > 0.001:
            failures.append(
                f"Total produced qty across done subcontract MOs is "
                f"{total_produced}, expected {ORDER_QTY}"
            )

    # ------------------------------------------------------------------
    # 4. Components consumed at subcontracting location
    # ------------------------------------------------------------------
    part_a = env["product.product"].search([("name", "=", PART_A)], limit=1)
    part_b = env["product.product"].search([("name", "=", PART_B)], limit=1)
    if not part_a or not part_b:
        return failures + [
            f"Components '{PART_A}' / '{PART_B}' missing"
        ]

    sub_loc = (
        subcontractor.with_company(env.company).property_stock_subcontractor
        or env.company.subcontracting_location_id
    )
    if not sub_loc:
        return failures + ["No subcontracting location resolvable"]

    qty_a = env["stock.quant"]._get_available_quantity(
        part_a, sub_loc, allow_negative=True,
    )
    qty_b = env["stock.quant"]._get_available_quantity(
        part_b, sub_loc, allow_negative=True,
    )
    if abs(qty_a - 0.0) > 0.001:
        failures.append(
            f"Part-A available qty at subcontracting location is {qty_a}, "
            f"expected 0.0 (seed was +{ORDER_QTY}, should have back-flushed)"
        )
    if abs(qty_b - 0.0) > 0.001:
        failures.append(
            f"Part-B available qty at subcontracting location is {qty_b}, "
            f"expected 0.0 (seed was +{ORDER_QTY}, should have back-flushed)"
        )

    # ------------------------------------------------------------------
    # 5. stock.lot records for the serials
    # ------------------------------------------------------------------
    for sn in EXPECTED_SERIALS:
        lot = env["stock.lot"].search([
            ("name", "=", sn),
            ("product_id", "=", finished.id),
        ], limit=1)
        if not lot:
            failures.append(
                f"stock.lot record '{sn}' for '{FINISHED_NAME}' was not created"
            )

    return failures
