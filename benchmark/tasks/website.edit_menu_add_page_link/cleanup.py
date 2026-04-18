"""Cleanup for website.edit_menu_add_page_link."""


def cleanup(env):
    env["website.menu"].with_context(active_test=False).search([
        "|",
        ("name", "=", "Benchmark Contact"),
        ("url", "=", "/benchmark-contact"),
    ]).unlink()
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", "/benchmark-contact"),
    ]).unlink()
