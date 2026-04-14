"""Seed public jobs for a public-to-backend recruitment task."""


def setup(env):
    platform_ops = env["hr.department"].create({"name": "Platform Ops"})
    customer_success = env["hr.department"].create({"name": "Customer Success"})

    jobs = [
        {
            "name": "Platform Support Specialist",
            "department_id": platform_ops.id,
            "is_published": True,
            "website_description": """
                <section><div class="container">
                    <p>Own the pager rotation and coordinate incident follow-through.</p>
                </div></section>
            """,
        },
        {
            "name": "Platform Support Coordinator",
            "department_id": platform_ops.id,
            "is_published": True,
            "website_description": """
                <section><div class="container">
                    <p>Coordinate onboarding checklists and reporting cadences.</p>
                </div></section>
            """,
        },
        {
            "name": "Customer Success Specialist",
            "department_id": customer_success.id,
            "is_published": True,
            "website_description": """
                <section><div class="container">
                    <p>Guide customer enablement programs and renewals.</p>
                </div></section>
            """,
        },
    ]
    env["hr.job"].create(jobs)


