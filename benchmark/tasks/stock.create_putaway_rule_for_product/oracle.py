"""Oracle for stock.create_putaway_rule_for_product.

Logs in via Playwright, then drives the workflow via JSON-RPC call_kw:

1. Resolve the WH/Stock parent location and the seeded
   WH/Stock/Bench Shelf A sub-location.
2. Resolve the 'Bench Putaway Product' product.
3. Create a stock.putaway.rule with
   location_in_id=WH/Stock, product_id=<product>,
   location_out_id=WH/Stock/Bench Shelf A.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PRODUCT_NAME = "Bench Putaway Product"
LOCATION_IN_COMPLETE = "WH/Stock"
LOCATION_OUT_COMPLETE = "WH/Stock/Bench Shelf A"


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")

    response = page.evaluate(
        """async ([productName, locInComplete, locOutComplete]) => {
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

            const locIn = await callKw({
                model: 'stock.location',
                method: 'search_read',
                args: [[['complete_name', '=', locInComplete]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!locIn.length) {
                throw new Error('Parent location not found: ' + locInComplete);
            }

            const locOut = await callKw({
                model: 'stock.location',
                method: 'search_read',
                args: [[['complete_name', '=', locOutComplete]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!locOut.length) {
                throw new Error('Sub-location not found: ' + locOutComplete);
            }

            const prods = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', productName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!prods.length) {
                throw new Error('Product not found: ' + productName);
            }

            // Defensive: drop any pre-existing putaway rule for this product.
            const existing = await callKw({
                model: 'stock.putaway.rule',
                method: 'search',
                args: [[['product_id', '=', prods[0].id]]],
                kwargs: {},
            });
            if (existing.length) {
                await callKw({
                    model: 'stock.putaway.rule',
                    method: 'unlink',
                    args: [existing],
                    kwargs: {},
                });
            }

            const ruleId = await callKw({
                model: 'stock.putaway.rule',
                method: 'create',
                args: [[{
                    location_in_id: locIn[0].id,
                    product_id: prods[0].id,
                    location_out_id: locOut[0].id,
                }]],
                kwargs: {},
            });

            return Array.isArray(ruleId) ? ruleId[0] : ruleId;
        }""",
        [PRODUCT_NAME, LOCATION_IN_COMPLETE, LOCATION_OUT_COMPLETE],
    )
    if not response:
        raise RuntimeError("Oracle failed to create the putaway rule")


run_oracle(oracle)
