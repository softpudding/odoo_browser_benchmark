"""Seed company data for the update-company-with-supplier-tag task.

Category 2 (MEDIUM): update one existing company record with several fields and
a tag while avoiding a similarly named distractor company.
"""

TARGET_COMPANY = "North Coast Fabrication"
DISTRACTOR_COMPANY = "North Coast Fabricators"
TAG_NAME = "Supplier"


def setup(env):
    tag = env["res.partner.category"].search([("name", "=", TAG_NAME)], limit=1)
    if not tag:
        env["res.partner.category"].create({"name": TAG_NAME})

    country = env.ref("base.us")
    washington = env["res.country.state"].search([
        ("code", "=", "WA"),
        ("country_id", "=", country.id),
    ], limit=1)

    target = env["res.partner"].search(
        [("name", "=", TARGET_COMPANY), ("is_company", "=", True)],
        limit=1,
    )
    if not target:
        target = env["res.partner"].create({
            "name": TARGET_COMPANY,
            "is_company": True,
            "phone": "+1 (206) 555-0101",
            "website": "www.northcoast.example.com",
            "country_id": country.id,
        })
    else:
        target.write({
            "is_company": True,
            "phone": "+1 (206) 555-0101",
            "website": "www.northcoast.example.com",
            "street": False,
            "city": False,
            "zip": False,
            "state_id": washington.id if washington else False,
            "country_id": country.id,
            "category_id": [(5, 0, 0)],
        })

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
