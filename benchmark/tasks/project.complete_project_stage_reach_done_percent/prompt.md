Go to the **Project** app.

Open the project **"Bench Progress Project"** — you'll land on its task
kanban board, grouped by stage. The columns left-to-right are:

1. **To Do**
2. **In Progress**
3. **Done**

There are exactly three tasks, all currently sitting in the **"To Do"**
column:

- **Task A**
- **Task B**
- **Task C**

You need to move **all three** task cards from the **"To Do"** column
to the **"Done"** column, so that the final board has **zero** cards in
"To Do" and **three** cards in "Done".

### How to move a card

Press and hold the mouse on the **task card** (the card body — the
rectangle showing the task title), drag it rightward over the "Done"
column, and release. The card will snap into the "Done" column.

Repeat for all three cards (Task A, Task B, Task C). Note that
**`project.task` has no "Change Stage" bulk action** in the cog /
Actions menu, and the list-view `Stage` column is read-only for
multi-edit — so you **must** drag each card one at a time.

The kanban view auto-saves as soon as each drop completes — there is no
explicit Save button.

### Rules

- You must change **`stage_id`** on each task to "Done" (the kanban
  stage). Do **NOT** open the task form and click the colored state pill
  in the form header — that widget sets `project.task.state` (a
  separate field) and leaves `stage_id` still pointing at "To Do",
  which does NOT satisfy the postcondition.
- Do **not** rename, archive, duplicate, or delete any of the three tasks.
- Do **not** change the task priority, tags, assignees, deadline, or description.
- Do **not** create any new tasks or new stages.
- Do **not** rename, fold, archive, or delete any of the three stages
  ("To Do", "In Progress", "Done").
- Do **not** touch any other project.
- The end state must have **all three** cards (Task A, Task B, Task C)
  in the **"Done"** column — partial completion (1 of 3 or 2 of 3) is
  a **failure**.
