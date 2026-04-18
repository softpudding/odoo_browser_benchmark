"""Seed a minimal website page for the image gallery / carousel insertion task.

The agent opens this page in the website builder and must insert an
Image Gallery snippet (which renders as a carousel) into the body.  We
deliberately do NOT use the home page (`/`) here — builder "duplicate
home" flows tend to corrupt that record and cause watchdog timeouts.
"""


def setup(env):
    website = env["website"].browse(1)

    # Clean up prior runs
    env["website.rewrite"].search([
        ("url_from", "in", ["/bench-gallery-test"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/bench-gallery-test"]),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": "Bench Gallery Test",
        "type": "qweb",
        "url": "/bench-gallery-test",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_gallery_test_page",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap" class="oe_structure oe_empty">
                    <section class="pt48 pb24">
                        <div class="container">
                            <h1 class="text-center mb-3">Our Portfolio</h1>
                            <p class="lead text-center">Add an image gallery below to showcase recent work.</p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
