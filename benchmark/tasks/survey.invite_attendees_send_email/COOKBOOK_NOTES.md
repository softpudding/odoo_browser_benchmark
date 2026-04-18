# Cookbook additions from survey.invite_attendees_send_email

## survey.invite wizard: `partner_ids` is hard-required AND `no_quick_create`

`survey.invite_views.xml` in Odoo 19 defines:

```xml
<field name="partner_ids"
    widget="many2many_tags_email"
    placeholder="Add existing contacts..." options="{'no_quick_create': True}"
    context="{'show_email': True, 'form_view_ref': 'base.view_partner_simple_form'}"
    required="True"
    invisible="not send_email"/>
```

Implications for benchmark tasks:

1. The form-level `required="True"` **blocks `action_invite`** (the Send
   button) if Recipients is empty — even though `emails` (Additional
   emails) is populated and `action_invite` server-side would accept
   `partner_ids=[]` with a non-empty `emails`. Free-text emails alone
   are insufficient via the UI.
2. `options="{'no_quick_create': True}"` disables the quick-create
   suggestion in the Recipients autocomplete, so typing a brand-new
   email does NOT offer a "Create '<email>'" row. Only pre-existing
   partners can be picked.

Task design consequence: to use the survey.invite wizard end-to-end via
the UI, seed the target recipients as `res.partner` rows first, and have
the agent type email (or name) and pick from autocomplete. The
Additional-emails text area is a distractor — filling it alone still
blocks Send because `partner_ids` validation fails.

## survey.invite.send_email defaults True for `access_mode='token'`

`_compute_send_email` sets `send_email = (survey_access_mode == 'token')`
and `action_send_survey` passes `default_send_email=(access_mode != 'public')`
to the wizard. Net effect:

- `access_mode='public'` (default): wizard opens with Send-by-Email OFF,
  Recipients/Subject/Body hidden; only Survey Link is shown (the "Share"
  flow).
- `access_mode='token'`: wizard opens with Send-by-Email ON, all the
  compose fields visible. This is the access mode to pick for email-based
  invite tasks.

## survey.user_input create emits two diff rows per partner

`survey.invite.action_invite` → `_prepare_answers` → `_create_answer`
creates a `survey.user_input` with `partner_id`, `email` (copied from the
partner), and `state='new'` (default). Under `state_spec.yaml`:

```yaml
survey.user_input:
  match_key: [email]
  fields: [email, state]
```

The diff engine emits **two** `create` rows per recipient — one for
`email` and one for `state=new`. `expected_state.json` must list both,
not just `email`, otherwise F1 caps at 0.67.

## SMTP sink is also required for survey.invite

`action_invite` calls `_send_mail` → `mail.mail.create(...)`, which is
later picked up by the outbox cron. However the HTTP request does NOT
await that cron — the `mail.mail` row is persisted regardless of
eventual SMTP delivery. The seed nevertheless stands up the aiosmtpd
sink because (a) Odoo's mail queue scans outbox rows on action_invite
return and (b) any UserError from mail composition (e.g., missing
`email_from`) DOES propagate inline and roll back the answers. The sink
+ catchall ICPs + `admin.partner_id.email` are the minimal triple that
keeps the transaction intact.
