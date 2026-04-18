# Cookbook notes for website_event.publish_event_register_via_portal

## event.event publish in the backend — no stage bar, no form toggle

Unlike `event.track`, `event.event` does NOT have a publish-driving
status bar. The event form header's `is_published` field uses the
`website_redirect_button` widget, which **only navigates** to the
frontend preview; it does not toggle the boolean. The inline "Publish"
link in the right-hand Event Details group (near the Visibility
dropdown) is declared with `invisible="website_published or
website_visibility == 'public'"` — since the default visibility is
`'public'`, the link is **hidden by default**.

Canonical backend ways to publish an `event.event`:

1. Call `event.event.website_publish_button()` via JSON-RPC (same
   method the website editor systray invokes; writes `website_published=True`
   which also sets `is_published=True`).
2. Navigate to the frontend preview and toggle the top-systray
   `Published` switch (Owl component — fragile under Playwright).
3. Change `website_visibility` to `'link'` or `'logged_users'` so the
   inline "Publish" button becomes visible, then click it. This also
   writes `website_visibility` as a side effect, so not a clean single-
   field flip.

For oracle scripts, JSON-RPC bypass of `website_publish_button()` is
the clean, deterministic path.

## Portal registration form — two stacked Bootstrap modals

The public registration flow uses two modals inserted into `document.body`:

1. `#modal_ticket_registration` — opened via Bootstrap
   `data-bs-toggle="modal"` from the event-page **Register** button.
   Contains a counter input and a submit button with class `.a-submit`.
   Submit is handled by `TicketDetails.onSubmitClick` (public interaction)
   which calls `rpc(formEl.action, FormData(...))` to
   `/event/<slug>/registration/new` and **inserts** the returned HTML
   (the attendees-details modal) into `document.body`.
2. `#modal_attendees_registration` — appears only after the ticket
   modal submit. Its inputs are named
   `{registration_index}-{question_type}-{question_id}` (e.g.
   `1-name-1`, `1-email-2`, `1-phone-3`). To locate these inputs,
   match by `name*='-name-'` (substring), NOT `name$='-name'`
   (suffix) — the suffix is the numeric question id, not the type.

## Default registration questions are auto-attached

When an `event.event` is created with no `event_type_id`, the
`_compute_question_ids` fallback pulls `event.question` records with
`is_default=True`: Name (mandatory), Email (mandatory), Phone
(optional). These are the inputs the agent fills on the portal
attendee form. No seed work needed.

## `event.registration.create` is invoked via `sudo()` — NOT in API trace

The `/event/<slug>/registration/confirm` controller creates the
registration via `request.env['event.registration'].sudo().create(...)`.
Because of the `sudo()` + the custom-controller entry point, the
`event.registration.create` ORM op does not appear in the instrumented
API trace. `trace_spec.required_ops` for portal-registration tasks
should NOT include `event.registration.create` — rely on state diff +
`check.py` instead.

Also: the `custom:/event/<slug>/registration/confirm` route carries
the event slug in the canonical_op, so matching on
`custom:/event/registration/confirm` fails too. If required_ops
matching is desired, the benchmark metrics engine would need slug-
stripped pattern matching, which it does not currently have. Leave
required_ops empty for these tasks.

## Calibration signal (BU single-shot pass)

Browser-use solved this hard-tier task on its first run in ~85s with
F1=1.0, 0 postcondition failures. The dual-modal chain + JSON-RPC
publish did not add enough friction to trip BU. To harden this pattern
for a future task:

- Configure multiple named tickets on the event and require selecting
  a specific one (forces non-default-counter interaction).
- Add `once_per_order=True` general questions with required `simple_choice`
  answers.
- Require the Owl systray toggle path (not the inline Publish link)
  for the backend publish step.
