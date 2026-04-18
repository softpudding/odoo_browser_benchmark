"""Seed a website page with empty SEO metadata for the set-page-seo-fields task.

Category: deep_ui_interaction (EASY).
Starting state: A published website.page at /bench-product with no meta title,
description, or keywords set. The agent must open the page's Optimize SEO
dialog and fill in the three SEO fields.
"""


PAGE_URL = "/bench-product"
PAGE_NAME = "Bench Product Landing"


def setup(env):
    website = env["website"].browse(1)

    env["website.page"].search([
        ("url", "=", PAGE_URL),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": PAGE_NAME,
        "type": "qweb",
        "url": PAGE_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_product_landing",
        "website_meta_title": False,
        "website_meta_description": False,
        "website_meta_keywords": False,
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Bench Product Landing</h1>
                            <div class="row">
                                <div class="col-lg-8 mx-auto">
                                    <h3>Our Flagship Bench Product</h3>
                                    <p>Handcrafted with premium materials and built to last a lifetime.</p>
                                    <p>Every Bench Product is backed by our lifetime warranty and ships free.</p>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
