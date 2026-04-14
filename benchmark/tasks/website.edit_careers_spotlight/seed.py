"""Seed a simple website page for editor-focused benchmarking."""


def setup(env):
    website = env["website"].browse(1)
    env["website.rewrite"].search([
        ("url_from", "in", ["/policy-studio", "/operations-playbooks"]),
    ]).unlink()
    env["website.page"].search([
        ("url", "in", ["/policy-studio", "/operations-playbooks"]),
    ]).unlink()

    env["website.page"].with_context(website_id=website.id).create({
        "name": "Policy Studio",
        "type": "qweb",
        "url": "/policy-studio",
        "is_published": True,
        "website_id": website.id,
        "key": "benchmark.policy_studio",
        "arch": """
            <t t-call="website.layout">
                <div id="wrap">
                    <section class="pt96 pb96">
                        <div class="container">
                            <h1 class="text-center mb-5">Policy Studio</h1>
                            <div class="row g-4">
                                <div class="col-lg-4">
                                    <div class="card h-100 shadow-sm">
                                        <div class="card-body d-flex flex-column">
                                            <h3>Audit Trails</h3>
                                            <p>Track every critical change.</p>
                                            <a class="btn btn-outline-primary mt-auto" href="/contactus">Read Audit Guide</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-4">
                                    <div class="card h-100 shadow-sm">
                                        <div class="card-body d-flex flex-column">
                                            <h3>Escalation Paths</h3>
                                            <p>Route urgent issues quickly.</p>
                                            <a class="btn btn-outline-primary mt-auto" href="/contactus">Open Escalation Map</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-4">
                                    <div class="card h-100 shadow-sm">
                                        <div class="card-body d-flex flex-column">
                                            <h3>Incident Reviews</h3>
                                            <p>Capture follow-up after incidents.</p>
                                            <a class="btn btn-outline-primary mt-auto" href="/contactus">Review Incident Notes</a>
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

