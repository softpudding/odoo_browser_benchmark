# website_slides cookbook notes — publish + prerequisite + attendees

New quirks observed while building
`website_sale_slides.assign_attendees_publish_course`:

- `slide.channel.prerequisite_channel_ids` domain is
  `[('id', '!=', id), ('visibility', '=', visibility), ('website_published', '=', website_published)]`
  — BOTH visibility and website_published must match the current form's
  values for a prerequisite candidate to appear in the many2many_tags
  autocomplete. If the seed pins the prerequisite to `members` +
  `is_published=True`, the agent must flip visibility to `members` AND
  publish BEFORE the prereq dropdown shows the candidate. Pre-publish
  prereq selection silently yields an empty dropdown.
- The backend form's `is_published` field uses `widget="website_redirect_button"`
  (navigation-only — same RedirectField as event.event). Publishing is NOT
  possible from the backend form. The working paths are (a) frontend
  `/slides/<slug>` Owl admin systray Unpublished/Published toggle (which
  calls `website_publish_button` on the model) or (b) toggling the
  `is_published` cell in the list view.
- `slide.channel.user_id` defaults to `self.env.uid`. When seeds run via
  `odoo shell` the uid is SUPERUSER_ID (id=1, OdooBot partner), so without
  an explicit `user_id=admin`, `create()` calls `_action_add_members` and
  enrolls OdooBot as an unwanted attendee on BOTH seeded courses. Set
  `user_id=admin.id` in the create vals, or unlink residual
  `slide.channel.partner` rows right after create. Same applies in cleanup:
  when searching pre-task state the OdooBot attendee row will leak unless
  scrubbed.
- `_compute_enroll` auto-coerces `enroll='invite'` when
  `visibility=='members'`. Writing `visibility='members'` alone is
  enough — no need to explicitly set enroll. Database check constraint
  `CHECK(visibility != 'members' OR enroll = 'invite')` enforces this.
- The `Add Attendees` header button opens `slide.channel.invite` in
  `enroll_mode=True`. `_compute_send_email` then sets `send_email=True`
  because `enroll_mode or visibility != 'public'` is True. The toggle is
  hidden (`invisible="enroll_mode or channel_visibility != 'public'"`),
  so the wizard cannot be completed without sending an email. Seed a
  working SMTP sink (aiosmtpd on 127.0.0.1:2525 + matching
  `ir.mail_server`) or the wizard's `mail.mail.send(raise_exception=True)`
  rolls back the transaction and no `slide.channel.partner` row is
  persisted (same pattern as the discuss invite-by-email cookbook entry).
- `slide.channel.partner` list view has `create="0"` — the admin cannot
  directly create attendee rows from the list; going through the wizard
  (with its mandatory `send_email`) is the only supported UI path.
- `slide.channel._action_add_members` starts with `_` so it is NOT
  callable over JSON-RPC `call_kw`. Oracle scripts that want to short-
  circuit the email step should create `slide.channel.partner` rows
  directly (`model: 'slide.channel.partner', method: 'create'`) with
  `member_status='joined'`.
- Browser-use failure mode observed: the prereq `many2many_tags` field
  accepts text input ("Bench 101") but BU often moves on without clicking
  the dropdown option, leaving `prerequisite_channel_ids=[]`. Tasks that
  rely on a m2m tag commit should validate the final record in check.py
  (the state_spec will not catch an uncommitted autocomplete).
