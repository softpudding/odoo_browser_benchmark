Go to the **Project** app.

Open the project **"Bench Close Project"** — you'll land on its task kanban.

Open the existing task **"Review document"** (click the kanban card) so the
task form is visible.

The task is currently in state **In Progress**. You need to mark it as
**Done** via the **state widget** on the task form:

1. In the form header (to the right of the task title, next to the 3-star
   priority widget), locate the colored **state pill / button** — it
   currently reads **"In Progress"** (a rounded-pill button with an
   outlined-secondary color).
2. **Click that pill once** to open its dropdown menu. The dropdown lists
   the selectable task states: `In Progress`, `Changes Requested`,
   `Approved`, `Cancelled`, `Done`.
3. Click the **"Done"** entry in the dropdown. The pill should turn green
   and its label should change to **"Done"** (with a check-circle icon).

Then **Save** the task (cloud/save icon in the top-left form header, or
the Save button, or just Ctrl+S — Odoo may auto-save as soon as the state
changes, but press Save to make sure).

## Rules

- Do **NOT** change the task title, project, stage, priority, tags,
  assignees, deadline, or description.
- Do **NOT** use the kanban stage pills in the form header (those change
  `stage_id`, which is different from `state`). You must use the state
  widget (the colored pill, NOT the stage statusbar).
- Do **NOT** archive, delete, duplicate, or rename the task.
- Do **NOT** create new tasks, projects, or stages.
- The final state must be **Done** (technical value `1_done`), NOT
  "Approved" and NOT "Cancelled".
- Only one task (`Review document`) exists on this project — leave it as
  the only task.
