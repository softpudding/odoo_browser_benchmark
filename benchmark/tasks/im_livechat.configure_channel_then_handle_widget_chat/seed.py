"""Seed for im_livechat.configure_channel_then_handle_widget_chat.

Single-tab variant (per calibration guidance — the multi-tab widget flow is
fragile under Playwright harnesses). The seed pre-builds the outcome of a
just-started live chat session so the agent only has to **reply** via Discuss
using a canned response shortcut.

Creates:
  * `im_livechat.channel` 'Bench Support' — admin is the sole operator.
  * `mail.canned.response` with shortcut 'hello' -> 'Hi, thanks for reaching
    out!' (visible to admin; no group restriction so it always resolves).
  * An anonymous visitor `res.partner` (no user account).
  * A `discuss.channel` of `channel_type='livechat'` with the admin as
    `livechat_operator_id`, linked to 'Bench Support', with BOTH admin and the
    anonymous visitor as channel_member_ids, and ONE waiting `mail.message`
    authored by the visitor with body 'Hi there'.

All prior runs are scrubbed first so the seed is idempotent. Cleanup of
pre-existing canned responses with source='hello' protects against shared-DB
reruns.
"""

CHANNEL_NAME = "Bench Support"
SESSION_NAME = "Visitor #BENCH-359"
# The partner name is what appears as the sidebar display name for a livechat
# session (see im_livechat's thread_model_patch.js). Must match what the prompt
# tells the agent to look for.
VISITOR_PARTNER_NAME = "Visitor #BENCH-359"
CANNED_SHORTCUT = "hello"
CANNED_SUBSTITUTION = "Hi, thanks for reaching out!"
WAITING_MESSAGE = "Hi there"


def setup(env):
    # --- Cleanup prior runs (child-first) ------------------------------------
    # Drop any prior discuss.channel livechat session for this bench run.
    old_channels = env["discuss.channel"].with_context(active_test=False).search(
        [("name", "=", SESSION_NAME)]
    )
    old_channels.sudo().unlink()

    # Drop the live chat channel 'Bench Support' (also removes linked rules).
    env["im_livechat.channel"].search([("name", "=", CHANNEL_NAME)]).unlink()

    # Drop any prior canned response with the same shortcut.
    env["mail.canned.response"].search(
        [("source", "=", CANNED_SHORTCUT)]
    ).unlink()

    # Drop prior anonymous visitor partner.
    env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VISITOR_PARTNER_NAME)]
    ).unlink()

    # --- Admin lookup --------------------------------------------------------
    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if not admin:
        raise RuntimeError("admin user not found; seed cannot proceed")

    # --- Live chat channel ---------------------------------------------------
    livechat_channel = env["im_livechat.channel"].create({
        "name": CHANNEL_NAME,
        "user_ids": [(6, 0, [admin.id])],
        "button_text": "Need help? Chat with us.",
        "default_message": "How may I help you?",
    })
    # Ensure the channel has at least one URL rule so it counts as configured.
    env["im_livechat.channel.rule"].create({
        "channel_id": livechat_channel.id,
        "action": "display_button",
        "regex_url": "/",
    })

    # --- Canned response -----------------------------------------------------
    # The `/mail/data` "mail.canned.response" endpoint filters records by
    # `create_uid = env.user.id OR group_ids in user.all_group_ids.ids`.
    # In odoo shell, the current user is `__system__` (id=1), not admin.
    # Therefore we MUST (a) create the canned response with admin as the
    # author via `with_user(admin)`, AND (b) share it with base.group_user
    # so it remains visible even if the harness re-seeds with a different
    # effective user.
    base_user_group = env.ref("base.group_user")
    env["mail.canned.response"].with_user(admin).create({
        "source": CANNED_SHORTCUT,
        "substitution": CANNED_SUBSTITUTION,
        "group_ids": [(6, 0, [base_user_group.id])],
    })

    # --- Anonymous visitor partner ------------------------------------------
    visitor_partner = env["res.partner"].create({
        "name": VISITOR_PARTNER_NAME,
        "email": False,
    })

    # --- Discuss channel (livechat type) ------------------------------------
    # The constraint requires livechat_operator_id for livechat channels.
    # Both admin and the visitor become members. The operator (admin) is the
    # session "owner" per the livechat model.
    session = env["discuss.channel"].create({
        "name": SESSION_NAME,
        "channel_type": "livechat",
        "livechat_channel_id": livechat_channel.id,
        "livechat_operator_id": admin.partner_id.id,
        "channel_member_ids": [
            (0, 0, {"partner_id": admin.partner_id.id}),
            (0, 0, {"partner_id": visitor_partner.id}),
        ],
    })

    # --- Waiting message from the visitor -----------------------------------
    # Post a message authored by the visitor partner so the admin sees an
    # incoming message to reply to. Use message_post so mail.message fields
    # (body, author_id, message_type) are set consistently.
    session.with_user(admin).sudo().message_post(
        body=WAITING_MESSAGE,
        author_id=visitor_partner.id,
        message_type="comment",
        subtype_xmlid="mail.mt_comment",
    )
