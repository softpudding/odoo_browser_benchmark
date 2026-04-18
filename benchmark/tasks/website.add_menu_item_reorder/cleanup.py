"""Cleanup for website.add_menu_item_reorder."""


NEW_MENU_NAME = "Bench Menu"
NEW_MENU_URL = "/bench-menu-target"
ANCHOR_MENU_NAME = "Bench Contact"
ANCHOR_MENU_URL = "/bench-contact-anchor"


def cleanup(env):
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
    env["ir.config_parameter"].sudo().search([
        ("key", "=", "benchmark.add_menu_item_reorder.root_menu_id"),
    ]).unlink()
