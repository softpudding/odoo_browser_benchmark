"""Cleanup for mrp.plan_workorder_block_resume_finish_mo."""


def cleanup(env):
    env["mrp.production"].search([("name", "=", "WH/MO/BENCH-WO-01")]).unlink()
    env["mrp.bom"].search([("product_tmpl_id.name", "in", ["Bench Workorder Unit", "Bench Workorder Component"])]).unlink()
    env["product.template"].search([("name", "in", ["Bench Workorder Unit", "Bench Workorder Component"])]).unlink()
    env["mrp.workcenter"].search([("name", "=", "Benchmark Workcell Alpha")]).unlink()
