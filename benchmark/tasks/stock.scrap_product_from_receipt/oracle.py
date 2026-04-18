"""Oracle for stock.scrap_product_from_receipt.

JSON-RPC oracle: locate the seeded receipt BENCH-RCV-SCRAP-01 and the
Bench Scrap Product, create a stock.scrap linked to that picking with
scrap_qty=2, and call action_validate so the scrap ends in 'done' state.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PRODUCT_NAME = "Bench Scrap Product"
RECEIPT_REF = "BENCH-RCV-SCRAP-01"


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")

    response = page.evaluate(
        """async ([productName, receiptRef]) => {
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

            const pickings = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [
                    [['origin', '=', receiptRef], ['state', '=', 'done']],
                    ['id', 'location_dest_id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!pickings.length) throw new Error('Receipt missing');
            const pickingId = pickings[0].id;
            // Destination of the done incoming picking is WH/Stock
            const destLocId = Array.isArray(pickings[0].location_dest_id)
                ? pickings[0].location_dest_id[0]
                : pickings[0].location_dest_id;

            // Create the scrap record. Leaving location_id and
            // scrap_location_id to the server defaults will pick
            // WH/Stock and Virtual Locations/Scrap (ok because the
            // picking is done). But we set them explicitly for safety.
            const scrapVals = {
                product_id: productId,
                product_uom_id: uomId,
                scrap_qty: 2,
                picking_id: pickingId,
                location_id: destLocId,
            };

            const scrapId = await callKw({
                model: 'stock.scrap',
                method: 'create',
                args: [[scrapVals]],
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
        [PRODUCT_NAME, RECEIPT_REF],
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
