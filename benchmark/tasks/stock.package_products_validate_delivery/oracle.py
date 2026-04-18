"""Oracle for stock.package_products_validate_delivery."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
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

            const pickingRes = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [[['origin', '=', 'BENCH-PACK-DEL-01']], ['id', 'move_line_ids']],
                kwargs: { limit: 1 },
            });
            if (!pickingRes.length) {
                throw new Error('missing picking');
            }
            const pickingId = pickingRes[0].id;
            const lines = await callKw({
                model: 'stock.move.line',
                method: 'search_read',
                args: [[['picking_id', '=', pickingId]], ['id', 'move_id']],
                kwargs: {},
            });
            for (const line of lines) {
                const move = await callKw({
                    model: 'stock.move',
                    method: 'read',
                    args: [[line.move_id[0]], ['product_uom_qty']],
                    kwargs: {},
                });
                await callKw({
                    model: 'stock.move.line',
                    method: 'write',
                    args: [[line.id], { quantity: move[0].product_uom_qty }],
                    kwargs: {},
                });
            }
            await callKw({ model: 'stock.picking', method: 'action_put_in_pack', args: [[pickingId]], kwargs: {} });
            await callKw({ model: 'stock.picking', method: 'button_validate', args: [[pickingId]], kwargs: {} });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
