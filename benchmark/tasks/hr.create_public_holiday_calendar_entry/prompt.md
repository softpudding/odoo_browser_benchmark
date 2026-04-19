# Add a Public Holiday for Bench Founder Day

You must register a new company-wide public holiday in the **Time Off** app's
configuration. Public holidays apply to all employees — they are stored as
`resource.calendar.leaves` rows with no specific resource assigned.

## Steps

1. Open the **Time Off** app (`/odoo/time-off`).
2. In the top menu, go to **Configuration → Public Holidays**. This opens
   the list of existing public holidays.
3. Click **New** to add a new public holiday row.
4. Fill in the new row with these exact values:
   - **Name**: `Bench Founder Day`
   - **Start Date** (`date_from`): `06/01/2026 00:00:00`
   - **End Date** (`date_to`): `06/01/2026 23:59:59`
   - **Working Hours** (`calendar_id`): leave the **default** value
     (the placeholder shows "All Schedules" — keep it blank so the
     holiday applies company-wide).
5. **Save** the list (click the cloud/save button in the list header, or
   click outside the row).

## Rules

- The name must be exactly `Bench Founder Day` — no extra spaces, no
  trailing punctuation.
- The holiday must be **company-wide** — do NOT set a specific
  **Resource** / employee on it (leave the resource blank). This is the
  default on the Public Holidays view.
- Use the exact **datetime** values above (`06/01/2026 00:00:00` to
  `06/01/2026 23:59:59`). Both fields are datetime inputs — type the date
  and time in one go.
- Leave **Working Hours** at its default (blank / "All Schedules"). Do
  NOT pick a specific working schedule from the dropdown.
- Do NOT create any other public holiday rows.
- Do NOT delete, archive, or modify any pre-existing public holidays.
- Do NOT navigate to a different module or create a record on a
  different model (no `hr.leave`, no `hr.leave.mandatory.day`).
