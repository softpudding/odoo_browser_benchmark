"""Seed for website_customer.publish_customer_reference_on_public_page.

Category: closed_loop_cross_module (medium).

Installs `website_customer` on demand (not in the base snapshot) and
creates one company `res.partner` named "Bench Happy Client" with the
fields required to qualify for the public `/customers` page:

- `is_company=True`
- `country_id` set (United States)
- `website` URL filled
- `assigned_partner_id` set (self-assigned to its own record via a
  separate seeded "Bench Delivery Partner" company, so the domain
  filter `assigned_partner_id != False` is satisfied). The implementing
  partner itself doesn't need to be published — only its role as the
  m2o target matters for the /customers domain.
- `website_published=False` (the agent must flip this True)

Cleanup is performed first so the task is idempotent across re-runs.
"""

CLIENT_NAME = "Bench Happy Client"
IMPLEMENTER_NAME = "Bench Delivery Partner"
CLIENT_WEBSITE = "http://benchhappyclient.example.com"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        return
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # Install website_customer on demand (pulls in website_crm_partner_assign
    # and website_partner).
    _ensure_module(env, "website_customer")

    # Cleanup prior runs (child-first). Clear any partner.assigned_partner_id
    # back-references and then unlink both companies.
    old_partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "in", [CLIENT_NAME, IMPLEMENTER_NAME]),
    ])
    if old_partners:
        # Null out any m2o back-refs pointing at these partners before unlink.
        referring = env["res.partner"].with_context(active_test=False).search([
            ("assigned_partner_id", "in", old_partners.ids),
        ])
        if referring:
            referring.sudo().write({"assigned_partner_id": False})
        try:
            old_partners.sudo().unlink()
        except Exception:
            # If unlink blocked by fk constraints from other modules, just
            # archive + rename so a fresh create works.
            old_partners.sudo().write({
                "name": "Obsolete Bench Reference (cleanup)",
                "active": False,
            })

    # Look up country US (present in base).
    country = env.ref("base.us", raise_if_not_found=False)

    # Create the "Implemented by" delivery partner (no special fields needed).
    implementer = env["res.partner"].create({
        "name": IMPLEMENTER_NAME,
        "is_company": True,
        "country_id": country.id if country else False,
    })

    # Create the customer reference, unpublished.
    env["res.partner"].create({
        "name": CLIENT_NAME,
        "is_company": True,
        "country_id": country.id if country else False,
        "website": CLIENT_WEBSITE,
        "city": "Austin",
        "street": "100 Market Street",
        "zip": "73301",
        "assigned_partner_id": implementer.id,
        "website_published": False,
        "is_published": False,
    })
