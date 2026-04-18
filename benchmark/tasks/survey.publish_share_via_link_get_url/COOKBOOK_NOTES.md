# Cookbook notes — survey.publish_share_via_link_get_url

## CopyClipboardChar widget readonly rendering

`widget="CopyClipboardChar"` (e.g. `survey.invite.survey_start_url` in the
share-a-survey wizard) wraps a `CharField` plus a copy button. When the field
is `readonly`, the inner `CharField` template renders as a `<span>` (not an
`<input>`) — so Playwright `input_value()` will time out.

Robust read pattern:

```python
link = page.locator(".modal:visible .o_field_widget[name='survey_start_url']").first
text = (link.text_content() or "").strip()
if "/survey/start/" not in text:
    inputs = link.locator("input")
    if inputs.count() > 0:
        text = (inputs.first.input_value() or "").strip()
```

## survey.survey has NO `state` field in Odoo 19

Despite the term "publish/draft" appearing in some prompts and STATUS rows,
`survey.survey` exposes only `active` (Boolean) and `session_state` (Selection,
ready/in_progress for live sessions). There is no `state='running'` field.
"Published / ready to share" maps to `active=True` and a non-null `access_token`,
with `access_mode='public'` to expose the public Survey Link in the share dialog.

## Survey share dialog (action_send_survey)

`survey.survey.action_send_survey` returns the `survey.invite` wizard. For
`access_mode='public'`, the wizard pre-sets `default_send_email=False`, exposes
the **Survey Link** (`survey_start_url`) field, and the only footer buttons are
**Send** (hidden when `send_email=False`) and **Close**. Closing the wizard has
no DB side effect — only **Send** actually invokes `survey.invite.action_invite`.
This makes the share dialog a clean "single-button + read-only side data" task.
