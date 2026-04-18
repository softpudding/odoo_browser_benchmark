"""Postcondition checks for sale.create_quotation_with_customer_pricelist.

Validates:
1. A draft (state='draft') sale.order for 'Bench Premium Co' exists.
2. That SO has pricelist_id == 'VIP 20% Off'.
3. It has exactly one order line: product 'Bench Standard Widget', qty 5.
4. Line price_unit reflects the 20% discount: 80.00 (list_price 100 - 20%).
5. No additional sale.order was created for 'Bench Regular Co' or other
   distractors tied to this task.
"""


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", "Bench Premium Co")], limit=1)
    if not partner:
        return ["Customer 'Bench Premium Co' not found"]

    product = env["product.product"].search(
        [("name", "=", "Bench Standard Widget")], limit=1
    )
    if not product:
        return ["Product 'Bench Standard Widget' not found"]

    pricelist = env["product.pricelist"].search([("name", "=", "VIP 20% Off")], limit=1)
    if not pricelist:
        return ["Pricelist 'VIP 20% Off' not found"]

    orders = env["sale.order"].search([("partner_id", "=", partner.id)])
    if not orders:
        return ["No sale.order found for 'Bench Premium Co'"]

    # Prefer a draft quotation
    drafts = orders.filtered(lambda o: o.state == "draft")
    if not drafts:
        failures.append(
            f"No draft quotation for 'Bench Premium Co'; found states={sorted(set(orders.mapped('state')))}"
        )
        return failures

    if len(drafts) > 1:
        failures.append(
            f"Expected exactly 1 draft quotation for 'Bench Premium Co', found {len(drafts)}"
        )

    so = drafts[0]

    # Pricelist check
    if not so.pricelist_id:
        failures.append("Quotation has no pricelist set")
    elif so.pricelist_id.id != pricelist.id:
        failures.append(
            f"Quotation pricelist is '{so.pricelist_id.name}', expected 'VIP 20% Off'"
        )

    # Line checks
    lines = so.order_line
    if len(lines) != 1:
        failures.append(f"Expected 1 order line, found {len(lines)}")
        return failures

    line = lines[0]
    if line.product_id.id != product.id:
        failures.append(
            f"Line product is '{line.product_id.name}', expected 'Bench Standard Widget'"
        )
    if line.product_uom_qty != 5:
        failures.append(
            f"Line quantity is {line.product_uom_qty}, expected 5"
        )
    # Accept 80.00 exactly, ±0.01 for float noise
    if abs(line.price_unit - 80.0) > 0.01:
        failures.append(
            f"Line unit price is {line.price_unit}, expected 80.00 (20% off 100.00)"
        )

    # Distractor: no SO for Bench Regular Co
    regular = env["res.partner"].search([("name", "=", "Bench Regular Co")], limit=1)
    if regular:
        reg_orders = env["sale.order"].search([("partner_id", "=", regular.id)])
        if reg_orders:
            failures.append(
                f"Unexpected sale.order(s) created for 'Bench Regular Co': {len(reg_orders)}"
            )

    return failures
