"""Seed a website with top-level menus and an unpublished menu target."""


def setup(env):
    website = env["website"].browse(1)
    root_menu = website.menu_id
    page_model = env["website.page"].with_context(website_id=website.id)

    # Clean prior task artifacts.
    env["website.menu"].search([
        ("name", "=", "Resources"),
        ("website_id", "=", website.id),
    ]).unlink()
    env["website.rewrite"].search([
        ("url_from", "in", ["/consulting", "/resources", "/support", "/contact"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/consulting", "/resources", "/support", "/contact"]),
    ]).unlink()

    for name, url in [
        ("Consulting", "/consulting"),
        ("Resources", "/resources"),
        ("Support", "/support"),
        ("Contact", "/contact"),
    ]:
        page_model.create({
            "name": name,
            "type": "qweb",
            "url": url,
            "is_published": True,
            "website_id": website.id,
            "key": f"benchmark.{name.lower().replace(' ', '_')}_page",
            "arch": f"""
                <t t-call="website.layout">
                    <div id="wrap"><section class="pt96 pb96"><div class="container"><h1>{name}</h1></div></section></div>
                </t>
            """,
        })

    env["website.menu"].search([
        ("website_id", "=", website.id),
        ("parent_id", "=", root_menu.id),
        ("name", "in", ["Consulting", "Support", "Contact"]),
    ]).unlink()

    for sequence, (name, url) in enumerate(
        [("Consulting", "/consulting"), ("Support", "/support"), ("Contact", "/contact")],
        start=20,
    ):
        env["website.menu"].create({
            "name": name,
            "url": url,
            "parent_id": root_menu.id,
            "website_id": website.id,
            "sequence": sequence,
        })
