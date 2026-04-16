"""Seed data for contacts.create_company_add_supplier_tag."""

TARGET_NAME = "North Coast Fabrication"
DISTRACTOR_NAME = "North Coast Fabrication East"


def _ensure_company(env, name, email):
    company = env["res.partner"].search([("name", "=", name)], limit=1)
    if company:
        company.write({
            "is_company": True,
            "email": email,
            "website": False,
            "street": False,
            "city": False,
            "zip": False,
            "phone": False,
            "category_id": [(5, 0, 0)],
        })
        return company
    return env["res.partner"].create({
        "name": name,
        "is_company": True,
        "email": email,
    })


def setup(env):
    env["res.partner"].search([("name", "=", TARGET_NAME)]).unlink()
    _ensure_company(env, DISTRACTOR_NAME, "east@northcoastfab.example.com")

    tag = env["res.partner.category"].search([("name", "=", "Supplier")], limit=1)
    if not tag:
        env["res.partner.category"].create({"name": "Supplier"})
