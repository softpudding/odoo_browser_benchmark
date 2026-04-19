# Promote "Bench Promote Me" — set a new Job Title

You are in the Odoo 19 **Employees** app logged in as **Administrator**.

An employee named **"Bench Promote Me"** has been seeded. Their current
**Job Title** is **Analyst**, and they have just been promoted and need
their Job Title updated.

## What to do

1. Open the **Employees** app.
2. Find the employee named **"Bench Promote Me"** in the list and open
   the employee form.
3. On the **Work** tab (the default tab shown when the form opens),
   locate the **Job Title** field — it is the free-text char field
   directly below the **Job Position** many2one (the Job Title field
   is NOT the same as Job Position).
4. Change the Job Title from `Analyst` to exactly:

   ```
   Senior Analyst
   ```

5. **Save** the employee form.

## Expected end state

- The employee **"Bench Promote Me"** has **Job Title** set to exactly
  `Senior Analyst` (`hr.employee.job_title == 'Senior Analyst'`).

## Rules

- Edit only the **Job Title** (`job_title`) field on this employee. Do
  NOT change the Job Position (`job_id`), department, work email, or
  any other field.
- The Job Title value must be **exactly** `Senior Analyst` — no extra
  whitespace, no quotes, and match capitalisation exactly.
- Do not rename the employee. Do not archive, delete, or duplicate the
  record.
- Do not create a new Job Position. Do not touch any other employee.
