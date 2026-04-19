Go to the **Project** app.

Open the project **"Bench Tag Proj"** — you'll land on its task kanban.

Create a **new task** with **all four** of the following details filled in, then
save. Do this in a single form submission (one new task record).

## New task details

- **Title (Task Name):** `Fix login bug`
- **Deadline (`Deadline` field, a.k.a. `date_deadline`):** `06/30/2026` (June 30, 2026)
- **Tags (`Tags` field, many2many_tags):** add **both** of these existing tags:
  - `urgent`
  - `backend`
- **Assignees (`Assignees` field, a.k.a. `user_ids`):** add **both** of these
  existing users:
  - `Mitchell Admin` (the Administrator — also shown as "Administrator" in some UIs)
  - `Bench Dev 2`

Both tags (`urgent` and `backend`) already exist in the database, so each should
appear as an existing option in the autocomplete dropdown — **do not create
new tags**, just pick the existing ones. Same for the users.

## How to do it

1. Navigate to **Project** and click the **"Bench Tag Proj"** project card.
2. Click **New** (top-left button on the task kanban / task list) to open a
   blank task form.
3. In the task form:
   a. Type `Fix login bug` as the task Title.
   b. Click the **Deadline** field and type `06/30/2026`, then press **Tab**
      (or click away) to close the date picker popover before doing anything
      else.
   c. Click the **Tags** field, type `urgent`, pick the existing `urgent` tag
      from the autocomplete dropdown. Repeat for `backend`.
   d. Click the **Assignees** field, type `Mitchell Admin` (or `Administrator`),
      pick the existing user from the autocomplete dropdown. Then type
      `Bench Dev 2` and pick that user too.
4. **Save** the task (cloud/save icon in the top-left form header, or press
   the Save button).

## Rules

- Create **exactly one** new task named `Fix login bug`.
- The new task must belong to the **"Bench Tag Proj"** project (clicking New
  from inside the project kanban already scopes the task to that project —
  do not change the Project field).
- Do **not** rename, archive, duplicate, or delete any existing tasks or tags.
- Do **not** create new `urgent` or `backend` tags — use the existing ones that
  appear in the autocomplete dropdown.
- Do **not** create a new user — `Bench Dev 2` already exists.
- Do **not** modify the stage, priority, description, or any other field on
  the new task beyond the four listed above.
