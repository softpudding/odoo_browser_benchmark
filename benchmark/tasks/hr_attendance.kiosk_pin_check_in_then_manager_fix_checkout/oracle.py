"""Oracle for hr_attendance.kiosk_pin_check_in_then_manager_fix_checkout."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/attendances")
    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const res = await callKw({
                model: 'hr.attendance',
                method: 'search_read',
                args: [[
                    ['employee_id.name', '=', 'Bench Kiosk Worker'],
                    ['check_in', '=', '2026-05-20 09:00:00']
                ], ['id']],
                kwargs: { limit: 1 },
            });
            if (!res.length) {
                throw new Error('attendance not found');
            }
            await callKw({
                model: 'hr.attendance',
                method: 'write',
                args: [[res[0].id], { check_out: '2026-05-20 17:00:00' }],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
