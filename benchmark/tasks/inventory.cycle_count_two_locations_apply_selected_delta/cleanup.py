"""Cleanup for inventory.cycle_count_two_locations_apply_selected_delta."""


def cleanup(env):
    product = env["product.product"].search([
        ("name", "=", "Bench Cycle Count Rotor"),
    ])
    if product:
        env["stock.quant"].search([("product_id", "in", product.ids)]).unlink()
        env["product.template"].search([("name", "=", "Bench Cycle Count Rotor")]).unlink()
