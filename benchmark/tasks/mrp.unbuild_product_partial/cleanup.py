"""Clean up mrp.unbuild_product_partial artifacts."""


def cleanup(env):
    env["mrp.unbuild"].search([("product_id.display_name", "=", "Field Controller Kit")]).unlink()
    env["mrp.bom"].search([("code", "=", "BOM-FCK-UNBUILD")]).unlink()
