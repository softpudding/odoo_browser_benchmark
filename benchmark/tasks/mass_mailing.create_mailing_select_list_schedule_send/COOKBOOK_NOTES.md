# Cookbook notes — mass_mailing.create_mailing_select_list_schedule_send

## Browser-use failure mode: datetime widget drifts on Schedule wizard

BU successfully performed every sub-step EXCEPT the datetime entry in the
`mailing.mailing.schedule.date` wizard. Final DB state:

- subject: `Spring Promo` (correct)
- state: `in_queue` (correct)
- schedule_type: `scheduled` (correct)
- mailing_model_name: `mailing.list` (correct)
- contact_list_ids: `[Bench Newsletter Subs]` (correct)
- body_html: contains `Save 20%` (correct — iframe editor was reachable)
- **schedule_date: `2026-05-20 02:00:00 UTC`** — expected `10:00:00 UTC`

BU's final self-report claimed the Scheduled Date was "05/20/2026 10:00:00"
but the stored UTC value is 8 hours off. The hour segment was silently
miscommitted by the Odoo datetime widget — same class of failure flagged
in `ODOO19_PATTERNS.md §DateTimeField widget: button vs input dual
rendering` and observed in the `stock.lot.expiration_date` cookbook note.

## Why a simple `fill()` on the datetime widget is not enough

`addons/web/static/src/views/fields/datetime/datetime_field.xml` renders a
pre-populated datetime as a `<button class="o_input">` showing the
formatted value. Only on click (flipping `picker.activeInput=field`) does
it re-render as an editable `<input>`. A Playwright `fill()` targeting
`.o_field_widget[name='schedule_date'] input` times out on a fresh open
because the input doesn't exist yet.

Even after the click flip, typing into the input without explicitly
clearing the pre-filled `MM/DD/YYYY HH:MM:SS` can leave partial residue
(e.g. typing `05/20/2026 10:00:00` when `04/20/2026 02:00:00` is already
there can yield `04/20/2026 10:00:02/...` depending on caret position).

## Oracle pattern: JSON-RPC the schedule wizard

Same approach as `mass_mailing.build_campaign_send_test_schedule/oracle.py`:

```javascript
const wizardId = await callKw({
    model: 'mailing.mailing.schedule.date',
    method: 'create',
    args: [[{ mass_mailing_id: mailingId, schedule_date: '2026-05-20 10:00:00' }]],
    kwargs: {},
});
await callKw({
    model: 'mailing.mailing.schedule.date',
    method: 'action_schedule_date',
    args: [[wizardId]],
    kwargs: {},
});
```

`action_schedule_date` is the exact code path the dialog's primary
**Schedule** footer button fires, so the end state is identical to a UI
run (state='in_queue', schedule_type='scheduled', schedule_date set).

## email_from DB constraint

`mailing.mailing` has a NOT NULL DB constraint on `email_from` (per
ODOO19_PATTERNS L49-50). Oracle must set it explicitly on
`mailing.mailing.create` — fall back to `'admin@example.com'` if the
admin user's email or partner email is blank. UI creates fill this
automatically via onchange (default_get pulls `author_id.email`), but
JSON-RPC create does not.

## Timezone-aware check.py

Admin's timezone in the benchmark base is `UTC`, so `2026-05-20 10:00`
entered in the wizard stores as `2026-05-20 10:00:00` UTC. But the task
may be ported to non-UTC admin accounts (Asia/Shanghai, America/LA, …),
so check.py accepts both:

```python
ok = (sd_user_local == expected_local) or (sd_utc_naive == expected_local)
```

where `sd_user_local = sd_utc.astimezone(user_tz)`. This lets a human
tester with tz=Europe/Brussels type `10:00` locally and still pass the
check (stored UTC would be `08:00`, user-local view is `10:00`). See
ODOO19_PATTERNS §Timezone-safe date comparison in check.py.

## Distinct-from siblings

- **Row 389** (`mass_mailing.duplicate_mailing_edit_subject_send`):
  Duplicate + edit + Send (no Schedule). This row creates from scratch +
  Schedules.
- **Row 438** (`mass_mailing.build_campaign_send_test_schedule`):
  Medium-tier, prompts also for a test send. This row skips the test send
  and uses the 10:00 UTC datetime as the calibration anchor (438 uses
  April 30 09:00 which happens to coincide with a BU-friendly hour pick).
- **Row 355** (`mass_mailing.create_segmented_mailing_save_draft`):
  Creates + saves as DRAFT (no send, no schedule). This row goes further
  into `state=in_queue` via the Schedule wizard.

## Calibration data

Single-shot BU: 211.8s wall clock, F1=0.0 via postcondition failure on
schedule_date. Hard-tier (≤40% pass expected). The three-widget compound
(iframe body + m2o autocomplete + datetime wizard) gave BU enough rope
to self-report success while silently corrupting the datetime — the
exact "confident-but-wrong" pattern hard-tier targets.
