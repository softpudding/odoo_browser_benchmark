"""Oracle for event_product.sell_event_product_fill_attendee_details.

Pure JSON-RPC oracle (allowed for oracle scripts). Reaches the target
end state directly rather than walking the multi-modal SO configurator
UI:

  1. Resolve seeded partner, event, ticket, product.
  2. Create a sale.order with one line for the ticket product+ticket
     (Standard on Bench Festival 2026) with qty=1.
  3. Call sale.order.action_confirm — Odoo auto-generates an
     event.registration linked to the ticket for the partner.
  4. Write the attendee name/email on that registration and make sure
     it's in the 'open' state.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


EVENT_NAME = "Bench Festival 2026"
TICKET_NAME = "Standard"
PRODUCT_NAME = "Bench Standard Ticket"
PARTNER_NAME = "Bench Attendee Customer"
ATTENDEE_NAME = "Bench Attendee Name"
ATTENDEE_EMAIL = "bench.attendee@example.com"


def oracle(page):
    login(page)
    # Land on Sales so the oracle looks like an admin operator working
    # through the sales module.
    navigate(page, "/odoo/sales")

    result = page.evaluate(
        """async (payload) => {
            const unwrapId = (v) => Array.isArray(v) ? v[0] : v;
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            // 1. Resolve partner.
            const partners = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', payload.partnerName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!partners.length) {
                throw new Error('Partner not found: ' + payload.partnerName);
            }
            const partnerId = partners[0].id;

            // 2. Resolve event.
            const events = await callKw({
                model: 'event.event',
                method: 'search_read',
                args: [[['name', '=', payload.eventName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!events.length) {
                throw new Error('Event not found: ' + payload.eventName);
            }
            const eventId = events[0].id;

            // 3. Resolve the Standard ticket.
            const tickets = await callKw({
                model: 'event.event.ticket',
                method: 'search_read',
                args: [[
                    ['event_id', '=', eventId],
                    ['name', '=', payload.ticketName],
                ], ['id', 'product_id', 'price']],
                kwargs: { limit: 1 },
            });
            if (!tickets.length) {
                throw new Error(
                    'Ticket not found: ' + payload.ticketName +
                    ' on ' + payload.eventName);
            }
            const ticket = tickets[0];
            const ticketId = ticket.id;
            const productId = unwrapId(ticket.product_id);
            if (!productId) {
                throw new Error('Ticket has no product_id');
            }

            // 4. Create SO with one line for the ticket.
            const orderIds = await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerId,
                    order_line: [[0, 0, {
                        product_id: productId,
                        product_uom_qty: 1.0,
                        event_id: eventId,
                        event_ticket_id: ticketId,
                        tax_ids: [[5, 0, 0]],
                    }]],
                }]],
                kwargs: {},
            });
            const orderId = unwrapId(orderIds);

            // 5. Confirm the SO — this triggers automatic creation of an
            //    event.registration linked to the ticket+partner.
            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[orderId]],
                kwargs: {},
            });

            // 6. Find the auto-generated registration. Odoo may create
            //    multiple registrations on confirm depending on qty; we
            //    expect one for qty=1. Match by event+ticket+SO.
            const regs = await callKw({
                model: 'event.registration',
                method: 'search_read',
                args: [[
                    ['event_id', '=', eventId],
                    ['event_ticket_id', '=', ticketId],
                    ['sale_order_id', '=', orderId],
                ], ['id', 'state', 'partner_id']],
                kwargs: {},
            });
            if (!regs.length) {
                throw new Error(
                    'Auto-generated registration not found for SO ' + orderId);
            }
            if (regs.length > 1) {
                throw new Error(
                    'Expected 1 registration, got ' + regs.length);
            }
            const regId = regs[0].id;

            // 7. Write the attendee details. Also ensure partner_id is set
            //    on the registration (action_confirm usually sets it from
            //    the SO partner, but we set it defensively).
            await callKw({
                model: 'event.registration',
                method: 'write',
                args: [[regId], {
                    partner_id: partnerId,
                    name: payload.attendeeName,
                    email: payload.attendeeEmail,
                }],
                kwargs: {},
            });

            // 8. Make sure the registration is in 'open' (Registered)
            //    state. sale.order.action_confirm normally triggers
            //    registration.action_confirm; call it again idempotently
            //    in case the auto-confirmation skipped (e.g., because the
            //    registration was missing required fields until we wrote
            //    the attendee details).
            const afterState = await callKw({
                model: 'event.registration',
                method: 'read',
                args: [[regId], ['state']],
                kwargs: {},
            });
            if (afterState[0].state !== 'open' && afterState[0].state !== 'done') {
                await callKw({
                    model: 'event.registration',
                    method: 'action_confirm',
                    args: [[regId]],
                    kwargs: {},
                });
            }

            // 9. Sanity read.
            const orderData = await callKw({
                model: 'sale.order',
                method: 'read',
                args: [[orderId], ['state', 'amount_total']],
                kwargs: {},
            });
            const regData = await callKw({
                model: 'event.registration',
                method: 'read',
                args: [[regId], ['state', 'name', 'email']],
                kwargs: {},
            });

            return { order: orderData[0], reg: regData[0] };
        }""",
        {
            "partnerName": PARTNER_NAME,
            "eventName": EVENT_NAME,
            "ticketName": TICKET_NAME,
            "attendeeName": ATTENDEE_NAME,
            "attendeeEmail": ATTENDEE_EMAIL,
        },
    )

    order = result["order"]
    reg = result["reg"]
    if order["state"] not in ("sale", "done"):
        raise RuntimeError(
            f"Oracle: order state is {order['state']}, expected sale/done"
        )
    if reg["state"] != "open":
        raise RuntimeError(
            f"Oracle: registration state is {reg['state']}, expected open"
        )
    if reg["name"] != ATTENDEE_NAME:
        raise RuntimeError(
            f"Oracle: registration name is {reg['name']}, "
            f"expected {ATTENDEE_NAME}"
        )
    if reg["email"] != ATTENDEE_EMAIL:
        raise RuntimeError(
            f"Oracle: registration email is {reg['email']}, "
            f"expected {ATTENDEE_EMAIL}"
        )


run_oracle(oracle)
