"""Cleanup for repair.cancel_repair_log_internal_reason."""


def cleanup(env):
    env["repair.order"].search([("name", "=", "RO/CANCEL/0001")]).unlink()
    env["product.template"].search(
        [("name", "in", ["Bench Cooler Compressor", "Bench Cooler Belt"])]
    ).unlink()
