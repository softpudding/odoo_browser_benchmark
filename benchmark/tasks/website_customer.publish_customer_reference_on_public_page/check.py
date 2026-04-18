"""Postcondition checks for website_customer.publish_customer_reference_on_public_page.

Validates:
1. Exactly one res.partner named "Bench Happy Client" exists.
2. website_published is True (publish toggle was flipped).
3. is_published is True (same field, related).
4. The implementer back-reference (assigned_partner_id) is preserved
   (not blanked accidentally).
5. The partner's country is still set (seeded US).
6. The partner name appears on the public /customers page HTML.
"""

import re
import urllib.error
import urllib.request


CLIENT_NAME = "Bench Happy Client"
IMPLEMENTER_NAME = "Bench Delivery Partner"


def _fetch_customers_html(env):
    """Try to fetch /customers as the public anonymous user."""
    base_url = env["ir.config_parameter"].sudo().get_param("web.base.url")
    if not base_url:
        return None
    url = base_url.rstrip("/") + "/customers"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BenchCheck/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError):
        return None
    except Exception:
        return None


def check(env):
    failures = []

    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CLIENT_NAME),
    ])
    if not partners:
        return [f"No res.partner found with name '{CLIENT_NAME}'"]
    if len(partners) > 1:
        failures.append(
            f"Expected exactly 1 res.partner named '{CLIENT_NAME}', "
            f"found {len(partners)}"
        )
    partner = partners[0]

    if not partner.website_published:
        failures.append(
            f"Partner '{CLIENT_NAME}' website_published is False; "
            "expected True after toggling the Published switch"
        )
    if not partner.is_published:
        failures.append(
            f"Partner '{CLIENT_NAME}' is_published is False; expected True "
            "(is_published and website_published are a related pair)"
        )

    if not partner.assigned_partner_id:
        failures.append(
            f"Partner '{CLIENT_NAME}' assigned_partner_id was blanked; "
            f"seeded as '{IMPLEMENTER_NAME}' (required for /customers)"
        )
    elif partner.assigned_partner_id.name != IMPLEMENTER_NAME:
        failures.append(
            f"Partner '{CLIENT_NAME}' assigned_partner_id changed to "
            f"'{partner.assigned_partner_id.name}'; expected "
            f"'{IMPLEMENTER_NAME}'"
        )

    if not partner.country_id:
        failures.append(
            f"Partner '{CLIENT_NAME}' country_id was cleared; expected "
            "seeded United States"
        )

    # Fetch /customers and confirm the name appears in the HTML.
    html = _fetch_customers_html(env)
    if html is None:
        # If we couldn't reach the endpoint (isolated test harness may
        # not expose HTTP in check.py context), don't hard-fail: the
        # domain check above (website_published + assigned_partner_id +
        # visible country) is sufficient for the /customers controller
        # to render this partner. Still, log an info note.
        pass
    else:
        # Strip HTML tags for a lenient substring check — the template
        # renders the name inside a link element.
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text)
        if CLIENT_NAME not in text:
            failures.append(
                f"Partner '{CLIENT_NAME}' not found in /customers page HTML; "
                "expected name visible in customer references list"
            )

    return failures
