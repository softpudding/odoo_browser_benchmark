# Create a private Discuss channel and invite two members

You are in the Odoo 19 **Discuss** app logged in as **Administrator**.

You need to spin up a new private **group** channel to coordinate a release
rehearsal, and invite two teammates to it.

## What to do

1. Open the **Discuss** app.
2. Create a new **private channel** (the grouped chat kind — "Group" /
   "Private Channel" — not a public #channel) named exactly:

   ```
   Release Rehearsal Team
   ```

3. Invite the following two users as members of that channel:
   - **Nadia Rossi**
   - **Oliver Chen**

## Rules

- The channel name must match exactly, including capitalization.
- The channel must be a private group channel (`channel_type = 'group'`),
  not a public channel and not a direct message.
- Both **Nadia Rossi** and **Oliver Chen** must end up as members of the
  channel (Administrator is automatically a member as the creator).
- Do not invite any other users besides Nadia Rossi and Oliver Chen.
- Do not create a second channel with the same name.
- Do not post any messages in the channel.
