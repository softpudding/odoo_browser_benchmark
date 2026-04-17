"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["purchase.order"].search([("origin", "=", "BENCH-NOTE-01")]).unlink()
