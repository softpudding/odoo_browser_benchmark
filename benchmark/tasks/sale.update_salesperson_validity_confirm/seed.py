"""Seed data for sale.update_salesperson_validity_confirm."""

PARTNER_NAME = "Cedar Grove Studio"
TARGET_ORDER = "S-QUOTE-VAL-01"
DISTRACTOR_ORDER = "S-QUOTE-VAL-02"


def _cleanup(env):
    orders = env["sale.order"].search([("name", "in", [TARGET_ORDER, DISTRACTOR_ORDER])])
    for order in orders:
        for inv in order.invoice_ids:
            if inv.state == "posted":
                inv.button_draft()
            inv.unlink()
        if order.state == "sale":
            order.action_cancel()
        if order.state == "cancel":
            order.action_draft()
        order.unlink()


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "customer_rank": 1,
        })
    return partner


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({"list_price": price})
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "list_price": price,
    })
    return tmpl.product_variant_id


def _ensure_salesperson(env):
    user = env["res.users"].search([("login", "=", "marc.demo")], limit=1)
    if user:
        internal = env.ref("base.group_user", raise_if_not_found=False)
        sales = env.ref("sales_team.group_sale_salesman", raise_if_not_found=False)
        groups = [g.id for g in (internal, sales) if g]
        if groups:
            user.write({"group_ids": [(4, gid) for gid in groups]})
        return user

    partner = env["res.partner"].search([("name", "=", "Marc Demo")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Marc Demo",
            "email": "marc.demo@example.com",
        })
    vals = {
        "name": "Marc Demo",
        "login": "marc.demo",
        "partner_id": partner.id,
    }
    internal = env.ref("base.group_user", raise_if_not_found=False)
    sales = env.ref("sales_team.group_sale_salesman", raise_if_not_found=False)
    groups = [g.id for g in (internal, sales) if g]
    if groups:
        vals["group_ids"] = [(6, 0, groups)]
    return env["res.users"].create(vals)


def _make_order(env, partner, user, name):
    order = env["sale.order"].create({
        "name": name,
        "partner_id": partner.id,
        "user_id": user.id,
    })
    products = [
        _ensure_product(env, "Studio Lighting Kit", 320.0),
        _ensure_product(env, "Backdrop Stand", 180.0),
    ]
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": products[0].id,
        "product_uom_qty": 3,
        "price_unit": 320.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": products[1].id,
        "product_uom_qty": 2,
        "price_unit": 180.0,
        "tax_ids": [(5, 0, 0)],
    })


def setup(env):
    _cleanup(env)

    partner = _ensure_partner(env)
    admin = env.ref("base.user_admin")
    _ensure_salesperson(env)
    _make_order(env, partner, admin, TARGET_ORDER)
    _make_order(env, partner, admin, DISTRACTOR_ORDER)
