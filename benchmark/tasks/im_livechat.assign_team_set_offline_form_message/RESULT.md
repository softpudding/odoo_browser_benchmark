ROW: 302
TASK_ID: im_livechat.assign_team_set_offline_form_message
DIFFICULTY: medium
SUMMARY: Open Website Support live chat channel via 3-dots Configure menu, switch Options tab, set 2 text fields, save.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## im_livechat.assign_team_set_offline_form_message

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 154.1s) |
| **F1** | 1.0 |
| **Odoo modules** | Live Chat |
| **Workflow** | Open Live Chat app, hover the seeded "Website Support" kanban card, click the 3-dots menu and choose Configure Channel to reach the form. Switch to the Options tab and update Notification Text (button_text) and Welcome Message (default_message) to the exact strings, then save. |
| **Capability tested** | Tab switching combined with multi-field text input on a non-default form view (Live Chat kanban opens session, not form). |
| **Notes** | Original task spec referenced offline_form_text / offline_email fields that do NOT exist on im_livechat.channel in Odoo 19; remapped to the real Options-tab text fields (button_text, default_message) preserving the "tab switch + multi-text-field input" hard pattern. Browser-use solved cleanly, so calibration is "easier" than the medium target. |
