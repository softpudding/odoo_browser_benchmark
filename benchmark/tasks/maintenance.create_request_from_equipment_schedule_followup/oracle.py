"""Oracle for maintenance.create_request_from_equipment_schedule_followup."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/maintenance-requests")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
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
            const todoType = await callKw({
                model: 'mail.activity.type',
                method: 'search_read',
                args: [[['name', '=', 'To-Do']], ['id']],
                kwargs: { limit: 1 },
            });
            const modelRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'maintenance.request']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!equipment.length || !user.length || !todoType.length || !modelRes.length) {
                return 'missing maintenance seed data';
            }

            const requestId = unwrapId(await callKw({
                model: 'maintenance.request',
                method: 'create',
                args: [[{
                    name: 'Inspect Forklift Battery Cooling',
                    equipment_id: equipment[0].id,
                    maintenance_team_id: equipment[0].maintenance_team_id[0],
                    user_id: user[0].id,
                }]],
                kwargs: {},
            }));
            await callKw({
                model: 'mail.activity',
                method: 'create',
                args: [[{
                    res_model_id: modelRes[0].id,
                    res_id: requestId,
                    activity_type_id: todoType[0].id,
                    summary: 'Review cooling test report',
                    date_deadline: '2026-05-23',
                    user_id: user[0].id,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
