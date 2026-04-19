"""Seed for hr.create_public_holiday_calendar_entry.

Difficulty: medium (Category: deep_ui_interaction).

Workflow exercised:
  Time Off app -> Configuration -> Public Holidays -> New -> fill editable-bottom
  inline row with Name + date_from + date_to + calendar_id (default kept) -> Save.

The agent must:
  - Navigate into the Time Off app and drill into
    Configuration -> Public Holidays (which is a filtered, editable-bottom
    list view over resource.calendar.leaves with
    domain=[('resource_id', '=', False)]).
  - Add a company-wide (no resource) holiday 'Bench Founder Day' on
    2026-06-01 00:00:00 -> 23:59:59.
  - Keep the auto-filled calendar_id (company default working schedule).

Seed responsibilities:
  - Force admin.tz='UTC' so typed datetimes in the UI map 1:1 to stored
    UTC values (no browser/local tz drift corrupting the timestamps).
  - Ensure admin has the Time Off Administrator group (manager) so the
    Configuration > Public Holidays menu item is visible and editable.
  - Wipe any leftover 'Bench Founder Day' resource.calendar.leaves rows
    from prior runs so the check count is deterministic.
  - Do NOT pre-create the public holiday; the agent creates it.
"""


HOLIDAY_NAME = "Bench Founder Day"


def setup(env):
    # Admin tz=UTC so typed UI datetimes map 1:1 to stored UTC values.
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if admin and admin.tz != "UTC":
        admin.write({"tz": "UTC"})

    # Ensure admin has the manager group (needed for the Configuration
    # menu + editable public holiday list). Base snapshot usually has
    # this already for admin, but belt-and-braces.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_responsible",
        "hr_holidays.group_hr_holidays_manager",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and admin and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    # Clean up any leftover Bench Founder Day rows from prior runs
    # (including archived) so the check counts are deterministic.
    leftover = env["resource.calendar.leaves"].search(
        [("name", "=", HOLIDAY_NAME)]
    )
    if leftover:
        leftover.unlink()
