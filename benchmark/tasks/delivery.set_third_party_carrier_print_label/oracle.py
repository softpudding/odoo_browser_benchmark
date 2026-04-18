"""Oracle for delivery.set_third_party_carrier_print_label.

Uses JSON-RPC call_kw to deterministically configure the carrier, apply
it to the picking, set the tracking reference, and validate the picking.
The browser-use agent must still solve via the UI.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/delivery-methods")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
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

            // 1. Create the shipping service product.
            const serviceProductId = unwrapId(await callKw({
                model: 'product.product',
                method: 'create',
                args: [[{
                    name: 'Bench Express Shipping',
                    type: 'service',
                    sale_ok: false,
                    purchase_ok: false,
                    list_price: 12.0,
                    invoice_policy: 'order',
                }]],
                kwargs: {},
            }));

            // 2. Create the fixed-price delivery carrier.
            const carrierId = unwrapId(await callKw({
                model: 'delivery.carrier',
                method: 'create',
                args: [[{
                    name: 'Bench Express',
                    delivery_type: 'fixed',
                    product_id: serviceProductId,
                    fixed_price: 12.0,
                }]],
                kwargs: {},
            }));

            // 3. Locate the outgoing delivery for S-BENCH-DLV-002.
            const orderRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'S-BENCH-DLV-002']], ['id', 'picking_ids']],
                kwargs: { limit: 1 },
            });
            if (!orderRes.length) {
                throw new Error('missing sale order');
            }
            const orderId = orderRes[0].id;
            const pickings = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [[['sale_id', '=', orderId], ['picking_type_code', '=', 'outgoing']], ['id', 'state', 'move_ids']],
                kwargs: { limit: 1 },
            });
            if (!pickings.length) {
                throw new Error('missing outgoing picking');
            }
            const pickingId = pickings[0].id;

            // 4. Apply carrier and tracking ref to the picking.
            await callKw({
                model: 'stock.picking',
                method: 'write',
                args: [[pickingId], {
                    carrier_id: carrierId,
                    carrier_tracking_ref: 'BX-TRACK-002',
                }],
                kwargs: {},
            });

            // 5. Push reserved quantities into the move `quantity` and mark
            //    them picked so button_validate doesn't open the
            //    not-enough-qty / nothing-to-transfer wizard.
            const moves = await callKw({
                model: 'stock.move',
                method: 'search_read',
                args: [[['picking_id', '=', pickingId]], ['id', 'product_uom_qty', 'quantity']],
                kwargs: {},
            });
            for (const m of moves) {
                await callKw({
                    model: 'stock.move',
                    method: 'write',
                    args: [[m.id], { quantity: m.product_uom_qty, picked: true }],
                    kwargs: {},
                });
            }

            // 6. Validate the picking. Use skip_backorder so we don't get a
            //    wizard. Quantities are already at full reserved so no
            //    backorder is needed anyway.
            await callKw({
                model: 'stock.picking',
                method: 'with_context',
                args: [[pickingId]],
                kwargs: {},
            }).catch(() => {});
            const validateRes = await callKw({
                model: 'stock.picking',
                method: 'button_validate',
                args: [[pickingId]],
                kwargs: { context: { skip_backorder: true } },
            });
            // If button_validate still returns a wizard action, accept defaults.
            if (validateRes && typeof validateRes === 'object' && validateRes.res_model) {
                const wizardCtx = Object.assign({}, validateRes.context || {}, {
                    active_id: pickingId,
                    active_ids: [pickingId],
                    active_model: 'stock.picking',
                });
                const wizardId = unwrapId(await callKw({
                    model: validateRes.res_model,
                    method: 'create',
                    args: [[{}]],
                    kwargs: { context: wizardCtx },
                }));
                await callKw({
                    model: validateRes.res_model,
                    method: 'process',
                    args: [[wizardId]],
                    kwargs: {},
                }).catch(() => {});
            }

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
