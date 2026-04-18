# Cookbook notes for event_sale.multi_ticket_checkout_two_attendees

## Multi-ticket registration modal — ticket counter input names

`modal_ticket_registration` renders one row per ticket (keyed by ticket
name) when `len(event.event_ticket_ids) > 1`. The counter input has
`name="nb_register-<ticket_id>"` and the `+`/`-` buttons carry
`data-input-name="nb_register-<ticket_id>"`. The `Register` submit
button is `.a-submit` and its JS handler (`TicketDetails.onSubmitClick`)
JSON-RPC-POSTs the form to `/event/<slug>/registration/new` and
`insert()`s the returned HTML (`#modal_attendees_registration`) into
`document.body`. The desktop Register CTA on the event detail page
uses `data-bs-toggle="modal" data-bs-target="#modal_ticket_registration"`
(the mobile `<a>` branch is skipped because `event_page` is not set
outside `/event/<slug>/page/<path>`).

## Paid-event Attendees modal — 'Go to Payment', not 'Confirm Registration'

On paid tickets (`any(ticket.price > 0)`), `website_event_sale` inherits
`registration_attendee_details` and **replaces** the submit-button
label from `Confirm Registration` to **`Go to Payment`**. Selectors
must match either text, or just filter on
`button[type='submit'].btn-primary` inside `#modal_attendees_registration`.

## Per-attendee rows — heading pattern `Ticket #N - <ticket_name>`

The attendees modal iterates `tickets` then `range(1, quantity+1)`,
bumping a shared `counter`. Each attendee section's `h5` heading reads
`Ticket #N - <ticket_name>` (space-dash-space). To tell which counter
maps to which ticket, match the heading text. Fallback: the hidden
input `<input class="d-none" name="{counter}-event_ticket_id"
value="{ticket.id}">` inside each section gives the `counter -> ticket
id` map directly.

## Paid checkout flow from portal registration

`/event/<slug>/registration/confirm` on a paid cart:
1. Creates `event.registration` rows via `sudo()`.
2. For anonymous carts, `CustomerPortal._create_or_update_address` sets
   the SO's partner from the first attendee. For logged-in users
   (admin, internal users), `_is_anonymous_cart()` is False and the
   existing cart partner is kept.
3. Redirects to `/shop/checkout?try_skip_step=true`.
4. `/shop/checkout` checks `_is_anonymous_cart` and whether delivery/
   billing addresses pass `_check_delivery_address` /
   `_check_billing_address`. Missing fields (for US: name, email, phone,
   street, city, state_id, zip, country_id) cause a redirect to
   `/shop/address`. Seed the admin's partner with a complete address
   to skip the address step.
5. With address complete, `try_skip_step=true` forwards to
   `/shop/payment`.

## Wire Transfer ends the SO in 'sent', not 'sale'

`payment_custom.PaymentTransaction._apply_updates` calls
`_set_pending()` for wire-transfer txs. The Sale override of
`PaymentTransaction._post_process` then runs
`action_quotation_sent()` on every linked SO in state `draft`, moving
it to `sent` — but does NOT call `action_confirm`. The SO stays in
`sent` (and registrations in `draft` state, `sale_status='to_pay'`)
until an internal user explicitly posts the payment. Check scripts
that assert SO in `sale` will fail on a Wire-Transfer-only flow. Use
`state in ('sent', 'sale', 'done')` or verify via check.py only.

## sale.async_emails=True is mandatory for Wire Transfer in ephemeral test DBs

The post-process chain calls
`sale.order._send_payment_succeeded_for_order_mail()` which triggers a
synchronous `message_post_with_source(..., force_send=True)`. Without a
valid SMTP provider (ephemeral snapshot DBs have none), this raises
inside `/payment/status/poll`, the cursor rolls back, and
`is_post_processed` stays False — leaving the SO stuck in `draft`.
Setting `sale.async_emails='True'` in seed defers the mail to a cron,
so the synchronous `_post_process` succeeds and the SO moves to
`sent`. This is now used by this task as a dependency.

## Payment providers default to 'disabled'

`payment.provider.state` defaults to `'disabled'`. Tasks that require
a specific provider to be pickable on `/shop/payment` must
`write({'state': 'enabled'})` in seed. To pin the pick to a single
provider, disable all others (`_disable_competing_providers` pattern)
so the radio list has only one entry. Wire Transfer =
`payment.payment_provider_transfer` xmlid.

## `payment_custom` + `website_event_sale` both need to be installed on demand

Neither is in `base_modules.txt`. Seed must `button_immediate_install`
both. `website_event_sale` drags in `website_event` + `sale_product`
dependencies. A minimum viable seed order is:
`website_event -> website_event_sale -> payment_custom`.

## Admin is NOT an anonymous cart

`sale.order._is_anonymous_cart()` returns True only when
`partner_id == website.user_id.partner_id` (the public user).  Admin
logged into `/event/<slug>/register` creates a cart with
`partner_id=admin.partner_id`, so the `/registration/confirm` shortcut
that overwrites SO partner from the first attendee does NOT fire.
Design note: if a task wants the SO partner to match a specific
non-admin name like "Buyer Biz", either seed a portal user with that
name and use a non-admin `login_context`, or log the agent out of
admin before the portal flow. This task takes the simpler path —
admin (Mitchell Admin) is the SO partner.
