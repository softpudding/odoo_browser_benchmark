# Result — event_sale.multi_ticket_checkout_two_attendees (row 354)

## Oracle

- **PASS**, wall clock **30.3s**, `StateDiffF1 = 1.0`, 10/10 edits matched,
  `RequiredOpRecall = 1.0`, no forbidden writes.

## Browser-Use (single-shot calibration)

- **PASS**, wall clock **69.5s**, `StateDiffF1 = 1.0`, 10/10 edits matched,
  no postcondition failures. The agent completed the whole portal flow
  (`/event` -> event page -> multi-ticket modal -> attendees -> checkout
  -> Wire Transfer pay) on the first try.

## Calibration verdict

Browser-use solved the task on a single shot despite the multi-ticket +
multi-attendee form + non-default Wire Transfer payment option. The
task remains **hard tier** (tier 3) as a representative closed-loop
back-office-published / public-portal purchase flow — useful to keep in
the benchmark even though BU passes first-shot, similar to
`website_event.publish_event_register_via_portal` (row 342).
The underlying friction (dual-modal chain + multi-attendee per-ticket
rows + explicit payment radio) is a useful negative control: it
confirms that BU *can* solve shop+event flows end-to-end when the
attendee fields are plainly labelled.

## Key design decisions

- **Wire Transfer ends the SO in `state='sent'`** (NOT `'sale'`).  The
  payment transaction goes to `pending`, and the Sale override of
  `_post_process` calls `action_quotation_sent()` — SO confirmation
  would require an internal user posting the payment later.  The
  check.py accepts `sent`/`sale`/`done` so the task is correct
  regardless of whether the admin later marks the wire as received.
- **`sale.async_emails=True`** must be set in the seed: otherwise the
  missing SMTP provider in the ephemeral test DB raises during
  `_send_payment_succeeded_for_order_mail`, which rolls back the
  cursor in `/payment/status/poll`, leaving the SO stuck in `draft`.
- **Admin partner billing address** (street/city/state_id/zip/phone/
  country) must be pre-populated so `/shop/checkout?try_skip_step=true`
  can forward directly to `/shop/payment` without the agent having to
  fill an address form.
- **Only Wire Transfer is enabled** in the seed; other providers are
  switched to `state='disabled'` so the agent has a single, determin-
  istic payment option to pick.
