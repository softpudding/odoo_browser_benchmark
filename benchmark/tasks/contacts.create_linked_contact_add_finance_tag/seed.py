"""Seed company contacts for the create-linked-contact-add-finance-tag task.

Category 2 (MEDIUM): create a child contact under the correct company, fill
contact and address fields, and add a tag while avoiding a similarly named
distractor company.
"""

COMPANY_NAME = "Lakeshore Manufacturing"
DISTRACTOR_COMPANY = "Lakeshore Manufacturing East"
TAG_NAME = "Finance"
CONTACT_NAME = "Dana Patel"


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

    _ensure_company(env, COMPANY_NAME, "ap@lakeshore.example.com")
    _ensure_company(env, DISTRACTOR_COMPANY, "east@lakeshore.example.com")

    tag = env["res.partner.category"].search([("name", "=", TAG_NAME)], limit=1)
    if not tag:
        env["res.partner.category"].create({"name": TAG_NAME})
