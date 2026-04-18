"""Oracle for maintenance.create_equipment_schedule_preventive_plan.

JSON-RPC: create the 'Machinery' category (if absent), then create the
'Bench Press 01' equipment with the required Expected MTBF, technician,
category, and Effective Date.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/equipments")
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

            const user = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'bench_tech']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!user.length) {
                return 'missing Bench Tech technician user';
            }

            let category = await callKw({
                model: 'maintenance.equipment.category',
                method: 'search_read',
                args: [[['name', '=', 'Machinery']], ['id']],
                kwargs: { limit: 1 },
            });
            let categoryId;
            if (category.length) {
                categoryId = category[0].id;
            } else {
                const created = await callKw({
                    model: 'maintenance.equipment.category',
                    method: 'create',
                    args: [[{ name: 'Machinery' }]],
                    kwargs: {},
                });
                categoryId = Array.isArray(created) ? created[0] : created;
            }

            await callKw({
                model: 'maintenance.equipment',
                method: 'create',
                args: [[{
                    name: 'Bench Press 01',
                    category_id: categoryId,
                    technician_user_id: user[0].id,
                    expected_mtbf: 30,
                    effective_date: '2026-06-01',
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
