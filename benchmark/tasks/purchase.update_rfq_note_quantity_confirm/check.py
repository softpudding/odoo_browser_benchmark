"""Postcondition checks for purchase.update_rfq_note_quantity_confirm."""


def check(env):
    failures = []
    vendor = env["res.partner"].search([("name", "=", "North Coast Components")], limit=1)
    if not vendor:
        return ["Vendor 'North Coast Components' not found"]
    po = env["purchase.order"].search([("partner_id", "=", vendor.id), ("origin", "=", "MED-RFQ-NOTE-01")], limit=1)
    if not po:
        return ["Target RFQ 'MED-RFQ-NOTE-01' not found"]
    if po.state != "purchase":
        failures.append(f"PO state is '{po.state}', expected 'purchase'")
    if (po.notes or "").strip() != "Deliver dock seals in two labeled pallets.":
        failures.append(f"Notes are '{po.notes}', expected exact delivery note")
    line = po.order_line.filtered(lambda l: l.product_id.name == "Dock Seal Kit")
    if not line:
        failures.append("Dock Seal Kit line not found")
    else:
        if line.product_qty != 24:
            failures.append(f"Dock Seal Kit quantity is {line.product_qty}, expected 24")
        if line.price_unit != 85.0:
            failures.append(f"Dock Seal Kit price is {line.price_unit}, expected 85.0")
    distractor = env["purchase.order"].search([("partner_id", "=", vendor.id), ("origin", "=", "MED-RFQ-NOTE-02")], limit=1)
    if distractor and distractor.state != "draft":
        failures.append(f"Distractor RFQ state is '{distractor.state}', expected 'draft'")
    return failures
