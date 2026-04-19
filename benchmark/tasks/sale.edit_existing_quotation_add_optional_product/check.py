"""Postcondition checks for sale.edit_existing_quotation_add_optional_product.

Validates:
1. Products `Bench Existing Item` / `Bench Extra Item` and partner
   `Bench Add Co` still exist.
2. Quotation `BENCH-ADD-LINE` still exists, state='draft', same customer,
   and exactly 2 order lines.
3. Existing line: Bench Existing Item qty=2, price_unit=30.0, unchanged.
4. New line: Bench Extra Item qty=4, price_unit=15.0.
5. amount_untaxed = amount_total = 2*30 + 4*15 = 120.0 (no taxes).
6. Exactly 1 sale.order row for Bench Add Co (no dup quotations).
"""

PARTNER_NAME = "Bench Add Co"
SO_NAME = "BENCH-ADD-LINE"
PRODUCT_EXISTING = "Bench Existing Item"
PRODUCT_EXTRA = "Bench Extra Item"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    product_existing = env["product.product"].search(
        [("name", "=", PRODUCT_EXISTING)], limit=1
    )
    product_extra = env["product.product"].search(
        [("name", "=", PRODUCT_EXTRA)], limit=1
    )
    if not product_existing:
        return [f"Product '{PRODUCT_EXISTING}' not found"]
    if not product_extra:
        return [f"Product '{PRODUCT_EXTRA}' not found"]

    # Exactly one SO for this customer (no duplicates created)
    partner_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", partner.id)]
    )
    if len(partner_orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_NAME}', "
            f"found {len(partner_orders)} (names: {partner_orders.mapped('name')})"
        )

    so = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)], limit=1
    )
    if not so:
        failures.append(f"Quotation '{SO_NAME}' not found")
        return failures

    if so.partner_id.id != partner.id:
        failures.append(
            f"SO customer is '{so.partner_id.display_name}', expected '{PARTNER_NAME}'"
        )
    if so.state != "draft":
        failures.append(
            f"SO state is '{so.state}', expected 'draft' (did you click Confirm?)"
        )

    lines = so.order_line
    if len(lines) != 2:
        failures.append(
            f"Expected exactly 2 order lines (1 existing + 1 new), found {len(lines)} "
            f"(products: {lines.mapped('product_id.name')}, "
            f"display_types: {lines.mapped('display_type')})"
        )
        return failures

    # Partition by product. Only product lines (display_type unset) are
    # expected — no section / note rows in this task.
    if any(l.display_type for l in lines):
        failures.append(
            "At least one line has a non-empty display_type "
            f"({[(l.product_id.display_name, l.display_type) for l in lines]}); "
            "the task requires two PRODUCT lines only, no sections / notes."
        )

    by_product = {l.product_id.id: l for l in lines}

    # --- Existing line: UNTOUCHED ---
    if product_existing.id not in by_product:
        failures.append(f"Missing line for product '{PRODUCT_EXISTING}'")
    else:
        le = by_product[product_existing.id]
        if abs(le.product_uom_qty - 2) > 0.001:
            failures.append(
                f"'{PRODUCT_EXISTING}' qty is {le.product_uom_qty}, "
                f"expected 2 (must not be modified)"
            )
        if abs(le.price_unit - 30.0) > 0.01:
            failures.append(
                f"'{PRODUCT_EXISTING}' price_unit is {le.price_unit}, "
                f"expected 30.0 (must not be modified)"
            )

    # --- New line: Bench Extra Item qty=4 price=15 ---
    if product_extra.id not in by_product:
        failures.append(
            f"Missing NEW line for product '{PRODUCT_EXTRA}' — "
            "did you pick the right product in the 'Add a product' row?"
        )
    else:
        lx = by_product[product_extra.id]
        if abs(lx.product_uom_qty - 4) > 0.001:
            failures.append(
                f"'{PRODUCT_EXTRA}' qty is {lx.product_uom_qty}, expected 4 "
                "(did you change the default qty=1 on the new row?)"
            )
        if abs(lx.price_unit - 15.0) > 0.01:
            failures.append(
                f"'{PRODUCT_EXTRA}' price_unit is {lx.price_unit}, expected 15.0 "
                "(must not be overridden; it is the product list_price)"
            )

    # --- amount_untaxed must reflect both lines ---
    # 2*30 + 4*15 = 60 + 60 = 120
    if abs(so.amount_untaxed - 120.0) > 0.01:
        failures.append(
            f"SO amount_untaxed is {so.amount_untaxed}, expected 120.0 "
            f"(2*30 + 4*15 = 60 + 60)"
        )
    if abs(so.amount_total - 120.0) > 0.01:
        failures.append(
            f"SO amount_total is {so.amount_total}, expected 120.0 "
            "(no taxes → equals amount_untaxed)"
        )

    return failures
