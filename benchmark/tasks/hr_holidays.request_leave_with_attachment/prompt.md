# Request an annual leave with a justification attachment

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

You need to submit your own 2-day time-off request AND attach a PDF
justification file to it via the chatter.

## What to do

1. In the **Time Off** app, click the **New** button to start a new request.
2. Fill in the request:
   - **Time Off Type**: `Annual Leave`
   - **Dates**: from **March 9, 2026** to **March 10, 2026** (2 days)
   - **Description**: `Family event`
3. Save the request so it moves to the submitted/**To Approve** state.
4. On the saved leave record, open the chatter panel on the right and use
   the **paperclip** (Attach files) icon to upload the PDF file located
   at `benchmark/tasks/hr_holidays.request_leave_with_attachment/seed_artifacts/leave_justification.pdf`.
   The attachment must be named exactly `leave_justification.pdf` and be
   linked to this leave record (res_model `hr.leave`).

## Rules

- Use the **Annual Leave** leave type exactly — not Sick Time Off or any
  other type.
- The request must cover exactly 2 days (March 9 and March 10, 2026).
- Do **not** approve or validate the request yourself — it should be left
  in the submitted/"To Approve" state.
- Upload the PDF through the **chatter paperclip**; do NOT paste the file
  contents into the description/notes field.
- The attachment must be linked to this `hr.leave` record (not some other
  record).
- Do **not** modify any other existing time-off requests.
- Do **not** delete the request.
