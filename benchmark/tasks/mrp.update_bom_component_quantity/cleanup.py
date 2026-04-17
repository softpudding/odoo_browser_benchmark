"""Clean up mrp.update_bom_component_quantity artifacts."""


def cleanup(env):
    env["mrp.bom"].search([("code", "=", "BOM-BENCH-MIXER")]).unlink()

