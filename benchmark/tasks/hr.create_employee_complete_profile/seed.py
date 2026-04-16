"""Seed for multi-tab employee creation task.

Category 5: Deep UI interaction.
The task requires filling fields across three distinct areas of the
employee form: the main form, the Work Information tab, and the Private
Information tab. Browser-use typically fills only the main form and
skips subsidiary tabs, leaving required fields empty.
"""


def setup(env):
    # --- Cleanup prior runs ---
    old = env["hr.employee"].search([("name", "=", "Jordan Mercer")])
    old.unlink()

    # Ensure the job position exists so the agent only needs to select it
    # (We want the challenge to be the multi-tab navigation, not job-creation UX)
    job = env["hr.job"].search([("name", "=", "Field Operations Coordinator")], limit=1)
    if not job:
        env["hr.job"].create({
            "name": "Field Operations Coordinator",
            "no_of_recruitment": 1,
        })

    # Ensure "Home" work location exists (standard Odoo default, but verify)
    home_loc = env["hr.work.location"].search(
        [("name", "=", "Home")], limit=1
    )
    if not home_loc:
        env["hr.work.location"].create({
            "name": "Home",
            "location_type": "home",
        })

    # Ensure Standard 40h work schedule exists
    schedule = env["resource.calendar"].search(
        [("name", "ilike", "Standard 40")], limit=1
    )
    if not schedule:
        env["resource.calendar"].create({
            "name": "Standard 40 hours/week",
            "hours_per_day": 8.0,
            "tz": "UTC",
        })
    # No employee record is seeded — agent must create it from scratch
