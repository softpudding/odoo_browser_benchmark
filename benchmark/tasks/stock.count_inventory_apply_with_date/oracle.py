"""Oracle for stock.count_inventory_apply_with_date.

Logs into Odoo through Playwright, then drives the workflow via JSON-RPC
call_kw on stock.quant. Writes inventory_quantity=25 and
inventory_date='2026-03-20' on the existing WH/Stock quant for
'Bench Stock Counter', then calls action_apply_inventory to create the
balancing inventory adjustment move.
"""

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
                    ['product_id.name', '=', 'Bench Stock Counter'],
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
                    inventory_quantity: 25.0,
                    inventory_date: '2026-03-20',
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
