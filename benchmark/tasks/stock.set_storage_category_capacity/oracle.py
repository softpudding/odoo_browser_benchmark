"""Oracle for stock.set_storage_category_capacity.

Logs in via Playwright, then drives the workflow via JSON-RPC call_kw:

1. Create the stock.storage.category 'Bench Small Bin' with max_weight=50
   and allow_new_product='same'.
2. Write storage_category_id on the seeded sub-location
   WH/Stock/Bench Small Bin Area.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


CATEGORY_NAME = "Bench Small Bin"
LOCATION_COMPLETE_NAME = "WH/Stock/Bench Small Bin Area"


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")

    response = page.evaluate(
        """async ([categoryName, locationComplete]) => {
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

            // Create the storage category.
            const catId = await callKw({
                model: 'stock.storage.category',
                method: 'create',
                args: [[{
                    name: categoryName,
                    max_weight: 50.0,
                    allow_new_product: 'same',
                }]],
                kwargs: {},
            });
            const categoryId = Array.isArray(catId) ? catId[0] : catId;

            // Look up the seeded sub-location.
            const locs = await callKw({
                model: 'stock.location',
                method: 'search_read',
                args: [[['complete_name', '=', locationComplete]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!locs.length) {
                throw new Error('target sub-location not found: ' + locationComplete);
            }
            const locId = locs[0].id;

            // Assign the storage category to the sub-location.
            await callKw({
                model: 'stock.location',
                method: 'write',
                args: [[locId], { storage_category_id: categoryId }],
                kwargs: {},
            });

            return 'ok';
        }""",
        [CATEGORY_NAME, LOCATION_COMPLETE_NAME],
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
