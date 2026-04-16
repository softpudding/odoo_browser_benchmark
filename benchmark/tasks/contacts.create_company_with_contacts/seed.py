"""Seed for the create-company-with-contacts task.

Category 5: Deep UI interaction.
The agent must create three contact records in sequence: one Company and two
Individuals linked to that company. Browser-use often fails to correctly set
the company linkage on the second contact, or enters incorrect job titles /
emails for one of the two individuals after creating multiple records.
The multi-record creation sequence (company → contact 1 → contact 2) causes
context drift.
"""


def setup(env):
    # --- Cleanup prior runs ---
    # Remove all three contacts if they exist from a prior run
    for name in ["Vantage Industrial Group", "Patricia Drum", "Steven Okafor"]:
        partners = env["res.partner"].search([("name", "=", name)])
        partners.unlink()
