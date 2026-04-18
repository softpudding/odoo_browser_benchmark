"""Seed a minimal website page for the image-snippet swap-source task.

Category: deep_ui_interaction (MEDIUM).

Starting state: a published website.page at /bench-image-page with a heading
section but no image snippet.  The agent must open this page in the website
builder, drag an Image snippet into the body, and swap its source image to a
specific library image (/web/image/website.library_image_10).  The seed is
idempotent: it removes any leftover page / rewrites at the same URL.
"""


PAGE_URL = "/bench-image-page"
PAGE_NAME = "Bench Image Page"


def setup(env):
    website = env["website"].browse(1)

    # Idempotent cleanup of any previous run's artifacts.
    env["website.rewrite"].search([
        ("url_from", "in", [PAGE_URL]),
    ]).unlink()
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", PAGE_URL),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": PAGE_NAME,
        "type": "qweb",
        "url": PAGE_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_image_page",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap" class="oe_structure oe_empty">
                    <section class="pt48 pb24">
                        <div class="container">
                            <h1 class="text-center mb-3">Our Image Showcase</h1>
                            <p class="lead text-center">Add an Image block below and swap its source to the requested library image.</p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
