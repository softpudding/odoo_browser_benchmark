# Change the Working Hours for "Bench Sched Me"

You are in the Odoo 19 **Employees** app logged in as **Administrator**.

An employee named **"Bench Sched Me"** has been seeded. Their current
**Working Hours** schedule is the company default (**Standard 40
hours/week**). They are moving to a part-time arrangement and need
their working schedule reassigned.

A working schedule named **"Part Time 20h"** has already been created
for you in the database — you just need to select it on the employee.

## What to do

1. Open the **Employees** app.
2. Find the employee named **"Bench Sched Me"** in the list and open
   the employee form.
3. Switch to the **Payroll** tab on the employee form. Under the
   **Schedule** section at the bottom of that tab, locate the
   **Working Hours** field — it is a many2one whose current value is
   **Standard 40 hours/week**.
4. Change the **Working Hours** value to exactly:

   ```
   Part Time 20h
   ```

   Click the field (or clear it), type `Part Time 20h`, and select
   **Part Time 20h** from the autocomplete dropdown.
5. **Save** the employee form.

## Expected end state

- The employee **"Bench Sched Me"** has **Working Hours** set to the
  `resource.calendar` named **"Part Time 20h"** (i.e.
  `hr.employee.resource_calendar_id` points at Part Time 20h).

## Rules

- Change only the **Working Hours** (`resource_calendar_id`) field on
  this employee. Do NOT change the Job Position, Job Title, department,
  work email, or any other field.
- Do not rename the employee. Do not archive, delete, or duplicate the
  record.
- Do not create a new working schedule — **Part Time 20h** has already
  been seeded for you; select it from the autocomplete.
- Do not modify the **Part Time 20h** or **Standard 40 hours/week**
  resource calendars themselves.
- Do not touch any other employee.
