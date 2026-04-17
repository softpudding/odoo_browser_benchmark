"""Seed for hr_holidays.create_leave_type."""

TYPE_NAME = "Conference Attendance"


def setup(env):
    # Remove prior runs of this exact leave type.
    env["hr.leave.type"].with_context(active_test=False).search([
        ("name", "=", TYPE_NAME),
    ]).unlink()

    # Make sure admin has config rights.
    admin = env.ref("base.user_admin")
    for grp in [
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_user",
    ]:
        g = env.ref(grp, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})
