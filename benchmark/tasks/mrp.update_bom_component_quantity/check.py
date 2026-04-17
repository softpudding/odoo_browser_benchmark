"""Postcondition checks for mrp.update_bom_component_quantity."""


def check(env):
    bom = env["mrp.bom"].search([("code", "=", "BOM-BENCH-MIXER")], limit=1)
    if not bom:
        return ["BoM BOM-BENCH-MIXER not found"]

    failures = []
    motor_line = bom.bom_line_ids.filtered(lambda l: l.product_id.display_name == "Motor Module")
    housing_line = bom.bom_line_ids.filtered(lambda l: l.product_id.display_name == "Aluminum Housing")
    if not housing_line:
        failures.append("Aluminum Housing line not found")
    elif abs(housing_line[0].product_qty - 3.0) > 0.01:
        failures.append(f"Aluminum Housing qty is {housing_line[0].product_qty}, expected 3.0")
    if not motor_line:
        failures.append("Motor Module line not found")
    elif abs(motor_line[0].product_qty - 1.0) > 0.01:
        failures.append(f"Motor Module qty changed to {motor_line[0].product_qty}, expected 1.0")
    return failures
