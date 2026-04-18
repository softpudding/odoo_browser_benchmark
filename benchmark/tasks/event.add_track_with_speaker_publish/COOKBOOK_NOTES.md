# Cookbook notes for event.add_track_with_speaker_publish

## event.track publish via stage side-effect

`event.track` inherits `website.published.mixin`, but the backend form's
publish control is the `website_redirect_button` widget — that widget ONLY
navigates to the frontend, it does NOT toggle `is_published`. The canonical
backend way to publish a track is to move its stage to one with
`is_fully_accessible=True` (default data: the **Published** stage at sequence
4). The `_synchronize_with_stage` hook in `website_event_track/models/event_track.py`
flips `is_published=True` as a side-effect of entering that stage.

Takeaway for task writers: if you want a "publish a track" step, tell the
agent to click the **Published** stage in the status bar. Don't tell them to
click "Go to Website" unless you want a website-frontend navigation side quest.

## website_event_track requires on-demand install

`website_event` and `website_event_track` are NOT in the base snapshot even
though `event` and `website` are. Any task touching `event.track` (or the
Tracks smart button on the event form) must install both via
`button_immediate_install()` in seed.py. See
`event.publish_event_register_attendee/seed.py` for the pattern.

## Browser-use handles this task cleanly (calibration)

With an explicit prompt pointing at the Published stage in the status bar,
BU solves the task in ~11 steps on single-shot. This is low calibration risk
for "medium" — the task still requires combining three field groups + a
multi-tab navigation + a non-obvious stage click, but BU's LLM absorbs the
instruction about the status-bar stage and executes it correctly.
