"""Postcondition checks for project.set_project_deadline_tags."""

from datetime import date


PROJECT_NAME = "Meridian Platform Build"
DISTRACTOR_PROJECT = "Meridian Dev Tools"
EXPECTED_DEADLINE = date(2026, 6, 30)
REQUIRED_TAGS = {"Launch", "Q3"}


def check(env):
    failures = []

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    # Check deadline
    if project.date != EXPECTED_DEADLINE:
        failures.append(
            f"Project deadline is {project.date}, expected {EXPECTED_DEADLINE}"
        )

    # Check tags
    actual_tags = set(project.tag_ids.mapped("name"))
    missing_tags = REQUIRED_TAGS - actual_tags
    if missing_tags:
        failures.append(
            f"Missing required tags: {sorted(missing_tags)}. Actual tags: {sorted(actual_tags)}"
        )

    # Distractor project must not be modified
    distractor = env["project.project"].search([("name", "=", DISTRACTOR_PROJECT)], limit=1)
    if not distractor:
        failures.append(f"Distractor project '{DISTRACTOR_PROJECT}' not found")
    else:
        if distractor.date:
            failures.append(
                f"Distractor project deadline was changed to {distractor.date}"
            )
        dist_tags = distractor.tag_ids.mapped("name")
        for tag in REQUIRED_TAGS:
            if tag in dist_tags:
                failures.append(f"Tag '{tag}' was added to the distractor project")

    return failures
