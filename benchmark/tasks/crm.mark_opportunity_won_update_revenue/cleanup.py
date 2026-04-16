"""Clean up artifacts from previous runs."""


OPP_NAMES = [
    "Crestline Networks - Managed VPN",
    "Crestline Networks - Firewall Expansion",
    "Crestline Retail - POS Refresh",
]


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search(
        [("name", "in", OPP_NAMES)]
    )
    if leads:
        env["mail.message"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()
