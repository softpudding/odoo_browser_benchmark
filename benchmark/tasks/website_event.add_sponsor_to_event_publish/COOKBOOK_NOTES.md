# Cookbook notes for website_event.add_sponsor_to_event_publish

## `event.sponsor` lives in `website_event_exhibitor`, not `website_event`

The `event.sponsor` model + the Sponsors smart button on `event.event` are
declared in `website_event_exhibitor` (manifest: `'depends': ['website_event']`).
Neither `website_event` nor `website_event_exhibitor` are in the benchmark
base snapshot. Seed must `button_immediate_install` `website_event_exhibitor`
(which transitively installs `website_event`) before creating the event or
the Sponsors smart button will not appear.

Default sponsor levels shipped by `website_event_exhibitor/data/event_sponsor_data.xml`:
`Bronze`, `Silver`, `Gold`. Seed can rely on `Silver` existing as default
data after install — no need to create the level.

## Sponsors is a smart button, NOT a notebook tab

Unlike `event.track` which exposes a Tracks smart button on the event form
AND has no inline tab, and unlike `event.registration` which has a Registrations
smart button, the Sponsors smart button opens a **kanban/list** view of
`event.sponsor` with `context={'default_event_id': active_id,
'search_default_event_id': active_id}`. Clicking **New** opens the full
sponsor form (no inline quick-create) — fields required: `partner_id`,
`sponsor_type_id` (both Many2one, `required=True`).

The kanban/list view shows sponsors from prior runs filtered by
`search_default_event_id` automatically, but the list is NOT filtered when
you land from the smart button if Odoo's kanban groups them by sponsor type.
Browser-use noted "existing sponsors (likely global or from a search
filter)" on first land — that's the filter domain showing adjacent events'
sponsors grouped together, not a seed-cleanup issue.

## Publish path: `website_redirect_button` + website systray toggle

`event.event` has no publish stage bar (unlike `event.track`). The form
header's `is_published` field uses the `website_redirect_button` widget
which **only navigates** to the frontend preview. The actual publish
toggle is the Owl systray switch in the website editor preview. See
`website_event.publish_event_register_via_portal` cookbook for the same
pattern.

Oracle uses JSON-RPC `event.event.website_publish_button()` bypass because
the Owl systray inside the iframe is fragile under Playwright. The bypass
is sanctioned per ODOO19_PATTERNS.md 'Oracle patterns' section. Browser-
use handled the UI toggle fine (it clicked the `input[type='checkbox']`
directly on the systray).

## Calibration: BU solves single-shot at medium tier

Browser-use solved this in ~17 steps, 125.6s, F1=1.0 on first run. The
multi-surface flow (smart-button sub-view → full form m2o fill → breadcrumb
back → website redirect → systray toggle) has four distinct UI contexts,
but BU's LLM recognises each because the prompt explicitly names the
widget and button labels ("Sponsors smart button", "Unpublished indicator",
"Unpublished switch"). Kept at medium tier/`primary_track: true`.

To harden a future variant:
- Require multiple sponsors at different levels (Gold + Silver) to force
  two nested New flows from the smart-button sub-view.
- Require setting the `exhibitor_type = 'exhibitor'` (non-default, surfaces
  the Description notebook + Opening Hours + live-mode fields) instead of
  the default `'sponsor'` (footer-logo-only).
- Combine with a per-sponsor publish toggle (the Published widget in the
  sponsor form button box is invisible when `exhibitor_type == 'sponsor'`
  — flipping `exhibitor_type = 'exhibitor'` first unlocks it).
