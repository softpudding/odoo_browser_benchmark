You will complete a two-phase recruitment workflow that round-trips
between the Odoo back-office and the public website.

# Phase 1 — Back-office: create and publish a new job

1. Open the **Recruitment** app (URL `/odoo/recruitment`).
2. Open **Configuration → Job Positions** (or click **New** from the
   Recruitment dashboard / job-positions kanban) and create a new
   job position with these exact values:
   - **Job Title / Position**: `Senior Widget Engineer`
   - **Department**: `Administration`
   - **Target** (number of new employees to recruit): `2`
   - **Job Description**: `Design and build widgets. Remote-friendly.`
3. **Save** the job.
4. Publish the job to the public website. Either:
   - Click the **Go to Website** smart button on the job form, then
     toggle the top-right **Unpublished → Published** switch, OR
   - Set the published state directly so the job becomes visible on
     `/jobs`.
   The result must be that the job is **Published** (visible to public
   visitors on `/jobs`).

# Phase 2 — Portal: submit an application as a candidate

5. Navigate to the public jobs page at `/jobs`.
6. Click the **Senior Widget Engineer** link to open the job detail
   page.
7. Click **Apply Now**.
8. Fill the public application form with:
   - **Your Name**: `Alex Portal`
   - **Your Email**: `alex.portal@example.com`
   - **Phone Number**: `+1 555 0199`
   - **LinkedIn Profile**: `linkedin.com/in/alex-portal`
   - **Short Introduction**: `Excited to apply for this role.`
9. **Submit** the application (the submit button is labelled "I'm
   feeling lucky"). You should land on a confirmation / thank-you
   page.

# Rules

- Do not create any other job positions.
- Do not create any other applicants.
- The job name and applicant fields must match the values above
  exactly (case-sensitive).
- Do not unpublish the job after publishing it.
