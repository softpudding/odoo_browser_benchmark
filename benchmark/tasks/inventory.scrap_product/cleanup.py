"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["stock.scrap"].search([("product_id.name", "=", "Steel Bracket 12\"")]).unlink()