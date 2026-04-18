"""Postcondition checks for website.submit_contact_form_create_crm_lead.

Verify that exactly one crm.lead was created from the contact form submission
with the expected contact_name, email_from, partner_name, name (subject),
phone and description, and that the backend page/view the task seeded is
still intact.
"""

import re


CONTACT_PAGE_URL = "/contactus-bench"

CONTACT_NAME = "Bench Prospect Q4"
CONTACT_EMAIL = "prospect@bench.test"
CONTACT_PHONE = "+15555551212"
CONTACT_COMPANY = "Bench Test Inc"
CONTACT_SUBJECT = "Requesting demo"
CONTACT_MESSAGE_SUBSTRING = "enterprise plan"


def _strip_html(html):
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = (text
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&#39;", "'")
            .replace("&quot;", '"'))
    return " ".join(text.split()).strip()


def _normalize_phone(val):
    return re.sub(r"[^0-9+]", "", val or "")


def check(env):
    failures = []

    # 1. The seeded contact page must still exist + be published.
    page = env["website.page"].search(
        [("url", "=", CONTACT_PAGE_URL)], limit=1
    )
    if not page:
        return [
            f"Seeded contact page {CONTACT_PAGE_URL} is missing — agent likely "
            f"navigated to or modified the wrong page."
        ]
    if not page.is_published:
        failures.append(
            f"Seeded contact page {CONTACT_PAGE_URL} is no longer published."
        )

    # 2. Exactly one crm.lead with the expected identity should exist.
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("email_from", "=ilike", CONTACT_EMAIL),
    ])
    if not leads:
        # Broaden the search in case email_from was blanked/normalized
        leads = env["crm.lead"].with_context(active_test=False).search([
            ("contact_name", "=", CONTACT_NAME),
        ])

    if not leads:
        failures.append(
            f"No crm.lead was created with email '{CONTACT_EMAIL}' or "
            f"contact_name '{CONTACT_NAME}'. The form submission never "
            f"reached the CRM pipeline."
        )
        return failures

    if len(leads) > 1:
        failures.append(
            f"Expected exactly 1 crm.lead, found {len(leads)} "
            f"(duplicate submissions?)"
        )

    lead = leads[0]

    # 3. Validate the lead's fields.
    if (lead.contact_name or "").strip() != CONTACT_NAME:
        failures.append(
            f"Lead contact_name is '{lead.contact_name}', expected "
            f"'{CONTACT_NAME}'"
        )
    if (lead.email_from or "").strip().lower() != CONTACT_EMAIL.lower():
        failures.append(
            f"Lead email_from is '{lead.email_from}', expected '{CONTACT_EMAIL}'"
        )
    if (lead.partner_name or "").strip() != CONTACT_COMPANY:
        failures.append(
            f"Lead partner_name is '{lead.partner_name}', expected "
            f"'{CONTACT_COMPANY}'"
        )
    # Phone may be normalized by phone_validation (e.g. '+1 555-555-1212')
    lead_phone = _normalize_phone(lead.phone)
    expected_phone = _normalize_phone(CONTACT_PHONE)
    if lead_phone != expected_phone:
        failures.append(
            f"Lead phone digits are '{lead_phone}', expected '{expected_phone}' "
            f"(raw lead.phone='{lead.phone}')"
        )
    # Lead name == form Subject
    if (lead.name or "").strip() != CONTACT_SUBJECT:
        failures.append(
            f"Lead name is '{lead.name}', expected subject '{CONTACT_SUBJECT}'"
        )
    # Description should contain the message substring (HTML-wrapped)
    desc_text = _strip_html(lead.description or "")
    if CONTACT_MESSAGE_SUBSTRING.lower() not in desc_text.lower():
        failures.append(
            f"Lead description '{desc_text}' does not contain "
            f"'{CONTACT_MESSAGE_SUBSTRING}'"
        )

    # 4. Lead should be of type 'lead' (default for crm.lead via website_crm).
    # Odoo may auto-convert to opportunity depending on team routing — we
    # accept both but flag if type is unknown.
    if lead.type not in ("lead", "opportunity"):
        failures.append(
            f"Lead.type is '{lead.type}', expected 'lead' or 'opportunity'"
        )

    return failures
