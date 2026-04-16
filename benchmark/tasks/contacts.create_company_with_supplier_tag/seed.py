"""Seed company data for the create-company-with-supplier-tag task.

Category 2 (MEDIUM): create one new company record with several fields and a
tag while avoiding a similarly named existing company.
"""

TARGET_COMPANY = "North Coast Fabrication"
DISTRACTOR_COMPANY = "North Coast Fabricators"
TAG_NAME = "Supplier"


def setup(env):
    env["res.partner"].search([("name", "=", TARGET_COMPANY)]).unlink()

    tag = env["res.partner.category"].search([("name", "=", TAG_NAME)], limit=1)
    if not tag:
        env["res.partner.category"].create({"name": TAG_NAME})

    country = env.ref("base.us")
    distractor = env["res.partner"].search(
        [("name", "=", DISTRACTOR_COMPANY), ("is_company", "=", True)],
        limit=1,
    )
    if not distractor:
        distractor = env["res.partner"].create({
            "name": DISTRACTOR_COMPANY,
            "is_company": True,
            "phone": "+1 (206) 555-0110",
            "website": "www.northcoastfabricators.example.com",
            "country_id": country.id,
        })
    else:
        distractor.write({
            "is_company": True,
            "phone": "+1 (206) 555-0110",
            "website": "www.northcoastfabricators.example.com",
            "country_id": country.id,
            "category_id": [(5, 0, 0)],
        })
