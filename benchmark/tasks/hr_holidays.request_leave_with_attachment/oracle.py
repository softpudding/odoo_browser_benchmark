"""Oracle for hr_holidays.request_leave_with_attachment.

Uses call_kw via page.evaluate to deterministically:
  - Resolve the admin employee + 'Annual Leave' leave type.
  - Create an hr.leave covering 2026-03-09 to 2026-03-10 with the
    seeded description.
  - Create an ir.attachment (PDF) linked to that hr.leave
    (res_model='hr.leave', res_id=<leave_id>).

Browser-use agents on the same task cannot drive the hidden
``<input type=file>`` behind the chatter paperclip and fail the
attachment check.
"""

import base64
import os

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


LEAVE_NAME = "Family event"
LEAVE_TYPE = "Annual Leave"
PDF_FILENAME = "leave_justification.pdf"

PDF_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "seed_artifacts",
    PDF_FILENAME,
)

# Fallback minimal PDF bytes, in case the seed artifact is missing for
# some reason. Kept in sync with seed.py.
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
        "leave_name": LEAVE_NAME,
        "leave_type": LEAVE_TYPE,
        "date_from": "2026-03-09 08:00:00",
        "date_to": "2026-03-10 17:00:00",
        "request_date_from": "2026-03-09",
        "request_date_to": "2026-03-10",
        "number_of_days": 2.0,
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

            // Resolve admin employee id.
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

            // Resolve leave type.
            const leaveTypes = await callKw(
                'hr.leave.type',
                'search_read',
                [[['name', '=', payload.leave_type]], ['id']],
                { limit: 1 },
            );
            if (!leaveTypes.length) {
                throw new Error('Leave type not found: ' + payload.leave_type);
            }
            const leaveTypeId = leaveTypes[0].id;

            // Create the hr.leave (confirm state by default via action_confirm).
            const leaveVals = {
                name: payload.leave_name,
                employee_id: employeeId,
                holiday_status_id: leaveTypeId,
                request_date_from: payload.request_date_from,
                request_date_to: payload.request_date_to,
                date_from: payload.date_from,
                date_to: payload.date_to,
                number_of_days: payload.number_of_days,
            };
            const created = await callKw(
                'hr.leave',
                'create',
                [[leaveVals]],
                {},
            );
            const leaveId = Array.isArray(created) ? created[0] : created;

            // Submit the leave -> 'confirm' (To Approve) state.
            try {
                await callKw('hr.leave', 'action_confirm', [[leaveId]], {});
            } catch (e) {
                // Some flows auto-confirm on create; ignore.
            }

            // Create the PDF attachment linked to the hr.leave record.
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
