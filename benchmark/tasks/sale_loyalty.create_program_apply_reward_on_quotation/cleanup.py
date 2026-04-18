"""Cleanup for sale_loyalty.create_program_apply_reward_on_quotation."""


def cleanup(env):
    env["sale.order"].search([("client_order_ref", "=", "HARBOR-LOYALTY-01")]).unlink()
    env["loyalty.program"].search([("name", "=", "Harbor 15% Quotation Reward")]).unlink()
    env["product.template"].search([("name", "=", "Harbor Signal Lamp")]).unlink()
