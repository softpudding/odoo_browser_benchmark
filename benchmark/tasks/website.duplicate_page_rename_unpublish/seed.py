"""Seed for website.duplicate_page_rename_unpublish.

Category: deep_ui_interaction (EASY).

Starting state: primary website (id=1) has a seeded, published website.page
named 'Bench Source Page' at '/bench-source-page'. The agent must duplicate
this page via the Pages list Actions menu, rename the copy to 'Bench
Duplicate Page' at '/bench-duplicate-page', and leave the copy unpublished.

This seed removes any leftover 'Bench Source Page' / 'Bench Duplicate Page'
pages (and any page sitting at either url) from prior runs so it is
idempotent.
"""


SOURCE_NAME = "Bench Source Page"
SOURCE_URL = "/bench-source-page"
DUPLICATE_NAME = "Bench Duplicate Page"
DUPLICATE_URL = "/bench-duplicate-page"


def setup(env):
    website = env["website"].browse(1)

    # Cleanup prior seeded / duplicated pages (match by either name or url,
    # across active and archived records) so the seed is idempotent.
    env["website.page"].with_context(active_test=False).search([
        "|", "|", "|",
        ("url", "=", SOURCE_URL),
        ("url", "=", DUPLICATE_URL),
        ("name", "=", SOURCE_NAME),
        ("name", "=", DUPLICATE_NAME),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": SOURCE_NAME,
        "type": "qweb",
        "url": SOURCE_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_source_page",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Bench Source Page</h1>
                            <p class="text-center">
                                This is the source benchmark page. Duplicate
                                it and rename the copy to "Bench Duplicate Page".
                            </p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
