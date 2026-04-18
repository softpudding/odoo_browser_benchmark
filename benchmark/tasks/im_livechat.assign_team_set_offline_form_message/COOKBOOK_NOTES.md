# Cookbook notes — im_livechat.assign_team_set_offline_form_message

## im_livechat.channel has NO `offline_form_text` / `offline_email` fields in Odoo 19

The model `im_livechat.channel` does not implement any "offline form" fields
(no `offline_form_text`, no `offline_email`, no `offline_*`). Searching the
entire `addons/im_livechat` module for "offline" yields only chatter/visitor-
disconnection helpers, never a channel-level offline form configuration.

The Options tab on the channel form view (`im_livechat_channel_view_form`)
exposes only:

- `button_text`         (Char, "Notification Text")
- `default_message`     (Char, "Welcome Message")
- `header_background_color`, `title_color`, `button_background_color`,
  `button_text_color`   (color widgets)
- `review_link`         (Char)
- `max_sessions_mode`, `max_sessions`, `block_assignment_during_call`
  (Session Limits group)

If a task description mentions an "offline form / offline email" on a Live Chat
channel, it is a phantom from older Odoo versions or another product. Map it
to `button_text` + `default_message` (or skip the task) — do **not** try to
seed/check non-existent fields, the seed will raise `ValueError: Invalid field`
and the agent will be unable to complete the workflow.
