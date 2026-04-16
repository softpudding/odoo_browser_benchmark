"""Seed an About Us page for the update-contact-info task.

Category: deep_ui_interaction (EASY).
Starting state: About Us page with contact info containing phone number
"+1 555 123 4567". The agent must change it to "+1 555 987 6543".
"""


def setup(env):
    website = env["website"].browse(1)

    env["website.page"].search([
        ("url", "=", "/about-us"),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": "About Us",
        "type": "qweb",
        "url": "/about-us",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.about_us",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">About Us</h1>
                            <div class="row">
                                <div class="col-lg-6">
                                    <h3>Our Story</h3>
                                    <p>We are a dedicated team committed to delivering excellence.</p>
                                </div>
                                <div class="col-lg-6">
                                    <h3>Contact Information</h3>
                                    <p><strong>Phone:</strong> +1 555 123 4567</p>
                                    <p><strong>Email:</strong> info@example.com</p>
                                    <p><strong>Address:</strong> 123 Main Street, Suite 100</p>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </t>
        """,
    })