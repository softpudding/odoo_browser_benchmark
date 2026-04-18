"""Postcondition checks for pos_restaurant.open_table_order_mark_ready."""


CONFIG_NAME = "Bench Restaurant"
FLOOR_NAME = "Main Floor"
STARTER_NAME = "Starter Salad"
MAIN_NAME = "Main Steak"


def check(env):
    failures = []

    config = env["pos.config"].search([("name", "=", CONFIG_NAME)], limit=1)
    if not config:
        return [f"POS config '{CONFIG_NAME}' is missing"]
    if not config.module_pos_restaurant:
        failures.append(
            f"POS config '{CONFIG_NAME}' is not a restaurant (module_pos_restaurant=False)"
        )

    sessions = env["pos.session"].search([("config_id", "=", config.id)])
    if not sessions:
        failures.append(f"No POS session was opened for '{CONFIG_NAME}'")
    else:
        open_sessions = sessions.filtered(
            lambda s: s.state in {"opened", "opening_control"}
        )
        if not open_sessions:
            failures.append(
                f"POS session for '{CONFIG_NAME}' is not open anymore "
                f"(states={[s.state for s in sessions]})"
            )

    # Exactly one T1 table on Main Floor.
    floor = env["restaurant.floor"].search([("name", "=", FLOOR_NAME)], limit=1)
    if not floor or config not in floor.pos_config_ids:
        return failures + [
            f"Floor '{FLOOR_NAME}' is missing or not linked to '{CONFIG_NAME}'"
        ]
    tables = env["restaurant.table"].search([("floor_id", "=", floor.id)])
    t1 = tables.filtered(lambda t: t.table_number == 1)
    if not t1:
        return failures + [f"Table T1 (table_number=1) on '{FLOOR_NAME}' is missing"]

    orders = env["pos.order"].search([("config_id", "=", config.id)])
    if len(orders) != 1:
        return failures + [
            f"Expected exactly 1 POS order on '{CONFIG_NAME}', found {len(orders)}"
        ]

    order = orders[0]

    # Order must be linked to T1.
    if not order.table_id:
        failures.append("POS order has no table_id set")
    elif order.table_id.id != t1.id:
        failures.append(
            f"POS order is attached to table '{order.table_id.display_name}', "
            f"expected T1 (id={t1.id})"
        )

    # Exactly two product lines: Starter Salad and Main Steak.
    product_names = sorted(order.lines.mapped("product_id.display_name"))
    expected_names = sorted([STARTER_NAME, MAIN_NAME])
    if product_names != expected_names:
        failures.append(
            f"Order lines products are {product_names}, expected {expected_names}"
        )
    if len(order.lines) != 2:
        failures.append(
            f"Expected exactly 2 order lines, found {len(order.lines)}"
        )

    # Per-line: Starter Salad at 15 x 1, Main Steak at 20 x 1.
    starter_lines = order.lines.filtered(
        lambda l: l.product_id.display_name == STARTER_NAME
    )
    main_lines = order.lines.filtered(
        lambda l: l.product_id.display_name == MAIN_NAME
    )
    if len(starter_lines) == 1:
        sl = starter_lines[0]
        if abs(sl.qty - 1.0) > 0.0001:
            failures.append(f"'{STARTER_NAME}' qty is {sl.qty}, expected 1.0")
        if abs(sl.price_unit - 15.0) > 0.01:
            failures.append(
                f"'{STARTER_NAME}' price_unit is {sl.price_unit}, expected 15.0"
            )
    else:
        failures.append(
            f"Expected exactly 1 '{STARTER_NAME}' line, found {len(starter_lines)}"
        )
    if len(main_lines) == 1:
        ml = main_lines[0]
        if abs(ml.qty - 1.0) > 0.0001:
            failures.append(f"'{MAIN_NAME}' qty is {ml.qty}, expected 1.0")
        if abs(ml.price_unit - 20.0) > 0.01:
            failures.append(
                f"'{MAIN_NAME}' price_unit is {ml.price_unit}, expected 20.0"
            )
    else:
        failures.append(
            f"Expected exactly 1 '{MAIN_NAME}' line, found {len(main_lines)}"
        )

    # Order must stay in draft (not paid, not invoiced) -- the task does NOT
    # include a payment step.
    if order.state not in {"draft"}:
        failures.append(
            f"POS order state is '{order.state}', expected 'draft' "
            f"(no payment step in this task)"
        )

    # Kitchen 'ready' signal: at least one restaurant.order.course on this
    # order must have fired=True.
    fired_courses = order.course_ids.filtered(lambda c: c.fired)
    if not fired_courses:
        failures.append(
            "No restaurant.order.course with fired=True found on the order; "
            "expected at least one fired (kitchen-ready) course."
        )

    return failures
