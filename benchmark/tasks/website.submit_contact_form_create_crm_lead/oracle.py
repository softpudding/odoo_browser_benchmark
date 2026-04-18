"""Oracle for website.submit_contact_form_create_crm_lead.

Open the frontend /contactus-bench page, fill every form field, click Submit,
and wait for the Thank You redirect. No login required — the contactus form
is public.
"""

from benchmark.oracle_helpers import full_url, run_oracle


CONTACT_PAGE_URL = "/contactus-bench"

CONTACT_NAME = "Bench Prospect Q4"
CONTACT_EMAIL = "prospect@bench.test"
CONTACT_PHONE = "+15555551212"
CONTACT_COMPANY = "Bench Test Inc"
CONTACT_SUBJECT = "Requesting demo"
CONTACT_MESSAGE = "Interested in the enterprise plan"


def oracle(page):
    # No login necessary — /contactus-bench is public.
    page.goto(full_url(CONTACT_PAGE_URL))
    page.wait_for_load_state("domcontentloaded")
    # Allow website interaction bundle to hydrate before we start filling.
    page.wait_for_timeout(2000)
    page.wait_for_selector("form#contactus_bench_form", timeout=30000)

    # Fill each field by its name attribute.
    page.fill("form#contactus_bench_form input[name='contact_name']", CONTACT_NAME)
    page.fill("form#contactus_bench_form input[name='phone']", CONTACT_PHONE)
    page.fill("form#contactus_bench_form input[name='email_from']", CONTACT_EMAIL)
    page.fill("form#contactus_bench_form input[name='partner_name']", CONTACT_COMPANY)
    page.fill("form#contactus_bench_form input[name='name']", CONTACT_SUBJECT)
    page.fill("form#contactus_bench_form textarea[name='description']", CONTACT_MESSAGE)

    page.wait_for_timeout(500)

    # Click Submit and wait for the thank-you redirect. The form snippet's
    # JS handler intercepts the click and POSTs to /website/form/crm.lead
    # asynchronously.
    with page.expect_navigation(
        url="**/contactus-thank-you**", timeout=25000
    ) as nav:
        page.click("form#contactus_bench_form .s_website_form_send")
    nav.value  # ensure navigation happened

    # Give the server a moment to finish creating the lead record.
    page.wait_for_timeout(1500)


run_oracle(oracle)
