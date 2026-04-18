"""Oracle for mrp.scrap_component_during_production.

Uses JSON-RPC `call_kw` against the Odoo backend from an authenticated
browser context. Finds the MO and the raw-material move for
Bench Component A, creates a stock.scrap for 2 units linked to the MO
and that move, validates the scrap, then finishes the MO.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


MO_NAME = "M-BENCH-PROD-001"
COMP_A = "Bench Component A"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")

    result = page.evaluate(
        """async ({moName, compName}) => {
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

            // 1. Find the MO by name.
            const moRecs = await callKw({
                model: 'mrp.production',
                method: 'search_read',
                args: [
                    [['name', '=', moName]],
                    ['id', 'state', 'move_raw_ids', 'location_src_id', 'location_dest_id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!moRecs.length) throw new Error('MO ' + moName + ' not found');
            const mo = moRecs[0];

            // 2. Find the raw-material move for Bench Component A.
            const moves = await callKw({
                model: 'stock.move',
                method: 'search_read',
                args: [
                    [['id', 'in', mo.move_raw_ids]],
                    ['id', 'product_id', 'location_id'],
                ],
                kwargs: {},
            });
            const compMove = moves.find(
                (m) => m.product_id && m.product_id[1] === compName
            );
            if (!compMove) {
                throw new Error('Could not find raw move for ' + compName);
            }
            const productId = compMove.product_id[0];
            const sourceLocId = compMove.location_id ? compMove.location_id[0] : false;

            // 3. Create stock.scrap record for 2 units. Leave
            // scrap_location_id to the onchange default; just providing
            // product/production/source is enough for Odoo to populate
            // the scrap destination.
            const scrapVals = {
                product_id: productId,
                scrap_qty: 2.0,
                production_id: mo.id,
                location_id: sourceLocId,
            };
            const scrapId = await callKw({
                model: 'stock.scrap',
                method: 'create',
                args: [scrapVals],
                kwargs: {},
            });

            // 5. Validate the scrap so it moves to 'done'.
            await callKw({
                model: 'stock.scrap',
                method: 'action_validate',
                args: [[scrapId]],
                kwargs: {},
            });

            // 6. Finish the MO. The pre_button_mark_done call may return
            // an action dict (a warning wizard); if so we accept it by
            // executing the underlying server action with the proper
            // context. Otherwise call button_mark_done directly.
            let finishResult;
            try {
                finishResult = await callKw({
                    model: 'mrp.production',
                    method: 'button_mark_done',
                    args: [[mo.id]],
                    kwargs: {},
                });
            } catch (err) {
                finishResult = { error: err.message };
            }

            // If a confirmation wizard comes back (immediate production,
            // consumption warning, etc.), try to auto-process it.
            if (
                finishResult &&
                typeof finishResult === 'object' &&
                finishResult.res_model &&
                finishResult.res_id
            ) {
                const wizModel = finishResult.res_model;
                const wizId = finishResult.res_id;
                // Most of these wizards have a primary action method like
                // action_confirm / process / button_mark_done.
                for (const method of [
                    'process',
                    'action_confirm',
                    'action_validate',
                    'button_mark_done',
                    'confirm',
                ]) {
                    try {
                        await callKw({
                            model: wizModel,
                            method: method,
                            args: [[wizId]],
                            kwargs: {},
                        });
                        break;
                    } catch (_e) {
                        /* try next */
                    }
                }
            }

            // 7. Read back final state.
            const [finalMo] = await callKw({
                model: 'mrp.production',
                method: 'read',
                args: [[mo.id], ['state', 'qty_produced']],
                kwargs: {},
            });
            const [finalScrap] = await callKw({
                model: 'stock.scrap',
                method: 'read',
                args: [[scrapId], ['state', 'scrap_qty', 'product_id']],
                kwargs: {},
            });
            return { mo: finalMo, scrap: finalScrap };
        }""",
        {"moName": MO_NAME, "compName": COMP_A},
    )

    if not result:
        raise RuntimeError("Oracle: no result returned")
    mo = result.get("mo") or {}
    scrap = result.get("scrap") or {}
    if mo.get("state") != "done":
        raise RuntimeError(
            f"Oracle: MO state is {mo.get('state')!r}, expected 'done'"
        )
    if abs(float(mo.get("qty_produced") or 0.0) - 5.0) > 1e-6:
        raise RuntimeError(
            f"Oracle: MO qty_produced is {mo.get('qty_produced')}, expected 5.0"
        )
    if scrap.get("state") != "done":
        raise RuntimeError(
            f"Oracle: scrap state is {scrap.get('state')!r}, expected 'done'"
        )
    if abs(float(scrap.get("scrap_qty") or 0.0) - 2.0) > 1e-6:
        raise RuntimeError(
            f"Oracle: scrap quantity is {scrap.get('scrap_qty')}, expected 2.0"
        )
    prod = scrap.get("product_id")
    if not (prod and prod[1] == COMP_A):
        raise RuntimeError(
            f"Oracle: scrap product is {prod!r}, expected {COMP_A!r}"
        )


run_oracle(oracle)
