"""Oracle for sale_purchase.mto_so_generate_po_change_vendor_confirm."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    response = page.evaluate(
        """async () => {
            const unwrap = (value) => Array.isArray(value) ? value[0] : value;
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

            const soRes = await callKw({
                model: 'sale.order',
                method: 'search_read',
                args: [[['client_order_ref', '=', 'MTO-VENDOR-SWITCH']], ['id', 'name']],
                kwargs: { limit: 1 },
            });
            const vendorRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Beacon Components']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!soRes.length || !vendorRes.length) {
                throw new Error('seed records missing');
            }

            const soId = soRes[0].id;
            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[soId]],
                kwargs: {},
            });

            const poRes = await callKw({
                model: 'purchase.order',
                method: 'search_read',
                args: [[['origin', '=', soRes[0].name]], ['id', 'order_line']],
                kwargs: { limit: 1 },
            });
            if (!poRes.length) {
                throw new Error('generated RFQ missing');
            }
            const poId = poRes[0].id;
            await callKw({
                model: 'purchase.order',
                method: 'write',
                args: [[poId], { partner_id: vendorRes[0].id }],
                kwargs: {},
            });

            if (poRes[0].order_line && poRes[0].order_line.length) {
                await callKw({
                    model: 'purchase.order.line',
                    method: 'write',
                    args: [[poRes[0].order_line[0]], { price_unit: 62 }],
                    kwargs: {},
                });
            }

            await callKw({
                model: 'purchase.order',
                method: 'button_confirm',
                args: [[poId]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
