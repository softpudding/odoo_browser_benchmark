"""Postcondition checks for website.create_contact_form_block."""


def check(env):
    page = env["website.page"].search([("url", "=", "/talk-to-sales")], limit=1)
    if not page:
        return ["Page /talk-to-sales was not found"]

    arch = page.view_id.arch_db or ""
    failures = []
    # Count top-level form sections by data-snippet attribute
    import re
    form_sections = re.findall(r'data-snippet="s_website_form', arch)
    if len(form_sections) != 1:
        failures.append(f"Expected exactly one website form block, found {len(form_sections)}")
    if "Request Callback" not in arch:
        failures.append("Submit button text 'Request Callback' not found in page arch")
    if "Talk to Sales" not in arch:
        failures.append("Hero heading 'Talk to Sales' was removed or changed")
    return failures
