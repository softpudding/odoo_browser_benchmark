"""Postcondition checks for website.create_contact_form_with_custom_field.

Verify that the Contact Us page now contains a custom Selection field labelled
"Inquiry Type" with three option labels (Sales / Support / Partnership), that
the existing form fields are intact, and that the page is still published.

The Odoo 19 website builder renders a custom Selection-type field as a set of
radio inputs inside ``s_website_form_multiple`` (default Display=Radio).  If
the user changed the Display to a select dropdown, the field renders as
``<select>`` with ``<option>`` children. Both encodings are accepted.
"""

import re


def _normalize_arch(arch):
    """Lower-case and collapse whitespace for tolerant substring search."""
    return re.sub(r"\s+", " ", (arch or "").lower())


def check(env):
    failures = []

    page = env["website.page"].search(
        [("url", "=", "/contactus-bench")], limit=1
    )
    if not page:
        return [
            "Contact page /contactus-bench is missing — agent likely changed "
            "or deleted the URL."
        ]

    if not page.is_published:
        failures.append("Contact page /contactus-bench is no longer published")

    arch = page.view_id.arch_db or page.view_id.arch or ""
    arch_norm = _normalize_arch(arch)

    # 1. The Inquiry Type label must be present in the form.
    if "inquiry type" not in arch_norm:
        failures.append(
            "Form does not contain a field labelled 'Inquiry Type'"
        )

    # 2. The new field must be a Selection-type, custom field. Either:
    #    (a) a div with data-type="selection" + s_website_form_custom, OR
    #    (b) a div containing a <select> element rendered by the builder.
    has_selection_div = (
        'data-type="selection"' in arch_norm
        and "s_website_form_custom" in arch_norm
    )
    has_select_tag = "<select" in arch_norm and "</select" in arch_norm
    if not (has_selection_div or has_select_tag):
        failures.append(
            "No Selection-type field found in the contact form arch "
            "(neither data-type=\"selection\" nor a <select> element)."
        )

    # 3. The three option labels must all appear inside the form.
    for opt in ("Sales", "Support", "Partnership"):
        if opt.lower() not in arch_norm:
            failures.append(f"Selection option {opt!r} missing from form arch")

    # 4. Required: either the new field's container has the
    #    s_website_form_required class, or its inputs/select carry a
    #    required attribute. We require evidence of "required" near the
    #    Inquiry Type label.
    inquiry_idx = arch_norm.find("inquiry type")
    if inquiry_idx >= 0:
        # Look at the surrounding 1500 chars for a required marker.
        window_start = max(0, inquiry_idx - 800)
        window_end = min(len(arch_norm), inquiry_idx + 1500)
        window = arch_norm[window_start:window_end]
        is_required = (
            "s_website_form_required" in window
            or 'required="1"' in window
            or 'required=""' in window
            or "required " in window  # bare required attribute
            or "required>" in window
            or "required/>" in window
            or "required ='" in window
        )
        if not is_required:
            failures.append(
                "Inquiry Type field is not marked required (no "
                "s_website_form_required class and no required attribute)."
            )

    # 5. Existing fields and Submit button must remain intact.
    must_keep = [
        "Your Name",
        "Your Email",
        "Phone Number",
        "Your Question",
        "s_website_form_send",  # Submit button class
    ]
    for snippet in must_keep:
        if snippet.lower() not in arch_norm:
            failures.append(f"Existing form content {snippet!r} is missing")

    # 6. URL and page name must not have changed.
    if page.url != "/contactus-bench":
        failures.append(
            f"Page URL changed to {page.url!r}, expected '/contactus-bench'"
        )
    if page.name != "Contact Us Bench":
        failures.append(
            f"Page name changed to {page.name!r}, expected 'Contact Us Bench'"
        )

    return failures
