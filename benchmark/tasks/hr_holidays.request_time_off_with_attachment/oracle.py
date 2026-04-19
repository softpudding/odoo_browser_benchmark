"""Oracle for hr_holidays.request_time_off_with_attachment.

Uses call_kw via page.evaluate to deterministically:
  - Resolve admin's hr.employee + the seeded 'Paid Leave' leave type.
  - Create an hr.leave covering 2026-07-01 -> 2026-07-02 (Wed/Thu = 2
    working days) with description 'Medical appointment'. hr.leave.state
    defaults to 'confirm' on create in Odoo 19 (no action_confirm method).
  - Create an ir.attachment(BENCH-JUST.pdf, res_model='hr.leave',
    res_id=<leave_id>) wrapping the seeded PDF bytes.

Browser-use cannot drive the hidden <input type=file> behind the chatter
paperclip, so its attachment step fails — that's the hard-tier anchor.
The oracle bypasses the UI with RPC to guarantee a deterministic PASS.
"""

import base64
import os

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


LEAVE_TYPE_NAME = "Paid Leave"
LEAVE_DESC = "Medical appointment"
PDF_FILENAME = "BENCH-JUST.pdf"

PDF_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "seed_artifacts",
    PDF_FILENAME,
)

# Fallback PDF bytes — kept in sync with seed.py. Only used if the seed
# artifact on disk is missing or empty (should not happen in practice).
FALLBACK_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n"
    b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n"
    b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>endobj\n"
    b"xref\n0 4\n0000000000 65535 f \n"
    b"0000000010 00000 n \n0000000053 00000 n \n0000000100 00000 n \n"
    b"trailer<< /Size 4 /Root 1 0 R >>\n"
    b"startxref\n160\n%%EOF\n"
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)

    if os.path.exists(PDF_PATH) and os.path.getsize(PDF_PATH) > 0:
        with open(PDF_PATH, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode("ascii")
    else:
        pdf_b64 = base64.b64encode(FALLBACK_PDF_BYTES).decode("ascii")

    payload = {
        "leave_desc": LEAVE_DESC,
        "leave_type_name": LEAVE_TYPE_NAME,
        "request_date_from": "2026-07-01",
        "request_date_to": "2026-07-02",
        "pdf_filename": PDF_FILENAME,
        "pdf_b64": pdf_b64,
    }

    response = page.evaluate(
        """async (payload) => {
            const callKw = async (model, method, args, kwargs) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { model, method, args, kwargs: kwargs || {} },
                    }),
                });
                const j = await res.json();
                if (j.error) {
                    throw new Error(JSON.stringify(j.error));
                }
                return j.result;
            };

            // 1. Resolve admin employee id.
            const adminUsers = await callKw(
                'res.users',
                'search_read',
                [[['login', '=', 'admin']], ['id']],
                { limit: 1 },
            );
            if (!adminUsers.length) {
                throw new Error('admin user not found');
            }
            const adminUserId = adminUsers[0].id;

            const employees = await callKw(
                'hr.employee',
                'search_read',
                [[['user_id', '=', adminUserId]], ['id']],
                { limit: 1 },
            );
            if (!employees.length) {
                throw new Error('admin employee not found');
            }
            const employeeId = employees[0].id;

            // 2. Resolve 'Paid Leave' leave type id.
            const leaveTypes = await callKw(
                'hr.leave.type',
                'search_read',
                [[['name', '=', payload.leave_type_name]], ['id']],
                { limit: 1 },
            );
            if (!leaveTypes.length) {
                throw new Error('Leave type not found: ' + payload.leave_type_name);
            }
            const leaveTypeId = leaveTypes[0].id;

            // 3. Create the hr.leave. State defaults to 'confirm' (To
            // Approve) on create — there is NO action_confirm method on
            // hr.leave in Odoo 19, and the task explicitly requires
            // leaving the record in 'confirm' (not approving it).
            const leaveVals = {
                name: payload.leave_desc,
                employee_id: employeeId,
                holiday_status_id: leaveTypeId,
                request_date_from: payload.request_date_from,
                request_date_to: payload.request_date_to,
            };
            const created = await callKw(
                'hr.leave',
                'create',
                [[leaveVals]],
                {},
            );
            const leaveId = Array.isArray(created) ? created[0] : created;
            if (!leaveId) {
                throw new Error('Failed to create hr.leave: ' + JSON.stringify(created));
            }

            // 4. Create the BENCH-JUST.pdf ir.attachment directly linked
            // to this hr.leave. This is the server-side equivalent of
            // the chatter-paperclip upload on the saved leave form.
            await callKw(
                'ir.attachment',
                'create',
                [[{
                    name: payload.pdf_filename,
                    res_model: 'hr.leave',
                    res_id: leaveId,
                    type: 'binary',
                    mimetype: 'application/pdf',
                    datas: payload.pdf_b64,
                }]],
                {},
            );

            return 'ok';
        }""",
        payload,
    )

    if response != "ok":
        raise RuntimeError(f"Unexpected oracle response: {response!r}")


run_oracle(oracle)
