ROW: 359
TASK_ID: im_livechat.configure_channel_then_handle_widget_chat
DIFFICULTY: hard
SUMMARY: Reply to a seeded live chat session in Discuss by triggering the ::hello canned-response shortcut through the composer suggestion popover, not by typing the substitution text manually.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## im_livechat.configure_channel_then_handle_widget_chat

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 69.5s, 9 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Live Chat, Discuss, Mail |
| **Workflow** | Seed pre-creates the live chat channel 'Bench Support' (admin as operator) with one URL rule, a `mail.canned.response` shortcut 'hello' -> 'Hi, thanks for reaching out!', an anonymous visitor partner 'Visitor #BENCH-359', and a `discuss.channel` (channel_type='livechat') with admin + visitor members and one waiting `mail.message` authored by the visitor with body 'Hi there'. The agent opens `/odoo/discuss`, selects the livechat session in the 'Bench Support' sidebar category, types `::hello` into the composer so the suggestion popover loads the canned response, clicks the `hello` option (which substitutes the shortcut with the full text), and sends the message with Enter/Send. |
| **Capability tested** | Triggering the Odoo 19 Discuss canned-response suggestion popover via the `::` delimiter and selecting the substitution from the NavigableList overlay instead of sending the literal shortcut text. Plus sidebar navigation into a livechat session inside the auto-collapsing `im_livechat.channel` category. Multi-tab widget flow was calibrated down to single-tab per the backlog guidance (Playwright multi-tab coordination is fragile). |
| **Notes** | Canned responses in Odoo 19 are triggered by **double-colon `::`**, NOT single-colon (single colon triggers the emoji picker); the backlog spec said `:hello` and was corrected to `::hello`. Cookbook quirk discovered & documented: `mail.canned.response` visibility in the `/mail/data` webclient endpoint is gated by `create_uid = env.user.id OR group_ids in user.all_group_ids.ids`. When the benchmark harness runs seed.py via `odoo-bin shell`, the effective user is `__system__` (id=1), NOT admin (id=2), so a vanilla `env["mail.canned.response"].create({...})` yields a record that the admin agent cannot see. Seed MUST `with_user(admin).create({..., "group_ids": [(6, 0, [base.group_user.id])]})` to expose the record. Browser-use solved the task on the first try (9 steps, 69.5s) — calibration slots this as "easier" than hard tier. |
