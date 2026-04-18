"""Seed for maintenance.schedule_preventive_plan_recurring.

Creates equipment "Conveyor Belt CB-7" in category "Warehouse Gear" assigned
to team "Bench Maintenance" with expected_mtbf=0.

The agent must:
  - set expected_mtbf=120 on the equipment, then
  - create a new maintenance.request with maintenance_type='preventive'
    (non-default radio choice) and a 30-day recurrence.
"""


def _ensure_maintenance_module(env):
    module = env["ir.module.module"].search([("name", "=", "maintenance")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def setup(env):
    _ensure_maintenance_module(env)

    admin = env.ref("base.user_admin")

    user = env["res.users"].search([("login", "=", "demo")], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": "Marc Demo",
            "login": "demo",
            "password": "demo",
            "group_ids": [(4, env.ref("base.group_user").id)],
        })

    team = env["maintenance.team"].search([("name", "=", "Bench Maintenance")], limit=1)
    if not team:
        team = env["maintenance.team"].create({"name": "Bench Maintenance"})

    category = env["maintenance.equipment.category"].search([("name", "=", "Warehouse Gear")], limit=1)
    if not category:
        category = env["maintenance.equipment.category"].create({
            "name": "Warehouse Gear",
            "technician_user_id": user.id,
        })

    # Cleanup prior runs.
    env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Monthly Belt Inspection"),
    ]).unlink()

    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Conveyor Belt CB-7"),
    ]).unlink()

    env["maintenance.equipment"].create({
        "name": "Conveyor Belt CB-7",
        "category_id": category.id,
        "owner_user_id": admin.id,
        "technician_user_id": user.id,
        "maintenance_team_id": team.id,
        "expected_mtbf": 0,
    })
