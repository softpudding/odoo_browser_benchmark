"""Postcondition checks for website.edit_careers_spotlight."""


def check(env):
    failures = []

    page = env["website.page"].search([("url", "=", "/operations-playbooks")], limit=1)
    if not page:
        return ["No website.page found at /operations-playbooks"]

    if page.name != "Operations Playbooks":
        failures.append(f"Page title is {page.name!r}, expected 'Operations Playbooks'")

    if not page.is_published:
        failures.append("Page is not published")

    if page.is_in_menu:
        failures.append("Page unexpectedly became visible in the main menu")

    arch_db = page.view_id.arch_db or ""
    required_strings = [
        "Policy Studio",
        "Audit Trails",
        "Track every critical change.",
        "Read Audit Guide",
        "Approval Workflows",
        "Route sensitive changes through explicit review.",
        "Read Workflow Policy",
        "Incident Reviews",
        "Capture follow-up after incidents.",
        "Review Incident Notes",
    ]
    for text in required_strings:
        if text not in arch_db:
            failures.append(f"Expected page text {text!r} not found in page arch")

    old_page = env["website.page"].search([("url", "=", "/policy-studio")], limit=1)
    if old_page:
        failures.append("Old page URL /policy-studio still exists as a website.page")

    return failures
