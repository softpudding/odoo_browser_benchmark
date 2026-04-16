"""Seed a medium company-creation workflow in Contacts."""

TARGET_NAME = "Harborview Components"
DISTRACTOR_NAME = "Harborview Component Services"


def _ensure_tag(env, name):
    tag = env["res.partner.category"].search([("name", "=", name)], limit=1)
    if not tag:
        tag = env["res.partner.category"].create({"name": name})
    return tag


def setup(env):
    supplier_tag = _ensure_tag(env, "Supplier")
    finance_tag = _ensure_tag(env, "Finance")

    env["res.partner"].search([
        ("name", "=", TARGET_NAME),
        ("is_company", "=", True),
    ]).unlink()

    distractor = env["res.partner"].search([
        ("name", "=", DISTRACTOR_NAME),
        ("is_company", "=", True),
    ], limit=1)
    if distractor:
        distractor.write({
            "phone": "+1 (415) 555-0102",
            "website": "www.harborview-services.example.com",
            "category_id": [(6, 0, [supplier_tag.id])],
        })
    else:
        env["res.partner"].create({
            "name": DISTRACTOR_NAME,
            "is_company": True,
            "phone": "+1 (415) 555-0102",
            "website": "www.harborview-services.example.com",
            "city": "Oakland",
            "zip": "94607",
            "country_id": env.ref("base.us").id,
            "category_id": [(6, 0, [supplier_tag.id])],
        })

    # Ensure the finance tag exists but is not pre-applied to the distractor.
    if finance_tag in env["res.partner"].search([
        ("name", "=", DISTRACTOR_NAME),
        ("is_company", "=", True),
    ], limit=1).category_id:
        env["res.partner"].search([
            ("name", "=", DISTRACTOR_NAME),
            ("is_company", "=", True),
        ], limit=1).write({"category_id": [(3, finance_tag.id)]})
