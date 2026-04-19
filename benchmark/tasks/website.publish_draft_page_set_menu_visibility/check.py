"""Postcondition checks for website.publish_draft_page_set_menu_visibility.

Validates:
1. The seeded /about-us page still exists with name='About Us' and is
   now PUBLISHED (both is_published and website_published True).
2. Exactly one new website.menu row exists with url='/about-us' on the
   primary website (id=1), parented under the site root menu
   (website.menu_id), with page_id pointing at the seeded page.
3. The distractor 'About' menu pointing at '/contactus' is still intact
   (name='About', url='/contactus') — the agent must NOT have edited it.
4. The seeded About Us page name/url are unchanged.
"""


PAGE_URL = "/about-us"
PAGE_NAME = "About Us"
DISTRACTOR_MENU_NAME = "About"
DISTRACTOR_MENU_URL = "/contactus"


def check(env):
    failures = []

    website = env["website"].browse(1)

    # --- 1. Page must exist, be named About Us, and be PUBLISHED. ---
    page = env["website.page"].search([("url", "=", PAGE_URL)], limit=1)
    if not page:
        return [
            f"Seeded page {PAGE_URL!r} is missing — the agent likely "
            "renamed or deleted the page."
        ]
    if page.name != PAGE_NAME:
        failures.append(
            f"Page name is {page.name!r}, expected {PAGE_NAME!r}"
        )
    if page.url != PAGE_URL:
        failures.append(
            f"Page url is {page.url!r}, expected {PAGE_URL!r}"
        )
    if not page.is_published:
        failures.append(
            "Page is_published is False — the agent did not publish "
            "the About Us page."
        )
    if not page.website_published:
        failures.append(
            "Page website_published is False — the publish toggle did "
            "not propagate. Try toggling the Published pill on the "
            "page row in the Pages list."
        )

    # --- 2. A website.menu with url='/about-us' must exist, be
    #        parented under the main website menu, and point at the page.
    menus = env["website.menu"].search([
        ("url", "=", PAGE_URL),
        ("website_id", "=", website.id),
    ])
    if not menus:
        failures.append(
            f"No website.menu row with url={PAGE_URL!r} on the primary "
            "website. Agent must either add the page to the menu "
            "(In Menu toggle in Page Properties) or create a new entry "
            "in Site → Menu Editor."
        )
        # Without a menu there's no further menu-level validation to do.
        return failures

    if len(menus) > 1:
        failures.append(
            f"Expected exactly 1 website.menu for url={PAGE_URL!r} on "
            f"website 1, found {len(menus)} — duplicate entries?"
        )

    menu = menus[0]
    if not menu.parent_id:
        failures.append(
            f"Menu '{menu.name}' has no parent_id — it must sit under "
            "the primary website's main menu."
        )
    elif menu.parent_id != website.menu_id:
        failures.append(
            f"Menu '{menu.name}' parent_id is "
            f"{menu.parent_id.name!r} (id={menu.parent_id.id}); expected "
            f"the main website menu (id={website.menu_id.id})."
        )

    if page and (not menu.page_id or menu.page_id != page):
        failures.append(
            "Menu page_id does not point at the seeded About Us page. "
            f"Got page_id={menu.page_id.id!r}, expected {page.id}. "
            "The backend usually auto-links page_id when the menu url "
            "matches an existing website.page url."
        )

    # --- 2b. 'About Us' must be the 2nd top-level entry (after Home).
    top_level = env["website.menu"].search([
        ("parent_id", "=", website.menu_id.id),
        ("website_id", "=", website.id),
    ], order="sequence, id")
    top_level_names = [m.name for m in top_level]
    if len(top_level) < 2:
        failures.append(
            f"Primary website has only {len(top_level)} top-level menu "
            f"entries ({top_level_names!r}); expected at least 2."
        )
    else:
        if top_level[0].name != "Home":
            failures.append(
                f"First top-level entry is {top_level[0].name!r}, "
                "expected 'Home' — do NOT re-order existing entries."
            )
        if top_level[1] != menu:
            failures.append(
                f"Second top-level entry is {top_level[1].name!r} "
                f"(url={top_level[1].url!r}); expected 'About Us' "
                f"(url='/about-us'). Current top-level order: "
                f"{top_level_names!r}. The new About Us entry must sit "
                "directly after Home — drag it up in the Menu Editor "
                "or set its Sequence between Home's (10) and the next."
            )

    # --- 3. The distractor 'About' menu on /contactus must be untouched. ---
    distractors = env["website.menu"].search([
        ("name", "=", DISTRACTOR_MENU_NAME),
        ("website_id", "=", website.id),
    ])
    if not distractors:
        failures.append(
            f"The distractor menu named {DISTRACTOR_MENU_NAME!r} is "
            "missing — it should NOT have been deleted."
        )
    else:
        # Odoo clones menus with missing website_id to every website;
        # just assert at least one distractor still has the /contactus URL.
        if not any(d.url == DISTRACTOR_MENU_URL for d in distractors):
            failures.append(
                f"The distractor {DISTRACTOR_MENU_NAME!r} menu URL was "
                f"changed from {DISTRACTOR_MENU_URL!r}. The agent must "
                "create a NEW menu entry for /about-us instead of editing "
                "the existing 'About' distractor."
            )

    return failures
