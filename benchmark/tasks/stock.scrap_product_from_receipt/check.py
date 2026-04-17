"""Postcondition checks for stock.scrap_product_from_receipt."""


def check(env):
    ref = "BENCH-SCRAP-REC-01"
    picking = env["stock.picking"].search([("origin", "=", ref)], limit=1)
    if not picking:
        return [f"Receipt {ref} not found"]

    scraps = env["stock.scrap"].search([("picking_id", "=", picking.id)])
    if len(scraps) != 1:
        return [f"Expected exactly one scrap linked to the receipt, found {len(scraps)}"]

    scrap = scraps[0]
    failures = []
    if scrap.product_id.display_name != 'Steel Bracket 12"':
        failures.append(f"Scrapped product is {scrap.product_id.display_name!r}")
    if abs(scrap.scrap_qty - 2.0) > 0.01:
        failures.append(f"Scrap quantity is {scrap.scrap_qty}, expected 2.0")
    if scrap.state != "done":
        failures.append(f"Scrap state is {scrap.state!r}, expected 'done'")
    return failures
