"""Clean up the benchmark website page."""


def cleanup(env):
    env["website.rewrite"].search([
        ("url_from", "in", ["/policy-studio", "/operations-playbooks"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/policy-studio", "/operations-playbooks"]),
    ]).unlink()

