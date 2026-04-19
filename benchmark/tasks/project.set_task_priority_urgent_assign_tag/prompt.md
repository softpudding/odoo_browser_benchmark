Go to the **Project** app.

Open the project **"Bench Prio Project"** — you'll land on its task kanban.

Open the existing task **"Fix critical bug"** (click the kanban card) so the
task form is visible.

Make exactly the following two changes on that task, then **save**:

1. **Priority:** set it to **exactly ONE filled star** (the FIRST of the
   three priority stars on the task form). In the task form, find the
   priority widget (three small star icons near the task title) and click
   **only the first star** so that **exactly one star is filled/yellow**
   and the other two stars remain empty. This corresponds to Odoo
   priority value `1` (i.e. `Medium priority`).

   Do **NOT** click a second or third star — the task should end up with
   exactly one filled star, not two and not three.
2. **Tags:** add the **existing** tag **`Bug`** to the **Tags** field (the
   many2many_tags field on the task form). Type `Bug`, then pick the
   existing `Bug` tag from the autocomplete dropdown.

Then **Save** the task (cloud/save icon in the top-left form header, or the
Save button).

## Rules

- Do **not** change the task title, project, stage, assignees, deadline, or
  description.
- Do **not** create a new `Bug` tag — the tag already exists in the database
  and should appear as an existing option in the autocomplete dropdown.
  If you see a "Create 'Bug'" entry, **do not click it**; pick the existing
  `Bug` tag instead.
- Do **not** create, rename, archive, or delete any other tasks or tags.
- Only one task (`Fix critical bug`) exists on this project — leave it as the
  only task.
