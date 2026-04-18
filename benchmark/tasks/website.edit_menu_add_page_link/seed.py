"""Seed for website.edit_menu_add_page_link.

Category: deep_ui_interaction (MEDIUM).

Starting state: primary website (id=1) has a seeded website.page at
'/benchmark-contact' but NO website.menu pointing to it. The agent must
add a new top-level menu entry 'Benchmark Contact' linking to that URL
via the Website app's Menu Editor.
"""


def setup(env):
    website = env["website"].browse(1)

    # Cleanup prior menu entries from earlier runs (name or url match).
    env["website.menu"].with_context(active_test=False).search([
        "|",
        ("name", "=", "Benchmark Contact"),
        ("url", "=", "/benchmark-contact"),
    ]).unlink()

    # Cleanup prior seeded page so this is idempotent.
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", "/benchmark-contact"),
    ]).unlink()

    # Seed a minimal website page at /benchmark-contact so the menu entry
    # can reference an existing page.
    env["website.page"].with_context(website_id=website.id).create({
        "name": "Benchmark Contact",
        "type": "qweb",
        "url": "/benchmark-contact",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.benchmark_contact",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Benchmark Contact</h1>
                            <p class="text-center">
                                Reach the benchmark team at contact@benchmark.example.com.
                            </p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
