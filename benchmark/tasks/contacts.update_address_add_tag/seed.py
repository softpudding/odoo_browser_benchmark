"""Seed a company contact for the update-address-add-tag task.

Category 2 (MEDIUM): Update multiple address fields, add a tag, and set
job position on an existing contact. Multiple field edits across the form
including address, tags (many2many), and text fields.
"""

COMPANY_NAME = "Brookfield Dynamics"


def setup(env):
    # --- Cleanup prior runs ---
    old = env["res.partner"].search([("name", "=", COMPANY_NAME)])
    old.unlink()

    # --- Ensure "Supplier" tag exists ---
    tag = env["res.partner.category"].search(
        [("name", "=", "Supplier")], limit=1
    )
    if not tag:
        env["res.partner.category"].create({"name": "Supplier"})

    # --- Create company contact with partial address ---
    env["res.partner"].create({
        "name": COMPANY_NAME,
        "is_company": True,
        "email": "info@brookfielddynamics.com",
        "phone": "+1 555 0300",
        "street": "100 Main Street",
        "city": "Seattle",
        "zip": "98101",
        "country_id": env.ref("base.us").id,
    })
