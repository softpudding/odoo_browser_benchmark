"""Clean up mrp.create_mo_consume_produce_done artifacts."""


def cleanup(env):
    mos = env["mrp.production"].search([("product_id.display_name", "=", "Bench Power Pack")])
    for mo in mos:
        if mo.state != "cancel":
            mo.action_cancel()
        mo.unlink()
    env["mrp.bom"].search([("code", "=", "BOM-BPP-01")]).unlink()

