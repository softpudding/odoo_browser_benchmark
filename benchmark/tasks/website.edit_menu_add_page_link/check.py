"""Postcondition checks for website.edit_menu_add_page_link.

Validates:
1. A website.menu named 'Benchmark Contact' exists on website_id=1.
2. Its url is '/benchmark-contact'.
3. It is a child of website 1's main menu (parent_id == website.menu_id).
4. It is linked to the seeded /benchmark-contact website.page via page_id.
5. No extra duplicate menus or page deletions.
"""


def check(env):
    failures = []

    website = env["website"].browse(1)

    page = env["website.page"].search([
        ("url", "=", "/benchmark-contact"),
    ], limit=1)
    if not page:
        failures.append("Seeded page '/benchmark-contact' is missing")

    menus = env["website.menu"].search([
        ("name", "=", "Benchmark Contact"),
        ("website_id", "=", website.id),
    ])
    if not menus:
        return ["No website.menu named 'Benchmark Contact' on the primary website"]

    if len(menus) > 1:
        failures.append(
            f"Expected exactly 1 'Benchmark Contact' menu on website 1, got {len(menus)}"
        )

    menu = menus[0]

    if menu.url != "/benchmark-contact":
        failures.append(f"Menu url is {menu.url!r}, expected '/benchmark-contact'")

    if not menu.parent_id or menu.parent_id != website.menu_id:
        failures.append(
            f"Menu parent_id is {menu.parent_id.name!r} "
            f"(id={menu.parent_id.id}), expected the main website menu "
            f"(id={website.menu_id.id})"
        )

    if page and (not menu.page_id or menu.page_id != page):
        failures.append(
            f"Menu page_id is {menu.page_id.id!r}, expected {page.id} "
            "(the seeded /benchmark-contact page)"
        )

    return failures
