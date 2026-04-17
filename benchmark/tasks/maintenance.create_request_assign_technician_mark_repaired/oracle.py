"""Oracle for maintenance.create_request_assign_technician_mark_repaired."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/maintenance-requests")
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

            const equipment = await callKw({
                model: 'maintenance.equipment',
                method: 'search_read',
                args: [[['name', '=', 'Forklift FL-88']], ['id', 'maintenance_team_id']],
                kwargs: { limit: 1 },
            });
            const user = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['name', '=', 'Marc Demo']], ['id']],
                kwargs: { limit: 1 },
            });
            const doneStage = await callKw({
                model: 'maintenance.stage',
                method: 'search_read',
                args: [[['done', '=', true]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!equipment.length || !user.length || !doneStage.length) {
                return 'missing maintenance seed data';
            }

            await callKw({
                model: 'maintenance.request',
                method: 'create',
                args: [[{
                    name: 'Replace Dock Sensor',
                    equipment_id: equipment[0].id,
                    maintenance_team_id: equipment[0].maintenance_team_id[0],
                    user_id: user[0].id,
                    stage_id: doneStage[0].id,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
