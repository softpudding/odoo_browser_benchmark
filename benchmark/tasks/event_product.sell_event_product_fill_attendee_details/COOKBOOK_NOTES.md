# event_product.sell_event_product_fill_attendee_details — quirks

## SO-line event configurator wizard fires only when product.event_ok=True

Setting `service_tracking='event'` on the product.template flips the
computed `event_ok` Boolean on the variant. When that product is picked
on a `sale.order.line`, the onchange returns an `event_configurator`
client action with `event_id` + `event_ticket_id` required. If the agent
(or oracle) uses `set_o2m_many2one(page, 0, "product_template_id", ...)`
the wizard opens within ~1s; no explicit "open wizard" click is needed.

## Registration editor is a one2many wizard pre-filled from partner

On `sale.order.action_confirm`, if any order line has an
`event_ticket_id`, `sale.order._action_confirm` calls
`registration.editor` which renders a `o2m` list with one row per
paid ticket quantity. Each row is **pre-filled** with the partner's
name/email — so an agent that just clicks the primary footer button
saves a registration with the Administrator's default name, not the
required attendee. To override, the agent has to click the Name cell
and replace the value before submitting. `_modal_fill_field_in_row`
helper (locate `.modal:visible .o_data_row td[name='name']`, click,
`fill('')`, re-fill, Tab) works reliably.

## Pre-seed the auto-default 'Registration for ...' ticket

`event.event.event_ticket_ids` auto-materializes a default ticket on
create. If the seed adds the paid `Standard Pass` ticket via `(0, 0, …)`
alongside a separate `Registration for Bench Summit` entry (both backed
by the `EVENT_REG` built-in product), the post-run diff captures only
the registration/SO the agent creates — no phantom ticket rows.

## state_spec scope-narrowing

Event registration/SO are the only records the agent mutates, so
`state_spec.yaml` only needs `event.registration` + `sale.order`. Keeping
`event.event.ticket` and `product.template` out of scope avoids
collisions with the base snapshot's duplicate 'Gift Card' product.template
records and the seed's `Registration for …` placeholder ticket.

## Browser-use wall-clock calibration

BU reached state F1=1.0 within the 360s budget but used almost all of it
navigating the two nested wizards, so `gave_up=True` flipped strict to
FAIL. For a medium-tier task this is a clean calibration: the agent's
final state is correct, but the time pressure from chained wizards makes
it non-trivial. A stricter variant would set `time_limit_sec=240` to
force an outright fail; a lenient variant would bump to 480.
