"""Clean up the benchmark website page."""


def cleanup(env):
    env["website.rewrite"].search([
        ("url_from", "in", ["/about-us", "/about-benchmark-industries"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/about-us", "/about-benchmark-industries"]),
    ]).unlink()
