"""Oracle for maintenance.create_equipment_assign_category_team."""

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

            const category = await callKw({
                model: 'maintenance.equipment.category',
                method: 'search_read',
                args: [[['name', '=', 'Warehouse Gear']], ['id']],
                kwargs: { limit: 1 },
            });
            const team = await callKw({
                model: 'maintenance.team',
                method: 'search_read',
                args: [[['name', '=', 'Bench Maintenance']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!category.length || !team.length) {
                return 'missing seed data (category or team)';
            }

            await callKw({
                model: 'maintenance.equipment',
                method: 'create',
                args: [[{
                    name: 'Dock Scanner DS-200',
                    serial_no: 'DS-200-SN-1042',
                    category_id: category[0].id,
                    maintenance_team_id: team[0].id,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
