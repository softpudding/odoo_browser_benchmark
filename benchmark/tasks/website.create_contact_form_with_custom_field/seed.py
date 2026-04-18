"""Seed a Contact Us page (/contactus-bench) with a stock form snippet.

The form contains: Your Name (custom required char), Your Email (model required
email), Phone Number (custom tel), Your Question (custom required text), and a
Submit button. The new "Inquiry Type" Selection field is intentionally absent —
the agent must add it via the website builder.
"""


CONTACT_PAGE_ARCH = """
<t name="Contact Us Bench" t-name="benchmark.contactus_bench_page">
    <t t-call="website.layout">
        <div id="wrap">
            <section class="pt48 pb32">
                <div class="container">
                    <h1 class="text-center mb-3">Contact Benchmark Industries</h1>
                    <p class="lead text-center mb-5">
                        Reach out to our team. We respond within one business day.
                    </p>
                    <section class="s_website_form pt16 pb16" data-vcss="001" data-snippet="s_website_form">
                        <div class="container-fluid">
                            <form action="/website/form/" method="post" enctype="multipart/form-data" class="o_mark_required" data-mark="*" data-pre-fill="true" data-model_name="mail.mail" data-success-mode="redirect" data-success-page="/contactus-thank-you">
                                <div class="s_website_form_rows row s_col_no_bgcolor">
                                    <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_dnone">
                                        <div class="row s_col_no_resize s_col_no_bgcolor">
                                            <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px">
                                                <span class="s_website_form_label_content"></span>
                                            </label>
                                            <div class="col-sm">
                                                <input type="hidden" class="form-control s_website_form_input" name="email_to" value="info@benchmark.example.com"/>
                                            </div>
                                        </div>
                                    </div>
                                    <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_custom s_website_form_required" data-type="char">
                                        <div class="row s_col_no_resize s_col_no_bgcolor">
                                            <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px" for="bench_name">
                                                <span class="s_website_form_label_content">Your Name</span>
                                                <span class="s_website_form_mark"> *</span>
                                            </label>
                                            <div class="col-sm">
                                                <input class="form-control s_website_form_input" type="text" name="name" required="1" data-fill-with="name" id="bench_name"/>
                                            </div>
                                        </div>
                                    </div>
                                    <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_custom" data-type="tel">
                                        <div class="row s_col_no_resize s_col_no_bgcolor">
                                            <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px" for="bench_phone">
                                                <span class="s_website_form_label_content">Phone Number</span>
                                            </label>
                                            <div class="col-sm">
                                                <input class="form-control s_website_form_input" type="tel" name="phone" data-fill-with="phone" id="bench_phone"/>
                                            </div>
                                        </div>
                                    </div>
                                    <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_model_required" data-type="email">
                                        <div class="row s_col_no_resize s_col_no_bgcolor">
                                            <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px" for="bench_email">
                                                <span class="s_website_form_label_content">Your Email</span>
                                                <span class="s_website_form_mark"> *</span>
                                            </label>
                                            <div class="col-sm">
                                                <input class="form-control s_website_form_input" type="email" name="email_from" required="" data-fill-with="email" id="bench_email"/>
                                            </div>
                                        </div>
                                    </div>
                                    <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_custom s_website_form_required" data-type="text">
                                        <div class="row s_col_no_resize s_col_no_bgcolor">
                                            <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px" for="bench_question">
                                                <span class="s_website_form_label_content">Your Question</span>
                                                <span class="s_website_form_mark"> *</span>
                                            </label>
                                            <div class="col-sm">
                                                <textarea class="form-control s_website_form_input" name="description" required="1" id="bench_question" rows="3"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mb-0 py-2 col-12 s_website_form_submit text-end s_website_form_no_submit_label" data-name="Submit Button">
                                        <div style="width: 200px;" class="s_website_form_label"/>
                                        <span id="s_website_form_result"/>
                                        <a href="#" role="button" class="btn btn-primary s_website_form_send">Submit</a>
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
    website = env["website"].browse(1)

    # Cleanup prior runs (rewrites + page + view)
    env["website.rewrite"].search([
        ("url_from", "in", ["/contactus-bench"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/contactus-bench"]),
    ]).unlink()
    env["ir.ui.view"].search([
        ("key", "=", "benchmark.contactus_bench_page"),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": "Contact Us Bench",
        "type": "qweb",
        "url": "/contactus-bench",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.contactus_bench_page",
        "arch": CONTACT_PAGE_ARCH,
    })
