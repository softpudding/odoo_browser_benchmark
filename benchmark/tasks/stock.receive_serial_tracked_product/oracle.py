"""Oracle for stock.receive_serial_tracked_product.

Logs in via Playwright, then drives the full serial-receipt workflow
via JSON-RPC call_kw (no Odoo imports):

1. Locate the draft incoming picking with origin BENCH-SN-RCV-01 and
   the serial-tracked product 'Bench Serial Gadget'.
2. Confirm + assign the picking so move_lines are created.
3. Replace the existing move_lines with three fresh lines of
   quantity 1, each linked to a newly-created stock.lot named
   SN-BENCH-001 / SN-BENCH-002 / SN-BENCH-003 (via the Vendors ->
   WH/Stock move).
4. Call stock.picking.button_validate and dismiss any backorder
   confirmation wizard by applying 'No Backorder'.
5. Sanity-check that the picking ended in state='done'.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PRODUCT_NAME = "Bench Serial Gadget"
RECEIPT_ORIGIN = "BENCH-SN-RCV-01"
SERIAL_NAMES = ("SN-BENCH-001", "SN-BENCH-002", "SN-BENCH-003")


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")

    result = page.evaluate(
        """async ([productName, receiptOrigin, serialNames]) => {
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

            // --- 1. Locate the draft picking & product ------------------
            const prods = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', productName]], ['id', 'uom_id', 'tracking']],
                kwargs: { limit: 1 },
            });
            if (!prods.length) {
                throw new Error('Product not found: ' + productName);
            }
            const product = prods[0];

            const pickings = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [[['origin', '=', receiptOrigin]], ['id', 'state', 'location_id', 'location_dest_id', 'picking_type_id']],
                kwargs: { limit: 1 },
            });
            if (!pickings.length) {
                throw new Error('Receipt not found: ' + receiptOrigin);
            }
            const picking = pickings[0];
            const pickingId = picking.id;

            // --- 2. Confirm + assign if still draft ---------------------
            if (['draft'].includes(picking.state)) {
                await callKw({
                    model: 'stock.picking',
                    method: 'action_confirm',
                    args: [[pickingId]],
                    kwargs: {},
                });
            }
            // Reserve / assign move lines (harmless if already assigned).
            try {
                await callKw({
                    model: 'stock.picking',
                    method: 'action_assign',
                    args: [[pickingId]],
                    kwargs: {},
                });
            } catch (e) {
                // action_assign may raise for supplier->stock with no rule; ignore.
            }

            // --- 3. Fetch the move + drop any existing move_lines -------
            const moves = await callKw({
                model: 'stock.move',
                method: 'search_read',
                args: [[
                    ['picking_id', '=', pickingId],
                    ['product_id', '=', product.id],
                ], ['id', 'product_uom_qty', 'location_id', 'location_dest_id']],
                kwargs: { limit: 1 },
            });
            if (!moves.length) {
                throw new Error('No stock.move found on the receipt for ' + productName);
            }
            const move = moves[0];

            const existingMls = await callKw({
                model: 'stock.move.line',
                method: 'search',
                args: [[['move_id', '=', move.id]]],
                kwargs: {},
            });
            if (existingMls.length) {
                await callKw({
                    model: 'stock.move.line',
                    method: 'unlink',
                    args: [existingMls],
                    kwargs: {},
                });
            }

            // --- 4. Create the three serial lots on the fly ------------
            const lotIds = [];
            for (const sn of serialNames) {
                // Drop any leftover lot with the same name (defensive — the
                // seed already cleans these up, but do it again if a
                // previous oracle run was aborted mid-flight).
                const stale = await callKw({
                    model: 'stock.lot',
                    method: 'search',
                    args: [[
                        ['name', '=', sn],
                        ['product_id', '=', product.id],
                    ]],
                    kwargs: {},
                });
                if (stale.length) {
                    await callKw({
                        model: 'stock.lot',
                        method: 'unlink',
                        args: [stale],
                        kwargs: {},
                    });
                }
                const newLotId = await callKw({
                    model: 'stock.lot',
                    method: 'create',
                    args: [[{
                        name: sn,
                        product_id: product.id,
                    }]],
                    kwargs: {},
                });
                lotIds.push(Array.isArray(newLotId) ? newLotId[0] : newLotId);
            }

            // --- 5. Create three move_lines, qty 1 each, with lot_id ----
            const mlValues = lotIds.map((lotId) => ({
                move_id: move.id,
                picking_id: pickingId,
                product_id: product.id,
                product_uom_id: product.uom_id[0],
                location_id: move.location_id[0],
                location_dest_id: move.location_dest_id[0],
                quantity: 1.0,
                lot_id: lotId,
            }));
            await callKw({
                model: 'stock.move.line',
                method: 'create',
                args: [mlValues],
                kwargs: {},
            });

            // --- 6. Validate the picking --------------------------------
            const validateResult = await callKw({
                model: 'stock.picking',
                method: 'button_validate',
                args: [[pickingId]],
                kwargs: {},
            });

            // If a backorder wizard opens, close it by applying "No Backorder".
            if (validateResult && typeof validateResult === 'object' && validateResult.res_model) {
                const ctx = validateResult.context || {};
                const wizModel = validateResult.res_model;
                // The usual wizard is stock.backorder.confirmation with
                // action process_cancel_backorder (= No Backorder).
                try {
                    const wizId = await callKw({
                        model: wizModel,
                        method: 'create',
                        args: [[Object.assign({}, ctx.default_pick_ids
                            ? { pick_ids: [[6, 0, ctx.default_pick_ids]] }
                            : {})]],
                        kwargs: { context: ctx },
                    });
                    const wizIdNum = Array.isArray(wizId) ? wizId[0] : wizId;
                    if (wizModel === 'stock.backorder.confirmation') {
                        await callKw({
                            model: wizModel,
                            method: 'process_cancel_backorder',
                            args: [[wizIdNum]],
                            kwargs: { context: ctx },
                        });
                    } else {
                        // Generic: try 'process' (immediate transfer, etc.)
                        try {
                            await callKw({
                                model: wizModel,
                                method: 'process',
                                args: [[wizIdNum]],
                                kwargs: { context: ctx },
                            });
                        } catch (err) {
                            // Fallback: try button_validate again.
                            await callKw({
                                model: 'stock.picking',
                                method: 'button_validate',
                                args: [[pickingId]],
                                kwargs: { context: { skip_backorder: true, skip_sanity_check: true } },
                            });
                        }
                    }
                } catch (err) {
                    // Fallback path: re-call button_validate with skip_backorder.
                    await callKw({
                        model: 'stock.picking',
                        method: 'button_validate',
                        args: [[pickingId]],
                        kwargs: { context: { skip_backorder: true, skip_sanity_check: true } },
                    });
                }
            }

            // --- 7. Sanity-check final state ----------------------------
            const final = await callKw({
                model: 'stock.picking',
                method: 'read',
                args: [[pickingId], ['state']],
                kwargs: {},
            });
            if (!final.length || final[0].state !== 'done') {
                throw new Error('Picking did not reach done state: ' + JSON.stringify(final));
            }

            return 'ok';
        }""",
        [PRODUCT_NAME, RECEIPT_ORIGIN, list(SERIAL_NAMES)],
    )
    if result != "ok":
        raise RuntimeError(f"Oracle reported unexpected result: {result!r}")


run_oracle(oracle)
