# website_event.publish_event_register_via_portal — Result

## Status

| Metric | Value |
|---|---|
| Oracle | PASS (F1 = 1.0, 23.1s) |
| Browser-Use | PASS (F1 = 1.0, 85.1s, single-shot) |
| Difficulty calibration | FAILED (intended hard, solved by BU) |
| Primary track | false (calibration too easy for tier 3) |

## Workflow summary

Back-office + portal round-trip:

1. Open `/odoo/events`, navigate to the seeded unpublished event
   `Bench Public Day`, and flip it to Published
   (via `event.event.website_publish_button()`).
2. Switch to the public portal at `/event`, click the event card,
   click **Register**, leave the single-ticket counter at `1`, click
   the inner **Register** button, fill the attendee form
   (name / email / phone), and click **Confirm Registration**.

## Design notes

- Seeds install `website_event` on demand via `button_immediate_install()`
  (not in the base snapshot).
- No tickets are configured on the seeded event, so the ticket modal
  renders the single-ticket layout with an input counter defaulting to
  `1`. BU does not need to click the `+` button.
- Default event questions (Name, Email, Phone) render automatically on
  the attendee-details modal because `_default_question_ids` pulls the
  `is_default=True` records when `event_type_id` is unset.
- `/event/<slug>/registration/confirm` creates `event.registration`
  via `sudo()`, so the ORM-level `event.registration.create` does NOT
  appear in the API trace. `trace_spec.required_ops` is intentionally
  empty; verification is done entirely via state diff + `check.py`.

## Why the oracle uses a JSON-RPC bypass for the publish step

`event.event.is_published` is rendered with the `website_redirect_button`
widget, which only navigates to the frontend preview. The canonical UI
path to publish is the website editor's top-systray "Unpublished/Published"
toggle (Owl component inside an iframe). That path is fragile under
Playwright and not what the `_synchronize_with_stage` pattern applies to
(stage-based publish only exists on `event.track`, not `event.event`).
Oracle bypass uses the same server method — `website_publish_button()` —
that the systray switch invokes.

## Calibration discussion

Tier-3 intended, but BU solved the task on the first shot at F1=1.0
in ~85s. The task is a straightforward sequence of (a) backend publish
toggle, (b) portal navigation, (c) modal-chained registration form. BU's
policy handles the dual-modal chain without breaking, and the default
ticket counter of `1` removes the `+` click hurdle.

To harden this task, future iterations could:

- Configure multiple tickets so BU must pick a specific one
  (e.g. 'VIP' vs 'Standard'), and require paying with a selected
  payment provider via `event_sale`.
- Add a `general_question_ids` entry (once_per_order=True) with a
  custom selection answer that must match an exact value, forcing
  BU to read a non-obvious question label.
- Require the agent to navigate to the website editor preview and
  click the actual UI Published toggle (Owl systray), which is
  empirically fragile for LLM-driven browser agents.

Kept at hard tier (primary_track=false) to preserve the closed-loop
cross-module back-office → portal pattern in the benchmark.
