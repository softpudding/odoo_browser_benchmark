"""Clean up artifacts from previous runs."""


def cleanup(env):
    lead_env = env["crm.lead"].with_context(active_test=False)
    leads = lead_env.search(
        [
            (
                "name",
                "in",
                [
                    "Blue Canyon Power Renewal",
                    "Blue Canyon Power Expansion",
                    "Blue Canyon Logistics Renewal",
                ],
            )
        ]
    )
    if leads:
        leads.unlink()
    env["crm.lost.reason"].search(
        [("name", "in", ["Deferred to FY27 budget", "Deferred to next budget cycle"])]
    ).unlink()
