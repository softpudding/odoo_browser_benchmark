"""Cleanup for stock_barcode.receive_via_barcode_scan_validate.

BLOCKED TASK — `stock_barcode` addon is not installed in this Community
checkout, so there is nothing to clean up. The guard below turns this
into a no-op that stays safe if the module ever becomes available
without the rest of the task being fleshed out.
"""


def cleanup(env):
    module = env["ir.module.module"].search(
        [("name", "=", "stock_barcode")], limit=1
    )
    if not module or module.state != "installed":
        return

    # Once the enterprise addon is vendored, cleanup would look like:
    #
    # pickings = env["stock.picking"].with_context(active_test=False).search(
    #     [("name", "=", "R-BENCH-BC-001")]
    # )
    # for picking in pickings:
    #     if picking.state not in ("done", "cancel"):
    #         picking.action_cancel()
    # pickings.sudo().unlink()
    # env["product.product"].with_context(active_test=False).search(
    #     [("default_code", "in", ["BENCH-A-001", "BENCH-B-002"])]
    # ).sudo().unlink()
