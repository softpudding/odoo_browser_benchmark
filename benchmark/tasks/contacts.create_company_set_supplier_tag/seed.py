"""Seed contact data for the create-company-set-supplier-tag task.

Category 2 (MEDIUM): the agent must create one company contact from scratch and
fill multiple contact fields, including a state/country many2one pair and one
many2many tag.
"""

COMPANY_NAME = "Harborview Fabrication"
TAG_NAME = "Supplier"


def setup(env):
    env["res.partner"].search([("name", "=", COMPANY_NAME)]).unlink()

    tag = env["res.partner.category"].search([("name", "=", TAG_NAME)], limit=1)
    if not tag:
        env["res.partner.category"].create({"name": TAG_NAME})
