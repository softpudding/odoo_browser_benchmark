"""Seed for maintenance.create_equipment_schedule_preventive_plan.

Creates the 'Bench Tech' technician user (if absent) and removes prior
'Bench Press 01' equipment + 'Machinery' category from previous runs so
the agent has to create the category from scratch. Expected MTBF
(writable) and Effective Date (writable) are the two target fields —
MTBF is readonly (computed) and must not be the agent's target.
"""


EQUIPMENT_NAME = "Bench Press 01"
CATEGORY_NAME = "Machinery"
TECHNICIAN_LOGIN = "bench_tech"
TECHNICIAN_NAME = "Bench Tech"


def setup(env):
    # Ensure the technician user exists.
    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", TECHNICIAN_LOGIN)], limit=1
    )
    if not user:
        user = env["res.users"].create({
            "name": TECHNICIAN_NAME,
            "login": TECHNICIAN_LOGIN,
            "password": TECHNICIAN_LOGIN,
            "group_ids": [(4, env.ref("base.group_user").id)],
        })
    else:
        if not user.active:
            user.active = True
        if user.name != TECHNICIAN_NAME:
            user.name = TECHNICIAN_NAME

    # Cleanup prior equipment so the Save creates a fresh record.
    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", EQUIPMENT_NAME),
    ]).unlink()

    # Cleanup prior 'Machinery' category so the agent must create it.
    # Only remove if no equipment still references it (protected by
    # _unlink_except_contains_maintenance_requests). After removing the
    # equipment above this should be safe.
    stale_cats = env["maintenance.equipment.category"].with_context(
        active_test=False
    ).search([("name", "=", CATEGORY_NAME)])
    for cat in stale_cats:
        if not cat.equipment_ids and not cat.maintenance_ids:
            cat.unlink()
