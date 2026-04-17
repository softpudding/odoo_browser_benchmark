"""Seed a simple sales landing page for form-block insertion."""


def setup(env):
    website = env["website"].browse(1)

    env["website.rewrite"].search([("url_from", "=", "/talk-to-sales")]).unlink()
    env["website.page"].search([("url", "=", "/talk-to-sales")]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": "Talk to Sales",
        "type": "qweb",
        "url": "/talk-to-sales",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.talk_to_sales_page",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="s_cover pt96 pb96" data-snippet="s_cover">
                        <div class="container text-center">
                            <h1>Talk to Sales</h1>
                            <p>Discuss rollout plans, implementation timelines, and pricing.</p>
                        </div>
                    </section>
                    <section class="pt48 pb48">
                        <div class="container">
                            <div class="row">
                                <div class="col-lg-8 mx-auto">
                                    <h2>Why teams contact us</h2>
                                    <p>They need quick answers before a warehouse systems purchase.</p>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
