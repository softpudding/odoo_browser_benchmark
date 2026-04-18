"""Seed three companies in two cities for a segmented Email Marketing draft.

Category: Deep UI interaction (domain editor + WYSIWYG body).
The agent must create a mailing.mailing record, switch the recipients model
from the default 'Mailing List' to 'Contact', open the domain widget and
add a single rule (City = Berlin) so that the recipient count drops from
all contacts to exactly 2 (the two Berlin companies), fill the email body
and save as draft (NOT send).
"""


SUBJECT = "Berlin April Bulletin"
PARTNERS = [
    {"name": "Berlin Alpha Co", "city": "Berlin", "email": "alpha@berlin.example.com"},
    {"name": "Berlin Beta Co", "city": "Berlin", "email": "beta@berlin.example.com"},
    {"name": "Munich Gamma Co", "city": "Munich", "email": "gamma@munich.example.com"},
]


def _ensure_mass_mailing_module(env):
    module = env["ir.module.module"].search([("name", "=", "mass_mailing")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def setup(env):
    _ensure_mass_mailing_module(env)

    # Cleanup any prior mailing with this subject (any state).
    env["mailing.mailing"].search([("subject", "=", SUBJECT)]).unlink()

    # Cleanup prior seed companies, but only if there are no business records
    # tying them down. Use sudo to bypass any record rules.
    for spec in PARTNERS:
        existing = env["res.partner"].sudo().search([
            ("name", "=", spec["name"]),
            ("is_company", "=", True),
        ])
        # Try to unlink; if blocked (e.g. referenced by other records), just
        # update the relevant fields in place to match the spec.
        survivors = env["res.partner"]
        for partner in existing:
            try:
                partner.unlink()
            except Exception:
                survivors |= partner
        if survivors:
            survivors.write({
                "city": spec["city"],
                "email": spec["email"],
                "is_company": True,
            })

    # Create fresh seed companies.
    for spec in PARTNERS:
        if env["res.partner"].sudo().search_count([
            ("name", "=", spec["name"]),
            ("city", "=", spec["city"]),
            ("is_company", "=", True),
        ]):
            continue
        env["res.partner"].create({
            "name": spec["name"],
            "is_company": True,
            "city": spec["city"],
            "email": spec["email"],
        })
