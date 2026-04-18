# Cookbook notes — im_livechat.configure_channel_then_handle_widget_chat

## `mail.canned.response` visibility: seed MUST create via `with_user(admin)` + `group_ids`

The `/mail/data` webclient endpoint (`webclient.py::_process_request_for_logged_in_user`)
filters canned-response records by:

```python
domain = ["|",
    ("create_uid", "=", request.env.user.id),
    ("group_ids", "in", request.env.user.all_group_ids.ids)]
```

When the benchmark harness runs `seed.py` via `odoo-bin shell`, the effective user is
`__system__` (id=1), NOT `admin` (id=2). A naive
`env["mail.canned.response"].create({"source": "...", "substitution": "..."})`
yields a record with `create_uid = __system__` and empty `group_ids`, which the
logged-in admin agent CANNOT see via the Discuss suggestion popover — even though
`env["mail.canned.response"].search([])` from any shell session returns it.

Symptom: oracle/agent types `::hello`, composer shows `::hello` as literal text,
no suggestion popover appears, `store["mail.canned.response"].records` stays empty.

Fix pattern (see this task's `seed.py`):

```python
base_user_group = env.ref("base.group_user")
env["mail.canned.response"].with_user(admin).create({
    "source": "hello",
    "substitution": "Hi, thanks for reaching out!",
    "group_ids": [(6, 0, [base_user_group.id])],
})
```

Either `with_user(admin)` OR a shared `group_ids` is sufficient; doing both is defensive.

## Canned response delimiter is `::` (double-colon), NOT `:hello`

The `suggestion_service.searchSuggestions` switch in
`addons/mail/static/src/core/common/suggestion_service.js` maps delimiters to types:

```js
case "@":  // partners
case "#":  // channels
case "::": // mail.canned.response   <-- double colon!
case ":":  // emoji (requires 2+ chars after)
```

Type `::hello` into the composer and the NavigableList popover will show matching
canned responses. A single `:hello` is parsed as an emoji search. Prompt phrasing
MUST say `::` explicitly or the agent will type `:hello` and fail.

The suggestion fetch is debounced 250ms (`suggestion_hook.js::DELAY_FETCH`). After
typing `::` wait at least 600–800ms for the RPC to return before expecting the
popover DOM.

## Discuss livechat sidebar: session name is the visitor partner name

For a `discuss.channel` with `channel_type='livechat'`, the sidebar item text
is computed from `thread.displayName` in `im_livechat`'s `thread_model_patch.js`:
the visitor partner's name is used (falls back to the channel's `name` when the
correspondent cannot be resolved). To make the prompt, seed and oracle all refer
to the same on-screen label, set the visitor `res.partner.name` equal to the
session `discuss.channel.name` — or accept that the on-screen label will be the
partner name.

Under the `im_livechat.channel` sidebar category (here "Bench Support"), livechat
sessions render as `.o-mail-DiscussSidebarChannel-itemName` nodes. The category
is `hideWhenEmpty: !this.are_you_inside` — i.e. hidden when the admin is not in
the `im_livechat.channel.user_ids`. Always `user_ids: [(6, 0, [admin.id])]` in
seed for the livechat channel, else the category collapses and the session is
unreachable from the sidebar.

## Livechat `discuss.channel` create via JSON-RPC/ORM requires `livechat_operator_id`

The model has a CHECK constraint:
`(channel_type = 'livechat' and livechat_operator_id is not null) or channel_type != 'livechat'`.
Minimum viable create vals for a seeded livechat session:

```python
env["discuss.channel"].create({
    "name": "Visitor #BENCH-359",
    "channel_type": "livechat",
    "livechat_channel_id": im_livechat_channel.id,
    "livechat_operator_id": admin.partner_id.id,
    "channel_member_ids": [
        (0, 0, {"partner_id": admin.partner_id.id}),
        (0, 0, {"partner_id": visitor_partner.id}),
    ],
})
```

A first `message_post` on the new channel auto-adds OdooBot as a third member
(standard mail behavior) — benign but visible in state dumps.

## Seed cleanup for livechat channels uses `active_test=False` + `sudo`

Old session records for the same bench session name may have already been
"closed" (have `livechat_end_dt`) but still `active=True`. They are regular
records — a normal `search([("name", "=", SESSION_NAME)])` finds them, but a
`sudo().unlink()` is safest because member records reference res.partner and
the ondelete chain is non-trivial.
