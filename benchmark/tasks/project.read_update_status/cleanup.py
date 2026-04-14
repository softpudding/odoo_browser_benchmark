"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env['project.project'].search([('name', '=', 'Q2 Launch')], limit=1)
    if project:
        # Reset the description (the field the task asks to write)
        project.write({'description': False})
        # Remove tasks — seed will recreate them
        env['project.task'].search([('project_id', '=', project.id)]).unlink()
