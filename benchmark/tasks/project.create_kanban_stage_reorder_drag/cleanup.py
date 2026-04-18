"""Clean up artifacts from previous runs of
project.create_kanban_stage_reorder_drag."""


PROJECT_NAME = "Bench Project A"
STAGE_NAMES = ["Triage", "In Progress", "Review", "Done", "Backlog Review"]


def cleanup(env):
    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", project.id),
        ]).unlink()
        stages = env["project.task.type"].with_context(active_test=False).search([
            ("project_ids", "in", [project.id]),
        ])
        for stage in stages:
            stage.write({"project_ids": [(3, project.id)]})
            if not stage.project_ids and stage.name in STAGE_NAMES:
                stage.unlink()
        project.unlink()

    # Last-resort: nuke any orphan 'Backlog Review' stage not linked to any
    # project (created by a prior task run that later dropped the project).
    orphans = env["project.task.type"].with_context(active_test=False).search([
        ("name", "=", "Backlog Review"),
    ])
    for s in orphans:
        if not s.project_ids:
            s.unlink()
