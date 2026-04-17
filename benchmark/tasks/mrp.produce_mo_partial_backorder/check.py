"""Postconditions for mrp.produce_mo_partial_backorder.

After a partial produce + Create Backorder, Odoo renames the original MO
to `<name>-001` (the produced portion, now done) and creates a sibling
`<name>-002` backorder for the remainder.

Validates:
1. Exactly one 'done' MO for Bench Chassis Z with qty_produced == 6.
2. Exactly one 'confirmed' (or 'progress') MO with product_qty == 4
   and qty_produced == 0 — the backorder.
3. Total MOs for Bench Chassis Z == 2 (no stray MOs created).
"""


def check(env):
    failures = []

    MO = env["mrp.production"]
    Product = env["product.product"]

    chassis = Product.search([("name", "=", "Bench Chassis Z")], limit=1)
    if not chassis:
        return ["Product 'Bench Chassis Z' not found — seed did not run"]

    all_mos = MO.search([("product_id", "=", chassis.id)])

    if len(all_mos) != 2:
        failures.append(
            f"Expected 2 MOs for 'Bench Chassis Z' (produced + backorder), "
            f"found {len(all_mos)}: {all_mos.mapped('name')}"
        )

    done_mos = all_mos.filtered(lambda m: m.state == "done")
    open_mos = all_mos.filtered(lambda m: m.state in ("confirmed", "progress", "to_close"))

    if len(done_mos) != 1:
        failures.append(
            f"Expected exactly one 'done' MO, found {len(done_mos)}"
        )
    else:
        d = done_mos[0]
        if d.qty_produced != 6.0:
            failures.append(
                f"Done MO qty_produced is {d.qty_produced}, expected 6.0 — "
                f"agent likely did not change Quantity Producing to 6"
            )
        if d.product_qty != 6.0:
            failures.append(
                f"Done MO product_qty is {d.product_qty}, expected 6.0 "
                f"(after backorder split)"
            )

    if len(open_mos) != 1:
        failures.append(
            f"Expected exactly one 'confirmed' backorder MO, found "
            f"{len(open_mos)} — agent likely chose 'No Backorder'"
        )
    else:
        b = open_mos[0]
        if b.product_qty != 4.0:
            failures.append(
                f"Backorder MO product_qty is {b.product_qty}, expected 4.0"
            )
        if b.qty_produced != 0.0:
            failures.append(
                f"Backorder MO qty_produced is {b.qty_produced}, expected 0.0"
            )

    return failures
