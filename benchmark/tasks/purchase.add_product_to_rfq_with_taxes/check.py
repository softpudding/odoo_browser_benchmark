"""Postcondition checks for purchase.add_product_to_rfq_with_taxes.

Validates:
1. Vendor 'Bench Tax Vendor' and both products still exist.
2. Purchase order 'BENCH-ADD-TAX' still exists, state='draft', same vendor.
3. PO has exactly 2 lines:
   - Original line: Bench Other Item, product_qty=2, no taxes (unchanged)
   - New line: Bench Taxable Item, product_qty=3, tax_ids contains
     Bench Tax 5%
4. Tax 'Bench Tax 5%' still exists with the seeded config.
5. No extra POs were created for Bench Tax Vendor.
"""

VENDOR_NAME = "Bench Tax Vendor"
PO_NAME = "BENCH-ADD-TAX"
PRODUCT_EXISTING = "Bench Other Item"
PRODUCT_NEW = "Bench Taxable Item"
TAX_NAME = "Bench Tax 5%"
EXPECTED_EXISTING_QTY = 2
EXPECTED_NEW_QTY = 3


def _close(a, b, tol=1e-6):
    return abs((a or 0.0) - (b or 0.0)) <= tol


def check(env):
    failures = []

    vendor = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    prod_existing = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_EXISTING)], limit=1
    )
    if not prod_existing:
        failures.append(f"Product '{PRODUCT_EXISTING}' not found")
    prod_new = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NEW)], limit=1
    )
    if not prod_new:
        failures.append(f"Product '{PRODUCT_NEW}' not found")

    tax = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", TAX_NAME),
    ], limit=1)
    if not tax:
        failures.append(f"Tax '{TAX_NAME}' not found")

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
        failures.append(
            f"PO state is '{po.state}', expected 'draft' — did agent confirm?"
        )

    lines = po.order_line
    if len(lines) != 2:
        failures.append(
            f"Expected exactly 2 order lines, found {len(lines)} "
            f"(products: {lines.mapped('product_id.display_name')})"
        )
        return failures

    # Partition by product.
    orig_line = lines.filtered(
        lambda l, _p=prod_existing: l.product_id.id == (_p.id if _p else 0)
    )
    new_line = lines.filtered(
        lambda l, _p=prod_new: l.product_id.id == (_p.id if _p else 0)
    )

    if not orig_line:
        failures.append(
            f"Original '{PRODUCT_EXISTING}' line missing — agent may have "
            f"replaced or deleted it"
        )
    elif len(orig_line) != 1:
        failures.append(
            f"Expected 1 line for '{PRODUCT_EXISTING}', found {len(orig_line)}"
        )
    else:
        ln = orig_line
        if not _close(ln.product_qty, EXPECTED_EXISTING_QTY):
            failures.append(
                f"Original line ({PRODUCT_EXISTING}) product_qty is "
                f"{ln.product_qty}, expected {EXPECTED_EXISTING_QTY} "
                f"(unchanged line)"
            )
        if ln.tax_ids:
            failures.append(
                f"Original line ({PRODUCT_EXISTING}) now has taxes "
                f"{ln.tax_ids.mapped('name')}; expected none — agent added "
                f"the tax on the WRONG row"
            )

    if not new_line:
        failures.append(
            f"New '{PRODUCT_NEW}' line not found — agent did not add the "
            f"taxable product line"
        )
    elif len(new_line) != 1:
        failures.append(
            f"Expected 1 new line for '{PRODUCT_NEW}', found {len(new_line)}"
        )
    else:
        ln = new_line
        if not _close(ln.product_qty, EXPECTED_NEW_QTY):
            failures.append(
                f"New line ({PRODUCT_NEW}) product_qty is {ln.product_qty}, "
                f"expected {EXPECTED_NEW_QTY}"
            )
        if tax and tax.id not in ln.tax_ids.ids:
            failures.append(
                f"New line ({PRODUCT_NEW}) tax_ids is "
                f"{ln.tax_ids.mapped('name')}; expected to contain "
                f"'{TAX_NAME}'"
            )

    return failures
