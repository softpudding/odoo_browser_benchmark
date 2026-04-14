"""Cleanup for calendar.schedule_recurring_steering_sync."""


def cleanup(env):
    env["calendar.event"].search([("name", "=", "Northwind Steering Sync")]).unlink()
