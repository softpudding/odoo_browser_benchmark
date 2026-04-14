"""Create a project with tasks in mixed stages."""


def setup(env):
    # Ensure project stages exist
    stage_new = env['project.task.type'].search([('name', '=', 'New')], limit=1)
    if not stage_new:
        stage_new = env['project.task.type'].create({'name': 'New', 'sequence': 1})

    stage_progress = env['project.task.type'].search([('name', '=', 'In Progress')], limit=1)
    if not stage_progress:
        stage_progress = env['project.task.type'].create({'name': 'In Progress', 'sequence': 10})

    stage_done = env['project.task.type'].search([('name', '=', 'Done')], limit=1)
    if not stage_done:
        stage_done = env['project.task.type'].create({'name': 'Done', 'sequence': 20})

    # Ensure Done stage is NOT folded so it's visible in kanban
    stage_done.write({'fold': False})

    # Create or find project
    project = env['project.project'].search([('name', '=', 'Q2 Launch')], limit=1)
    if not project:
        project = env['project.project'].create({
            'name': 'Q2 Launch',
            'type_ids': [(6, 0, [stage_new.id, stage_progress.id, stage_done.id])],
        })
    else:
        project.type_ids = [(6, 0, [stage_new.id, stage_progress.id, stage_done.id])]

    # Clear description from previous runs
    project.write({'description': False})

    # Remove existing tasks
    env['project.task'].search([('project_id', '=', project.id)]).unlink()

    # Create 5 tasks: 2 done, 1 in progress, 2 new
    tasks = [
        ('Design landing page', stage_done),
        ('Write copy', stage_done),
        ('Build email template', stage_progress),
        ('Set up analytics', stage_new),
        ('Final QA review', stage_new),
    ]
    for name, stage in tasks:
        env['project.task'].create({
            'name': name,
            'project_id': project.id,
            'stage_id': stage.id,
        })
