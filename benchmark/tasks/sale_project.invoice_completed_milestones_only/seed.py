"""Seed a sale_project milestone-based 'invoice 2 of 4 already-reached' task.

Category: side-effect trap (wizard auto-quantity).

Creates a confirmed sales order S-BENCH-MS-002 for "Bench Quad Milestone
Client" with 1 line of "Bench Quad Milestone Service" (qty=4, price=500)
where the service product uses service_policy='delivered_milestones' and
service_tracking='task_in_project'. After confirmation, the auto-generated
project is normalized to contain exactly 4 milestones linked to the SO line:

    - "M1 Setup"   (is_reached=True,  deadline 2026-04-01)
    - "M2 Build"   (is_reached=True,  deadline 2026-05-01)
    - "M3 Test"    (is_reached=False, deadline 2026-06-01)
    - "M4 Launch"  (is_reached=False, deadline 2026-07-01)

Each milestone delivers 1/4 of the line, so qty_delivered=2 (M1+M2 reached)
and the Create Invoice wizard auto-fills quantity_to_invoice=2.

Difficulty design: the agent must NOT touch the milestones (they are already
in the right state). The Create Invoice wizard's auto-detected qty=2 is the
trap -- agents often re-enter or override the qty, or assume "all 4" because
they see four lines. The correct action is to accept the wizard default.
"""

PARTNER_NAME = "Bench Quad Milestone Client"
PRODUCT_NAME = "Bench Quad Milestone Service"
PRODUCT_CODE = "SERV-BENCH-MS-Q"
SO_REF = "S-BENCH-MS-002"

MILESTONES = [
    ("M1 Setup", "2026-04-01", True),
    ("M2 Build", "2026-05-01", True),
    ("M3 Test", "2026-06-01", False),
    ("M4 Launch", "2026-07-01", False),
]


def _ensure_module(env):
    module = env["ir.module.module"].search([("name", "=", "sale_project")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def _cleanup(env):
    # Remove prior runs: invoices, SO, milestones, project, partner, product.
    orders = env["sale.order"].search([("client_order_ref", "=", SO_REF)])
    for order in orders:
        for invoice in order.invoice_ids.filtered(
            lambda m: m.move_type == "out_invoice"
        ):
            if invoice.state == "posted":
                invoice.button_draft()
            invoice.unlink()
        for project in order.project_ids:
            env["project.milestone"].search([("project_id", "=", project.id)]).unlink()
            env["project.task"].search([("project_id", "=", project.id)]).unlink()
            project.unlink()
        if order.state == "sale":
            order.action_cancel()
        order.unlink()

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        leftover_invoices = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ])
        for inv in leftover_invoices:
            if inv.state == "posted":
                inv.button_draft()
            inv.unlink()

    product = env["product.product"].search([("default_code", "=", PRODUCT_CODE)], limit=1)
    if product:
        leftover_milestones = env["project.milestone"].search([
            ("sale_line_id.product_id", "=", product.id),
        ])
        leftover_milestones.unlink()


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    vals = {
        "email": "billing@quadmilestone.example.com",
        "customer_rank": 1,
    }
    if partner:
        partner.write(vals)
        return partner
    vals["name"] = PARTNER_NAME
    return env["res.partner"].create(vals)


def _ensure_product(env):
    template = env["product.template"].search([("default_code", "=", PRODUCT_CODE)], limit=1)
    vals = {
        "name": PRODUCT_NAME,
        "default_code": PRODUCT_CODE,
        "list_price": 500.0,
        "standard_price": 500.0,
        "type": "service",
        "invoice_policy": "delivery",
        "service_type": "milestones",
        "service_tracking": "task_in_project",
    }
    if template:
        template.write(vals)
        return template.product_variant_id
    template = env["product.template"].create(vals)
    return template.product_variant_id


def setup(env):
    _ensure_module(env)
    _cleanup(env)

    partner = _ensure_partner(env)
    product = _ensure_product(env)

    order = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": SO_REF,
    })
    line = env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": product.id,
        "product_uom_qty": 4.0,
        "price_unit": 500.0,
        "name": "Bench Quad Milestone Service - 4 milestones",
        "tax_ids": [(5, 0, 0)],
    })

    order.action_confirm()

    project = order.project_ids[:1]
    if not project:
        project = env["project.project"].create({
            "name": f"{PARTNER_NAME} - {PRODUCT_NAME}",
            "partner_id": partner.id,
            "allow_milestones": True,
            "sale_line_id": line.id,
        })
    else:
        project = project[0]
        project.write({"allow_milestones": True})

    # Wipe any auto-generated milestones for deterministic seed state.
    env["project.milestone"].search([("project_id", "=", project.id)]).unlink()

    # Each milestone is 1/4 of the line; M1 + M2 reached -> qty_delivered=2.
    for name, deadline, reached in MILESTONES:
        env["project.milestone"].create({
            "name": name,
            "project_id": project.id,
            "sale_line_id": line.id,
            "deadline": deadline,
            "is_reached": reached,
            "quantity_percentage": 0.25,
        })
