"""Database seed for website_hr_recruitment.apply_guru_job.

Creates the prerequisite records needed for the task:
- A department ("guru team")
- A published job posting ("Guru") in that department

Mirrors the setup in:
  addons/website_hr_recruitment/tests/test_website_hr_recruitment.py::test_tour
"""


def setup(env):
    """Seed the database with the required records."""
    department = env["hr.department"].create({"name": "guru team"})
    env["hr.job"].create({
        "name": "Guru",
        "is_published": True,
        "department_id": department.id,
    })
