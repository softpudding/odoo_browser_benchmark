"""Clean up artifacts from previous runs.

Wipes the hr.leave record named 'Family event' and any ir.attachment
rows linked to it so the seed can re-run deterministically.
"""


LEAVE_NAME = "Family event"


def cleanup(env):
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    if leaves:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.leave"),
            ("res_id", "in", leaves.ids),
        ])
        if attachments:
            attachments.unlink()
        for leave in leaves:
            if leave.state == "validate":
                leave.action_refuse()
                leave.action_draft()
            elif leave.state in ("confirm", "validate1"):
                leave.action_draft()
        leaves.unlink()
