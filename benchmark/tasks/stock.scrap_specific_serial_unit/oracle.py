"""Oracle for stock.scrap_specific_serial_unit.

JSON-RPC: locate the seeded product + the SN-A002 lot + WH/Stock location,
create a stock.scrap with quantity 1, and validate it.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PRODUCT_NAME = "Bench Sensor Module"
TARGET_SERIAL = "SN-A002"
REASON_TEXT = "Manufacturer recall - middle batch only"


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")

    response = page.evaluate(
        """async ([productName, targetSerial, reason]) => {
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

            const products = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', productName]], ['id', 'uom_id']],
                kwargs: { limit: 1 },
            });
            if (!products.length) throw new Error('Product missing');
            const productId = products[0].id;
            const uomId = Array.isArray(products[0].uom_id)
                ? products[0].uom_id[0]
                : products[0].uom_id;

            const lots = await callKw({
                model: 'stock.lot',
                method: 'search_read',
                args: [
                    [['name', '=', targetSerial], ['product_id', '=', productId]],
                    ['id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!lots.length) throw new Error('Target lot missing');
            const lotId = lots[0].id;

            const stockLocs = await callKw({
                model: 'stock.location',
                method: 'search_read',
                args: [
                    [['usage', '=', 'internal'], ['name', '=', 'Stock']],
                    ['id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!stockLocs.length) throw new Error('Stock location missing');
            const stockLocId = stockLocs[0].id;

            const scrapId = await callKw({
                model: 'stock.scrap',
                method: 'create',
                args: [[{
                    product_id: productId,
                    lot_id: lotId,
                    product_uom_id: uomId,
                    scrap_qty: 1,
                    location_id: stockLocId,
                    origin: reason,
                }]],
                kwargs: {},
            });

            await callKw({
                model: 'stock.scrap',
                method: 'action_validate',
                args: [[Array.isArray(scrapId) ? scrapId[0] : scrapId]],
                kwargs: {},
            });

            return 'ok';
        }""",
        [PRODUCT_NAME, TARGET_SERIAL, REASON_TEXT],
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
