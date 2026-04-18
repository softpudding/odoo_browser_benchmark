"""Oracle for inventory.cycle_count_two_locations_apply_selected_delta."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-stock.action_view_inventory_tree")
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

            const quantRes = await callKw({
                model: 'stock.quant',
                method: 'search_read',
                args: [[
                    ['product_id.name', '=', 'Bench Cycle Count Rotor'],
                    ['location_id.complete_name', '=', 'WH/Stock']
                ], ['id']],
                kwargs: { limit: 1 },
            });
            if (!quantRes.length) {
                throw new Error('target quant not found');
            }
            const quantId = quantRes[0].id;
            await callKw({
                model: 'stock.quant',
                method: 'write',
                args: [[quantId], {
                    inventory_quantity: 12.0,
                    inventory_quantity_set: true,
                }],
                kwargs: {},
            });
            await callKw({
                model: 'stock.quant',
                method: 'action_apply_inventory',
                args: [[quantId]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
