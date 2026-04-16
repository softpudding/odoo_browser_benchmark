"""Seed a project for the set_project_deadline_tags task.

Category 2 (MEDIUM): Find a project and update its settings — set the deadline
date using a date picker and add two tags using the many2many tag widget.

The agent must navigate to project settings (not task editing) and interact
with both a date field and a tag selector.
"""

PROJECT_NAME = "Meridian Platform Build"
DISTRACTOR_PROJECT = "Meridian Dev Tools"


def _cleanup(env):
    for name in [PROJECT_NAME, DISTRACTOR_PROJECT]:
        project = env["project.project"].search([("name", "=", name)])
        for p in project:
            p.task_ids.unlink()
            p.unlink()
    # Clean up tags if we created them (they may remain across runs — that's fine)


def _ensure_tag(env, name):
    tag = env["project.tags"].search([("name", "=", name)], limit=1)
    if not tag:
        tag = env["project.tags"].create({"name": name})
    return tag


def setup(env):
    _cleanup(env)

    # Ensure tags exist so the agent can select them (pre-create so they appear in search)
    _ensure_tag(env, "Launch")
    _ensure_tag(env, "Q3")
    _ensure_tag(env, "Q2")  # distractor tag that should NOT be added

    # Target project — start date pre-set to June 1 so the form's
    # required="date_start or date" validation passes when agent sets
    # only the deadline (end date). No tags, no deadline yet.
    env["project.project"].create({
        "name": PROJECT_NAME,
        "date_start": "2026-06-01",
    })

    # Distractor project — should not be modified
    env["project.project"].create({
        "name": DISTRACTOR_PROJECT,
    })
