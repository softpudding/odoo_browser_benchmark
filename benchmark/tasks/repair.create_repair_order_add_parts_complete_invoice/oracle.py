"""Oracle for repair.create_repair_order_add_parts_complete_invoice."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/repairs")
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

            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Repair Harbor']], ['id']],
                kwargs: { limit: 1 },
            });
            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench Pump Core']], ['id']],
                kwargs: { limit: 1 },
            });
            const partRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench Repair Seal']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!partnerRes.length || !productRes.length || !partRes.length) {
                throw new Error('missing repair setup');
            }

            const repairId = unwrapId(await callKw({
                model: 'repair.order',
                method: 'create',
                args: [[{
                    name: 'RO/BENCH/0001',
                    partner_id: partnerRes[0].id,
                    product_id: productRes[0].id,
                    product_qty: 1,
                    move_ids: [[0, 0, {
                        product_id: partRes[0].id,
                        repair_line_type: 'add',
                        product_uom_qty: 1,
                        quantity: 1,
                    }]],
                }]],
                kwargs: {},
            }));
            await callKw({ model: 'repair.order', method: 'action_create_sale_order', args: [[repairId]], kwargs: {} });
            await callKw({ model: 'repair.order', method: 'action_validate', args: [[repairId]], kwargs: {} });
            await callKw({ model: 'repair.order', method: 'action_assign', args: [[repairId]], kwargs: {} });
            await callKw({ model: 'repair.order', method: 'action_repair_start', args: [[repairId]], kwargs: {} });
            await callKw({ model: 'repair.order', method: 'action_repair_end', args: [[repairId]], kwargs: {} });

            const repairRes = await callKw({
                model: 'repair.order',
                method: 'read',
                args: [[repairId], ['sale_order_id']],
                kwargs: {},
            });
            const saleOrderId = repairRes[0].sale_order_id[0];
            await callKw({ model: 'sale.order', method: 'action_confirm', args: [[saleOrderId]], kwargs: {} });
            const invoiceWizardId = unwrapId(await callKw({
                model: 'sale.advance.payment.inv',
                method: 'create',
                args: [[{
                    advance_payment_method: 'delivered',
                    sale_order_ids: [[6, 0, [saleOrderId]]],
                }]],
                kwargs: { context: { active_id: saleOrderId, active_ids: [saleOrderId] } },
            }));
            await callKw({
                model: 'sale.advance.payment.inv',
                method: 'create_invoices',
                args: [[invoiceWizardId]],
                kwargs: { context: { active_id: saleOrderId, active_ids: [saleOrderId] } },
            });
            const saleRes = await callKw({
                model: 'sale.order',
                method: 'read',
                args: [[saleOrderId], ['invoice_ids']],
                kwargs: {},
            });
            const invoiceIds = saleRes[0].invoice_ids || [];
            if (!invoiceIds.length) {
                throw new Error('invoice not created');
            }
            await callKw({ model: 'account.move', method: 'action_post', args: [invoiceIds], kwargs: {} });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
