"""Seed for website.publish_draft_page_set_menu_visibility.

Category: deep_ui_interaction (HARD).

Starting state:
- Primary website (id=1) has a seeded website.page titled 'About Us' at
  url '/about-us'. It is UNPUBLISHED (`is_published=False`,
  `website_published=False`).
- NO `website.menu` entry points at '/about-us' (neither on the main
  website nor on any other). The seed removes any stale 'About Us'
  menu or page entry from prior runs so the task is idempotent.
- A distractor top-level menu entry called 'About' already exists on
  the primary website's main menu pointing at '/contactus' — it is
  present to tempt the agent into editing the wrong entry instead of
  creating a new one. The agent must NOT touch this distractor.

Agent workflow:
    Website → Site → Pages → open 'About Us' → flip the Published
    pill / boolean toggle ON → enable the 'Add to Menu' / 'In Menu'
    toggle in the page properties dialog, OR open Site → Menu Editor
    and create a new top-level entry pointing at '/about-us'.

End state the check validates:
- `website.page.is_published = True` for '/about-us' on website 1.
- A `website.menu` row exists with `url='/about-us'`, `website_id=1`,
  `parent_id == website_1.menu_id` (the site root menu), `page_id ==
  the /about-us page`.
- The distractor 'About' menu on /contactus is untouched.
"""


PAGE_URL = "/about-us"
PAGE_NAME = "About Us"
PAGE_KEY = "benchmark.about_us_draft_page"
PAGE_ARCH = """
<t name="About Us Draft" t-name="benchmark.about_us_draft_page">
    <t t-call="website.layout">
        <div id="wrap">
            <section class="pt96 pb96">
                <div class="container">
                    <h1 class="text-center mb-4">About Bench Industries</h1>
                    <p class="lead text-center">
                        Founded in 2019, Bench Industries makes test fixtures
                        for browser-based evaluation of LLM agents.
                    </p>
                </div>
            </section>
        </div>
    </t>
</t>
"""

DISTRACTOR_MENU_NAME = "About"
DISTRACTOR_MENU_URL = "/contactus"


def setup(env):
    website = env["website"].browse(1)

    # --- Cleanup any stale seeded menu / page from prior runs. ---
    # Remove menus that may have matched either the target url or name.
    env["website.menu"].with_context(active_test=False).search([
        "|", "|",
        ("url", "=", PAGE_URL),
        ("page_id.url", "=", PAGE_URL),
        "&",
        ("name", "=", PAGE_NAME),
        ("website_id", "=", website.id),
    ]).unlink()

    # Remove the distractor menu if a stale copy exists, so we seed a
    # single canonical distractor pointing at /contactus (NOT /about-us).
    env["website.menu"].with_context(active_test=False).search([
        ("name", "=", DISTRACTOR_MENU_NAME),
        ("website_id", "=", website.id),
    ]).unlink()

    # Remove any stale website.rewrite / page.
    env["website.rewrite"].search([
        ("url_from", "in", [PAGE_URL]),
    ]).unlink()
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", PAGE_URL),
    ]).unlink()
    env["ir.ui.view"].search([("key", "=", PAGE_KEY)]).unlink()

    # --- Create the UNPUBLISHED 'About Us' page. ---
    page = env["website.page"].with_context(website_id=website.id).create({
        "name": PAGE_NAME,
        "type": "qweb",
        "url": PAGE_URL,
        "is_published": False,
        "website_id": website.id,
        "key": PAGE_KEY,
        "arch": PAGE_ARCH,
    })
    # Belt + suspenders: website_published is computed from is_published
    # via the website.published.mixin inverse — force it to False in case
    # a default on the mixin flipped it.
    if page.is_published or page.website_published:
        page.write({"is_published": False, "website_published": False})

    # --- Seed the distractor 'About' menu pointing at /contactus. ---
    # (Its presence means a careless agent may edit this menu's URL
    # instead of creating a new menu entry for /about-us.)
    env["website.menu"].with_context(website_id=website.id).create({
        "name": DISTRACTOR_MENU_NAME,
        "url": DISTRACTOR_MENU_URL,
        "parent_id": website.menu_id.id,
        "website_id": website.id,
        "sequence": 150,
    })
