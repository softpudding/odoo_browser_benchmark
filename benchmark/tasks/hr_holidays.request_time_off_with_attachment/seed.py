"""Seed for hr_holidays.request_time_off_with_attachment.

HARD (tier 3): Agent must (a) create an hr.leave of type 'Paid Leave'
spanning 2026-07-01 -> 2026-07-02 (2 working days, Wed-Thu) with
description 'Medical appointment', (b) save so it lands in state='confirm'
(To Approve), and (c) attach the pre-seeded BENCH-JUST.pdf via the chatter
paperclip so an ir.attachment(res_model='hr.leave', res_id=<leave_id>,
name='BENCH-JUST.pdf') exists.

The chatter paperclip triggers a hidden <input type=file> that browser-use
cannot reliably drive — that's the primary calibration lever.

Seed responsibilities:
  - Create/refresh a `Paid Leave` hr.leave.type with requires_allocation=False
    (Boolean, not Selection — see cookbook for row 451) + leave_validation_type='hr'
    so admin (who has the HR groups) can see/submit the request without
    needing a pre-approved allocation.
  - Ensure admin has an hr.employee record (the leave's employee_id).
  - Drop any prior 'Medical appointment' leaves and prior BENCH-JUST.pdf
    attachments (on hr.leave) so the seed is idempotent.
  - Write a tiny valid PDF to seed_artifacts/BENCH-JUST.pdf on disk so the
    agent (and oracle) have a file path to upload / read.
"""

import os


LEAVE_TYPE_NAME = "Paid Leave"
LEAVE_DESC = "Medical appointment"
PDF_FILENAME = "BENCH-JUST.pdf"
TASK_ID = "hr_holidays.request_time_off_with_attachment"

# Minimal valid PDF bytes — PDF header + trivial catalog/pages/page stanza.
# Not intended to render as a rich document; only used to prove non-empty
# binary content reached ir.attachment.datas/raw via the chatter upload.
PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n"
    b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n"
    b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>endobj\n"
    b"xref\n0 4\n0000000000 65535 f \n"
    b"0000000010 00000 n \n0000000053 00000 n \n0000000100 00000 n \n"
    b"trailer<< /Size 4 /Root 1 0 R >>\n"
    b"startxref\n160\n%%EOF\n"
)


def _ensure_pdf_on_disk():
    """Make sure seed_artifacts/BENCH-JUST.pdf exists with real bytes."""
    try:
        import benchmark
        bench_dir = os.path.dirname(os.path.abspath(benchmark.__file__))
    except Exception:
        bench_dir = os.path.join(os.getcwd(), "benchmark")
    artifact_dir = os.path.join(bench_dir, "tasks", TASK_ID, "seed_artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    path = os.path.join(artifact_dir, PDF_FILENAME)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "wb") as f:
            f.write(PDF_BYTES)


def _drop_prior_records(env, leave_type_id):
    """Remove prior 'Medical appointment' leaves (+ their attachments) so the
    seed is idempotent and the agent creates the request from scratch.
    """
    prior_leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_DESC),
    ])
    # Also drop any prior leaves of our type with admin employee — defensive
    # in case a prior run saved the leave without the description (e.g. BU
    # skipped the description field).
    admin = env.ref("base.user_admin")
    admin_emp = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if leave_type_id and admin_emp:
        prior_leaves |= env["hr.leave"].with_context(active_test=False).search([
            ("holiday_status_id", "=", leave_type_id),
            ("employee_id", "=", admin_emp.id),
        ])

    if prior_leaves:
        # Drop linked attachments first.
        atts = env["ir.attachment"].with_context(active_test=False).search([
            ("res_model", "=", "hr.leave"),
            ("res_id", "in", prior_leaves.ids),
        ])
        if atts:
            atts.unlink()
        for leave in prior_leaves:
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
            prior_leaves.unlink()
        except Exception:
            pass

    # Belt-and-suspenders: drop any stale BENCH-JUST.pdf attachments on
    # hr.leave whose parent leave has gone away.
    env["ir.attachment"].with_context(active_test=False).search([
        ("name", "=", PDF_FILENAME),
        ("res_model", "=", "hr.leave"),
    ]).unlink()


def setup(env):
    admin = env.ref("base.user_admin")

    # Grant admin the Time Off groups so the leave type with
    # leave_validation_type='hr' is accessible and the new-request form
    # loads cleanly for admin.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    # Ensure admin has an employee record so the hr.leave can resolve
    # employee_id automatically on the new-request form.
    admin_emp = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if not admin_emp:
        admin_emp = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
        })

    # Create / refresh the 'Paid Leave' leave type. In this Odoo 19 build
    # hr.leave.type.requires_allocation is a fields.Boolean (default=True),
    # NOT a Selection — see COOKBOOK_NOTES in sibling task
    # hr_holidays.request_sick_leave_approve_self. We pass False so the
    # request can be created WITHOUT a pre-approved allocation.
    # leave_validation_type='hr' preserves the Confirm -> Approve lifecycle
    # (state defaults to 'confirm' on create in Odoo 19; there is no
    # action_confirm method).
    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE_NAME)], limit=1
    )
    type_vals = {
        "name": LEAVE_TYPE_NAME,
        "requires_allocation": False,
        "leave_validation_type": "hr",
        "request_unit": "day",
        "time_type": "leave",
    }
    if leave_type:
        leave_type.write(type_vals)
    else:
        leave_type = env["hr.leave.type"].create(type_vals)

    # Wipe prior leaves + attachments so the agent starts fresh.
    _drop_prior_records(env, leave_type.id)

    # Ensure the BENCH-JUST.pdf artifact exists on disk.
    _ensure_pdf_on_disk()
