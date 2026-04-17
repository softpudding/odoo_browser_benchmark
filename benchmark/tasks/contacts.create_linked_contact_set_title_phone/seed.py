"""Seed company contacts for contacts.create_linked_contact_set_title_phone."""

COMPANY_NAME = "Seabird Logistics"
DISTRACTOR_COMPANY = "Seabird Logistics West"
CONTACT_NAME = "Leah Morgan"


def _ensure_company(env, name, email):
    company = env["res.partner"].search([("name", "=", name)], limit=1)
    if company:
        company.write({"is_company": True, "email": email})
        return company
    return env["res.partner"].create({
        "name": name,
        "is_company": True,
        "email": email,
    })


def setup(env):
    env["res.partner"].search([("name", "=", CONTACT_NAME)]).unlink()
    _ensure_company(env, COMPANY_NAME, "ops@seabird.example.com")
    _ensure_company(env, DISTRACTOR_COMPANY, "west@seabird.example.com")
