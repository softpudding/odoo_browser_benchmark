"""Seed for maintenance.create_request_from_equipment_schedule_followup."""


REQUEST_NAME = "Inspect Forklift Battery Cooling"
EQUIPMENT_NAME = "Forklift FL-88"
TEAM_NAME = "Bench Maintenance"
CATEGORY_NAME = "Warehouse Gear"
TECHNICIAN_LOGIN = "demo"
TECHNICIAN_NAME = "Marc Demo"
ACTIVITY_SUMMARY = "Review cooling test report"


def setup(env):
    admin = env.ref("base.user_admin")
    user = env["res.users"].search([("login", "=", TECHNICIAN_LOGIN)], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": TECHNICIAN_NAME,
            "login": TECHNICIAN_LOGIN,
            "password": TECHNICIAN_LOGIN,
            "group_ids": [(4, env.ref("base.group_user").id)],
        })
    else:
        user.write({"name": TECHNICIAN_NAME})

    team = env["maintenance.team"].search([("name", "=", TEAM_NAME)], limit=1)
    if not team:
        team = env["maintenance.team"].create({"name": TEAM_NAME})

    category = env["maintenance.equipment.category"].search([("name", "=", CATEGORY_NAME)], limit=1)
    if not category:
        category = env["maintenance.equipment.category"].create({
            "name": CATEGORY_NAME,
            "technician_user_id": user.id,
        })
    else:
        category.write({"technician_user_id": user.id})

    requests = env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", REQUEST_NAME),
    ])
    if requests:
        env["mail.activity"].search([
            ("res_model", "=", "maintenance.request"),
            ("res_id", "in", requests.ids),
        ]).unlink()
        requests.unlink()

    equipment = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", EQUIPMENT_NAME),
    ], limit=1)
    if equipment:
        if not equipment.active:
            equipment.active = True
        equipment.write({
            "category_id": category.id,
            "owner_user_id": admin.id,
            "technician_user_id": user.id,
            "maintenance_team_id": team.id,
        })
    else:
        env["maintenance.equipment"].create({
            "name": EQUIPMENT_NAME,
            "category_id": category.id,
            "owner_user_id": admin.id,
            "technician_user_id": user.id,
            "maintenance_team_id": team.id,
        })
