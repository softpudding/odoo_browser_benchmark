"""Seed a sale_project closed-loop handoff task."""


TARGET_REF = "SERV-PROJ-17"
DISTRACTOR_REF = "SERV-PROJ-18"


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
    if template:
        template.write({
            "name": name,
            "list_price": price,
            "type": "service",
            "invoice_policy": "delivery",
            "service_type": "manual",
            "service_tracking": "task_in_project",
            "uom_id": hour_uom.id,
        })
        return template.product_variant_id

    template = env["product.template"].create({
        "name": name,
        "default_code": code,
        "list_price": price,
        "type": "service",
        "invoice_policy": "delivery",
        "service_type": "manual",
        "service_tracking": "task_in_project",
        "uom_id": hour_uom.id,
    })
    return template.product_variant_id


def setup(env):
    env["sale.order"].search([("client_order_ref", "in", [TARGET_REF, DISTRACTOR_REF])]).unlink()

    implementation = _ensure_service_product(
        env, "Implementation Sprint Service", "SERV-PROJ-IMP", 180.0
    )
    training = _ensure_service_product(
        env, "Training Workshop Service", "SERV-PROJ-TRN", 120.0
    )
    support = _ensure_service_product(
        env, "Support Audit Service", "SERV-PROJ-SUP", 90.0
    )

    target_partner = _ensure_partner(env, "Bluebird Labs", "ops@bluebird.example.com")
    distractor_partner = _ensure_partner(env, "Bluebird Systems", "west@bluebird.example.com")

    target_order = env["sale.order"].create({
        "partner_id": target_partner.id,
        "client_order_ref": TARGET_REF,
    })
    env["sale.order.line"].create({
        "order_id": target_order.id,
        "product_id": implementation.id,
        "product_uom_qty": 6,
        "price_unit": implementation.list_price,
        "name": "Implementation stream",
    })
    env["sale.order.line"].create({
        "order_id": target_order.id,
        "product_id": training.id,
        "product_uom_qty": 4,
        "price_unit": training.list_price,
        "name": "Training stream",
    })

    distractor_order = env["sale.order"].create({
        "partner_id": distractor_partner.id,
        "client_order_ref": DISTRACTOR_REF,
    })
    env["sale.order.line"].create({
        "order_id": distractor_order.id,
        "product_id": support.id,
        "product_uom_qty": 2,
        "price_unit": support.list_price,
        "name": "Support audit stream",
    })
