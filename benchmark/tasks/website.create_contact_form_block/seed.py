"""Seed a minimal website page for the contact-form block task.

Category: deep_ui_interaction (HARD).

Starting state: a published website.page at /bench-contact-form with a heading
section but no form.  The agent must open this page in the website builder,
drop a Form snippet, re-point it at res.partner (Contact), keep the default
Subject field, and add a custom 'Your Message' Long Text field.  The seed is
idempotent: it removes any leftover page / rewrites at the same URL.
"""


PAGE_URL = "/bench-contact-form"
PAGE_NAME = "Bench Contact Form"


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
        "key": "benchmark.bench_contact_form",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap" class="oe_structure oe_empty">
                    <section class="pt48 pb24">
                        <div class="container">
                            <h1 class="text-center mb-3">Contact Us</h1>
                            <p class="lead text-center">Add a Form block below, point it at Contact (res.partner), keep the Subject field, and add a 'Your Message' Long Text field.</p>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })
