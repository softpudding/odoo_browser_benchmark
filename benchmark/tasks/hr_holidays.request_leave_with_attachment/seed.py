"""Seed for hr_holidays.request_leave_with_attachment.

Ensure an 'Annual Leave' leave type exists, the admin employee has an
allocation so they can submit a 2-day request, and the PDF justification
artifact exists on disk so the agent can upload it through the chatter.

Also wipe any prior hr.leave records (and their linked attachments) with
the seeded description so the task runs deterministically.
"""

import os


LEAVE_NAME = "Family event"
LEAVE_TYPE = "Annual Leave"
PDF_FILENAME = "leave_justification.pdf"
TASK_ID = "hr_holidays.request_leave_with_attachment"

# Minimal valid PDF content (PDF header + trivial structure). Browsers and
# Odoo both accept this as a binary attachment; it is not meant to render
# as a real document.
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
    """Make sure the leave_justification.pdf artifact exists on disk."""
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


def setup(env):
    # Wipe prior leave records with the seeded description, along with any
    # ir.attachment rows linked to them.
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    if prior:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.leave"),
            ("res_id", "in", prior.ids),
        ])
        if attachments:
            attachments.unlink()
        for leave in prior:
            if leave.state == "validate":
                leave.action_refuse()
                leave.action_draft()
            elif leave.state in ("confirm", "validate1"):
                leave.action_draft()
        prior.unlink()

    admin = env.ref("base.user_admin")
    admin_employee = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if not admin_employee:
        admin_employee = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
        })

    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE)], limit=1
    )
    if not leave_type:
        leave_type = env["hr.leave.type"].create({
            "name": LEAVE_TYPE,
            "requires_allocation": True,
            "leave_validation_type": "manager",
        })
    else:
        leave_type.write({
            "requires_allocation": True,
            "leave_validation_type": "manager",
        })

    existing_alloc = env["hr.leave.allocation"].with_context(
        active_test=False
    ).search([
        ("employee_id", "=", admin_employee.id),
        ("holiday_status_id", "=", leave_type.id),
        ("state", "=", "validate"),
    ])
    if sum(existing_alloc.mapped("number_of_days")) < 5:
        alloc = env["hr.leave.allocation"].create({
            "name": "Annual allocation for admin",
            "holiday_status_id": leave_type.id,
            "employee_id": admin_employee.id,
            "number_of_days": 20,
            "allocation_type": "regular",
            "date_from": "2026-01-01",
        })
        if alloc.state == "draft":
            alloc.action_confirm()
        if alloc.state == "confirm":
            alloc.action_approve()

    _ensure_pdf_on_disk()
