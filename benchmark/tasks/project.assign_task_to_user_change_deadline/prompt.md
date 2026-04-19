Go to the **Project** app.

Open the project **"Bench Assign Project"** — you'll land on its task kanban.

Open the existing task **"Bench Assign Task"** (click the kanban card) so the
task form is visible.

Make exactly the following two changes on that task, then **save**:

1. **Assignees (`Assignees` field, a.k.a. `user_ids`):** add the existing
   internal user **`Bench Dev`** to the Assignees many2many field. Type
   `Bench Dev`, then pick the existing `Bench Dev` user from the autocomplete
   dropdown. **Do NOT** click any `Create "Bench Dev" as new user...` row —
   the user already exists.
2. **Deadline (`Deadline` field, a.k.a. `date_deadline`):** set the deadline
   to **`06/30/2026`** (June 30, 2026). Click the Deadline field, type
   `06/30/2026`, then press **Tab** (or click away) to close the date-picker
   popover before clicking any other control.

Then **Save** the task (cloud/save icon in the top-left form header, or the
Save button).

## Rules

- Do **not** change the task title, project, stage, priority, tags, or
  description.
- Do **not** create a new `Bench Dev` user — the user already exists in the
  database and should appear as an existing option in the autocomplete
  dropdown. If you see a `Create "Bench Dev" as new user...` entry, **do
  not click it**; pick the existing `Bench Dev` user instead.
- Do **not** remove any other assignees (there are none seeded — only
  `Bench Dev` should end up in the Assignees list).
- Do **not** create, rename, archive, or delete any other tasks, users, or
  projects.
- Only one task (`Bench Assign Task`) exists on this project — leave it as
  the only task.
