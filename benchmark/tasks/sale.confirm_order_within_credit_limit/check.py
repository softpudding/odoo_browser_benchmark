"""Postcondition checks for sale.confirm_order_within_credit_limit."""


TARGET_SUBJECT = "Atlas credit-cleared quotation"
TARGET_BODY = "Please review the adjusted quotation within the remaining credit allowance."
REQUIRED_RECIPIENTS = {
    "billing@atlas-field.example.com",
    "creditdesk@atlas-field.example.com",
}


def check(env):
    failures = []

    target = env["sale.order"].search(
        [("client_order_ref", "=", "CREDIT-OPS-09")], limit=1
    )
    distractor = env["sale.order"].search(
        [("client_order_ref", "=", "CREDIT-OPS-08")], limit=1
    )
    if not target:
        return ["Target quotation CREDIT-OPS-09 not found"]
    if not distractor:
        return ["Distractor quotation CREDIT-OPS-08 not found"]

    if target.partner_id.name != "Atlas Field Systems":
        failures.append(
            f"Target quotation partner is {target.partner_id.name!r}, expected 'Atlas Field Systems'"
        )
    if target.state != "sale":
        failures.append(f"Target quotation state is {target.state!r}, expected 'sale'")
    if str(target.validity_date) != "2026-05-22":
        failures.append(
            f"Target quotation expiration is {target.validity_date!r}, expected '2026-05-22'"
        )

    expected_lines = {
        "Field Router Kit": {"qty": 3.0, "price": 400.0},
        "On-site Commissioning": {"qty": 1.0, "price": 1100.0},
    }
    product_lines = target.order_line.filtered(lambda l: l.product_id)
    if len(product_lines) != 2:
        failures.append(
            f"Target quotation has {len(product_lines)} product lines, expected 2"
        )
    for line in product_lines:
        exp = expected_lines.get(line.product_id.name)
        if exp is None:
            failures.append(f"Unexpected target line {line.product_id.name!r}")
            continue
        if abs(float(line.product_uom_qty or 0.0) - exp["qty"]) > 0.001:
            failures.append(
                f"{line.product_id.name} qty is {line.product_uom_qty}, expected {exp['qty']}"
            )
        if abs(float(line.price_unit or 0.0) - exp["price"]) > 0.001:
            failures.append(
                f"{line.product_id.name} unit price is {line.price_unit}, expected {exp['price']}"
            )

    if target.client_order_ref != "CREDIT-OPS-09":
        failures.append(
            f"Target quotation customer reference is {target.client_order_ref!r}, expected 'CREDIT-OPS-09'"
        )

    if abs(float(target.amount_total or 0.0) - 2300.0) > 0.001:
        failures.append(f"Target quotation total is {target.amount_total}, expected 2300.0")

    if target.partner_credit_warning:
        failures.append("Target quotation still shows a partner credit warning")

    messages = env["mail.message"].search(
        [
            ("model", "=", "sale.order"),
            ("res_id", "=", target.id),
            ("subject", "=", TARGET_SUBJECT),
        ],
        order="id desc",
    )
    if not messages:
        failures.append("Target quotation is missing the expected sent email message")
    else:
        if TARGET_BODY.lower() not in (messages[0].body or "").lower():
            failures.append("Target quotation email body does not contain the expected text")
        recipient_emails = {
            email for email in messages[0].partner_ids.mapped("email") if email
        }
        missing = REQUIRED_RECIPIENTS - recipient_emails
        if missing:
            failures.append(
                f"Target quotation email recipients missing expected email(s): {sorted(missing)}"
            )
        extra = recipient_emails - REQUIRED_RECIPIENTS
        if extra:
            failures.append(
                f"Target quotation email recipients include unexpected email(s): {sorted(extra)}"
            )
        if "creditdesk@atlas-fleet.example.com" in recipient_emails:
            failures.append("Distractor fleet credit contact was included on the target quotation email")

    if distractor.state != "draft":
        failures.append(f"Distractor quotation state changed to {distractor.state!r}")

    distractor_lines = {
        "Field Router Kit": {"qty": 2.0, "price": 400.0},
        "On-site Commissioning": {"qty": 1.0, "price": 1100.0},
    }
    for line in distractor.order_line.filtered(lambda l: l.product_id):
        exp = distractor_lines.get(line.product_id.name)
        if exp is None:
            continue
        if abs(float(line.product_uom_qty or 0.0) - exp["qty"]) > 0.001:
            failures.append(
                f"Distractor line {line.product_id.name} qty changed to {line.product_uom_qty}"
            )
        if abs(float(line.price_unit or 0.0) - exp["price"]) > 0.001:
            failures.append(
                f"Distractor line {line.product_id.name} price changed to {line.price_unit}"
            )

    return failures
