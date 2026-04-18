"""Cleanup for stock.scrap_specific_serial_unit."""

PRODUCT_NAME = "Bench Sensor Module"
SERIALS = ["SN-A001", "SN-A002", "SN-A003"]


def cleanup(env):
    env["stock.scrap"].search([("product_id.display_name", "=", PRODUCT_NAME)]).unlink()
    env["stock.move.line"].search([("product_id.display_name", "=", PRODUCT_NAME)]).unlink()
    env["stock.move"].search([("product_id.display_name", "=", PRODUCT_NAME)]).unlink()
    env["stock.lot"].search([
        ("name", "in", SERIALS),
        ("product_id.display_name", "=", PRODUCT_NAME),
    ]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
