"""Seed a website page with heading, paragraph, and extra content for editing benchmark."""


def setup(env):
    website = env["website"].browse(1)

    # Clean up prior runs
    env["website.rewrite"].search([
        ("url_from", "in", ["/about-us", "/about-benchmark-industries"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/about-us", "/about-benchmark-industries"]),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": "About Us",
        "type": "qweb",
        "url": "/about-us",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.about_us_page",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb48">
                        <div class="container">
                            <h2 class="text-center mb-4">About Our Company</h2>
                            <p class="lead text-center mb-5">We are a dynamic enterprise committed to delivering value across every sector we operate in.</p>
                        </div>
                    </section>
                    <section class="pb96">
                        <div class="container">
                            <h3 class="text-center mb-4">Our Core Values</h3>
                            <div class="row g-4">
                                <div class="col-lg-4">
                                    <div class="card h-100 shadow-sm">
                                        <div class="card-body text-center">
                                            <h4>Innovation</h4>
                                            <p>Pushing boundaries with cutting-edge solutions.</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-4">
                                    <div class="card h-100 shadow-sm">
                                        <div class="card-body text-center">
                                            <h4>Integrity</h4>
                                            <p>Upholding the highest ethical standards.</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-4">
                                    <div class="card h-100 shadow-sm">
                                        <div class="card-body text-center">
                                            <h4>Excellence</h4>
                                            <p>Striving for quality in everything we do.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
