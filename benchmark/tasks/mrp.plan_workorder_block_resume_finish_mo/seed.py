"""Seed for mrp.plan_workorder_block_resume_finish_mo."""


def setup(env):
    admin = env.ref("base.user_admin")
    routings_group = env.ref("mrp.group_mrp_routings")
    if routings_group not in admin.group_ids:
        admin.write({"group_ids": [(4, routings_group.id)]})

    env["mrp.production"].search([("name", "=", "WH/MO/BENCH-WO-01")]).unlink()
    env["mrp.bom"].search([("product_tmpl_id.name", "in", ["Bench Workorder Unit", "Bench Workorder Component"])]).unlink()
    env["product.template"].search([("name", "in", ["Bench Workorder Unit", "Bench Workorder Component"])]).unlink()
    env["mrp.workcenter"].search([("name", "=", "Benchmark Workcell Alpha")]).unlink()

    warehouse = env["stock.warehouse"].search([], limit=1)
    component = env["product.product"].create({
        "name": "Bench Workorder Component",
        "type": "consu",
        "is_storable": True,
    })
    finished = env["product.product"].create({
        "name": "Bench Workorder Unit",
        "type": "consu",
        "is_storable": True,
    })
    workcenter = env["mrp.workcenter"].create({
        "name": "Benchmark Workcell Alpha",
        "resource_calendar_id": env.ref("resource.resource_calendar_std").id,
        "time_start": 0.0,
        "time_stop": 24.0,
    })
    bom = env["mrp.bom"].create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1.0,
        "type": "normal",
        "consumption": "flexible",
        "operation_ids": [(0, 0, {
            "name": "Assembly Run",
            "workcenter_id": workcenter.id,
            "time_cycle_manual": 15.0,
        })],
    })
    env["mrp.bom.line"].create({
        "bom_id": bom.id,
        "product_id": component.id,
        "product_qty": 2.0,
    })

    env["stock.quant"].with_context(inventory_mode=True).create({
        "product_id": component.id,
        "location_id": warehouse.lot_stock_id.id,
        "inventory_quantity": 20.0,
    }).action_apply_inventory()

    mo = env["mrp.production"].create({
        "name": "WH/MO/BENCH-WO-01",
        "product_id": finished.id,
        "product_qty": 3.0,
        "bom_id": bom.id,
    })
    mo.action_confirm()
