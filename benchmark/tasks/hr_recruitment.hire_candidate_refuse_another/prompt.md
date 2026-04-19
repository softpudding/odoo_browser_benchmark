Go to the **Recruitment** app (URL path `/odoo/recruitment`). A job
position named **Bench Role** has been seeded with two active
applicants in the pipeline:

- **Top Candidate** — the person you want to hire
- **Runner Up** — the person you want to refuse

Both sit in the **Initial Qualification** stage. A custom refuse
reason **Not a fit** has been seeded. You must do BOTH of the
following; the order does not matter but each step must be completed
exactly as described.

## 1. Hire the Top Candidate

1. On the Recruitment home kanban, click the **Bench Role** job card
   to open its Applications kanban (or open Recruitment → Applications
   → All Applications and filter by Bench Role).
2. Open the **Top Candidate** applicant card so you see the applicant
   form.
3. On the form **status bar** (the row of stage pills at the top),
   click the last stage **Contract Signed**. This is the "hired" stage
   — clicking it sets the hire date on the applicant.
4. A green **Hired** ribbon should now appear on the form. A new
   header button labelled **Create Employee** becomes visible. Click
   **Create Employee**. Odoo navigates to a pre-filled new employee
   form carrying the applicant's name and job.
5. Before saving the pre-filled employee form, edit the
   **Job Title** field (the line directly under the employee's name,
   shown as "Job Title e.g. Sales Manager") and replace its content
   with the literal string:

   `Bench Role (Hired)`

   The field may be pre-filled with `Bench Role` (copied from the
   job position) — overwrite it with `Bench Role (Hired)`.
6. Click the **cloud/save** button (or hit Save) to persist the
   employee.

After this step, the applicant **Top Candidate** must have an
`employee_id` set (you can confirm by returning to the applicant form
and seeing an "Employee" smart button in the top-right button box)
and that employee's **Job Title** must be exactly `Bench Role (Hired)`.

## 2. Refuse the Runner Up with reason *Not a fit*

1. Navigate back to the **Bench Role** applications list (Recruitment
   → Bench Role → Applications, or Recruitment → Applications → All
   Applications filtered by Bench Role).
2. Open the **Runner Up** applicant form.
3. In the form header click the **Refuse** button. A wizard modal
   titled *Refuse Reason* opens (model `applicant.get.refuse.reason`).
4. In that wizard, under **Reason**, click the **Not a fit** badge so
   it becomes the selected reason (the widget is a row of coloured
   badges — select exactly `Not a fit`, not any of the other seeded
   reasons).
5. If the **Send Email** toggle is enabled, turn it **off** (we do not
   want to email the applicant).
6. Click the wizard's primary **Refuse** button at the bottom of the
   modal. The dialog closes and the Runner Up is archived with a red
   "Refused" ribbon.

After this step, the applicant **Runner Up** must have
`active=False` and `refuse_reason_id` equal to **Not a fit**.

## Rules

- Hire **Top Candidate** and refuse **Runner Up** — not the other way
  around. Do not refuse Top Candidate and do not hire Runner Up.
- Use the **Contract Signed** status-bar stage (or the Create Employee
  header button) to hire — do NOT manually edit the `employee_id`
  field or go through Employees → New.
- The refuse reason MUST be exactly **Not a fit** (case-sensitive).
  Do not pick *Does not fit the job requirements* or any other seeded
  reason.
- Do not delete, rename, or archive the **Bench Role** job itself.
- Do not create any other applicants, refuse reasons, or employees
  beyond the single employee the Create Employee button produces.
- The new employee's **Job Title** must be exactly
  `Bench Role (Hired)` — not `Bench Role`, not `Hired`, not any
  other variation.
- Two other seeded refuse reasons look similar (*Not a good fit*,
  *Not a fit - incomplete application*). Do NOT pick those — pick
  exactly **`Not a fit`**.
- Leave every other seeded applicant, stage, and refuse reason
  untouched.
