"""Postcondition checks for crm.create_opportunity_add_quotation_send.

Validates:
1. Opportunity exists with correct fields (revenue=45000, stage=Qualified).
2. Quotation exists linked to the opportunity.
3. Quotation has exactly 2 lines with correct products/qty/price.
4. Customer reference = "PLG-Q2-2026".
5. Quotation state = 'sent' (email was sent).
6. Email subject matches expected value.
7. Distractor opportunity unchanged.
"""

PARTNER_NAME = "Pinnacle Logistics Group"
EXPECTED_REVENUE = 45000.0
CUSTOMER_REF = "PLG-Q2-2026"
EMAIL_SUBJECT = "Pinnacle Logistics - Warehouse Management Proposal"
DISTRACTOR_OPP = "Pinnacle Logistics Solutions - Fleet GPS"
DISTRACTOR_REVENUE = 18000.0

EXPECTED_LINES = {
    "Warehouse Management Module": {"product_uom_qty": 3.0, "price_unit": 8500.0},
    "Implementation Service": {"product_uom_qty": 1.0, "price_unit": 12000.0},
}


def check(env):
    failures = []

    # --- Opportunity checks ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    leads = env["crm.lead"].with_context(active_test=False).search([
        ("partner_id", "=", partner.id),
        ("type", "=", "opportunity"),
    ])
    if not leads:
        return [f"No opportunity found for partner '{PARTNER_NAME}'"]

    lead = leads[0]

    if not lead.stage_id or lead.stage_id.name != "Qualified":
        stage_name = lead.stage_id.name if lead.stage_id else "(none)"
        failures.append(
            f"Opportunity stage is '{stage_name}', expected 'Qualified'"
        )

    if abs((lead.expected_revenue or 0.0) - EXPECTED_REVENUE) > 0.01:
        failures.append(
            f"Opportunity expected_revenue={lead.expected_revenue}, "
            f"expected {EXPECTED_REVENUE}"
        )

    if lead.contact_name != "Derek Voss":
        failures.append(
            f"Opportunity contact_name is {lead.contact_name!r}, expected 'Derek Voss'"
        )

    # --- Quotation checks ---
    orders = env["sale.order"].search([
        ("client_order_ref", "=", CUSTOMER_REF),
    ])
    if not orders:
        # Try finding by opportunity link
        orders = env["sale.order"].search([
            ("opportunity_id", "=", lead.id),
        ])
        if orders:
            failures.append(
                f"Quotation found linked to opportunity but customer ref is "
                f"{orders[0].client_order_ref!r}, expected '{CUSTOMER_REF}'"
            )
        else:
            return failures + ["No quotation found with customer ref 'PLG-Q2-2026' or linked to opportunity"]

    so = orders[0]

    # Check link to opportunity
    if not so.opportunity_id or so.opportunity_id.id != lead.id:
        failures.append("Quotation is not linked to the target opportunity")

    # Check state = sent
    if so.state != "sent":
        failures.append(f"Quotation state is '{so.state}', expected 'sent'")

    # Check customer reference
    if so.client_order_ref != CUSTOMER_REF:
        failures.append(
            f"Customer reference is {so.client_order_ref!r}, expected '{CUSTOMER_REF}'"
        )

    # Check expiration date
    if str(so.validity_date) != "2026-07-01":
        failures.append(
            f"Expiration date is '{so.validity_date}', expected '2026-07-01'"
        )

    # Check order lines
    product_lines = so.order_line.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
        and l.product_id
    )

    if len(product_lines) != 2:
        failures.append(
            f"Expected 2 product lines, found {len(product_lines)} "
            f"(products: {[l.product_id.name for l in product_lines]})"
        )

    remaining = dict(EXPECTED_LINES)
    for line in product_lines:
        name = line.product_id.name
        if name not in remaining:
            failures.append(f"Unexpected product line: {name}")
            continue
        exp = remaining.pop(name)
        for field, val in exp.items():
            actual = getattr(line, field)
            if abs(actual - val) > 0.01:
                failures.append(f"{name}.{field}: expected {val}, got {actual}")

    for missing in remaining:
        failures.append(f"Missing product line: {missing}")

    # Check email subject on sent message
    messages = env["mail.message"].search([
        ("model", "=", "sale.order"),
        ("res_id", "=", so.id),
        ("subject", "=", EMAIL_SUBJECT),
    ], order="id desc")
    if not messages:
        failures.append(
            f"No sent email found with subject '{EMAIL_SUBJECT}'"
        )

    # --- Distractor checks ---
    distractor = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", DISTRACTOR_OPP),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor opportunity '{DISTRACTOR_OPP}' is missing")
    else:
        if abs((distractor.expected_revenue or 0.0) - DISTRACTOR_REVENUE) > 0.01:
            failures.append(
                f"Distractor revenue changed to {distractor.expected_revenue}, "
                f"expected {DISTRACTOR_REVENUE}"
            )

    return failures
