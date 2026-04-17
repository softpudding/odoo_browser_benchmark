"""Oracle for hr_holidays.allocate_leave_then_request_against_balance."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off-approval")
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
                args: [[['name', '=', 'Marc Demo']], ['id']],
                kwargs: { limit: 1 },
            });
            const leaveTypeRes = await callKw({
                model: 'hr.leave.type',
                method: 'search_read',
                args: [[['name', '=', 'Sick Time Off']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!employeeRes.result?.length || !leaveTypeRes.result?.length) {
                return 'missing employee or leave type';
            }

            const employeeId = employeeRes.result[0].id;
            const leaveTypeId = leaveTypeRes.result[0].id;

            const allocCreateRes = await callKw({
                model: 'hr.leave.allocation',
                method: 'create',
                args: [[{
                    name: 'Quarter-End Sick Leave Buffer',
                    employee_id: employeeId,
                    holiday_status_id: leaveTypeId,
                    number_of_days: 4,
                    allocation_type: 'regular',
                }]],
                kwargs: {},
            });
            const allocId = Array.isArray(allocCreateRes.result) ? allocCreateRes.result[0] : allocCreateRes.result;
            await callKw({
                model: 'hr.leave.allocation',
                method: 'action_confirm',
                args: [[allocId]],
                kwargs: {},
            });
            await callKw({
                model: 'hr.leave.allocation',
                method: 'action_approve',
                args: [[allocId]],
                kwargs: {},
            });

            const leaveCreateRes = await callKw({
                model: 'hr.leave',
                method: 'create',
                args: [[{
                    name: 'Warehouse flu recovery',
                    employee_id: employeeId,
                    holiday_status_id: leaveTypeId,
                    request_date_from: '2026-06-23',
                    request_date_to: '2026-06-24',
                }]],
                kwargs: {},
            });
            const leaveId = Array.isArray(leaveCreateRes.result) ? leaveCreateRes.result[0] : leaveCreateRes.result;
            await callKw({
                model: 'hr.leave',
                method: 'action_confirm',
                args: [[leaveId]],
                kwargs: {},
            });
            await callKw({
                model: 'hr.leave',
                method: 'action_approve',
                args: [[leaveId]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
