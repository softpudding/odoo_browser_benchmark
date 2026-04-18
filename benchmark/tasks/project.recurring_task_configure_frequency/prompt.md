# Configure a recurring schedule on a project task

In the **Project** app, open the project named **"Bench Recurring Project"**
and then open the task named **"Weekly Status Update"**. The task already
exists and is currently a one-off (non-recurring) task.

Convert this task into a recurring task with the following schedule:

- Turn on **Recurrent** (the repeat / refresh icon next to the Deadline date).
- **Repeat Every:** `1`
- **Repeat unit:** `Weeks`
- **Until:** select **`Until`** (not "Forever") and set the end date to
  **`06/13/2026`** (this represents 8 weekly occurrences ending on
  June 13, 2026).
- Save the task.

## Where to find the controls

After opening the task you will see a "Deadline" field on the right-hand
side. Immediately to the right of the Deadline date is a small repeat icon
(a circular arrow). Clicking that icon toggles the **Recurrent** flag. Once
it is enabled, a row of controls appears underneath:

```
Repeat Every  [ 1 ]  [ Weeks v ]  [ Until v ]  [ End Date ]
```

Set the values exactly as listed above, then save.

## Rules

- Do **not** rename, archive, or delete the project or the task.
- Do **not** create any additional tasks or projects.
- Do **not** change the Recurrent flag on any other task.
- Make sure to **save** the form (Cloud / Save button) so the new
  recurrence settings are persisted.
- Use exactly the date `06/13/2026` for "Until". A different date will
  fail the postcondition.
