"""Oracle for mail.create_channel_set_custom_avatar_pin_two_messages.

Uses call_kw to deterministically:
  - Create the public channel `engineering-hub` with the description.
  - Set image_128 to the avatar PNG bytes (base64).
  - Post the three messages in order.
  - Pin the first and the third one (NOT the PR message).
"""

import base64
import json
import os

from benchmark.oracle_helpers import login, navigate, run_oracle


CHANNEL_NAME = "engineering-hub"
DESCRIPTION = "Weekly engineering updates"
MESSAGES = [
    "Weekly standup Monday 10am",
    "Please review PR #1042",
    "Reminder: retro on Thursday",
]
PIN_INDICES = [0, 2]  # First and third messages.

AVATAR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "seed_artifacts",
    "avatar.png",
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")

    with open(AVATAR_PATH, "rb") as f:
        avatar_b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "channel_name": CHANNEL_NAME,
        "description": DESCRIPTION,
        "messages": MESSAGES,
        "pin_indices": PIN_INDICES,
        "avatar_b64": avatar_b64,
    }

    response = page.evaluate(
        """async (payload) => {
            const callKw = async (model, method, args, kwargs) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { model, method, args, kwargs: kwargs || {} },
                    }),
                });
                const j = await res.json();
                if (j.error) {
                    throw new Error(JSON.stringify(j.error));
                }
                return j.result;
            };

            // Resolve current partner so the creator becomes a member.
            const adminUser = await callKw(
                'res.users',
                'search_read',
                [[['login', '=', 'admin']], ['partner_id']],
                { limit: 1 },
            );
            if (!adminUser || !adminUser.length) {
                throw new Error('admin user not found');
            }
            const adminPartnerId = adminUser[0].partner_id[0];

            // Create the public channel directly with channel_type='channel'.
            const created = await callKw(
                'discuss.channel',
                'create',
                [[{
                    name: payload.channel_name,
                    channel_type: 'channel',
                    description: payload.description,
                    image_128: payload.avatar_b64,
                    channel_member_ids: [
                        [0, 0, { partner_id: adminPartnerId }],
                    ],
                }]],
                {},
            );
            const channelId = Array.isArray(created) ? created[0] : created;

            // Post the three messages, capture ids in order.
            const messageIds = [];
            for (const body of payload.messages) {
                const created = await callKw(
                    'mail.message',
                    'create',
                    [[{
                        model: 'discuss.channel',
                        res_id: channelId,
                        body: body,
                        message_type: 'comment',
                        subtype_id: false,
                    }]],
                    {},
                );
                const mid = Array.isArray(created) ? created[0] : created;
                messageIds.push(mid);
            }

            // Pin the requested messages.
            for (const idx of payload.pin_indices) {
                await callKw(
                    'discuss.channel',
                    'set_message_pin',
                    [[channelId], messageIds[idx], true],
                    {},
                );
            }

            return 'ok';
        }""",
        payload,
    )

    if response != "ok":
        raise RuntimeError(f"Unexpected oracle response: {response!r}")


run_oracle(oracle)
