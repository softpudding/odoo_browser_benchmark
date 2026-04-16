"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["crm.lead"].search([
        ("name", "in", [
            "Spark Innovations - Pager SaaS",
            "Riverstone Retail - Fitting Line",
        ]),
    ]).unlink()
