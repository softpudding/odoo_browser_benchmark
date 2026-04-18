# survey.invite_attendees_send_email — RESULT

## Verdict

| Metric | Value |
|---|---|
| **Oracle** | PASS (19s) |
| **Browser-Use** | PASS (136s) |
| **F1** | 1.0 |
| **Required op recall** | 1.0 (`survey.invite.action_invite` fired) |
| **Write precision** | 1.0 |
| **Harmful write rate** | 0.0 |
| **Strict clean** | True |

Task calibrates as **medium-easy** in practice: Browser-Use solves the
multi-recipient compose-wizard flow cleanly when the recipients are
already existing partners and the field is a conventional
`many2many_tags_email` autocomplete. The Subject override is also
successfully handled.

## Workflow

1. Kanban open "Bench Onboarding Quiz" → form.
2. Click form-header **Send** → opens `survey.invite` wizard modal.
3. In **Recipients** (many2many_tags_email), type each email (`alice@x.com`,
   `bob@y.com`, `carol@z.com`), pick the matching seeded partner from
   autocomplete. Three chips accumulate.
4. Clear the auto-filled **Subject** and set it to `Please complete onboarding`.
5. Click modal-footer **Send** → `survey.invite.action_invite` fires and
   creates one `survey.user_input` per partner.

## Seed setup

- One `survey.survey` `Bench Onboarding Quiz`, `access_mode='token'`,
  `users_login_required=False`, one simple_choice question.
- Three pre-existing `res.partner` records (Alice/Bob/Carol Invitee)
  keyed by the target emails.
- Detached `aiosmtpd` Sink Controller on `127.0.0.1:2525` + matching
  `ir.mail_server` so `mail.mail.send(raise_exception=True)` inside
  `action_invite` does not roll back the transaction.
- Admin partner has `email='admin@bench.test'`; catchall ICPs set.

## Outcome

Task is included in the benchmark as a **positive calibration signal** for
medium tier: it documents that BU can complete a multi-recipient compose
wizard when recipients are pre-existing partners reachable via
autocomplete. Tasks that need to fail BU should require free-text email
entry into a view where the field is bound with `required="True"` AND
`no_quick_create` — a combination that blocks BU from using either path.

## Known quirks (see COOKBOOK_NOTES.md)

- `survey.invite.partner_ids` has `required="True"` + `no_quick_create`,
  so the Additional-emails-only path fails in the UI.
- `survey.invite._compute_send_email` flips True when
  `survey_access_mode='token'`, exposing Recipients/Subject/Body by default.
- After `action_invite`, `survey.user_input.state='new'` is the default
  — must be in `expected_state.json` alongside `email` as a "create" diff row.
