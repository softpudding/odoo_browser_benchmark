"""Postcondition checks for sale.configure_pricelist_apply_to_order_line.

Validates:
1. Pricelist 'Bench 10% Off' exists with at least one rule that has:
   - applied_on == '3_global' (All Products)
   - compute_price == 'formula'
   - abs(price_discount - 10.0) <= 0.001 (10% off)
2. A draft sale.order for 'Bench Price Co' exists with
   pricelist_id -> 'Bench 10% Off'.
3. That SO has exactly one order line: product 'Bench Price Item', qty=1,
   price_unit == 180.00 (200 * (1 - 10/100)).
"""

PARTNER_NAME = "Bench Price Co"
PRODUCT_NAME = "Bench Price Item"
PRICELIST_NAME = "Bench 10% Off"


def check(env):
    failures = []

    # ---- Product / partner existence ----
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    # ---- Pricelist ----
    pricelists = env["product.pricelist"].with_context(active_test=False).search(
        [("name", "=", PRICELIST_NAME)]
    )
    if not pricelists:
        failures.append(f"Pricelist '{PRICELIST_NAME}' not found")
        return failures
    if len(pricelists) > 1:
        failures.append(
            f"Expected exactly 1 pricelist named '{PRICELIST_NAME}', found {len(pricelists)}"
        )
    pricelist = pricelists[0]

    items = pricelist.item_ids
    if not items:
        failures.append(f"Pricelist '{PRICELIST_NAME}' has no rules (item_ids empty)")
    else:
        # Require at least one rule matching the formula / 10% / global spec
        matches = items.filtered(
            lambda it: (
                it.applied_on == "3_global"
                and it.compute_price == "formula"
                and abs(it.price_discount - 10.0) <= 0.001
            )
        )
        if not matches:
            descs = []
            for it in items:
                descs.append(
                    f"(applied_on={it.applied_on}, compute_price={it.compute_price}, "
                    f"price_discount={it.price_discount}, percent_price={it.percent_price}, "
                    f"fixed_price={it.fixed_price}, base={it.base})"
                )
            failures.append(
                "Pricelist rule not configured as Formula/10%/AllProducts. "
                "Got: " + "; ".join(descs)
            )

    # ---- Sale Order ----
    orders = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", partner.id),
    ])
    if not orders:
        failures.append(f"No sale.order found for '{PARTNER_NAME}'")
        return failures

    drafts = orders.filtered(lambda o: o.state == "draft")
    if not drafts:
        failures.append(
            f"No draft quotation for '{PARTNER_NAME}'; "
            f"order states found: {sorted(set(orders.mapped('state')))}"
        )
        return failures
    if len(drafts) > 1:
        failures.append(
            f"Expected exactly 1 draft quotation for '{PARTNER_NAME}', found {len(drafts)}"
        )

    so = drafts[0]

    # Pricelist on SO
    if not so.pricelist_id:
        failures.append("Quotation has no pricelist set")
    elif so.pricelist_id.id != pricelist.id:
        failures.append(
            f"Quotation pricelist is '{so.pricelist_id.name}', expected '{PRICELIST_NAME}'"
        )

    # Lines
    lines = so.order_line
    product_lines = lines.filtered(lambda l: not l.display_type)
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product order line, found {len(product_lines)} "
            f"(total lines including sections/notes: {len(lines)})"
        )
        return failures

    extras = lines - product_lines
    if extras:
        types = sorted(set(extras.mapped("display_type")))
        failures.append(
            f"SO has unexpected non-product lines ({types}); "
            "expected only 1 plain product line"
        )

    line = product_lines[0]
    if line.product_id.id != product.id:
        failures.append(
            f"Line product is '{line.product_id.name}', expected '{PRODUCT_NAME}'"
        )
    if abs(line.product_uom_qty - 1.0) > 0.001:
        failures.append(
            f"Line quantity is {line.product_uom_qty}, expected 1"
        )
    # Accept 180.00 exactly, ±0.01 for float noise
    if abs(line.price_unit - 180.0) > 0.01:
        failures.append(
            f"Line unit price is {line.price_unit}, expected 180.00 "
            f"(10% off 200.00 via pricelist formula)"
        )

    return failures
