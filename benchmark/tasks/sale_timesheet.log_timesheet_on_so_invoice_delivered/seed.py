"""Seed for sale_timesheet.log_timesheet_on_so_invoice_delivered.

Category: cross-module workflow (Sale -> auto-generated Task -> Timesheets
-> return to SO -> Create Invoice wizard with non-default-sibling radio).

Creates a confirmed sales order S-BENCH-TS-001 for 'Bench Services Co' with
a single line for the service product 'Bench Consulting'. The product uses:

    service_policy = 'delivered_timesheet'
        (= invoice_policy='delivery' + service_type='timesheet')
    service_tracking = 'task_in_project'

so confirmation auto-creates a `project.project` + a single
`project.task` whose timesheet hours drive `sale.order.line.qty_delivered`.

The seed also creates a distractor service product 'Bench Widget Supply'
with `service_policy='delivered_manual'` (delivery-based manual qty) to
harden the calibration — agent must NOT touch that product.
"""

PARTNER_NAME = "Bench Services Co"
SERVICE_NAME = "Bench Consulting"
SERVICE_CODE = "SERV-BENCH-TS"
DISTRACTOR_NAME = "Bench Widget Supply"
DISTRACTOR_CODE = "SERV-BENCH-MAN"
SO_REF = "S-BENCH-TS-001"


def _ensure_modules(env):
    """sale_timesheet pulls in hr_timesheet; neither is in base snapshot."""
    for mod_name in ("hr_timesheet", "sale_timesheet"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            try:
                mod.button_immediate_install()
            except Exception:
                # Partial install should not abort the seed; later code
                # will raise a clear error if the bridge fields are missing.
                pass


def _cleanup(env):
    # Drop any prior invoices, SOs, tasks, projects, products, partner.
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        leftover_invoices = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ])
        for inv in leftover_invoices:
            if inv.state == "posted":
                inv.button_draft()
            inv.sudo().unlink()

    orders = env["sale.order"].search([("client_order_ref", "=", SO_REF)])
    for order in orders:
        for invoice in order.invoice_ids.filtered(
            lambda m: m.move_type == "out_invoice"
        ):
            if invoice.state == "posted":
                invoice.button_draft()
            invoice.sudo().unlink()
        for project in order.project_ids:
            env["account.analytic.line"].search([
                ("project_id", "=", project.id),
            ]).sudo().unlink()
            env["project.task"].search([
                ("project_id", "=", project.id),
            ]).sudo().unlink()
            project.sudo().unlink()
        if order.state == "sale":
            order.action_cancel()
        order.sudo().unlink()

    # Stale products from prior runs
    for code in (SERVICE_CODE, DISTRACTOR_CODE):
        prod = env["product.product"].search([("default_code", "=", code)], limit=1)
        if prod:
            tmpl = prod.product_tmpl_id
            prod.sudo().unlink()
            if tmpl.exists():
                tmpl.sudo().unlink()


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        partner.write({
            "email": "billing@benchservices.example.com",
            "customer_rank": 1,
        })
        return partner
    return env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "billing@benchservices.example.com",
        "customer_rank": 1,
    })


def _ensure_service_product(env):
    """Service product with service_policy='delivered_timesheet'."""
    vals = {
        "name": SERVICE_NAME,
        "default_code": SERVICE_CODE,
        "list_price": 150.0,
        "standard_price": 100.0,
        "type": "service",
        # delivered_timesheet is stored via invoice_policy + service_type
        # (see _get_service_to_general_map in sale_timesheet product model).
        "invoice_policy": "delivery",
        "service_type": "timesheet",
        "service_tracking": "task_in_project",
        "taxes_id": [(5, 0, 0)],
    }
    template = env["product.template"].create(vals)
    # Hours UoM auto-assigned by onchange when service_type='timesheet';
    # ensure it anyway for deterministic create path.
    hour_uom = env.ref("uom.product_uom_hour", raise_if_not_found=False)
    if hour_uom and template.uom_id != hour_uom:
        template.write({"uom_id": hour_uom.id})
    return template.product_variant_id


def _ensure_distractor_product(env):
    """Distractor: delivered_manual service (invoice_policy='delivery',
    service_type='manual'). Same delivery-based invoicing but manual qty —
    tests that the agent doesn't accidentally log hours against this one."""
    vals = {
        "name": DISTRACTOR_NAME,
        "default_code": DISTRACTOR_CODE,
        "list_price": 50.0,
        "standard_price": 25.0,
        "type": "service",
        "invoice_policy": "delivery",
        "service_type": "manual",
        "service_tracking": "no",
        "taxes_id": [(5, 0, 0)],
    }
    template = env["product.template"].create(vals)
    return template.product_variant_id


def setup(env):
    _ensure_modules(env)
    _cleanup(env)

    partner = _ensure_partner(env)
    service = _ensure_service_product(env)
    # Distractor is created but NOT linked to the SO; it just sits in the
    # catalog as a trap so the agent can misread the prompt.
    _ensure_distractor_product(env)

    # Ensure admin has hr_timesheet user group so the Timesheets tab is
    # visible on the task form (the tab has `groups="hr_timesheet.group_hr_timesheet_user"`).
    admin = env.ref("base.user_admin")
    ts_grp = env.ref("hr_timesheet.group_hr_timesheet_user", raise_if_not_found=False)
    if ts_grp and admin.id not in ts_grp.user_ids.ids:
        ts_grp.sudo().write({"user_ids": [(4, admin.id)]})

    order = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": SO_REF,
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": service.id,
        "product_uom_qty": 10.0,
        "price_unit": 150.0,
        "name": "Bench Consulting - 10h engagement",
        "tax_ids": [(5, 0, 0)],
    })

    # Confirming triggers _timesheet_service_generation() which creates a
    # project + a single task tied to the SO line (service_tracking='task_in_project').
    order.action_confirm()

    # Sanity check: the auto-generated project + task must exist.
    assert order.project_ids, (
        f"Seed: SO {SO_REF} did not auto-generate a project; check service_tracking."
    )
    project = order.project_ids[0]
    tasks = env["project.task"].search([("project_id", "=", project.id)])
    assert len(tasks) == 1, (
        f"Seed: expected exactly 1 task on auto-generated project, found {len(tasks)}"
    )

    # Make sure we have zero timesheet lines to start with (no qty_delivered yet).
    env["account.analytic.line"].search([
        ("project_id", "=", project.id),
    ]).sudo().unlink()

    env.cr.execute("SELECT 1")
