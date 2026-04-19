You will complete a two-phase recruitment workflow that crosses the public
website and the back-office Recruitment app.

## Phase 1 — Submit a public application

The public Jobs page already has a published position titled
**"Senior Backend Engineer"**.

1. Open the public Jobs page at `/jobs` (no login needed).
2. Click the **"Senior Backend Engineer"** job link.
3. Click **"Apply"** (or **"Apply Now"**) to open the application form.
4. Fill the form with these exact values:
   - **Your Name**: `Bench Candidate`
   - **Email**: `bench.candidate@example.com`
   - **Phone**: `+1 555 0143`
   - **LinkedIn Profile**: `linkedin.com/in/bench-candidate`
   - **Short Introduction** (cover letter): `Excited to interview for the Senior Backend Engineer role.`
5. Click the submit button (labelled **"Send"** / **"I'm feeling lucky"**, class `.s_website_form_send`).
6. Wait for the confirmation / thank-you message.

## Phase 2 — Schedule an Interview activity (back-office)

Now log in as the admin user and open the **Recruitment** app
(`/odoo/recruitment`).

1. Open the **"Senior Backend Engineer"** job pipeline to see the newly created
   applicant (**Bench Candidate**).
2. Click Bench Candidate's kanban card to open the applicant form.
3. In the chatter at the bottom, click the **Activities** icon (or the
   **"Activity"** button) to schedule a new activity. In the modal:
   - **Activity Type**: **Meeting** (change from the default "To-Do")
   - **Summary**: `Interview`
   - **Due Date**: `05/04/2026` (May 4, 2026)
4. Click **Schedule** (or **Save**) to confirm the activity.

## Rules

- Do **not** delete or archive any existing applicants.
- Do **not** move Bench Candidate to a different stage — she should stay at
  the default initial stage.
- The applicant's **Email** must be `bench.candidate@example.com` exactly.
- The activity **Summary** must be exactly `Interview` (not "Schedule interview"
  or "First interview").
- The activity **Due Date** must be **2026-05-04** (May 4, 2026).
- Only create **one** applicant and **one** activity.
