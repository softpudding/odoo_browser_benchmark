"""Postcondition checks for mrp.unbuild_product_back_to_components.

Validates:
  * Exactly one mrp.unbuild for Bench Assembly.
  * Unbuild state='done', mo_id is False (product-driven unbuild),
    product_qty=2.0.
  * stock.quant on WH/Stock post-state:
      - Bench Assembly on-hand = 0 (2 were consumed)
      - Bench Screw on-hand >= 6 (2 x 3 returned)
      - Bench Housing on-hand >= 2 (2 x 1 returned)
  * No extra MOs were created for these products.
"""

FINISHED = "Bench Assembly"
SCREW = "Bench Screw"
HOUSING = "Bench Housing"


def _on_hand(env, product_name, location):
    product = env["product.product"].search(
        [("name", "=", product_name)], limit=1
    )
    if not product:
        return None
    return env["stock.quant"]._get_available_quantity(product, location)


def check(env):
    failures = []

    Unbuild = env["mrp.unbuild"]
    Product = env["product.product"]

    finished = Product.search([("name", "=", FINISHED)], limit=1)
    if not finished:
        return [f"Finished product {FINISHED!r} not found"]

    unbuilds = Unbuild.search([("product_id", "=", finished.id)])
    if not unbuilds:
        return failures + [
            f"No mrp.unbuild found for product {FINISHED!r} — the task "
            "requires creating and validating an unbuild order."
        ]
    if len(unbuilds) > 1:
        failures.append(
            f"Expected exactly 1 unbuild for {FINISHED!r}, "
            f"found {len(unbuilds)}: {unbuilds.mapped('name')}"
        )

    u = unbuilds[0]
    if u.state != "done":
        failures.append(
            f"Unbuild {u.name} state is {u.state!r}, expected 'done' "
            "(the Unbuild / Validate button must be clicked)"
        )
    if u.mo_id:
        failures.append(
            f"Unbuild is linked to Manufacturing Order "
            f"{u.mo_id.display_name!r}; the task requires a product-driven "
            "unbuild with Manufacturing Order left blank."
        )
    if abs((u.product_qty or 0.0) - 2.0) > 1e-6:
        failures.append(
            f"Unbuild quantity is {u.product_qty}, expected 2.0"
        )
    if u.product_id.id != finished.id:
        failures.append(
            f"Unbuild product is {u.product_id.name!r}, "
            f"expected {FINISHED!r}"
        )

    # --- Stock deltas at WH/Stock ---
    warehouse = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    stock_loc = warehouse.lot_stock_id

    fin_on_hand = _on_hand(env, FINISHED, stock_loc)
    if fin_on_hand is None:
        failures.append(f"Product {FINISHED!r} missing")
    elif abs(fin_on_hand - 0.0) > 1e-6:
        failures.append(
            f"{FINISHED} on-hand at WH/Stock is {fin_on_hand}, expected 0 "
            "(2 units should have been consumed by the unbuild)"
        )

    screw_on_hand = _on_hand(env, SCREW, stock_loc)
    if screw_on_hand is None:
        failures.append(f"Product {SCREW!r} missing")
    elif screw_on_hand < 6.0 - 1e-6:
        failures.append(
            f"{SCREW} on-hand at WH/Stock is {screw_on_hand}, expected "
            ">= 6 (3 per assembly x 2 unbuilt)"
        )

    housing_on_hand = _on_hand(env, HOUSING, stock_loc)
    if housing_on_hand is None:
        failures.append(f"Product {HOUSING!r} missing")
    elif housing_on_hand < 2.0 - 1e-6:
        failures.append(
            f"{HOUSING} on-hand at WH/Stock is {housing_on_hand}, expected "
            ">= 2 (1 per assembly x 2 unbuilt)"
        )

    # --- No stray MOs for any of these products ---
    extra_mos = env["mrp.production"].search([
        ("product_id.name", "in", [FINISHED, SCREW, HOUSING]),
    ])
    if extra_mos:
        failures.append(
            f"Unexpected manufacturing order(s) created: "
            f"{extra_mos.mapped('name')} — the task requires a direct "
            "unbuild with no linked MO."
        )

    return failures
