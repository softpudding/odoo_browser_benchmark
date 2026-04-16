"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["crm.lead"].with_context(active_test=False).search([
        ("name", "in", ["Northwind Renewal Review", "Northwind Renewal Pilot"])
    ]).unlink()
