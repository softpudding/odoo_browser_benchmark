# Create a private group channel, invite a member, and upload an attachment

You are in Odoo 19 logged in as **Administrator**, on the **Discuss** app.

You need to spin up a new private **group** channel, invite one specific
teammate to it, and upload a small text file as an attachment to a message
in that channel.

## What to do

1. Open the **Discuss** app.
2. Create a new **private channel** of type **Group** (the grouped chat
   kind — "Group" / "Private Channel" — not a public `#channel`, not a
   direct message) named exactly:

   ```
   Bench Project Sync
   ```

3. Invite the following user as a member of that channel:
   - **Channel Member Bob** (login `channel.bob`, email
     `channel.bob@bench.test`)

4. In the channel composer at the bottom of the channel, attach a small
   text file named exactly:

   ```
   sync-notes.txt
   ```

   with this exact content (a single line, no trailing newline required):

   ```
   Kickoff agenda for Bench Project Sync.
   ```

   Send the message so the attachment is posted to the channel. The
   message body itself can be empty — only the attachment matters.

## Rules

- The channel name must match exactly, including capitalization.
- The channel must be a private group channel (`channel_type = 'group'`),
  not a public channel and not a direct message.
- **Channel Member Bob** must be a member of the channel (Administrator
  is automatically a member as the creator).
- Do not invite any other users besides Channel Member Bob.
- Do not create a second channel with the same name.
- Exactly one attachment named `sync-notes.txt` must be linked to the
  channel (`res_model = 'discuss.channel'`, `res_id` = the new channel's
  id). Do not upload any other files to the channel.
- Do not delete the channel or remove yourself from it after creating it.
