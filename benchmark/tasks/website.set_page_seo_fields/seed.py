"""Seed a website page with empty SEO metadata for the set-page-seo-fields task.

Category: deep_ui_interaction (EASY).
Starting state: A published website.page at /bench-seo-page with no meta title,
description, or keywords set. The agent must open the page's Promote / Optimize
SEO dialog and fill in the three SEO fields.
"""


PAGE_URL = "/bench-seo-page"
PAGE_NAME = "Bench SEO Page"


def setup(env):
    website = env["website"].browse(1)

    # Idempotent cleanup of any previous run's artifacts.
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", PAGE_URL),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": PAGE_NAME,
        "type": "qweb",
        "url": PAGE_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_seo_page",
        "website_meta_title": False,
        "website_meta_description": False,
        "website_meta_keywords": False,
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Bench SEO Page</h1>
                            <div class="row">
                                <div class="col-lg-8 mx-auto">
                                    <h3>About this page</h3>
                                    <p>This page is used to validate that SEO metadata can be set via the Promote / Optimize SEO dialog.</p>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
