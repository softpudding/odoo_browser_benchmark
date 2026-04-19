"""Postcondition checks for sale.create_sale_quotation_from_opportunity_smart_button.

Validates:
1. A draft (state='draft') sale.order exists for 'Bench Opp Co'.
2. That sale.order is linked to the opportunity 'Bench Opp Sale' via
   `opportunity_id` — the key evidence that the agent used the Quotations
   smart button on the opportunity (which sets `default_opportunity_id`).
3. Exactly one order line: product 'Bench Opp Product', qty=2, price 100.00.
4. Opportunity fields were not disturbed (partner, revenue, type).
"""


OPP_NAME = "Bench Opp Sale"
PARTNER_NAME = "Bench Opp Co"
PRODUCT_NAME = "Bench Opp Product"
EXPECTED_REVENUE = 10000.0


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    lead = env["crm.lead"].with_context(active_test=False).search(
        [("name", "=", OPP_NAME)], limit=1
    )
    if not lead:
        return [f"Opportunity '{OPP_NAME}' not found"]

    # --- Opportunity guardrails (unchanged by the task) ---
    if lead.type != "opportunity":
        failures.append(f"Opportunity type is '{lead.type}', expected 'opportunity'")
    if not lead.partner_id or lead.partner_id.id != partner.id:
        actual = lead.partner_id.name if lead.partner_id else None
        failures.append(
            f"Opportunity partner is '{actual}', expected '{PARTNER_NAME}'"
        )
    if abs((lead.expected_revenue or 0.0) - EXPECTED_REVENUE) > 0.01:
        failures.append(
            f"Opportunity expected revenue is {lead.expected_revenue}, expected {EXPECTED_REVENUE}"
        )

    # --- Locate the newly-created quotation ---
    orders_by_opp = env["sale.order"].search([("opportunity_id", "=", lead.id)])
    if not orders_by_opp:
        failures.append(
            f"No sale.order linked to opportunity '{OPP_NAME}' (opportunity_id). "
            "Did the agent use the Quotations smart button on the opportunity?"
        )
        return failures

    if len(orders_by_opp) > 1:
        failures.append(
            f"Expected exactly 1 sale.order for opportunity '{OPP_NAME}', "
            f"found {len(orders_by_opp)}"
        )

    so = orders_by_opp[0]

    # --- Partner check ---
    if not so.partner_id or so.partner_id.id != partner.id:
        actual = so.partner_id.name if so.partner_id else None
        failures.append(
            f"Quotation partner is '{actual}', expected '{PARTNER_NAME}'"
        )

    # --- State: must remain a draft quotation ---
    if so.state != "draft":
        failures.append(
            f"Quotation state is '{so.state}', expected 'draft'"
        )

    # --- Lines: exactly one Bench Opp Product qty=2 ---
    lines = so.order_line
    if len(lines) != 1:
        failures.append(
            f"Expected exactly 1 order line, found {len(lines)}"
        )
        return failures
    line = lines[0]
    if line.product_id.id != product.id:
        failures.append(
            f"Line product is '{line.product_id.name}', expected '{PRODUCT_NAME}'"
        )
    if abs(line.product_uom_qty - 2.0) > 1e-6:
        failures.append(
            f"Line qty is {line.product_uom_qty}, expected 2"
        )
    if abs(line.price_unit - 100.0) > 0.01:
        failures.append(
            f"Line unit price is {line.price_unit}, expected 100.00"
        )

    # --- No extra sale.orders for this partner (beyond the one above) ---
    orders_by_partner = env["sale.order"].search([("partner_id", "=", partner.id)])
    stray = orders_by_partner.filtered(lambda o: o.id != so.id)
    if stray:
        failures.append(
            f"Unexpected extra sale.order(s) for '{PARTNER_NAME}': "
            f"found {len(stray)} besides the task's quotation"
        )

    return failures
