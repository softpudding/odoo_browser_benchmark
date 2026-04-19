"""Postcondition checks for product.configure_stock_route_for_product.

Validates:
    1. product.template 'Bench MTO Item' still exists and is active.
    2. Its route_ids contains exactly one route: the MTO route
       (xmlid stock.route_warehouse0_mto).
    3. No other route was (accidentally) enabled — checkbox groups are
       easy to mis-click.
    4. Product identity fields (name/type/is_storable) unchanged.
"""

PRODUCT_NAME = "Bench MTO Item"


def check(env):
    failures = []

    Template = env["product.template"].with_context(active_test=False)
    templates = Template.search([("name", "=", PRODUCT_NAME)])

    if len(templates) == 0:
        return [f"Product template '{PRODUCT_NAME}' is missing"]
    if len(templates) > 1:
        return [
            f"Expected exactly 1 product.template '{PRODUCT_NAME}', "
            f"found {len(templates)}"
        ]

    tmpl = templates[0]

    # Product integrity (sanity against stray edits on the wrong field).
    if not tmpl.active:
        failures.append(
            f"Product '{PRODUCT_NAME}' must remain active (not archived)."
        )
    if tmpl.type != "consu":
        failures.append(
            f"Product type is '{tmpl.type}', expected 'consu' — agent may "
            f"have edited the product type."
        )
    if not tmpl.is_storable:
        failures.append(
            "Product is_storable is False, expected True — agent may "
            "have flipped the storable toggle."
        )

    # Resolve the MTO route by xmlid. The stock module ships it inactive
    # but the seed activated it.
    mto_route = env.ref(
        "stock.route_warehouse0_mto", raise_if_not_found=False
    )
    if not mto_route:
        failures.append(
            "stock.route_warehouse0_mto (Replenish on Order MTO) route "
            "record is missing from the database."
        )
        return failures
    if not mto_route.active:
        failures.append(
            "Replenish on Order (MTO) route is inactive — seed did not "
            "activate it (or the agent unpublished it)."
        )

    # The critical assertion: route_ids on the product must contain
    # exactly the MTO route.
    route_ids = set(tmpl.route_ids.ids)
    if mto_route.id not in route_ids:
        failures.append(
            f"Product '{PRODUCT_NAME}' route_ids is "
            f"{tmpl.route_ids.mapped('name')!r}; expected it to contain "
            f"'Replenish on Order (MTO)' (xmlid stock.route_warehouse0_mto)."
        )

    extra_ids = route_ids - {mto_route.id}
    if extra_ids:
        extra_routes = env["stock.route"].browse(list(extra_ids))
        failures.append(
            f"Product '{PRODUCT_NAME}' has extra routes enabled: "
            f"{extra_routes.mapped('name')!r}. Only "
            f"'Replenish on Order (MTO)' should be ticked."
        )

    return failures
