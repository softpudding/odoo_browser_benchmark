"""Oracle for sale_stock.confirm_so_manual_reserve_validate_delivery."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
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

            const so = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'BENCH-SO-RESERVE']], ['id', 'name']],
                kwargs: { limit: 1 },
            });
            if (!so.length) {
                return 'missing sale order seed data';
            }

            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[so[0].id]],
                kwargs: {},
            });

            const actualPickings = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [[['origin', '=', so[0].name]], ['id', 'origin']],
                kwargs: { limit: 1 },
            });
            const targetPicking = actualPickings[0];
            if (!targetPicking) {
                return 'no delivery created';
            }

            await callKw({
                model: 'stock.picking',
                method: 'action_assign',
                args: [[targetPicking.id]],
                kwargs: {},
            });

            const moves = await callKw({
                model: 'stock.move',
                method: 'search_read',
                args: [[['picking_id', '=', targetPicking.id]], ['id', 'product_uom_qty']],
                kwargs: { limit: 20 },
            });
            for (const move of moves) {
                await callKw({
                    model: 'stock.move',
                    method: 'write',
                    args: [[move.id], { quantity: move.product_uom_qty }],
                    kwargs: {},
                });
            }

            await callKw({
                model: 'stock.picking',
                method: 'button_validate',
                args: [[targetPicking.id]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
