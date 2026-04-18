"""Oracle for mrp.create_mo_consume_produce_done.

Uses JSON-RPC `call_kw` against the Odoo backend from an authenticated
browser context. Creates a mrp.production for 3 units of Bench Assembly
from scratch, confirms it (which generates the raw-material moves from
the BoM), assigns reservations, sets qty_producing=3, and finally marks
it as done, transparently handling any consumption/backorder wizard
that pops up.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


FINISHED = "Bench Assembly"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")

    result = page.evaluate(
        """async ({finishedName}) => {
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

            // 1. Resolve the finished product.
            const prodRecs = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', finishedName]], ['id', 'product_tmpl_id']],
                kwargs: { limit: 1 },
            });
            if (!prodRecs.length) throw new Error('Product ' + finishedName + ' not found');
            const productId = prodRecs[0].id;
            const tmplId = prodRecs[0].product_tmpl_id[0];

            // 2. Resolve the BoM for that product template.
            const bomRecs = await callKw({
                model: 'mrp.bom',
                method: 'search_read',
                args: [[['product_tmpl_id', '=', tmplId]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!bomRecs.length) throw new Error('BoM for ' + finishedName + ' not found');
            const bomId = bomRecs[0].id;

            // 3. Create the MO. We omit 'name' so Odoo auto-assigns a
            //    reference; the task description does not pin a name.
            const moId = await callKw({
                model: 'mrp.production',
                method: 'create',
                args: [{
                    product_id: productId,
                    product_qty: 3.0,
                    bom_id: bomId,
                }],
                kwargs: {},
            });

            // 4. Confirm it so raw-material moves are populated.
            await callKw({
                model: 'mrp.production',
                method: 'action_confirm',
                args: [[moId]],
                kwargs: {},
            });

            // 5. Try to reserve components (not strictly required).
            try {
                await callKw({
                    model: 'mrp.production',
                    method: 'action_assign',
                    args: [[moId]],
                    kwargs: {},
                });
            } catch (_e) {
                try {
                    await callKw({
                        model: 'mrp.production',
                        method: '_action_assign',
                        args: [[moId]],
                        kwargs: {},
                    });
                } catch (_e2) { /* ignore */ }
            }

            // 6. Set qty_producing=3 so Mark as Done produces the full qty.
            await callKw({
                model: 'mrp.production',
                method: 'write',
                args: [[moId], { qty_producing: 3.0 }],
                kwargs: {},
            });
            // Calling set_qty_producing() cascades qty_producing down to
            // the raw-material moves (populates move.quantity so the
            // moves actually consume the right amount on Mark as Done).
            try {
                await callKw({
                    model: 'mrp.production',
                    method: 'set_qty_producing',
                    args: [[moId]],
                    kwargs: {},
                });
            } catch (_e) { /* ignore */ }

            // 7. Finish the MO. pre_button_mark_done may return a
            //    wizard dict (consumption warning or backorder). Try
            //    button_mark_done first; if it returns a wizard action,
            //    execute the wizard's primary method.
            let finishResult;
            try {
                finishResult = await callKw({
                    model: 'mrp.production',
                    method: 'button_mark_done',
                    args: [[moId]],
                    kwargs: {},
                });
            } catch (err) {
                finishResult = { error: err.message };
            }

            if (
                finishResult &&
                typeof finishResult === 'object' &&
                finishResult.res_model &&
                finishResult.res_id
            ) {
                const wizModel = finishResult.res_model;
                const wizId = finishResult.res_id;
                for (const method of [
                    'process',
                    'action_confirm',
                    'action_validate',
                    'button_mark_done',
                    'confirm',
                    'action_done',
                ]) {
                    try {
                        await callKw({
                            model: wizModel,
                            method: method,
                            args: [[wizId]],
                            kwargs: {},
                        });
                        break;
                    } catch (_e) { /* try next */ }
                }
            }

            // 8. Read back final state.
            const [finalMo] = await callKw({
                model: 'mrp.production',
                method: 'read',
                args: [[moId], ['state', 'qty_produced', 'product_qty', 'name']],
                kwargs: {},
            });
            return { mo: finalMo };
        }""",
        {"finishedName": FINISHED},
    )

    if not result:
        raise RuntimeError("Oracle: no result returned")
    mo = result.get("mo") or {}
    if mo.get("state") != "done":
        raise RuntimeError(
            f"Oracle: MO state is {mo.get('state')!r}, expected 'done'"
        )
    if abs(float(mo.get("qty_produced") or 0.0) - 3.0) > 1e-6:
        raise RuntimeError(
            f"Oracle: MO qty_produced is {mo.get('qty_produced')}, expected 3.0"
        )
    if abs(float(mo.get("product_qty") or 0.0) - 3.0) > 1e-6:
        raise RuntimeError(
            f"Oracle: MO product_qty is {mo.get('product_qty')}, expected 3.0"
        )


run_oracle(oracle)
