ROW: 353
TASK_ID: event_product.sell_event_product_fill_attendee_details
DIFFICULTY: medium
SUMMARY: Sell a seeded event ticket product on a new SO for Bench Attendee Co, pick the event + ticket in the configurator wizard, confirm the SO, then fill attendee Name + Email in the registration editor modal.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 1.0
CALIBRATION: matches

DETAIL_SECTION:
## event_product.sell_event_product_fill_attendee_details

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Events (event_product / event_sale bridge) |
| **Workflow** | From Sales, create a new quotation for Bench Attendee Co, add a `Bench Summit Ticket` line; the `event_configurator` wizard pops because `product.event_ok=True`, pick event `Bench Summit` + ticket `Standard Pass` and Ok. Confirm the SO -> `registration.editor` wizard opens pre-filled from the partner; overwrite Name = `Alice Attendee`, Email = `alice@bench.test`, then submit. |
| **Capability tested** | Chain of two modal wizards triggered by SO actions (configurator on product pick, registration editor on confirm), combined with overriding the default-filled attendee fields. |
| **Notes** | Oracle passes deterministically. Browser-use reached the correct final state (all 9 atomic edits match) but exhausted the 360s wall-clock budget so `gave_up=True` -> strict FAIL while StateDiffF1=1.0. The calibration trap (fill the attendee tab, don't just click the primary footer button) works: BU had to iterate through two nested wizards and edit a pre-filled o2m row. |
