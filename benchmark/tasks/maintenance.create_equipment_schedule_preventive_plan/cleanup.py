"""Cleanup for maintenance.create_equipment_schedule_preventive_plan."""


def cleanup(env):
    equipment = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Bench Press 01"),
    ])
    equipment.unlink()

    stale_cats = env["maintenance.equipment.category"].with_context(
        active_test=False
    ).search([("name", "=", "Machinery")])
    for cat in stale_cats:
        if not cat.equipment_ids and not cat.maintenance_ids:
            cat.unlink()
