"""Cleanup artifacts from prior runs of
purchase.send_rfq_email_with_template_signature."""


TARGET_REF = "R-BENCH-EMAIL-001"
DISTRACTOR_REF = "R-BENCH-EMAIL-002"


def cleanup(env):
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_ref", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for po in pos:
        env["mail.message"].search([
            ("model", "=", "purchase.order"),
            ("res_id", "=", po.id),
        ]).unlink()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()

    env["ir.mail_server"].with_context(active_test=False).search(
        [("name", "=", "benchmark_fake_smtp")]
    ).unlink()
