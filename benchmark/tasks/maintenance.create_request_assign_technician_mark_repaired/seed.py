"""Seed for maintenance.create_request_assign_technician_mark_repaired."""


def setup(env):
    admin = env.ref("base.user_admin")
    user = env["res.users"].search([("login", "=", "demo")], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": "Marc Demo",
            "login": "demo",
            "password": "demo",
            "group_ids": [(4, env.ref("base.group_user").id)],
        })

    team = env["maintenance.team"].search([], limit=1)
    if not team:
        team = env["maintenance.team"].create({"name": "Bench Maintenance"})

    category = env["maintenance.equipment.category"].search([("name", "=", "Warehouse Gear")], limit=1)
    if not category:
        category = env["maintenance.equipment.category"].create({
            "name": "Warehouse Gear",
            "technician_user_id": user.id,
        })

    env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Replace Dock Sensor"),
    ]).unlink()

    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Forklift FL-88"),
    ]).unlink()

    env["maintenance.equipment"].create({
        "name": "Forklift FL-88",
        "category_id": category.id,
        "owner_user_id": admin.id,
        "technician_user_id": user.id,
        "maintenance_team_id": team.id,
    })
