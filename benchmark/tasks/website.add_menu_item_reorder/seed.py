"""Seed for website.add_menu_item_reorder.

Category: deep_ui_interaction (MEDIUM).

Starting state:
- Primary website (id=1) has a top-level menu root (website.menu_id) with
  an existing `Home` entry at sequence=10 and a seeded `Bench Contact`
  entry at sequence=20.
- A seeded website.page exists at '/bench-menu-target' (target URL for
  the new menu entry the agent must create).
- No 'Bench Menu' menu entry exists yet.

The agent must add a new top-level menu entry named 'Bench Menu' pointing
to '/bench-menu-target' and reorder it so that it sits between 'Home' and
'Bench Contact' (sequence strictly between 10 and 20).
"""


NEW_MENU_NAME = "Bench Menu"
NEW_MENU_URL = "/bench-menu-target"
ANCHOR_MENU_NAME = "Bench Contact"
ANCHOR_MENU_URL = "/bench-contact-anchor"


def setup(env):
    website = env["website"].browse(1)
    root_menu = website.menu_id  # Main top-level menu for this website

    # ------------------------------------------------------------------
    # 1. Idempotent cleanup of prior-run artifacts.
    # ------------------------------------------------------------------
    env["website.menu"].with_context(active_test=False).search([
        "|", "|", "|",
        ("name", "=", NEW_MENU_NAME),
        ("url", "=", NEW_MENU_URL),
        ("name", "=", ANCHOR_MENU_NAME),
        ("url", "=", ANCHOR_MENU_URL),
    ]).unlink()

    env["website.page"].with_context(active_test=False).search([
        "|",
        ("url", "=", NEW_MENU_URL),
        ("url", "=", ANCHOR_MENU_URL),
    ]).unlink()

    # ------------------------------------------------------------------
    # 2. Seed the target page the new menu will point to.
    # ------------------------------------------------------------------
    env["website.page"].with_context(website_id=website.id).create({
        "name": "Bench Menu Target",
        "type": "qweb",
        "url": NEW_MENU_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_menu_target",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Bench Menu Target</h1>
                            <p class="text-center">
                                Landing page for the Bench Menu top-level entry.
                            </p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })

    # ------------------------------------------------------------------
    # 3. Seed the Bench Contact anchor page + top-level menu entry at
    #    sequence 20, so the required "between Home and Bench Contact"
    #    ordering is unambiguous.
    # ------------------------------------------------------------------
    env["website.page"].with_context(website_id=website.id).create({
        "name": "Bench Contact",
        "type": "qweb",
        "url": ANCHOR_MENU_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_contact_anchor",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Bench Contact</h1>
                            <p class="text-center">Benchmark anchor page.</p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })

    env["website.menu"].create({
        "name": ANCHOR_MENU_NAME,
        "url": ANCHOR_MENU_URL,
        "parent_id": root_menu.id,
        "website_id": website.id,
        "sequence": 20,
    })

    # ------------------------------------------------------------------
    # 4. Pin 'Home' at sequence=10 and push any other existing top-level
    #    menus (Shop, Contact Us, etc.) to sequence>=30 so Home(10) and
    #    Bench Contact(20) are the only entries in [10..20]. This makes
    #    the "reorder into position 2" requirement unambiguous.
    # ------------------------------------------------------------------
    top_level = env["website.menu"].search([
        ("parent_id", "=", root_menu.id),
        ("website_id", "=", website.id),
    ])
    home = top_level.filtered(lambda m: (m.url or "").strip() in ("/", "/home"))
    if home:
        home[0].sequence = 10

    # Push every OTHER existing top-level entry (that isn't Home or the
    # anchor we just created) out to sequence >= 30 to keep the 10..20
    # window clean.
    seq = 30
    for menu in top_level.sorted("sequence"):
        if menu == home[:1] or menu.name == ANCHOR_MENU_NAME:
            continue
        menu.sequence = seq
        seq += 10

    # ------------------------------------------------------------------
    # 5. Record the main-menu root id in ir.config_parameter so the
    #    oracle (which talks over JSON-RPC and does not have ORM access)
    #    can resolve the correct parent without guessing.
    # ------------------------------------------------------------------
    env["ir.config_parameter"].sudo().set_param(
        "benchmark.add_menu_item_reorder.root_menu_id",
        str(root_menu.id),
    )
