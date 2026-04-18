"""Oracle for maintenance.fill_description_schedule_window_move_to_repaired.

JSON-RPC: locate the seeded request, write description + schedule_date +
schedule_end + the Repaired stage in one go.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


REQUEST_NAME = "Replace Conveyor Drive Belt"
DESCRIPTION = (
    "Belt cracked at the splice. Replaced with new spare from inventory. "
    "Tensioner re-aligned and idler bearings greased."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/maintenance")

    response = page.evaluate(
        """async ([requestName, description]) => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const requests = await callKw({
                model: 'maintenance.request',
                method: 'search_read',
                args: [[['name', '=', requestName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!requests.length) throw new Error('Maintenance request missing');
            const requestId = requests[0].id;

            const stageRes = await callKw({
                model: 'ir.model.data',
                method: 'search_read',
                args: [
                    [['module', '=', 'maintenance'], ['name', '=', 'stage_3']],
                    ['res_id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!stageRes.length) throw new Error('Repaired stage missing');
            const repairedStageId = stageRes[0].res_id;

            await callKw({
                model: 'maintenance.request',
                method: 'write',
                args: [[requestId], {
                    description: '<p>' + description + '</p>',
                    schedule_date: '2026-04-15 09:00:00',
                    schedule_end: '2026-04-15 11:00:00',
                    stage_id: repairedStageId,
                }],
                kwargs: {},
            });

            return 'ok';
        }""",
        [REQUEST_NAME, DESCRIPTION],
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
