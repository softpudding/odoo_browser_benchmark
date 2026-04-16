"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["sale.order"].search([("client_order_ref", "=", "BENCH-VALID-01")]).unlink()
