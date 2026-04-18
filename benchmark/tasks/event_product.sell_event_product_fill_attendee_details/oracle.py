"""Oracle for event_product.sell_event_product_fill_attendee_details."""

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

            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Northwind Workshops']], ['id']],
                kwargs: { limit: 1 },
            });
            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Enablement Seat Product']], ['id']],
                kwargs: { limit: 1 },
            });
            const eventRes = await callKw({
                model: 'event.event',
                method: 'search_read',
                args: [[['name', '=', 'Partner Enablement Day']], ['id']],
                kwargs: { limit: 1 },
            });
            const ticketRes = await callKw({
                model: 'event.event.ticket',
                method: 'search_read',
                args: [[['name', '=', 'Workshop Seat'], ['event_id', '=', eventRes[0].id]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!partnerRes.length || !productRes.length || !eventRes.length || !ticketRes.length) {
                throw new Error('seed records missing');
            }

            const orderId = unwrap(await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerRes[0].id,
                    order_line: [[0, 0, {
                        product_id: productRes[0].id,
                        product_uom_qty: 1,
                        price_unit: 95,
                        tax_ids: [[6, 0, []]],
                        event_id: eventRes[0].id,
                        event_ticket_id: ticketRes[0].id,
                    }]],
                }]],
                kwargs: {},
            }));

            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[orderId]],
                kwargs: {},
            });

            const regRes = await callKw({
                model: 'event.registration',
                method: 'search_read',
                args: [[['sale_order_id', '=', orderId]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!regRes.length) {
                throw new Error('generated registration missing');
            }
            const regId = regRes[0].id;
            await callKw({
                model: 'event.registration',
                method: 'write',
                args: [[regId], {
                    name: 'Jordan Rivera',
                    email: 'jordan.rivera@example.com',
                }],
                kwargs: {},
            });
            await callKw({
                model: 'event.registration',
                method: 'action_confirm',
                args: [[regId]],
                kwargs: {},
            });
            if (!regId) {
                throw new Error('registration update failed');
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
