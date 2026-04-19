# Schedule a To-Do activity on a contact

You are in the Odoo 19 **Contacts** app logged in as **Administrator**.

A contact named **`Bench Activity Partner`** already exists (it is a company
contact). We need to plan a follow-up call with them, so you should schedule
a **To-Do** activity on this contact's chatter with a specific summary, due
date, and note.

## What to do

1. Open **Contacts** (top-level app).
2. Click the **`Bench Activity Partner`** contact to open its form.
3. Scroll to the chatter panel on the right / below the form so its action
   buttons are visible.
4. Click the **Activities** button in the chatter header (it looks like a
   small clock icon with the label `Activities`). This opens the
   **Schedule Activity** modal (wizard `mail.activity.schedule`).
5. In the wizard, fill the fields exactly:

   - **Activity Type**: `To-Do` (this is the default — leave it selected).
   - **Summary**: `Follow up call`
   - **Due Date**: `05/15/2026` (so the `date_deadline` stores as
     `2026-05-15`).
   - **Note**: In the rich-text note editor, type:

     ```
     Discuss Q2 plan
     ```

6. Click the **Schedule** button in the wizard footer to save the activity.

## Expected end state

- Exactly one `mail.activity` row exists on the `Bench Activity Partner`
  contact with:
  - `res_model = 'res.partner'`
  - `res_id` = the seeded partner's id
  - `activity_type_id.name = 'To-Do'`
  - `summary = 'Follow up call'`
  - `date_deadline = 2026-05-15`
  - `note` HTML contains the text `Q2 plan`

## Rules

- Do NOT rename, archive, merge, or delete the `Bench Activity Partner`
  contact.
- Do NOT post a chatter message (Send message) or internal Log note —
  only the **Schedule Activity** wizard is required.
- Do NOT mark the activity as done or "Mark as Done & Schedule Next";
  leave it as an open planned activity.
- Do NOT change the Activity Type away from **To-Do** (which is the
  default in the wizard).
- Do NOT create a second activity — exactly one scheduled activity is
  expected.
