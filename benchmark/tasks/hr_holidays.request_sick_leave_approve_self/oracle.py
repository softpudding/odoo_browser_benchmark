"""Oracle for hr_holidays.request_sick_leave_approve_self.

Performs the two-step role lifecycle:
  (1) Create an hr.leave of type 'Sick Leave' for
      'Bench Sick Employee' on 2026-05-11 to 2026-05-12
      (two working days). hr.leave.state defaults to 'confirm'
      on create — there is no action_confirm method in Odoo 19.
  (2) Approve it so it reaches state='validate'.

The real task difficulty is the two-phase submit + approve across the
employee and manager perspectives plus the date-widget entry. The oracle
uses RPC call_kw to ensure deterministic PASS; the UI is stable but
fragile to render-timing changes on the new-request dialog.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off")
    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };

            const employeeRes = await callKw({
                model: 'hr.employee',
                method: 'search_read',
                args: [[['name', '=', 'Bench Sick Employee']], ['id']],
                kwargs: { limit: 1 },
            });
            const leaveTypeRes = await callKw({
                model: 'hr.leave.type',
                method: 'search_read',
                args: [[['name', '=', 'Sick Leave']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!employeeRes.result?.length || !leaveTypeRes.result?.length) {
                return 'missing employee or leave type';
            }

            const employeeId = employeeRes.result[0].id;
            const leaveTypeId = leaveTypeRes.result[0].id;

            const leaveCreateRes = await callKw({
                model: 'hr.leave',
                method: 'create',
                args: [[{
                    name: 'Sick leave benchmark',
                    employee_id: employeeId,
                    holiday_status_id: leaveTypeId,
                    request_date_from: '2026-05-11',
                    request_date_to: '2026-05-12',
                }]],
                kwargs: {},
            });
            const leaveId = Array.isArray(leaveCreateRes.result)
                ? leaveCreateRes.result[0]
                : leaveCreateRes.result;
            if (!leaveId) {
                return 'failed to create leave: ' + JSON.stringify(leaveCreateRes);
            }

            // hr.leave.state defaults to 'confirm' on create, so we can
            // skip an explicit submit step and go directly to approval.
            // Approve as manager: confirm -> validate.
            const approveRes = await callKw({
                model: 'hr.leave',
                method: 'action_approve',
                args: [[leaveId]],
                kwargs: {},
            });
            if (approveRes.error) {
                return 'action_approve failed: ' + JSON.stringify(approveRes.error);
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
