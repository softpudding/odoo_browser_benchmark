# Cookbook Notes — calendar.invite_organize_with_event_agenda_attachment

## New quirks discovered

### 1. calendar.event attendee side-effect: 2 x `invitation.ics` attachments per create

When a `calendar.event` is created with non-empty `partner_ids`, Odoo's
mail framework auto-generates one `ir.attachment` named `invitation.ics`
per invited attendee, linked back to the event
(`res_model='calendar.event'`, `res_id=event.id`).

Implication for `state_spec.yaml` / `expected_state.json`:
- Tracking `ir.attachment` with `match_key: [name, res_model]` emits
  phantom "create" rows for `[invitation.ics, calendar.event]` that will
  explode the extras count and drop F1 → 0 even for the oracle.
- The public/global asset cache (`bus.websocket_worker_assets.min.js`,
  `web.assets_frontend.min.css`, etc.) also flows through ir.attachment
  on first page load of each run, adding ~10 unrelated rows.
- **Fix:** don't track `ir.attachment` in state_spec at all. Verify the
  expected attachment via `check.py` directly (search `res_model`,
  `res_id`, `name`).

### 2. Admin timezone is NOT UTC in the benchmark base snapshot

`benchmark_base` ships with the admin user's `tz` set to a
America/Los_Angeles-family tz (observed: writing `14:00 UTC` stored as
`22:00` local). Oracles that hardcode `"2026-05-20 14:00:00"` as a UTC
string will land 8 hours off local time and fail a check that pins the
local hour.

Canonical pattern in the oracle:
```python
admin_tz = page.evaluate(...)  # call_kw res.users search_read ['tz']
local_dt = pytz.timezone(admin_tz).localize(
    datetime(2026, 5, 20, 14, 0, 0)
)
utc_iso = local_dt.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
```

### 3. Browser-use `available_file_paths` sandbox blocks seeded file uploads

Browser-use refuses to drive an `<input type="file">` with a path that
hasn't been explicitly whitelisted via the `available_file_paths`
kwarg on `Agent(...)`. Our default benchmark runner does NOT pass this
through, so any seed-provided artifact (e.g.
`benchmark/tasks/<task>/seed_artifacts/agenda.txt`) is rejected with:

```
File path ... is not available. To fix: The user must add this file
path to the available_file_paths parameter when creating the Agent.
```

This is a second, independent reason BU fails file-upload tasks on top
of the native OS file dialog issue. It makes any "upload this seeded
file" task reliably fail BU until the runner is updated. Good for
hard-tier calibration, bad if we later want to ceiling-test BU on file
uploads.

### 4. Oracle pattern for `ir.attachment` linked to a brand-new record

Create the parent record first, grab its id (unwrap from an array
result), then create the attachment in a second `call_kw` with
`res_model` + `res_id` set explicitly. Odoo accepts:

```js
{
  name: 'agenda.txt',
  res_model: 'calendar.event',
  res_id: eventId,
  type: 'binary',
  mimetype: 'text/plain',
  datas: <base64>,
}
```

No need to go through the chatter composer or `message_post` — a direct
`ir.attachment.create` with `res_model/res_id` is enough to show up in
the event's Files panel and pass a `check.py` that searches for
attachments linked to the event.
