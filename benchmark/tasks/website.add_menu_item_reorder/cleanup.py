"""Clean up website.add_menu_item_reorder artifacts."""


def cleanup(env):
    website = env["website"].browse(1)
    env["website.menu"].search([
        ("website_id", "=", website.id),
        ("name", "=", "Resources"),
    ]).unlink()
    env["website.rewrite"].search([
        ("url_from", "in", ["/consulting", "/resources", "/support", "/contact"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/consulting", "/resources", "/support", "/contact"]),
    ]).unlink()

