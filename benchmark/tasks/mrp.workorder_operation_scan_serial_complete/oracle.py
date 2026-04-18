"""Oracle for mrp.workorder_operation_scan_serial_complete.

Drives the MO-BENCH-WO work order through its full lifecycle via
JSON-RPC, overriding the default-reserved serial (SN-A) with SN-B
before finishing the work order. The browser-use agent must achieve
the same end state through the MO / work-order UI — but because the
Shop Floor tablet UI and the Detailed Operations popup are fragile
under Playwright, the oracle uses call_kw for determinism.

Sequence:
  1. search_read MO-BENCH-WO + its workorder_ids + component raw move.
  2. button_start on the workorder (state: ready -> progress).
  3. Rewrite move_line_ids on the Bench Serial Part raw move so the
     only move line has lot_id = SN-B (delete any line pointing at
     another serial; create/update one pointing at SN-B).
  4. button_finish on the workorder (state: progress -> done). This
     also picks the raw moves (which by then correctly reference SN-B).
  5. button_mark_done on the MO (state: progress -> done).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


MO_NAME = "MO-BENCH-WO"
COMPONENT_NAME = "Bench Serial Part"
REQUIRED_SERIAL = "SN-B"


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

            // 1. Find the MO.
            const moRows = await callKw({
                model: 'mrp.production',
                method: 'search_read',
                args: [[['name', '=', payload.moName]],
                       ['id', 'workorder_ids', 'move_raw_ids']],
                kwargs: { limit: 1 },
            });
            if (!moRows.length) throw new Error('MO not found: ' + payload.moName);
            const moId = moRows[0].id;
            const woIds = moRows[0].workorder_ids || [];
            const rawIds = moRows[0].move_raw_ids || [];
            if (woIds.length !== 1) {
                throw new Error('Expected exactly 1 workorder, got ' + woIds.length);
            }
            const woId = woIds[0];

            // 2. Resolve the SN-B lot id.
            const lots = await callKw({
                model: 'stock.lot',
                method: 'search_read',
                args: [[['name', '=', payload.serialName],
                        ['product_id.name', '=', payload.componentName]],
                       ['id']],
                kwargs: { limit: 1 },
            });
            if (!lots.length) throw new Error('Serial not found: ' + payload.serialName);
            const snBId = lots[0].id;

            // 3. Find the component raw move.
            const rawMoves = await callKw({
                model: 'stock.move',
                method: 'search_read',
                args: [[['id', 'in', rawIds],
                        ['product_id.name', '=', payload.componentName]],
                       ['id', 'move_line_ids', 'product_uom_qty']],
                kwargs: {},
            });
            if (!rawMoves.length) {
                throw new Error('Component raw move not found for ' + payload.componentName);
            }
            const compMove = rawMoves[0];

            // 4. button_start on the workorder (ready -> progress).
            await callKw({
                model: 'mrp.workorder',
                method: 'button_start',
                args: [[woId]],
                kwargs: {},
            });

            // 5. Rewrite move_line_ids: delete all existing lines, create a
            // single one with lot_id = SN-B and quantity = 1.
            if (compMove.move_line_ids && compMove.move_line_ids.length) {
                await callKw({
                    model: 'stock.move.line',
                    method: 'unlink',
                    args: [compMove.move_line_ids],
                    kwargs: {},
                });
            }
            // Fetch the move's location fields for the new line.
            const moveDetails = await callKw({
                model: 'stock.move',
                method: 'read',
                args: [[compMove.id],
                       ['product_id', 'product_uom', 'location_id',
                        'location_dest_id', 'company_id']],
                kwargs: {},
            });
            const md = moveDetails[0];
            await callKw({
                model: 'stock.move.line',
                method: 'create',
                args: [[{
                    move_id: compMove.id,
                    product_id: md.product_id[0],
                    product_uom_id: md.product_uom[0],
                    location_id: md.location_id[0],
                    location_dest_id: md.location_dest_id[0],
                    company_id: md.company_id[0],
                    lot_id: snBId,
                    quantity: 1.0,
                }]],
                kwargs: {},
            });

            // Mark the move as already picked so button_finish does not
            // overwrite our choice via _set_quantity_done.
            await callKw({
                model: 'stock.move',
                method: 'write',
                args: [[compMove.id], { picked: true }],
                kwargs: {},
            });

            // 6. button_finish on the workorder.
            await callKw({
                model: 'mrp.workorder',
                method: 'button_finish',
                args: [[woId]],
                kwargs: {},
            });

            // 7. button_mark_done on the MO.
            await callKw({
                model: 'mrp.production',
                method: 'button_mark_done',
                args: [[moId]],
                kwargs: {},
            });

            // 8. Read back final state for sanity.
            const moFinal = await callKw({
                model: 'mrp.production',
                method: 'read',
                args: [[moId], ['state', 'qty_produced']],
                kwargs: {},
            });
            const woFinal = await callKw({
                model: 'mrp.workorder',
                method: 'read',
                args: [[woId], ['state']],
                kwargs: {},
            });
            const finalMls = await callKw({
                model: 'stock.move.line',
                method: 'search_read',
                args: [[['move_id', '=', compMove.id]],
                       ['id', 'lot_id', 'quantity', 'picked']],
                kwargs: {},
            });
            return {
                mo: moFinal[0],
                wo: woFinal[0],
                mls: finalMls,
            };
        }""",
        {
            "moName": MO_NAME,
            "componentName": COMPONENT_NAME,
            "serialName": REQUIRED_SERIAL,
        },
    )

    mo = result["mo"]
    wo = result["wo"]
    mls = result["mls"]

    if mo["state"] != "done":
        raise RuntimeError(
            f"Oracle: MO state is {mo['state']!r}, expected 'done'"
        )
    if wo["state"] != "done":
        raise RuntimeError(
            f"Oracle: WO state is {wo['state']!r}, expected 'done'"
        )
    consumed = [(ml["lot_id"][1] if ml["lot_id"] else None,
                 ml["quantity"], ml["picked"]) for ml in mls]
    consumed_names = [c[0] for c in consumed if c[2] and c[1] > 0]
    if consumed_names != [REQUIRED_SERIAL]:
        raise RuntimeError(
            f"Oracle: expected consumed=[{REQUIRED_SERIAL!r}], got "
            f"{consumed_names} (all mls: {consumed})"
        )

    # Navigate the visible page back to the MO list so the end state
    # is a normal page (for screenshot).
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(600)


run_oracle(oracle)
