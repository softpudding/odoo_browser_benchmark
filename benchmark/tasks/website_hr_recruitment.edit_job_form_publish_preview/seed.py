"""Seed for website_hr_recruitment.edit_job_form_publish_preview.

Category: deep_ui_interaction (medium).

A single unpublished `hr.job` named "Bench QA Engineer" is created with:
- empty `description` (backend Summary/Job Description HTML field)
- pre-populated `website_description` containing a "Requirements"
  section that mentions "Python, Playwright, 2+ yrs"
- is_published/website_published = False

The agent must:
1. Edit `description` to the exact expected phrase via the backend
   Summary tab HTML editor.
2. Toggle `website_published` (Published boolean_toggle) to True.
3. Save and click Go to Website to preview /jobs/<slug>.

The website_description Requirements content is pre-seeded so the
agent does NOT need to touch the fragile iframe frontend editor —
this keeps the task at medium difficulty while still letting check.py
assert on the Requirements section staying intact.

Cleanup is performed first for idempotency.
"""

JOB_NAME = "Bench QA Engineer"

WEBSITE_DESCRIPTION_HTML = """<section class="pt32">
  <div class="container">
    <div class="row">
      <div class="col-lg-8 pb32">
        <h2>About the Role</h2>
        <p>Join the Bench Products QA team to build and maintain
        automated browser test coverage for our flagship products.</p>
        <h3>Requirements</h3>
        <ul>
          <li>Python, Playwright, 2+ yrs of test automation experience</li>
          <li>Comfortable reading production Odoo source code</li>
          <li>Clear written communication</li>
        </ul>
      </div>
    </div>
  </div>
</section>"""


def setup(env):
    # ----- Cleanup prior runs -----
    old_jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    if old_jobs:
        # Unlink any applicants linked to these jobs first (shouldn't exist, but be safe)
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "in", old_jobs.ids),
        ]).unlink()
        old_jobs.unlink()

    # ----- Ensure a department to attach to -----
    dept = env["hr.department"].search([("name", "=", "Administration")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Administration"})

    # ----- Create the unpublished job -----
    env["hr.job"].create({
        "name": JOB_NAME,
        "department_id": dept.id,
        "no_of_recruitment": 1,
        "description": False,  # empty; agent must type into Summary HTML editor
        "website_description": WEBSITE_DESCRIPTION_HTML,
        "website_published": False,
        "is_published": False,
    })
