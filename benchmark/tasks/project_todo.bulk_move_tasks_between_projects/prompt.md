# Move three specific tasks from Bench Proj A to Bench Proj B

You are logged in to Odoo 19 as **Administrator** in the **Project** app.

Two projects exist:

- **Bench Proj A** — currently holds **four** tasks (Alpha, Bravo, Charlie, Delta).
- **Bench Proj B** — currently empty.

You must **reassign three specific tasks** from *Bench Proj A* to *Bench Proj B*:

- **Bench Task Alpha** — move to *Bench Proj B*
- **Bench Task Bravo** — move to *Bench Proj B*
- **Bench Task Charlie** — move to *Bench Proj B*
- **Bench Task Delta** — **do NOT move** this one; it must stay in *Bench Proj A*.

## What to do

1. Open **Project** (URL `/odoo/project`).
2. Open the **Bench Proj A** project card to see its tasks.
3. For each of the three target tasks (Alpha, Bravo, Charlie):
   a. Open the task (click it to open the **form view**).
   b. Change its **Project** field from `Bench Proj A` to `Bench Proj B`.
      Use the project autocomplete / many2one widget on the form and pick
      *Bench Proj B* from the dropdown.
   c. **Save** the form (cloud/save icon or press the Save button).
   d. Navigate back to the Bench Proj A task list (breadcrumbs or back
      navigation) to open the next target task.
4. When done, *Bench Proj A* must contain exactly **1** task (Delta) and
   *Bench Proj B* must contain exactly **3** tasks (Alpha, Bravo, Charlie).

> **Note.** Odoo 19 Community has no dedicated "Move to Project" bulk
> action in the list/kanban cog Actions menu — the supported way to change
> a task's project is to edit the **Project** field on the task's form
> view. Work task-by-task: open → edit Project → Save → back to list →
> next task.

## Rules

- Move **exactly** Alpha, Bravo and Charlie — all three — into
  **Bench Proj B**.
- **Do NOT move** Bench Task Delta. It must remain in Bench Proj A at the
  end of the task.
- Do **not** rename any task, change any task's stage, tags, assignees,
  deadline, or priority.
- Do **not** create any new project or any new task.
- Do **not** archive or delete any task or project.
- Do **not** duplicate any task.
- You must reassign via the **Project field on the task form view**; do
  not attempt to delete-and-recreate the tasks in *Bench Proj B*.
