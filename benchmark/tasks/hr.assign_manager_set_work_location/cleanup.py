"""Cleanup for hr.assign_manager_set_work_location."""


def cleanup(env):
    env["hr.employee"].search([("name", "in", ["Nadia Reyes", "Maya Ortiz"])]).unlink()
