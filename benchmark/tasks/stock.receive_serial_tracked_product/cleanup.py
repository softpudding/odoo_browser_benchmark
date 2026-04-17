"""Clean up stock.receive_serial_tracked_product artifacts."""


def cleanup(env):
    ref = "BENCH-SERIAL-REC-01"
    env["stock.lot"].search([("name", "in", ["CSX-001", "CSX-002", "CSX-003"])]).unlink()
    picks = env["stock.picking"].search([("origin", "=", ref)])
    for pick in picks:
        if pick.state not in ("cancel", "done"):
            pick.action_cancel()
        pick.unlink()
