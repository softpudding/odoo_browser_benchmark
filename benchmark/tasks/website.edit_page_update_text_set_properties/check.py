"""Postcondition checks for website.edit_page_update_text_set_properties."""


def check(env):
    failures = []

    # The page should now exist at the new URL
    page = env["website.page"].search([("url", "=", "/about-benchmark-industries")], limit=1)
    if not page:
        # Maybe the agent didn't change the URL - check old URL too
        page = env["website.page"].search([("url", "=", "/about-us")], limit=1)
        if page:
            failures.append("Page URL was not changed: still at /about-us, expected /about-benchmark-industries")
        else:
            return ["No website.page found at /about-benchmark-industries or /about-us"]
    else:
        # URL was changed correctly - also check old URL is gone
        old_page = env["website.page"].search([("url", "=", "/about-us")], limit=1)
        if old_page:
            failures.append("Old page URL /about-us still exists as a separate website.page")

    # Check page title
    expected_title = "About Benchmark Industries | Our Story"
    if page.name != expected_title:
        failures.append(f"Page title is {page.name!r}, expected {expected_title!r}")

    # Check published status preserved
    if not page.is_published:
        failures.append("Page is no longer published")

    # Check arch content
    arch_db = page.view_id.arch_db or ""

    # Heading must be updated
    if "About Benchmark Industries" not in arch_db:
        failures.append("Updated heading 'About Benchmark Industries' not found in page arch")

    if "About Our Company" in arch_db:
        failures.append("Old heading 'About Our Company' still present in page arch")

    # Paragraph must be updated
    expected_para = "Benchmark Industries is a leading provider of industrial automation solutions, serving clients worldwide since 2015."
    if expected_para not in arch_db:
        failures.append(f"Expected paragraph text not found in page arch")

    if "We are a dynamic enterprise" in arch_db:
        failures.append("Old paragraph text 'We are a dynamic enterprise' still present in page arch")

    # Core Values section must be preserved
    preserved_strings = [
        "Our Core Values",
        "Innovation",
        "Pushing boundaries with cutting-edge solutions.",
        "Integrity",
        "Upholding the highest ethical standards.",
        "Excellence",
        "Striving for quality in everything we do.",
    ]
    for text in preserved_strings:
        if text not in arch_db:
            failures.append(f"Preserved content {text!r} was removed or altered")

    return failures
