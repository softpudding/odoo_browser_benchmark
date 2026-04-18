You are finalizing a new recruitment posting for **Bench Products**.

Start from the Recruitment app. The job position **"Bench QA Engineer"**
has already been seeded. It is currently **unpublished**, its short
Summary/Description is empty, and its public Website Description
already contains a **Requirements** section (do NOT change the website
description — just leave it alone).

Complete all of the following, in order:

1. Open the **Recruitment** app (URL `/odoo/recruitment`).
2. From the Job Positions kanban, click **Configure** on the
   **Bench QA Engineer** card to open the full job form.
3. On the job form, open the **Summary** notebook tab ("Job
   Description" / "Summary" page) and type exactly this description
   into the HTML editor body:

   `Write automated tests for Bench Products.`

4. Flip the **Published** boolean toggle on the job form to ON
   (publish the job). This toggle sits next to the "Target" / "new
   employees" row in the Details/Recruitment section.
5. **Save** the job.
6. After saving, click the **Go to Website** smart button in the
   button box to preview the job. You should land on the public
   page `/jobs/<slug>` (the URL contains the job slug) and see the
   seeded **Requirements** section (Python, Playwright, 2+ yrs).

# Rules

- Do not rename the job.
- Do not edit the Website Description / frontend page content.
- Do not create or delete any other job positions.
- Do not create any applicants.
- Do not unpublish the job after publishing it.
- The description text in step 3 must match exactly
  (case-sensitive), and must be the only text you add to the
  Summary body.
