"""Seed a sale_project closed-loop rollout handoff task.

Category 1: Closed-loop cross-module workflow.
The agent must confirm a quotation, update the generated project,
then return to Sales to finish the originating order.
"""


TARGET_REF = "ROLL-PROJ-31"
LIVE_REF = "ROLL-PROJ-31-LIVE"
DISTRACTOR_REF = "ROLL-PROJ-32"


def _ensure_partner(env, name, email):
    partner = env["res.partner"].search([("name", "=", name)], limit=1)
    if partner:
        partner.write({"email": email})
        return partner
    return env["res.partner"].create({
        "name": name,
        "email": email,
    })


def _ensure_service_product(env, name, code, price):
    template = env["product.template"].search([("default_code", "=", code)], limit=1)
    hour_uom = env.ref("uom.product_uom_hour")
    values = {
        "name": name,
        "default_code": code,
        "list_price": price,
        "type": "service",
        "invoice_policy": "delivery",
        "service_type": "manual",
        "service_tracking": "task_in_project",
        "uom_id": hour_uom.id,
    }
    if template:
        template.write(values)
        return template.product_variant_id

    template = env["product.template"].create(values)
    return template.product_variant_id


def setup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", [TARGET_REF, LIVE_REF, DISTRACTOR_REF]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel"):
            order.unlink()

    discovery = _ensure_service_product(
        env, "Discovery Workshop Service", "ROLL-PROJ-DSC", 1500.0
    )
    golive = _ensure_service_product(
        env, "Go-Live Review Service", "ROLL-PROJ-GLR", 1200.0
    )
    audit = _ensure_service_product(
        env, "Site Audit Service", "ROLL-PROJ-AUD", 700.0
    )

    target_partner = _ensure_partner(
        env, "Atlas Retail Group", "ops@atlas-retail.example.com"
    )
    distractor_partner = _ensure_partner(
        env, "Atlas Retail Services", "west@atlas-retail.example.com"
    )

    target_order = env["sale.order"].create({
        "partner_id": target_partner.id,
        "client_order_ref": TARGET_REF,
    })
    env["sale.order.line"].create({
        "order_id": target_order.id,
        "product_id": discovery.id,
        "product_uom_qty": 8,
        "price_unit": discovery.list_price,
        "name": "Discovery Workshop",
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": target_order.id,
        "product_id": golive.id,
        "product_uom_qty": 6,
        "price_unit": golive.list_price,
        "name": "Go-Live Review",
        "tax_ids": [(5, 0, 0)],
    })

    distractor_order = env["sale.order"].create({
        "partner_id": distractor_partner.id,
        "client_order_ref": DISTRACTOR_REF,
    })
    env["sale.order.line"].create({
        "order_id": distractor_order.id,
        "product_id": audit.id,
        "product_uom_qty": 2,
        "price_unit": audit.list_price,
        "name": "Site Audit",
        "tax_ids": [(5, 0, 0)],
    })
