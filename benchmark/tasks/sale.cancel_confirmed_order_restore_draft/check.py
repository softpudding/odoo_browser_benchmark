"""Postcondition checks for sale.cancel_confirmed_order_restore_draft.

Validates:
1. Products and partner still exist.
2. The BENCH-CANCEL-RESTORE sale.order for Bench Cancel Co is in
   state='draft' (NOT 'cancel', 'sale', 'sent').
3. The order still has the same 2 lines (A qty=2, B qty=3).
4. Exactly 1 sale.order exists for Bench Cancel Co.
"""

PARTNER_NAME = "Bench Cancel Co"
CLIENT_REF = "BENCH-CANCEL-RESTORE"
PRODUCT_A = "Bench Cancel Item A"
PRODUCT_B = "Bench Cancel Item B"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    product_a = env["product.product"].search([("name", "=", PRODUCT_A)], limit=1)
    product_b = env["product.product"].search([("name", "=", PRODUCT_B)], limit=1)
    if not product_a:
        return [f"Product '{PRODUCT_A}' not found"]
    if not product_b:
        return [f"Product '{PRODUCT_B}' not found"]

    # --- Find the sale order by client_order_ref ---
    order = env["sale.order"].with_context(active_test=False).search(
        [("client_order_ref", "=", CLIENT_REF)], limit=1
    )
    if not order:
        failures.append(
            f"Sale order with client_order_ref='{CLIENT_REF}' not found"
        )
        return failures

    if order.partner_id.id != partner.id:
        failures.append(
            f"Order customer is '{order.partner_id.display_name}', "
            f"expected '{PARTNER_NAME}'"
        )

    if order.state != "draft":
        failures.append(
            f"Order state is '{order.state}', expected 'draft' "
            f"(must cancel then click Set to Quotation to reset)"
        )

    # Order lines should still be the seeded pair, untouched
    lines = order.order_line
    if len(lines) != 2:
        failures.append(
            f"Order expected 2 order_line rows, found {len(lines)}"
        )
    else:
        by_product = {l.product_id.id: l for l in lines}
        if product_a.id not in by_product:
            failures.append(f"Missing line for '{PRODUCT_A}'")
        elif abs(by_product[product_a.id].product_uom_qty - 2) > 0.001:
            failures.append(
                f"'{PRODUCT_A}' qty is {by_product[product_a.id].product_uom_qty}, expected 2"
            )
        if product_b.id not in by_product:
            failures.append(f"Missing line for '{PRODUCT_B}'")
        elif abs(by_product[product_b.id].product_uom_qty - 3) > 0.001:
            failures.append(
                f"'{PRODUCT_B}' qty is {by_product[product_b.id].product_uom_qty}, expected 3"
            )

    # Total rows tied to this partner
    partner_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", partner.id)]
    )
    if len(partner_orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_NAME}', "
            f"found {len(partner_orders)} (names: {partner_orders.mapped('name')})"
        )

    return failures
