"""Postcondition checks for website.add_menu_item_reorder.

Validates:
1. A website.menu named 'Bench Menu' exists on website id=1.
2. Its url is '/bench-menu-target'.
3. It is parented under the main website menu (website.menu_id).
4. Its sequence is strictly between 10 (Home) and 20 (Bench Contact) —
   i.e. it sits in position 2 of the top-level menu.
5. Home and Bench Contact anchor entries still exist and still have
   sequence 10 and 20 respectively (not reordered away).
"""


NEW_MENU_NAME = "Bench Menu"
NEW_MENU_URL = "/bench-menu-target"
ANCHOR_MENU_NAME = "Bench Contact"
ANCHOR_MENU_URL = "/bench-contact-anchor"


def check(env):
    failures = []

    website = env["website"].browse(1)
    root_menu = website.menu_id

    # --- The seeded target page must still exist -----------------------
    target_page = env["website.page"].search([
        ("url", "=", NEW_MENU_URL),
    ], limit=1)
    if not target_page:
        failures.append(f"Seeded page {NEW_MENU_URL!r} is missing")

    # --- The new Bench Menu entry ------------------------------------
    bench_menus = env["website.menu"].search([
        ("name", "=", NEW_MENU_NAME),
        ("website_id", "=", website.id),
    ])
    if not bench_menus:
        return [f"No website.menu named {NEW_MENU_NAME!r} on the primary website"]
    if len(bench_menus) > 1:
        failures.append(
            f"Expected exactly 1 {NEW_MENU_NAME!r} menu on website 1, "
            f"got {len(bench_menus)}"
        )
    bench = bench_menus[0]

    if bench.url != NEW_MENU_URL:
        failures.append(
            f"{NEW_MENU_NAME} url is {bench.url!r}, expected {NEW_MENU_URL!r}"
        )

    if not bench.parent_id or bench.parent_id != root_menu:
        failures.append(
            f"{NEW_MENU_NAME} parent_id is "
            f"{bench.parent_id.display_name!r} (id={bench.parent_id.id}), "
            f"expected the main website menu (id={root_menu.id})"
        )

    if not (10 < bench.sequence < 20):
        failures.append(
            f"{NEW_MENU_NAME} sequence is {bench.sequence}, expected a value "
            "strictly between 10 (Home) and 20 (Bench Contact)"
        )

    # --- Home anchor must still be at sequence 10 ----------------------
    home = env["website.menu"].search([
        ("parent_id", "=", root_menu.id),
        ("website_id", "=", website.id),
        ("url", "in", ("/", "/home")),
    ], limit=1)
    if home and home.sequence != 10:
        failures.append(
            f"Home menu sequence moved to {home.sequence}, expected 10"
        )

    # --- Bench Contact anchor must still be at sequence 20 -------------
    anchor = env["website.menu"].search([
        ("name", "=", ANCHOR_MENU_NAME),
        ("website_id", "=", website.id),
    ], limit=1)
    if not anchor:
        failures.append(
            f"Seeded anchor menu {ANCHOR_MENU_NAME!r} is missing"
        )
    else:
        if anchor.sequence != 20:
            failures.append(
                f"Anchor {ANCHOR_MENU_NAME!r} sequence moved to "
                f"{anchor.sequence}, expected 20"
            )
        if anchor.url != ANCHOR_MENU_URL:
            failures.append(
                f"Anchor {ANCHOR_MENU_NAME!r} url changed to {anchor.url!r}, "
                f"expected {ANCHOR_MENU_URL!r}"
            )

    # --- Position-2 sanity: ordered top-level listing ------------------
    top_level = env["website.menu"].search([
        ("parent_id", "=", root_menu.id),
        ("website_id", "=", website.id),
    ], order="sequence, id")
    names_in_order = [m.name for m in top_level]
    # Bench Menu must appear after Home but before Bench Contact.
    if NEW_MENU_NAME in names_in_order and ANCHOR_MENU_NAME in names_in_order:
        bench_idx = names_in_order.index(NEW_MENU_NAME)
        anchor_idx = names_in_order.index(ANCHOR_MENU_NAME)
        if bench_idx >= anchor_idx:
            failures.append(
                f"Order wrong: {names_in_order} — {NEW_MENU_NAME!r} must come "
                f"before {ANCHOR_MENU_NAME!r}"
            )

    return failures
