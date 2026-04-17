"""Postcondition checks for website.add_menu_item_reorder."""


def check(env):
    website = env["website"].browse(1)
    root_menu = website.menu_id
    menus = env["website.menu"].search(
        [("website_id", "=", website.id), ("parent_id", "=", root_menu.id)],
        order="sequence, id",
    )
    names = [menu.name for menu in menus if menu.name in {"Home", "Consulting", "Resources", "Support", "Contact"}]

    failures = []
    resources = menus.filtered(lambda m: m.name == "Resources")
    if len(resources) != 1:
        failures.append(f"Expected exactly one Resources menu, found {len(resources)}")
    elif resources.url != "/resources":
        failures.append(f"Resources menu URL is {resources.url!r}, expected '/resources'")

    expected_order = ["Home", "Consulting", "Resources", "Support", "Contact"]
    if names[:5] != expected_order:
        failures.append(f"Top-level menu order is {names[:5]!r}, expected {expected_order!r}")

    return failures
