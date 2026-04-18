"""Seed a sale_project milestone-based partial-delivery invoicing task.

Category: cross-module workflow (Project milestones -> Sales -> Invoice wizard).

Creates a confirmed sales order S-BENCH-MS-001 for "Bench Milestone Client"
with 1 line of "Bench Milestone Service" (qty=3, price=1000) where the
service product uses service_policy='delivered_milestones' and
service_tracking='task_in_project'. After confirmation, the auto-generated
project is normalized to contain exactly 3 milestones linked to the SO line:

    - "Design Phase"  (deadline 2026-05-01)
    - "Build Phase"   (deadline 2026-05-15)
    - "Launch Phase"  (deadline 2026-06-01)

All 3 milestones start with is_reached=False and quantity_percentage=1/3 so
that reaching exactly one milestone produces qty_delivered=1 on the SO line
and the Create Invoice wizard auto-fills quantity_to_invoice=1.
"""

PARTNER_NAME = "Bench Milestone Client"
PRODUCT_NAME = "Bench Milestone Service"
PRODUCT_CODE = "SERV-BENCH-MS"
SO_REF = "S-BENCH-MS-001"

MILESTONES = [
    ("Design Phase", "2026-05-01"),
    ("Build Phase", "2026-05-15"),
    ("Launch Phase", "2026-06-01"),
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

    # Belt-and-suspenders: kill any leftover invoices/milestones/projects/partner
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
    if partner:
        partner.write({
            "email": "billing@benchmilestone.example.com",
            "customer_rank": 1,
        })
        return partner
    return env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "billing@benchmilestone.example.com",
        "customer_rank": 1,
    })


def _ensure_product(env):
    template = env["product.template"].search([("default_code", "=", PRODUCT_CODE)], limit=1)
    vals = {
        "name": PRODUCT_NAME,
        "default_code": PRODUCT_CODE,
        "list_price": 1000.0,
        "standard_price": 1000.0,
        "type": "service",
        # service_policy='delivered_milestones' is computed from
        # invoice_policy='delivery' + service_type='milestones'.
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
        "product_uom_qty": 3.0,
        "price_unit": 1000.0,
        "name": "Bench Milestone Service - 3 milestones",
        "tax_ids": [(5, 0, 0)],
    })

    # Confirming the SO triggers _handle_milestones() which creates a project
    # (because service_tracking='task_in_project') and may auto-create or
    # auto-adopt one milestone for the SO line.
    order.action_confirm()

    project = order.project_ids[:1]
    if not project:
        # Defensive: if no project was generated, create one.
        project = env["project.project"].create({
            "name": f"{PARTNER_NAME} - {PRODUCT_NAME}",
            "partner_id": partner.id,
            "allow_milestones": True,
            "sale_line_id": line.id,
        })
    else:
        project = project[0]
        project.write({"allow_milestones": True})

    # Wipe any auto-generated milestones on this project so the seed state is
    # deterministic (exactly the 3 milestones described in the prompt).
    env["project.milestone"].search([("project_id", "=", project.id)]).unlink()

    # Each milestone delivers 1/3 of the line so reaching one milestone yields
    # qty_delivered = 1 (since product_uom_qty=3).
    for name, deadline in MILESTONES:
        env["project.milestone"].create({
            "name": name,
            "project_id": project.id,
            "sale_line_id": line.id,
            "deadline": deadline,
            "is_reached": False,
            "quantity_percentage": 1.0 / 3.0,
        })
