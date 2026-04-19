Send a reminder SMS to both reviewers assigned to the **Bench SMS Project**.

## Step 1 — Open the Tasks list for Bench SMS Project

1. Open the **Project** app.
2. From the Projects kanban, click the **Bench SMS Project** card (or use its "# Tasks" shortcut) so you land on the tasks list/kanban for that project.
3. Switch to **list** view (the list icon in the top-right breadcrumb) if it isn't already active.

## Step 2 — Multi-select both reviewer tasks

The list shows two seeded tasks:

- **Urgent Review Request — Reviewer A** (customer: *Bench Reviewer A*)
- **Urgent Review Request — Reviewer B** (customer: *Bench Reviewer B*)

Tick the checkbox at the left of **both** rows so both tasks are selected (the control panel should then show a multi-record selection banner).

## Step 3 — Launch the Send SMS action

1. With both tasks selected, open the cog **Actions** menu in the control panel.
2. Click **Send SMS**.
3. A dialog titled *Send an SMS* opens in mass mode (2 recipients).

## Step 4 — Fill body and send

1. In the **Message** field, type exactly:

   `Reminder: please review by EOD`

2. Click **Send now** (the secondary footer button — NOT *Put in queue*).

## Rules

- Do not deselect either task before clicking Send SMS.
- Do not change the recipient phone numbers or the task customers.
- Send exactly once. Do not re-open the dialog.
- Click **Send now**, not *Put in queue*, so the messages go out immediately (the check inspects the persisted SMS records either way, but sending now is the expected UX).
- Do not navigate away to a different project before sending.
