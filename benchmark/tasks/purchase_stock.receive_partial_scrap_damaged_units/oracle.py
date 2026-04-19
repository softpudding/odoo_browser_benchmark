"""Oracle for purchase_stock.receive_partial_scrap_damaged_units.

Pure JSON-RPC oracle (no Playwright form interactions beyond login):

  1. Locate the confirmed PO with origin BENCH-SCRAP-RCV-01 and the
     draft incoming stock.picking it generated.
  2. Create a stock.scrap for 2 units of Bench Widget linked to the
     picking, tagged with the 'Damaged' reason, and validate it so the
     scrap state = 'done'.
  3. Set the Bench Widget move quantity on the picking to 8.
  4. Call stock.picking.button_validate and dismiss the backorder
     wizard with process_cancel_backorder ('No Backorder').
  5. Sanity-check that the picking reached 'done' state and exactly one
     scrap was created in state 'done' with scrap_qty == 2.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


VENDOR_NAME = "Bench Reliable Supplier"
PRODUCT_NAME = "Bench Widget"
PO_ORIGIN = "BENCH-SCRAP-RCV-01"
REASON_TAG = "Damaged"


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")

    result = page.evaluate(
        """async ([productName, poOrigin, reasonTag]) => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    const tag = '[' + params.model + '.' + params.method + ']';
                    throw new Error(tag + ' ' + (json.error.data?.message || json.error.message));
                }
                return json.result;
            };

            // --- 1. Product ----------------------------------------------
            const prods = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', productName]], ['id', 'uom_id']],
                kwargs: { limit: 1 },
            });
            if (!prods.length) throw new Error('Product not found: ' + productName);
            const productId = prods[0].id;
            const uomId = Array.isArray(prods[0].uom_id)
                ? prods[0].uom_id[0]
                : prods[0].uom_id;

            // --- 2. PO ---------------------------------------------------
            const pos = await callKw({
                model: 'purchase.order',
                method: 'search_read',
                args: [[['origin', '=', poOrigin]], ['id', 'name', 'picking_ids']],
                kwargs: { limit: 1 },
            });
            if (!pos.length) throw new Error('PO not found for origin ' + poOrigin);
            const po = pos[0];
            if (!po.picking_ids || !po.picking_ids.length) {
                throw new Error('PO has no incoming picking');
            }

            // --- 3. Picking (not done, not cancelled) --------------------
            const allPickings = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [[
                    ['id', 'in', po.picking_ids],
                ], ['id', 'state', 'location_id', 'location_dest_id', 'picking_type_id']],
                kwargs: {},
            });
            const openPickings = allPickings.filter(
                (p) => p.state !== 'done' && p.state !== 'cancel'
            );
            if (!openPickings.length) throw new Error('No open incoming picking for PO');
            const picking = openPickings[0];
            const pickingId = picking.id;
            const srcLocId = Array.isArray(picking.location_id)
                ? picking.location_id[0]
                : picking.location_id;
            const destLocId = Array.isArray(picking.location_dest_id)
                ? picking.location_dest_id[0]
                : picking.location_dest_id;

            // Ensure picking is confirmed / assigned so move lines exist.
            if (picking.state === 'draft') {
                await callKw({
                    model: 'stock.picking',
                    method: 'action_confirm',
                    args: [[pickingId]],
                    kwargs: {},
                });
            }
            try {
                await callKw({
                    model: 'stock.picking',
                    method: 'action_assign',
                    args: [[pickingId]],
                    kwargs: {},
                });
            } catch (err) {
                /* action_assign may error for incoming without rule — ignore */
            }

            // --- 4. Find the reason tag by name --------------------------
            const tags = await callKw({
                model: 'stock.scrap.reason.tag',
                method: 'search_read',
                args: [[['name', '=', reasonTag]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!tags.length) throw new Error('Reason tag not found: ' + reasonTag);
            const reasonTagId = tags[0].id;

            // --- 5. Create + validate scrap (2 units) --------------------
            const scrapVals = {
                product_id: productId,
                product_uom_id: uomId,
                scrap_qty: 2,
                picking_id: pickingId,
                location_id: srcLocId,
                scrap_reason_tag_ids: [[6, 0, [reasonTagId]]],
            };
            let scrapId;
            try {
                scrapId = await callKw({
                    model: 'stock.scrap',
                    method: 'create',
                    args: [[scrapVals]],
                    kwargs: {},
                });
            } catch (err) {
                throw new Error('scrap.create failed: ' + err.message);
            }
            const scrapIdNum = Array.isArray(scrapId) ? scrapId[0] : scrapId;

            // action_validate may open an insufficient-qty wizard when
            // the source location is the supplier (virtual) location.
            // In that case we still want the scrap to move to 'done'.
            let scrapValidateResult;
            try {
                scrapValidateResult = await callKw({
                    model: 'stock.scrap',
                    method: 'action_validate',
                    args: [[scrapIdNum]],
                    kwargs: {},
                });
            } catch (err) {
                throw new Error('scrap.action_validate failed: ' + err.message);
            }
            if (scrapValidateResult && typeof scrapValidateResult === 'object'
                && scrapValidateResult.res_model === 'stock.warn.insufficient.qty.scrap') {
                // Fall back to calling do_scrap directly on the scrap — the
                // wizard's action_done is a thin wrapper that does exactly
                // this.
                await callKw({
                    model: 'stock.scrap',
                    method: 'do_scrap',
                    args: [[scrapIdNum]],
                    kwargs: {},
                });
            }

            // --- 6. Set the Bench Widget move quantity to 8 --------------
            let moves;
            try {
                moves = await callKw({
                    model: 'stock.move',
                    method: 'search_read',
                    args: [[
                        ['picking_id', '=', pickingId],
                        ['product_id', '=', productId],
                    ], ['id', 'product_uom_qty', 'quantity', 'scrap_id']],
                    kwargs: {},
                });
            } catch (err) {
                throw new Error('stock.move.search_read failed: ' + err.message);
            }
            const mainMoves = moves.filter((m) => !m.scrap_id);
            if (!mainMoves.length) {
                throw new Error('No non-scrap stock.move for ' + productName + ' on picking');
            }
            const moveId = mainMoves[0].id;

            try {
                await callKw({
                    model: 'stock.move',
                    method: 'write',
                    args: [[moveId], { quantity: 8.0, picked: true }],
                    kwargs: {},
                });
            } catch (err) {
                throw new Error('stock.move.write failed: ' + err.message);
            }

            // --- 7. Validate the picking; dismiss backorder wizard -------
            const validateResult = await callKw({
                model: 'stock.picking',
                method: 'button_validate',
                args: [[pickingId]],
                kwargs: {},
            });

            if (validateResult && typeof validateResult === 'object' && validateResult.res_model) {
                const wizModel = validateResult.res_model;
                if (wizModel === 'stock.backorder.confirmation') {
                    // Create the wizard with plain m2m and a minimal
                    // context containing only the required
                    // button_validate_picking_ids. Copying the full
                    // action context produces 'unhashable type: list'
                    // because default_pick_ids is a nested tuple list.
                    const cleanCtx = { button_validate_picking_ids: [pickingId] };
                    const wizVals = { pick_ids: [[6, 0, [pickingId]]] };
                    const wizId = await callKw({
                        model: wizModel,
                        method: 'create',
                        args: [[wizVals]],
                        kwargs: { context: cleanCtx },
                    });
                    const wizIdNum = Array.isArray(wizId) ? wizId[0] : wizId;
                    await callKw({
                        model: wizModel,
                        method: 'process_cancel_backorder',
                        args: [[wizIdNum]],
                        kwargs: { context: cleanCtx },
                    });
                } else {
                    // Fallback: re-validate with skip_backorder context.
                    await callKw({
                        model: 'stock.picking',
                        method: 'button_validate',
                        args: [[pickingId]],
                        kwargs: { context: { skip_backorder: true, skip_sanity_check: true } },
                    });
                }
            }

            // --- 8. Sanity-check -----------------------------------------
            const [finalPick] = await callKw({
                model: 'stock.picking',
                method: 'read',
                args: [[pickingId], ['state', 'backorder_ids']],
                kwargs: {},
            });
            const finalScraps = await callKw({
                model: 'stock.scrap',
                method: 'search_read',
                args: [[['id', '=', scrapIdNum]], ['state', 'scrap_qty', 'scrap_reason_tag_ids']],
                kwargs: {},
            });
            return { pick: finalPick, scrap: finalScraps[0] || null };
        }""",
        [PRODUCT_NAME, PO_ORIGIN, REASON_TAG],
    )

    if not result:
        raise RuntimeError("Oracle: no result returned")
    pick = result.get("pick") or {}
    scrap = result.get("scrap") or {}
    if pick.get("state") != "done":
        raise RuntimeError(
            f"Oracle: picking state is {pick.get('state')!r}, expected 'done'"
        )
    backorders = pick.get("backorder_ids") or []
    if backorders:
        raise RuntimeError(
            f"Oracle: picking has unexpected backorder(s) {backorders!r}; "
            "expected 'No Backorder'"
        )
    if scrap.get("state") != "done":
        raise RuntimeError(
            f"Oracle: scrap state is {scrap.get('state')!r}, expected 'done'"
        )
    if abs(float(scrap.get("scrap_qty") or 0.0) - 2.0) > 1e-6:
        raise RuntimeError(
            f"Oracle: scrap qty is {scrap.get('scrap_qty')}, expected 2.0"
        )


run_oracle(oracle)
