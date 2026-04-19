"""Cleanup for hr.create_public_holiday_calendar_entry."""


HOLIDAY_NAME = "Bench Founder Day"


def cleanup(env):
    env["resource.calendar.leaves"].search(
        [("name", "=", HOLIDAY_NAME)]
    ).unlink()
