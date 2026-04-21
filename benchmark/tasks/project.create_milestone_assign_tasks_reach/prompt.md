# Create a milestone, assign two tasks to it, then mark it as reached

You are logged in to Odoo 19 as **Administrator** in the **Project** app.

A project called **Bench Milestone Proj** already exists. It has
**Milestones** enabled and currently contains three tasks:

- **T1 - Draft Spec**
- **T2 - Build Prototype**
- **T3 - Review Final**

None of the tasks are linked to a milestone yet, and the project has no
milestones.

## What to do

1. Go to **Project** (URL `/odoo/project`) and open **Bench Milestone Proj**.
2. Open the project's **Milestones** panel (from the project card's kebab /
   three-dots menu on the Projects dashboard) and create a **new milestone** with:
   - **Name:** `Phase 1 Complete`
   - **Deadline:** `2026-06-01` (June 1, 2026)

   Leave the **Reached** flag unchecked for now. Save the new milestone.
3. Open task **T1 - Draft Spec** in its form view and set its
   **Milestone** field to `Phase 1 Complete`. Save.
4. Open task **T2 - Build Prototype** in its form view and set its
   **Milestone** field to `Phase 1 Complete`. Save.
5. **Do NOT** assign a milestone to **T3 - Review Final**. It must remain
   with no milestone set.
6. Go back to the `Phase 1 Complete` milestone (via the Milestones panel)
   and mark it **Reached** (tick the `Reached` checkbox / set
   `is_reached = True`). Save.

After you are done:
- A `project.milestone` record named `Phase 1 Complete` exists on
  **Bench Milestone Proj** with deadline `2026-06-01` and
  `is_reached = True`.
- **T1 - Draft Spec** and **T2 - Build Prototype** both have
  `milestone_id = Phase 1 Complete`.
- **T3 - Review Final** still has **no** milestone (`milestone_id = False`).

## Rules

- Create **exactly one** new milestone on this project, named
  `Phase 1 Complete` with deadline `2026-06-01`.
- Assign the milestone **only** to T1 and T2 — do not add it to T3.
- Do **not** create any extra tasks, delete any task, or rename any task.
- Do **not** change any task's stage, deadline, priority, tags, or assignees.
- Do **not** create any other milestone on the project.
- Do **not** archive or delete the project.
