"""Seed company contacts for the create-linked-contact-add-tag task.

Category 2 (MEDIUM): Create a person contact linked to the correct existing
company and add a tag while avoiding a similarly named distractor company.
"""

COMPANY_NAME = "Seabird Logistics"
DISTRACTOR_COMPANY = "Seabird Logistics West"
TAG_NAME = "Logistics"
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

    tag = env["res.partner.category"].search([("name", "=", TAG_NAME)], limit=1)
    if not tag:
        env["res.partner.category"].create({"name": TAG_NAME})
