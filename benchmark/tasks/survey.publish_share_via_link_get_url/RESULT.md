ROW: 308
TASK_ID: survey.publish_share_via_link_get_url
DIFFICULTY: easy
SUMMARY: Open seeded 'Customer Pulse Q2' survey, click Share, verify public /survey/start URL, close dialog.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: matches

DETAIL_SECTION:
## survey.publish_share_via_link_get_url

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Surveys |
| **Workflow** | Open the seeded 'Customer Pulse Q2' survey from the Surveys app kanban, click the form-header Share button (calls `survey.survey.action_send_survey`), confirm the Share-a-Survey wizard exposes the `/survey/start/<token>` public URL via the CopyClipboardChar widget, and close the dialog without sending an email. |
| **Capability tested** | Single-button form-header action that opens a wizard exposing read-only side data — the agent must press the right header button and recognise the dialog satisfies the request without further interaction. |
| **Notes** | Task has no DB state change; expected_state.json is empty `[]`. PASS criteria are anchored on `survey.survey.action_send_survey` in trace_spec required_ops plus check.py invariants (active=True, access_mode='public', access_token non-null, certification False, single seeded question intact). The CopyClipboardChar widget renders the URL inside the field widget but NOT as a queryable `<input>` element when readonly — oracle reads via `text_content()` on the field widget div, falling back to inner inputs. BU solved it in 10 steps (~68s wall clock). |
