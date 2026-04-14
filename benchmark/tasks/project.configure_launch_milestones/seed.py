"""Seed a project that requires milestone feature discovery."""


def setup(env):
    stage_specs = [
        ("New", 1),
        ("In Progress", 10),
        ("Done", 20),
    ]
    stage_ids = []
    for name, sequence in stage_specs:
        stage = env["project.task.type"].search([("name", "=", name)], limit=1)
        if not stage:
            stage = env["project.task.type"].create({
                "name": name,
                "sequence": sequence,
            })
        if name == "Done":
            stage.write({"fold": False})
        stage_ids.append(stage.id)

    project = env["project.project"].search([("name", "=", "Atlas Redesign")], limit=1)
    if not project:
        project = env["project.project"].create({
            "name": "Atlas Redesign",
            "type_ids": [(6, 0, stage_ids)],
        })
    else:
        project.type_ids = [(6, 0, stage_ids)]

    env["project.task"].search([("project_id", "=", project.id)]).unlink()
    env["project.milestone"].search([("project_id", "=", project.id)]).unlink()
    project.write({
        "allow_milestones": False,
        "description": False,
    })


