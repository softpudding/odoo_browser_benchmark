"""Oracle for maintenance.archive_equipment_create_replacement.

Archives the seeded 'Old Belt OB-99' equipment via the form Actions menu,
then creates the replacement 'New Belt NB-100' record (same category,
specific serial number) via JSON-RPC. JSON-RPC is permitted for oracles
per ODOO19_PATTERNS.md; the browser-use agent must still solve the task
through the UI.
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

            const category = await callKw({
                model: 'maintenance.equipment.category',
                method: 'search_read',
                args: [[['name', '=', 'Warehouse Gear']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!category.length) {
                return 'missing seed data (Warehouse Gear category)';
            }

            const oldBelt = await callKw({
                model: 'maintenance.equipment',
                method: 'search_read',
                args: [[['name', '=', 'Old Belt OB-99']], ['id', 'active']],
                kwargs: { limit: 1, context: { active_test: false } },
            });
            if (!oldBelt.length) {
                return 'missing seed data (Old Belt OB-99)';
            }

            // Archive the old belt (action_archive sets active=False).
            await callKw({
                model: 'maintenance.equipment',
                method: 'action_archive',
                args: [[oldBelt[0].id]],
                kwargs: {},
            });

            // Create the replacement equipment.
            await callKw({
                model: 'maintenance.equipment',
                method: 'create',
                args: [[{
                    name: 'New Belt NB-100',
                    serial_no: 'NB-100-SN-2026',
                    category_id: category[0].id,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
