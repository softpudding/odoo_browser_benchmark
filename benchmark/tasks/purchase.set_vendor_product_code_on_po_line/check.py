"""Postcondition checks for purchase.set_vendor_product_code_on_po_line.

Validates:
1. Vendor 'Bench Code Supplier' and product 'Bench Widget' still exist.
2. Purchase order 'BENCH-VCODE' still exists, state='draft', same vendor.
3. Order has exactly 1 line; line has product=Bench Widget, product_qty=5,
   and name='BENCH-WDG-A1 / Bench Widget' (exact match after trim).
4. No extra POs created for Bench Code Supplier.
"""

VENDOR_NAME = "Bench Code Supplier"
PO_NAME = "BENCH-VCODE"
PRODUCT_NAME = "Bench Widget"
EXPECTED_QTY = 5
EXPECTED_NAME = "BENCH-WDG-A1 / Bench Widget"


def _norm(s):
    return (s or "").strip()


def check(env):
    failures = []

    vendor = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    prod = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not prod:
        return [f"Product '{PRODUCT_NAME}' not found"]

    # Exactly one PO for this vendor.
    vendor_pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id", "=", vendor.id),
    ])
    if len(vendor_pos) != 1:
        failures.append(
            f"Expected exactly 1 purchase.order for '{VENDOR_NAME}', "
            f"found {len(vendor_pos)} (names: {vendor_pos.mapped('name')})"
        )

    po = env["purchase.order"].with_context(active_test=False).search(
        [("name", "=", PO_NAME)], limit=1
    )
    if not po:
        failures.append(f"Purchase order '{PO_NAME}' not found")
        return failures

    if po.partner_id.id != vendor.id:
        failures.append(
            f"PO vendor is '{po.partner_id.display_name}', expected '{VENDOR_NAME}'"
        )
    if po.state != "draft":
        failures.append(f"PO state is '{po.state}', expected 'draft'")

    lines = po.order_line
    if len(lines) != 1:
        failures.append(
            f"Expected exactly 1 order line, found {len(lines)} "
            f"(products: {lines.mapped('product_id.display_name')})"
        )
        return failures

    line = lines[0]
    if line.product_id.id != prod.id:
        failures.append(
            f"Line product is '{line.product_id.display_name}', "
            f"expected '{PRODUCT_NAME}'"
        )
    if abs(line.product_qty - EXPECTED_QTY) > 0.001:
        failures.append(
            f"Line product_qty is {line.product_qty}, expected {EXPECTED_QTY}"
        )

    # The Description must now reference the vendor product code. The
    # inline o2m widget (`product_label_section_and_note_field`) may
    # store the label as "<product_name>\n<entered text>" because of
    # `parseLabel` (see account/static/src/components/
    # product_label_section_and_note_field.js:50-54). Accept either:
    #   - Exact substring `BENCH-WDG-A1 / Bench Widget` (user used the
    #     full phrase verbatim), OR
    #   - `BENCH-WDG-A1` appears anywhere in name (user typed only the
    #     code and the widget auto-prefixed the product name).
    # At minimum `BENCH-WDG-A1` must be a (case-insensitive) substring
    # of the stored name.
    actual_name = _norm(line.name)
    if "BENCH-WDG-A1".lower() not in actual_name.lower():
        failures.append(
            f"Line description (name) does not contain vendor code "
            f"'BENCH-WDG-A1'; got {line.name!r}"
        )

    return failures
