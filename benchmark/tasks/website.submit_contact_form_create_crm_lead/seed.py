"""Seed a pre-configured contact form page wired to crm.lead.

The default /contactus page ships with data-model_name="mail.mail" which creates
an email instead of a CRM lead. In a real deployment an admin would swap the
form action to "Create an Opportunity" via the website builder — that UI
workflow is covered by website.create_contact_form_with_custom_field.

This task seeds a separate page at /contactus-bench whose form is already
configured to create a crm.lead record, so the workflow becomes:
frontend form fill + submit -> backend crm.lead creation.

Field mapping (form input name -> crm.lead field):
    contact_name  -> contact_name
    email_from    -> email_from
    phone         -> phone
    partner_name  -> partner_name   (company)
    name          -> name           (opportunity subject line)
    description   -> description    (message)

The task verifies that after submitting the form, a crm.lead exists with the
exact contact_name, email_from, partner_name, name, phone and description set
from the form values.

Calibration: website_crm auto-installs when both website and crm are in the
base modules — the whitelist for crm.lead form fields (contact_name,
partner_name, description, name, phone, email_from, ...) is registered by
website_crm's data/ir_model_data.xml `formbuilder_whitelist` call.
"""

CONTACT_PAGE_URL = "/contactus-bench"
CONTACT_PAGE_KEY = "benchmark.contactus_bench_lead_page"

# Target values the agent must enter
CONTACT_NAME = "Bench Prospect Q4"
CONTACT_EMAIL = "prospect@bench.test"
CONTACT_PHONE = "+15555551212"
CONTACT_COMPANY = "Bench Test Inc"
CONTACT_SUBJECT = "Requesting demo"
CONTACT_MESSAGE = "Interested in the enterprise plan"


CONTACT_PAGE_ARCH = """
<t name="Contact Us Bench (Lead)" t-name="benchmark.contactus_bench_lead_page">
    <t t-call="website.layout">
        <div id="wrap">
            <section class="pt48 pb32">
                <div class="container">
                    <h1 class="text-center mb-3">Contact Benchmark Industries</h1>
                    <p class="lead text-center mb-5">
                        Fill out the form below and a sales representative will reach out.
                    </p>
                    <section class="s_website_form pt16 pb16" data-vcss="001" data-snippet="s_website_form">
                        <div class="container">
                            <form id="contactus_bench_form" action="/website/form/" method="post" enctype="multipart/form-data" class="o_mark_required s_website_form_no_recaptcha" data-mark="*" data-pre-fill="true" data-model_name="crm.lead" data-success-mode="redirect" data-success-page="/contactus-thank-you">
                                <div class="s_website_form_rows row s_col_no_bgcolor">
                                    <div class="mb-3 col-lg-6 s_website_form_field s_website_form_required s_website_form_model_required" data-type="char" data-name="Field">
                                        <label class="s_website_form_label" style="width: 200px" for="bench_contact_name">
                                            <span class="s_website_form_label_content">Name</span>
                                            <span class="s_website_form_mark"> *</span>
                                        </label>
                                        <input id="bench_contact_name" type="text" class="form-control s_website_form_input" name="contact_name" required="" data-fill-with="name"/>
                                    </div>
                                    <div class="mb-3 col-lg-6 s_website_form_field s_website_form_custom" data-type="char" data-name="Field">
                                        <label class="s_website_form_label" style="width: 200px" for="bench_phone">
                                            <span class="s_website_form_label_content">Phone Number</span>
                                        </label>
                                        <input id="bench_phone" type="tel" class="form-control s_website_form_input" name="phone" data-fill-with="phone"/>
                                    </div>
                                    <div class="mb-3 col-lg-6 s_website_form_field s_website_form_required s_website_form_model_required" data-type="email" data-name="Field">
                                        <label class="s_website_form_label" style="width: 200px" for="bench_email">
                                            <span class="s_website_form_label_content">Email</span>
                                            <span class="s_website_form_mark"> *</span>
                                        </label>
                                        <input id="bench_email" type="email" class="form-control s_website_form_input" name="email_from" required="" data-fill-with="email"/>
                                    </div>
                                    <div class="mb-3 col-lg-6 s_website_form_field" data-type="char" data-name="Field">
                                        <label class="s_website_form_label" style="width: 200px" for="bench_company">
                                            <span class="s_website_form_label_content">Company</span>
                                        </label>
                                        <input id="bench_company" type="text" class="form-control s_website_form_input" name="partner_name" data-fill-with="commercial_company_name"/>
                                    </div>
                                    <div class="mb-3 col-12 s_website_form_field s_website_form_required s_website_form_model_required" data-type="char" data-name="Field">
                                        <label class="s_website_form_label" style="width: 200px" for="bench_subject">
                                            <span class="s_website_form_label_content">Subject</span>
                                            <span class="s_website_form_mark"> *</span>
                                        </label>
                                        <input id="bench_subject" type="text" class="form-control s_website_form_input" name="name" required=""/>
                                    </div>
                                    <div class="mb-3 col-12 s_website_form_field s_website_form_required" data-type="text" data-name="Field">
                                        <label class="s_website_form_label" style="width: 200px" for="bench_message">
                                            <span class="s_website_form_label_content">Message</span>
                                            <span class="s_website_form_mark"> *</span>
                                        </label>
                                        <textarea id="bench_message" class="form-control s_website_form_input" name="description" required="" rows="6"></textarea>
                                    </div>
                                    <div class="mb-0 py-2 col-12 s_website_form_submit s_website_form_no_submit_label text-end" data-name="Submit Button">
                                        <div style="width: 200px;" class="s_website_form_label"/>
                                        <a href="#" role="button" class="btn btn-primary s_website_form_send">Submit</a>
                                        <span id="s_website_form_result"></span>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </section>
                </div>
            </section>
        </div>
    </t>
</t>
"""


def setup(env):
    website = env["website"].search([], limit=1)
    if not website:
        website = env["website"].browse(1)

    # --- Disable any global reCAPTCHA hooks that might block the frontend
    # form submission (no site key set means reCAPTCHA is silently skipped,
    # but we also flag the form with s_website_form_no_recaptcha just in case
    # a site key is configured in the base DB).
    icp = env["ir.config_parameter"].sudo()
    icp.set_param("recaptcha_private_key", "")
    icp.set_param("recaptcha_public_key", "")

    # --- Remove any stale leads from prior runs ---
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        "|", "|",
        ("email_from", "=", CONTACT_EMAIL),
        ("contact_name", "=", CONTACT_NAME),
        ("name", "=", CONTACT_SUBJECT),
    ])
    if old_leads:
        # Unlink mail messages/activities first to avoid FK issues
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        old_leads.unlink()

    # --- Remove any prior seeded page + view ---
    env["website.rewrite"].search([
        ("url_from", "in", [CONTACT_PAGE_URL]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", [CONTACT_PAGE_URL]),
    ]).unlink()
    env["ir.ui.view"].search([
        ("key", "=", CONTACT_PAGE_KEY),
    ]).unlink()

    # --- Create the pre-configured contact form page ---
    env["website.page"].with_context(website_id=website.id).create({
        "name": "Contact Us Bench (Lead)",
        "type": "qweb",
        "url": CONTACT_PAGE_URL,
        "is_published": True,
        "website_id": website.id,
        "key": CONTACT_PAGE_KEY,
        "arch": CONTACT_PAGE_ARCH,
    })
