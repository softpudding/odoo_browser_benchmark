"""Oracle for event_sale.multi_ticket_checkout_two_attendees.

Pure JSON-RPC oracle (allowed for oracle scripts). Reaches the target
end state directly:

  1. Resolve seeded partner, event, and both tickets.
  2. Create a single sale.order with TWO lines (one per ticket).
  3. Call sale.order.action_confirm — Odoo auto-generates one
     event.registration per ticket.
  4. Write the correct attendee name/email on each registration so
     they match the prompt. Ensure both registrations are in 'open'
     state.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


EVENT_NAME = "Bench Summit 2026"
TICKET_EARLY = "Early Bird"
TICKET_VIP = "VIP"
PRODUCT_EARLY = "Bench Summit Early Bird Ticket"
PRODUCT_VIP = "Bench Summit VIP Ticket"
PARTNER_NAME = "Bench Summit Customer"

ATTENDEE_EARLY_NAME = "Alice Summit Attendee"
ATTENDEE_EARLY_EMAIL = "alice.summit@example.com"
ATTENDEE_VIP_NAME = "Bob Summit Attendee"
ATTENDEE_VIP_EMAIL = "bob.summit@example.com"


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

            // 3. Resolve both tickets.
            const tickets = await callKw({
                model: 'event.event.ticket',
                method: 'search_read',
                args: [[
                    ['event_id', '=', eventId],
                    ['name', 'in', [payload.ticketEarly, payload.ticketVip]],
                ], ['id', 'name', 'product_id', 'price']],
                kwargs: {},
            });
            const earlyTicket = tickets.find(t => t.name === payload.ticketEarly);
            const vipTicket = tickets.find(t => t.name === payload.ticketVip);
            if (!earlyTicket || !vipTicket) {
                throw new Error('Missing ticket(s) on ' + payload.eventName);
            }
            const earlyProductId = unwrapId(earlyTicket.product_id);
            const vipProductId = unwrapId(vipTicket.product_id);
            if (!earlyProductId || !vipProductId) {
                throw new Error('Ticket(s) missing product_id');
            }

            // 4. Create SO with two lines (one per ticket).
            const orderIds = await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerId,
                    order_line: [
                        [0, 0, {
                            product_id: earlyProductId,
                            product_uom_qty: 1.0,
                            event_id: eventId,
                            event_ticket_id: earlyTicket.id,
                            tax_ids: [[5, 0, 0]],
                        }],
                        [0, 0, {
                            product_id: vipProductId,
                            product_uom_qty: 1.0,
                            event_id: eventId,
                            event_ticket_id: vipTicket.id,
                            tax_ids: [[5, 0, 0]],
                        }],
                    ],
                }]],
                kwargs: {},
            });
            const orderId = unwrapId(orderIds);

            // 5. Confirm the SO — this triggers automatic creation of
            //    event.registration records, one per ticket.
            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[orderId]],
                kwargs: {},
            });

            // 6. Find the auto-generated registrations.
            const regs = await callKw({
                model: 'event.registration',
                method: 'search_read',
                args: [[
                    ['event_id', '=', eventId],
                    ['sale_order_id', '=', orderId],
                ], ['id', 'state', 'partner_id', 'event_ticket_id']],
                kwargs: {},
            });
            if (regs.length !== 2) {
                throw new Error(
                    'Expected 2 registrations for SO ' + orderId +
                    ', got ' + regs.length);
            }
            const earlyReg = regs.find(
                r => unwrapId(r.event_ticket_id) === earlyTicket.id);
            const vipReg = regs.find(
                r => unwrapId(r.event_ticket_id) === vipTicket.id);
            if (!earlyReg || !vipReg) {
                throw new Error('Failed to match registrations to tickets');
            }

            // 7. Write the attendee details on each registration.
            await callKw({
                model: 'event.registration',
                method: 'write',
                args: [[earlyReg.id], {
                    partner_id: partnerId,
                    name: payload.attendeeEarlyName,
                    email: payload.attendeeEarlyEmail,
                }],
                kwargs: {},
            });
            await callKw({
                model: 'event.registration',
                method: 'write',
                args: [[vipReg.id], {
                    partner_id: partnerId,
                    name: payload.attendeeVipName,
                    email: payload.attendeeVipEmail,
                }],
                kwargs: {},
            });

            // 8. Ensure both registrations are in 'open' state.
            const regStates = await callKw({
                model: 'event.registration',
                method: 'read',
                args: [[earlyReg.id, vipReg.id], ['state']],
                kwargs: {},
            });
            const needConfirm = regStates
                .filter(r => r.state !== 'open' && r.state !== 'done')
                .map(r => r.id);
            if (needConfirm.length) {
                await callKw({
                    model: 'event.registration',
                    method: 'action_confirm',
                    args: [needConfirm],
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
                args: [[earlyReg.id, vipReg.id], ['state', 'name', 'email', 'event_ticket_id']],
                kwargs: {},
            });

            return { order: orderData[0], regs: regData };
        }""",
        {
            "partnerName": PARTNER_NAME,
            "eventName": EVENT_NAME,
            "ticketEarly": TICKET_EARLY,
            "ticketVip": TICKET_VIP,
            "attendeeEarlyName": ATTENDEE_EARLY_NAME,
            "attendeeEarlyEmail": ATTENDEE_EARLY_EMAIL,
            "attendeeVipName": ATTENDEE_VIP_NAME,
            "attendeeVipEmail": ATTENDEE_VIP_EMAIL,
        },
    )

    order = result["order"]
    regs = result["regs"]
    if order["state"] not in ("sale", "done"):
        raise RuntimeError(
            f"Oracle: order state is {order['state']}, expected sale/done"
        )
    if abs(order["amount_total"] - 600.0) > 0.01:
        raise RuntimeError(
            f"Oracle: order amount_total is {order['amount_total']}, "
            f"expected 600.0"
        )
    if len(regs) != 2:
        raise RuntimeError(
            f"Oracle: expected 2 registrations, got {len(regs)}"
        )
    for reg in regs:
        if reg["state"] != "open":
            raise RuntimeError(
                f"Oracle: registration {reg['name']!r} state is "
                f"{reg['state']}, expected open"
            )


run_oracle(oracle)
