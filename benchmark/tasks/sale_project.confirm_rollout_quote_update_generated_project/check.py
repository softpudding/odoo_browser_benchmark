"""Postcondition checks for sale_project.confirm_rollout_quote_update_generated_project."""


def check(env):
    failures = []

    order = env["sale.order"].search([
        ("client_order_ref", "in", ["ROLL-PROJ-31", "ROLL-PROJ-31-LIVE"]),
    ], limit=1)
    distractor = env["sale.order"].search([
        ("client_order_ref", "=", "ROLL-PROJ-32"),
    ], limit=1)
    if not order or not distractor:
        return ["Missing seeded quotations for sale_project rollout task"]

    if order.state != "sale":
        failures.append(f"Target quotation state is {order.state!r}, expected 'sale'")
    if order.client_order_ref != "ROLL-PROJ-31-LIVE":
        failures.append(
            f"Target customer reference is {order.client_order_ref!r}, expected 'ROLL-PROJ-31-LIVE'"
        )
    if distractor.state != "draft":
        failures.append(
            f"Distractor quotation state is {distractor.state!r}, expected to remain 'draft'"
        )

    project = order.project_id
    if not project:
        failures.append("Confirmed sales order did not expose a generated project")
        return failures

    if "2 rollout tasks generated from ROLL-PROJ-31" not in (project.description or ""):
        failures.append(
            f"Project description is {project.description!r}, expected the exact summary text"
        )

    kickoff = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Atlas Rollout Kickoff"),
    ], limit=1)
    signoff = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Atlas Go-Live Signoff"),
    ], limit=1)

    if not kickoff:
        failures.append("Missing renamed task 'Atlas Rollout Kickoff'")
    elif kickoff.stage_id.name != "In Progress":
        failures.append(
            f"Kickoff task stage is {kickoff.stage_id.name!r}, expected 'In Progress'"
        )

    if not signoff:
        failures.append("Missing renamed task 'Atlas Go-Live Signoff'")
    elif signoff.stage_id.name != "Done":
        failures.append(
            f"Signoff task stage is {signoff.stage_id.name!r}, expected 'Done'"
        )

    if env["project.task"].search_count([
        ("project_id", "=", project.id),
        ("name", "in", ["Discovery Workshop", "Go-Live Review"]),
    ]):
        failures.append("Original generated task names are still present in the target project")

    if env["project.task"].search_count([("project_id", "=", project.id)]) != 2:
        failures.append("Target project should contain exactly 2 tasks after the update")

    return failures
