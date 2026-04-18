"""Oracle for stock.adjust_inventory_with_location_filter.

Logs in via Playwright, then drives the adjustment via JSON-RPC. Only the
Shelf A quant is touched: inventory_quantity=42, inventory_date set,
action_apply_inventory. Shelf B is left alone.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PRODUCT_NAME = "Bench Multi Loc Product"
SHELF_A_COMPLETE = "WH/Stock/Shelf A"


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-stock.action_view_inventory_tree")
    response = page.evaluate(
        """async ([productName, shelfComplete]) => {
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

            const quantRes = await callKw({
                model: 'stock.quant',
                method: 'search_read',
                args: [[
                    ['product_id.name', '=', productName],
                    ['location_id.complete_name', '=', shelfComplete]
                ], ['id']],
                kwargs: { limit: 1 },
            });
            if (!quantRes.length) {
                throw new Error('target Shelf A quant not found');
            }
            const quantId = quantRes[0].id;

            await callKw({
                model: 'stock.quant',
                method: 'write',
                args: [[quantId], {
                    inventory_quantity: 42.0,
                    inventory_date: '2026-04-19',
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
        [PRODUCT_NAME, SHELF_A_COMPLETE],
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
