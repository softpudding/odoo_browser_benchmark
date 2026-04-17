"""Postcondition checks for stock.receive_serial_tracked_product."""


def check(env):
    ref = "BENCH-SERIAL-REC-01"
    picking = env["stock.picking"].search([("origin", "=", ref)], limit=1)
    if not picking:
        return [f"Receipt {ref} not found"]

    failures = []
    if picking.state != "done":
        failures.append(f"Receipt state is {picking.state!r}, expected 'done'")

    serials = env["stock.move.line"].search([
        ("picking_id", "=", picking.id),
        ("quantity", "=", 1.0),
        ("lot_id", "!=", False),
    ])
    names = sorted(serials.mapped("lot_id.name"))
    expected = ["CSX-001", "CSX-002", "CSX-003"]
    if names != expected:
        failures.append(f"Serial numbers are {names!r}, expected {expected!r}")
    return failures
