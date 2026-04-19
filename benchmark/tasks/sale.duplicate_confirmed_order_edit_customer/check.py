"""Postcondition checks for sale.duplicate_confirmed_order_edit_customer.

Validates:
1. Partners `Bench Orig Co`, `Bench Clone Co` and both products still exist.
2. Original sale.order (client_order_ref='BENCH-DUP') is unchanged:
   state='sale', partner=Bench Orig Co, same two seeded lines.
3. A NEW draft sale.order exists for `Bench Clone Co` (the duplicate):
   state='draft', exactly 2 order lines matching the seeded products and
   quantities (copy_data carried the lines over from the original).
4. No SO for Bench Clone Co is in state='sale'/'sent'/'cancel' (copy must
   stay draft).
5. No stray SOs created for Bench Orig Co beyond the original.
"""

PARTNER_ORIG = "Bench Orig Co"
PARTNER_CLONE = "Bench Clone Co"
CLIENT_REF = "BENCH-DUP"
PRODUCT_A = "Bench SO Dup Item A"
PRODUCT_B = "Bench SO Dup Item B"


def _assert_two_lines(order, product_a, product_b, failures, label):
    lines = order.order_line
    if len(lines) != 2:
        failures.append(
            f"{label}: expected 2 order_line rows, found {len(lines)}"
        )
        return
    by_product = {l.product_id.id: l for l in lines}
    if product_a.id not in by_product:
        failures.append(f"{label}: missing line for '{PRODUCT_A}'")
    elif abs(by_product[product_a.id].product_uom_qty - 2) > 0.001:
        failures.append(
            f"{label}: '{PRODUCT_A}' qty is "
            f"{by_product[product_a.id].product_uom_qty}, expected 2"
        )
    if product_b.id not in by_product:
        failures.append(f"{label}: missing line for '{PRODUCT_B}'")
    elif abs(by_product[product_b.id].product_uom_qty - 3) > 0.001:
        failures.append(
            f"{label}: '{PRODUCT_B}' qty is "
            f"{by_product[product_b.id].product_uom_qty}, expected 3"
        )


def check(env):
    failures = []

    orig_partner = env["res.partner"].search(
        [("name", "=", PARTNER_ORIG)], limit=1
    )
    clone_partner = env["res.partner"].search(
        [("name", "=", PARTNER_CLONE)], limit=1
    )
    if not orig_partner:
        return [f"Customer '{PARTNER_ORIG}' not found"]
    if not clone_partner:
        return [f"Customer '{PARTNER_CLONE}' not found"]

    product_a = env["product.product"].search(
        [("name", "=", PRODUCT_A)], limit=1
    )
    product_b = env["product.product"].search(
        [("name", "=", PRODUCT_B)], limit=1
    )
    if not product_a:
        return [f"Product '{PRODUCT_A}' not found"]
    if not product_b:
        return [f"Product '{PRODUCT_B}' not found"]

    # --- Original must still exist and be unchanged ---
    original = env["sale.order"].with_context(active_test=False).search(
        [("client_order_ref", "=", CLIENT_REF)], limit=1
    )
    if not original:
        failures.append(
            f"Original sale.order with client_order_ref='{CLIENT_REF}' "
            f"is missing (it must not be deleted)"
        )
    else:
        if original.partner_id.id != orig_partner.id:
            failures.append(
                f"Original customer is '{original.partner_id.display_name}', "
                f"expected '{PARTNER_ORIG}' (original must NOT be edited)"
            )
        if original.state != "sale":
            failures.append(
                f"Original state is '{original.state}', expected 'sale' "
                f"(original must NOT be cancelled, reset, or re-confirmed)"
            )
        _assert_two_lines(original, product_a, product_b, failures, "Original")

    # --- Find the duplicate: a different sale.order for Bench Clone Co ---
    clone_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", clone_partner.id)]
    )

    if not clone_orders:
        failures.append(
            f"No duplicate sale.order found for '{PARTNER_CLONE}' — the "
            f"copy's Customer field should be '{PARTNER_CLONE}'"
        )
        return failures

    if len(clone_orders) > 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_CLONE}', found "
            f"{len(clone_orders)} (names: {clone_orders.mapped('name')})"
        )

    dup = clone_orders[0]

    if dup.state != "draft":
        failures.append(
            f"Duplicate state is '{dup.state}', expected 'draft' "
            f"(do NOT confirm the copy)"
        )

    # Duplicate must NOT carry the source's client_order_ref (copy=False),
    # and the agent was not instructed to type a new one, so it should
    # be empty / False.
    if dup.client_order_ref:
        failures.append(
            f"Duplicate client_order_ref is {dup.client_order_ref!r}, "
            f"expected empty (sale.order.client_order_ref has copy=False)"
        )

    _assert_two_lines(dup, product_a, product_b, failures, "Duplicate")

    # --- Original partner should still have exactly 1 SO ---
    orig_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", orig_partner.id)]
    )
    if len(orig_orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_ORIG}', found "
            f"{len(orig_orders)} (names: {orig_orders.mapped('name')})"
        )

    return failures
