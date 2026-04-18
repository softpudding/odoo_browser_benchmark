"""Clean up the seeded contact form page and any created lead."""


CONTACT_PAGE_URL = "/contactus-bench"
CONTACT_PAGE_KEY = "benchmark.contactus_bench_lead_page"

CONTACT_NAME = "Bench Prospect Q4"
CONTACT_EMAIL = "prospect@bench.test"
CONTACT_SUBJECT = "Requesting demo"


def cleanup(env):
    # Drop any leads created during the task run.
    leads = env["crm.lead"].with_context(active_test=False).search([
        "|", "|",
        ("email_from", "=", CONTACT_EMAIL),
        ("contact_name", "=", CONTACT_NAME),
        ("name", "=", CONTACT_SUBJECT),
    ])
    if leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()

    env["website.rewrite"].search([
        ("url_from", "in", [CONTACT_PAGE_URL]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", [CONTACT_PAGE_URL]),
    ]).unlink()
    env["ir.ui.view"].search([
        ("key", "=", CONTACT_PAGE_KEY),
    ]).unlink()
