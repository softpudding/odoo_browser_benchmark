"""Cleanup for stock.package_products_validate_delivery."""


def cleanup(env):
    env["stock.picking"].search([("origin", "in", ["BENCH-PACK-DEL-01", "BENCH-PACK-DEL-OTHER"])]).unlink()
    env["product.template"].search([("name", "in", ["Packed Valve Kit", "Packed Sensor Cable"])]).unlink()
