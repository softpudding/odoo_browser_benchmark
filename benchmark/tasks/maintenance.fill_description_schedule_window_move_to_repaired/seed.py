"""Seed for maintenance.fill_description_schedule_window_move_to_repaired."""

REQUEST_NAME = "Replace Conveyor Drive Belt"
EQUIPMENT_NAME = "Conveyor CV-22"


def setup(env):
    env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", REQUEST_NAME),
    ]).unlink()
    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", EQUIPMENT_NAME),
    ]).unlink()

    admin = env.ref("base.user_admin")
    team = env["maintenance.team"].search([], limit=1)
    if not team:
        team = env["maintenance.team"].create({"name": "Bench Maintenance"})

    equipment = env["maintenance.equipment"].create({
        "name": EQUIPMENT_NAME,
        "owner_user_id": admin.id,
        "technician_user_id": admin.id,
        "maintenance_team_id": team.id,
    })

    in_progress_stage = env.ref("maintenance.stage_1")  # In Progress

    env["maintenance.request"].create({
        "name": REQUEST_NAME,
        "equipment_id": equipment.id,
        "user_id": admin.id,
        "owner_user_id": admin.id,
        "maintenance_team_id": team.id,
        "stage_id": in_progress_stage.id,
        "maintenance_type": "corrective",
    })
