"""Clean up the benchmark website gallery page."""


def cleanup(env):
    env["website.rewrite"].search([
        ("url_from", "in", ["/bench-gallery-test"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/bench-gallery-test"]),
    ]).unlink()
