"""Cleanup for hr_holidays.create_leave_type."""

TYPE_NAME = "Conference Attendance"


def cleanup(env):
    env["hr.leave.type"].with_context(active_test=False).search([
        ("name", "=", TYPE_NAME),
    ]).unlink()
