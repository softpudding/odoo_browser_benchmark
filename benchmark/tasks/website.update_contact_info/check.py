"""Postcondition checks for website.update_contact_info.

Validates:
1. About Us page exists at /about-us
2. Page contains updated phone number +1 555 987 6543
3. Page is still published
"""


def check(env):
    failures = []

    page = env["website.page"].search([("url", "=", "/about-us")], limit=1)
    if not page:
        return ["About Us page not found at /about-us"]

    if not page.is_published:
        failures.append("Page is not published")

    arch_db = page.view_id.arch_db or ""
    expected_phone = "+1 555 987 6543"
    if expected_phone not in arch_db:
        failures.append(f"Phone number '{expected_phone}' not found in page content")

    old_phone = "+1 555 123 4567"
    if old_phone in arch_db:
        failures.append(f"Old phone number '{old_phone}' still present in page")

    return failures