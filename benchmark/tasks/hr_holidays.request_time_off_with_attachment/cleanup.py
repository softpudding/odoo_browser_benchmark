"""Cleanup for hr_holidays.request_time_off_with_attachment.

Reverses the seed: drop any 'Medical appointment' leaves (+ linked
attachments), all Paid Leave records for admin, any BENCH-JUST.pdf
attachments on hr.leave, and the 'Paid Leave' leave type itself (if we
can — leave types may be pinned by demo data).
"""


LEAVE_TYPE_NAME = "Paid Leave"
LEAVE_DESC = "Medical appointment"
PDF_FILENAME = "BENCH-JUST.pdf"


def cleanup(env):
    admin = env.ref("base.user_admin")
    admin_emp = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE_NAME)], limit=1
    )

    # 1. Drop any leaves tied to admin/Paid Leave or matching the seeded
    #    description so both the description-named and auto-named variants
    #    are removed.
    leave_domains = [[("name", "=", LEAVE_DESC)]]
    if leave_type and admin_emp:
        leave_domains.append([
            ("employee_id", "=", admin_emp.id),
            ("holiday_status_id", "=", leave_type.id),
        ])

    all_leaves = env["hr.leave"].with_context(active_test=False)
    targets = env["hr.leave"]
    for dom in leave_domains:
        targets |= all_leaves.search(dom)

    if targets:
        atts = env["ir.attachment"].with_context(active_test=False).search([
            ("res_model", "=", "hr.leave"),
            ("res_id", "in", targets.ids),
        ])
        if atts:
            atts.unlink()
        for leave in targets:
            try:
                if leave.state == "validate":
                    leave.action_refuse()
            except Exception:
                pass
            try:
                if leave.state in ("confirm", "validate1", "refuse"):
                    leave.action_draft()
            except Exception:
                pass
        try:
            targets.unlink()
        except Exception:
            pass

    # 2. Drop any orphan BENCH-JUST.pdf attachments on hr.leave that
    #    survived the leave unlink.
    env["ir.attachment"].with_context(active_test=False).search([
        ("name", "=", PDF_FILENAME),
        ("res_model", "=", "hr.leave"),
    ]).unlink()
