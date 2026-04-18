Create a public Discuss channel with a custom avatar, post three messages, and pin exactly two of them.

1. Open Discuss.
2. Create a public channel (channel type: Channel) named `engineering-hub`.
3. Set the channel description to:
   `Weekly engineering updates`
4. Upload a custom channel avatar (image_128) using the file located at
   `benchmark/tasks/mail.create_channel_set_custom_avatar_pin_two_messages/seed_artifacts/avatar.png`.
5. Post these three messages in this exact order, as separate messages:
   1. `Weekly standup Monday 10am`
   2. `Please review PR #1042`
   3. `Reminder: retro on Thursday`
6. Pin exactly these two messages in the channel:
   - `Weekly standup Monday 10am`
   - `Reminder: retro on Thursday`

Rules:
- The channel must be a public Channel (not a private group, not a chat).
- Channel name must be exactly `engineering-hub` (no other casing, no prefix/suffix).
- Description must be exactly `Weekly engineering updates`.
- All three messages must be posted, in the order listed above.
- Only the two listed messages must be pinned. The PR review message
  (`Please review PR #1042`) MUST NOT be pinned.
- Do not create any additional channels, messages, or pins.
