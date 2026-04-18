"""Postcondition checks for website.create_contact_form_block.

The agent must have inserted a Form snippet into `/bench-contact-form`,
switched its `data-model_name` to `res.partner`, kept the default Subject
field, and added a 'Your Message' Long Text (textarea) field.  We verify
via the view's arch_db rather than the iframe DOM because the arch is the
authoritative, persisted state.
"""

import re


PAGE_URL = "/bench-contact-form"
PAGE_NAME = "Bench Contact Form"
SEEDED_HEADING = "Contact Us"


def check(env):
    failures = []

    page = env["website.page"].search(
        [("url", "=", PAGE_URL)], limit=1
    )
    if not page:
        return [
            f"Target page {PAGE_URL} is missing; it should have been "
            f"seeded and preserved by the agent."
        ]

    arch_db = page.view_id.arch_db or ""

    # There must be a <form> element on the page.
    if "<form" not in arch_db:
        failures.append(
            "Expected at least one <form> tag in the page arch after "
            "adding the Form snippet."
        )
        # Without a form there's little else to check; return early.
        return failures

    # The form must point at res.partner (Contact), not the default
    # mail.mail.  Allow single or double quotes.
    if not re.search(r'data-model_name\s*=\s*["\']res\.partner["\']', arch_db):
        failures.append(
            "Expected the form's data-model_name to be 'res.partner' "
            "(Contact); not found."
        )

    # The form snippet class is what Odoo renders for the Form block.
    if "s_website_form" not in arch_db:
        failures.append(
            "Expected the form to use the s_website_form snippet class."
        )

    # The default Subject field must still be present (label content).
    if not re.search(
        r'<span[^>]*class="[^"]*s_website_form_label_content[^"]*"[^>]*>\s*Subject\s*</span>',
        arch_db,
    ):
        failures.append(
            "Expected a form field labelled 'Subject' to be kept."
        )

    # The custom 'Your Message' field must be present with a textarea
    # (Long Text).
    if not re.search(
        r'<span[^>]*class="[^"]*s_website_form_label_content[^"]*"[^>]*>\s*Your Message\s*</span>',
        arch_db,
    ):
        failures.append(
            "Expected a custom form field labelled 'Your Message'."
        )

    # The Your Message field must be rendered as a <textarea> (Long
    # Text), not as a plain input.  We look for a textarea anywhere in
    # the form arch.  The snippet 'Long Text' field-type produces a
    # <textarea>.
    if "<textarea" not in arch_db:
        failures.append(
            "Expected the 'Your Message' field to render as a "
            "<textarea> (Long Text)."
        )

    # The seeded heading must not have been deleted.
    if SEEDED_HEADING not in arch_db:
        failures.append(
            f"Seeded heading '{SEEDED_HEADING}' is missing; the agent "
            f"should have added the Form snippet alongside, not replaced "
            f"the page content."
        )

    # Page URL and title should be unchanged.
    if page.name != PAGE_NAME:
        failures.append(
            f"Page name changed to {page.name!r}; expected {PAGE_NAME!r}."
        )
    if page.url != PAGE_URL:
        failures.append(
            f"Page URL changed to {page.url!r}; expected {PAGE_URL!r}."
        )

    # Page must stay published.
    if not page.is_published:
        failures.append("Page was unpublished; it must stay published.")

    return failures
