"""Oracle for mrp.bom_with_kit_component_confirm_mo.

Creates a Manufacturing Order via JSON-RPC for the pre-seeded
Bench Assembly product (qty 1) and calls action_confirm. On confirm the
phantom/kit Bench Kit BoM auto-expands, and move_raw_ids becomes 3 rows
(Bench Sub-A + Bench Sub-B + Bench Frame).

The browser-use agent must perform the same workflow via the MO form;
the oracle uses JSON-RPC for determinism (kit expansion and BoM
auto-selection on the form can be fragile in Playwright).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


MO_NAME = "M-BENCH-KIT-001"
ASSEMBLY_NAME = "Bench Assembly"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    result = page.evaluate(
        """async (payload) => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params,
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(
                        json.error.data?.message || json.error.message
                    );
                }
                return json.result;
            };

            // 1. Resolve the Bench Assembly product.product id.
            const products = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', payload.assemblyName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!products.length) {
                throw new Error('Bench Assembly product not found');
            }
            const productId = products[0].id;

            // 2. Resolve the normal BoM for Bench Assembly.
            const boms = await callKw({
                model: 'mrp.bom',
                method: 'search_read',
                args: [[['product_tmpl_id.name', '=', payload.assemblyName],
                        ['type', '=', 'normal']],
                       ['id']],
                kwargs: { limit: 1 },
            });
            if (!boms.length) {
                throw new Error('Bench Assembly normal BoM not found');
            }
            const bomId = boms[0].id;

            // 3. Create the draft MO.
            const moIds = await callKw({
                model: 'mrp.production',
                method: 'create',
                args: [[{
                    name: payload.moName,
                    product_id: productId,
                    product_qty: 1.0,
                    bom_id: bomId,
                }]],
                kwargs: {},
            });
            const moId = Array.isArray(moIds) ? moIds[0] : moIds;

            // 4. Confirm the MO so the phantom kit BoM auto-expands.
            await callKw({
                model: 'mrp.production',
                method: 'action_confirm',
                args: [[moId]],
                kwargs: {},
            });

            // 5. Read back the MO state + raw moves for sanity logging.
            const moData = await callKw({
                model: 'mrp.production',
                method: 'read',
                args: [[moId], ['name', 'state', 'product_qty', 'move_raw_ids']],
                kwargs: {},
            });
            const rawIds = moData[0].move_raw_ids || [];
            const rawData = rawIds.length
                ? await callKw({
                    model: 'stock.move',
                    method: 'read',
                    args: [rawIds, ['product_id', 'product_uom_qty']],
                    kwargs: {},
                })
                : [];
            return { mo: moData[0], raws: rawData };
        }""",
        {
            "assemblyName": ASSEMBLY_NAME,
            "moName": MO_NAME,
        },
    )

    mo = result["mo"]
    raws = result["raws"]
    if mo["state"] != "confirmed":
        raise RuntimeError(
            f"Oracle: MO state is {mo['state']!r}, expected 'confirmed'"
        )
    if len(raws) != 3:
        raw_names = [r["product_id"][1] for r in raws]
        raise RuntimeError(
            f"Oracle: expected 3 raw moves after kit expansion, "
            f"got {len(raws)} ({raw_names})"
        )
    raw_names = [r["product_id"][1] for r in raws]
    if any("Bench Kit" in n for n in raw_names):
        raise RuntimeError(
            f"Oracle: Bench Kit present in raw moves — phantom BoM did "
            f"not expand. Raw products: {raw_names}"
        )

    # Navigate the agent-visible page to the MO form so the end state
    # is a normal UI page (for screenshot / manual verification).
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
