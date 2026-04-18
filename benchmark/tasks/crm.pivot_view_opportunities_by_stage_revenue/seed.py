"""Seed CRM opportunities across stages for the pivot-by-stage task.

Category 1 (EASY): Switch the CRM pipeline to pivot view, group by Stage,
set the Measures to Expected Revenue, and save the view as a favorite
named "Bench Stage Revenue Pivot".

Seeds four opportunities spread across different stages with distinct
expected_revenue values so that the pivot table has meaningful cells.
Also removes any prior "Bench Stage Revenue Pivot" favorite filter.
"""

FAVORITE_NAME = "Bench Stage Revenue Pivot"

SEED_OPPS = [
    {
        "name": "Bench Pivot Alpha",
        "partner_name": "Bench Pivot Alpha",
        "email": "alpha@benchpivot.test",
        "stage": "New",
        "revenue": 10000.0,
    },
    {
        "name": "Bench Pivot Bravo",
        "partner_name": "Bench Pivot Bravo",
        "email": "bravo@benchpivot.test",
        "stage": "Qualified",
        "revenue": 25000.0,
    },
    {
        "name": "Bench Pivot Charlie",
        "partner_name": "Bench Pivot Charlie",
        "email": "charlie@benchpivot.test",
        "stage": "Proposition",
        "revenue": 42000.0,
    },
    {
        "name": "Bench Pivot Delta",
        "partner_name": "Bench Pivot Delta",
        "email": "delta@benchpivot.test",
        "stage": "Won",
        "revenue": 80000.0,
    },
]


def _get_or_create_stage(env, name, sequence):
    stage = env["crm.stage"].search([("name", "=", name)], limit=1)
    if not stage:
        stage = env["crm.stage"].create({"name": name, "sequence": sequence})
    return stage


def setup(env):
    # --- Cleanup any prior favorite with this exact name ---
    env["ir.filters"].search([
        ("name", "=", FAVORITE_NAME),
        ("model_id", "=", "crm.lead"),
    ]).unlink()

    # --- Cleanup any prior seeded opportunities ---
    partner_names = [opp["partner_name"] for opp in SEED_OPPS]
    env["crm.lead"].search([("partner_name", "in", partner_names)]).unlink()

    # --- Ensure required stages exist ---
    stage_map = {}
    for idx, stage_name in enumerate(["New", "Qualified", "Proposition", "Won"], start=1):
        stage_map[stage_name] = _get_or_create_stage(env, stage_name, idx)

    # --- Sales team and admin user ---
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)

    # --- Create the seeded opportunities ---
    for opp in SEED_OPPS:
        env["crm.lead"].create({
            "name": opp["name"],
            "partner_name": opp["partner_name"],
            "email_from": opp["email"],
            "type": "opportunity",
            "stage_id": stage_map[opp["stage"]].id,
            "expected_revenue": opp["revenue"],
            "team_id": sales_team.id if sales_team else False,
            "user_id": admin.id if admin else False,
            "description": f"Seeded opportunity for pivot-by-stage benchmark ({opp['stage']}).",
        })
