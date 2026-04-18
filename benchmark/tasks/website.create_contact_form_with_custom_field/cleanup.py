"""Clean up the benchmark contact-us page."""


def cleanup(env):
    env["website.rewrite"].search([
        ("url_from", "in", ["/contactus-bench"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/contactus-bench"]),
    ]).unlink()
    env["ir.ui.view"].search([
        ("key", "=", "benchmark.contactus_bench_page"),
    ]).unlink()
