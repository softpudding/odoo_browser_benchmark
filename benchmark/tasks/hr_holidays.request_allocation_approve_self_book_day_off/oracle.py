"""Oracle for hr_holidays.request_allocation_approve_self_book_day_off.

Uses RPC call_kw to (1) create + confirm + approve a 5-day Bench Bonus Days
allocation for Bench Worker, then (2) create + confirm + approve a 1-day
leave against it on 2026-05-15. RPC is used instead of UI scraping because
the real difficulty lives in the two-phase allocation-then-leave order + the
two Approve clicks; the UI is stable but fragile to render timing changes.
"""

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
                args: [[['name', '=', 'Bench Worker']], ['id']],
                kwargs: { limit: 1 },
            });
            const leaveTypeRes = await callKw({
                model: 'hr.leave.type',
                method: 'search_read',
                args: [[['name', '=', 'Bench Bonus Days']], ['id']],
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
                    name: 'Q2 bonus',
                    employee_id: employeeId,
                    holiday_status_id: leaveTypeId,
                    number_of_days: 5,
                    allocation_type: 'regular',
                }]],
                kwargs: {},
            });
            const allocId = Array.isArray(allocCreateRes.result) ? allocCreateRes.result[0] : allocCreateRes.result;
            if (!allocId) return 'failed to create allocation: ' + JSON.stringify(allocCreateRes);
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
                    name: 'Bench day off',
                    employee_id: employeeId,
                    holiday_status_id: leaveTypeId,
                    request_date_from: '2026-05-15',
                    request_date_to: '2026-05-15',
                }]],
                kwargs: {},
            });
            const leaveId = Array.isArray(leaveCreateRes.result) ? leaveCreateRes.result[0] : leaveCreateRes.result;
            if (!leaveId) return 'failed to create leave: ' + JSON.stringify(leaveCreateRes);
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
