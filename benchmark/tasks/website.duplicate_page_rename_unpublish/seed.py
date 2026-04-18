"""Seed for website.duplicate_page_rename_unpublish.

Category: deep_ui_interaction (EASY).

Starting state: primary website (id=1) has a seeded, published website.page
named 'Bench Original' at '/bench-original'. The agent must duplicate this
page via the Pages list Actions menu, rename the copy to 'Bench Original
Draft' at '/bench-original-draft', and leave the copy unpublished.

This seed removes any leftover 'Bench Original' / 'Bench Original Draft'
pages from prior runs so it is idempotent.
"""


ORIGINAL_NAME = "Bench Original"
ORIGINAL_URL = "/bench-original"
DRAFT_NAME = "Bench Original Draft"
DRAFT_URL = "/bench-original-draft"


def setup(env):
    website = env["website"].browse(1)

    # Cleanup prior seeded / duplicated pages (match by either name or url,
    # across active and archived records) so the seed is idempotent.
    env["website.page"].with_context(active_test=False).search([
        "|", "|", "|",
        ("url", "=", ORIGINAL_URL),
        ("url", "=", DRAFT_URL),
        ("name", "=", ORIGINAL_NAME),
        ("name", "=", DRAFT_NAME),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": ORIGINAL_NAME,
        "type": "qweb",
        "url": ORIGINAL_URL,
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.bench_original",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Bench Original</h1>
                            <p class="text-center">
                                This is the original benchmark page. Duplicate
                                it and rename the copy to "Bench Original Draft".
                            </p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
