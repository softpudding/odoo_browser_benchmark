"""Postcondition checks for sale_project.confirm_quote_and_update_generated_project."""


def check(env):
    failures = []

    order = env["sale.order"].search([
        ("client_order_ref", "in", ["SERV-PROJ-17", "SERV-PROJ-17-LIVE"]),
    ], limit=1)
    other_order = env["sale.order"].search([("client_order_ref", "=", "SERV-PROJ-18")], limit=1)
    if not order or not other_order:
        return ["Missing seeded sales orders for sale_project handoff task"]

    if order.state != "sale":
        failures.append(f"Target quotation state is {order.state!r}, expected 'sale'")
    if order.client_order_ref != "SERV-PROJ-17-LIVE":
        failures.append(
            f"Target customer reference is {order.client_order_ref!r}, expected 'SERV-PROJ-17-LIVE'"
        )
    if other_order.state != "draft":
        failures.append(
            f"Distractor quotation state is {other_order.state!r}, expected to remain 'draft'"
        )

    project = order.project_id
    if not project:
        failures.append("Confirmed sales order did not expose a generated project")
        return failures

    if "2 service tasks generated from SERV-PROJ-17" not in (project.description or ""):
        failures.append(
            f"Project description is {project.description!r}, expected the exact summary text"
        )

    kickoff = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Bluebird Sprint Kickoff"),
    ], limit=1)
    training = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Bluebird Training Review"),
    ], limit=1)

    if not kickoff:
        failures.append("Missing renamed task 'Bluebird Sprint Kickoff'")
    elif kickoff.stage_id.name != "In Progress":
        failures.append(
            f"Kickoff task stage is {kickoff.stage_id.name!r}, expected 'In Progress'"
        )

    if not training:
        failures.append("Missing renamed task 'Bluebird Training Review'")
    elif training.stage_id.name != "Done":
        failures.append(
            f"Training task stage is {training.stage_id.name!r}, expected 'Done'"
        )

    if env["project.task"].search_count([
        ("project_id", "=", project.id),
        ("name", "in", ["Implementation stream", "Training stream"]),
    ]):
        failures.append("Original generated task names are still present in the target project")

    if env["project.task"].search_count([("project_id", "=", project.id)]) != 2:
        failures.append("Target project should contain exactly 2 tasks after the update")

    return failures
