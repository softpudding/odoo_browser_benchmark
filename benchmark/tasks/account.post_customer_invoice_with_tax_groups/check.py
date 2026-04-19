"""Postcondition checks for account.post_customer_invoice_with_tax_groups.

Validates:
1. A new account.move with move_type='out_invoice' exists for customer
   'Bench Tax Cust' with invoice_date=2026-05-10.
2. State is 'posted' (agent clicked Confirm).
3. Exactly one product line: Bench Tax Service qty=1 price_unit=200.
4. Line's tax_ids contains 'Bench Sale Tax 20%' AND does NOT contain
   'Bench Sale Tax 10%' (the discrimination signal).
5. Invoice totals: amount_untaxed=200, amount_tax=40, amount_total=240.
6. No extra out_invoice records created for this customer (exactly one).
"""

from datetime import date


CUSTOMER_NAME = "Bench Tax Cust"
PRODUCT_NAME = "Bench Tax Service"
TAX_10_NAME = "Bench Sale Tax 10%"
TAX_20_NAME = "Bench Sale Tax 20%"
EXPECTED_DATE = date(2026, 5, 10)
EXPECTED_QTY = 1
EXPECTED_PRICE = 200.0
EXPECTED_UNTAXED = 200.0
EXPECTED_TAX = 40.0
EXPECTED_TOTAL = 240.0


def _close(a, b, tol=1e-2):
    return abs((a or 0.0) - (b or 0.0)) <= tol


def check(env):
    failures = []

    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not customer:
        return [f"Customer {CUSTOMER_NAME!r} not found"]

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        failures.append(f"Product {PRODUCT_NAME!r} not found")

    tax_10 = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", TAX_10_NAME),
    ], limit=1)
    tax_20 = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", TAX_20_NAME),
    ], limit=1)
    if not tax_10:
        failures.append(f"Tax {TAX_10_NAME!r} not found")
    if not tax_20:
        failures.append(f"Tax {TAX_20_NAME!r} not found")

    # Find the out_invoice for this customer. Use a defensive filter on
    # move_type to ignore any non-invoice moves (journal entries) that
    # might carry the same partner.
    invoices = env["account.move"].search([
        ("partner_id", "=", customer.id),
        ("move_type", "=", "out_invoice"),
    ])

    if not invoices:
        return failures + [
            f"No customer invoice (out_invoice) found for "
            f"{CUSTOMER_NAME!r}. Did the agent click New and save?"
        ]
    if len(invoices) > 1:
        failures.append(
            f"Expected exactly 1 customer invoice for {CUSTOMER_NAME!r}, "
            f"found {len(invoices)} "
            f"(names: {invoices.mapped('name')})"
        )

    # Most recent / highest id is the agent's run.
    inv = invoices.sorted(key=lambda m: m.id)[-1]

    # --- Gate 1: header values ---
    if inv.invoice_date != EXPECTED_DATE:
        failures.append(
            f"Invoice invoice_date is {inv.invoice_date!r}, "
            f"expected {EXPECTED_DATE!s} (05/10/2026)"
        )

    # --- Gate 2: posted ---
    if inv.state != "posted":
        failures.append(
            f"Invoice state is {inv.state!r}, expected 'posted' "
            f"(did the agent click Confirm?)"
        )

    # --- Gate 3: exactly one product line with the correct fields ---
    product_lines = inv.invoice_line_ids.filtered(
        lambda l: l.display_type in (False, "product") and l.product_id
    )
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line on the invoice, found "
            f"{len(product_lines)} "
            f"(products: {product_lines.mapped('product_id.display_name')}). "
            f"Agent may have added a phantom empty line or extras."
        )
        return failures

    line = product_lines[0]
    if product and line.product_id.id != product.id:
        failures.append(
            f"Invoice line product is {line.product_id.name!r}, "
            f"expected {PRODUCT_NAME!r}"
        )
    if not _close(line.quantity, EXPECTED_QTY, tol=1e-3):
        failures.append(
            f"Invoice line quantity is {line.quantity}, "
            f"expected {EXPECTED_QTY}"
        )
    if not _close(line.price_unit, EXPECTED_PRICE):
        failures.append(
            f"Invoice line price_unit is {line.price_unit}, "
            f"expected {EXPECTED_PRICE}"
        )

    # --- Gate 4: tax discrimination ---
    tax_names = set(line.tax_ids.mapped("name"))
    if tax_20 and tax_20.id not in line.tax_ids.ids:
        failures.append(
            f"Invoice line tax_ids is {sorted(tax_names)}; "
            f"expected to contain {TAX_20_NAME!r}. "
            f"Did the agent forget to set the tax, or pick the wrong one?"
        )
    if tax_10 and tax_10.id in line.tax_ids.ids:
        failures.append(
            f"Invoice line tax_ids contains {TAX_10_NAME!r} -- the agent "
            f"picked the WRONG tax. Expected only {TAX_20_NAME!r}."
        )

    # --- Gate 5: totals ---
    if not _close(inv.amount_untaxed, EXPECTED_UNTAXED):
        failures.append(
            f"Invoice amount_untaxed is {inv.amount_untaxed}, "
            f"expected {EXPECTED_UNTAXED}"
        )
    if not _close(inv.amount_tax, EXPECTED_TAX):
        failures.append(
            f"Invoice amount_tax is {inv.amount_tax}, "
            f"expected {EXPECTED_TAX} "
            f"(200.00 * 20% = 40.00 -- wrong tax would give 20.00 for "
            f"10% or 60.00 for both)"
        )
    if not _close(inv.amount_total, EXPECTED_TOTAL):
        failures.append(
            f"Invoice amount_total is {inv.amount_total}, "
            f"expected {EXPECTED_TOTAL}"
        )

    return failures
