# Create a Discuss channel, invite two members, and post a welcome message

You are in the Odoo 19 **Discuss** app logged in as **Administrator**.

We need to spin up a new public channel so the team can coordinate, invite two
internal teammates, and drop a welcome message.

## What to do

1. Open the **Discuss** app (`/odoo/discuss`).
2. In the left sidebar, find the **Channels** category header. Click the
   **+** (plus) icon next to **Channels** to open the channel creation input.
3. Type the channel name exactly:

   ```
   team-bench
   ```

   Then confirm by pressing **Enter** or clicking the **Create channel**
   suggestion. This creates a public `channel_type='channel'` record — NOT a
   direct message, NOT a private group.
4. Once the new **#team-bench** channel opens, click the **Invite People**
   action in the channel header (user-plus icon, labelled "Invite People").
5. In the invite side panel search, add both of these internal users as
   members (they are already seeded in this database):
   - **Bench Alice**
   - **Bench Bob**

   Both names should appear as selected chips above the invite button.
6. Click the **Invite** button to add them to the channel.
7. The channel view is now visible with three members. Click into the
   **message composer** at the bottom of the channel and type the exact
   text:

   ```
   Welcome team!
   ```

8. Press **Enter** to send the message. The message must appear in the
   channel feed.

## Rules

- The channel name must be exactly `team-bench` (lowercase, with the dash).
- The channel type must be **public `channel`**, not a group/DM. When you
  press + next to "Channels" and type a name + Enter, Odoo creates a
  public channel by default (this is correct).
- Do not invite any users besides **Bench Alice** and **Bench Bob**.
- Do not create a second channel with the same or different name.
- Do not rename, archive, or delete `team-bench` after creating it.
- The welcome message body must contain the word `Welcome team` — typing
  `Welcome team!` exactly is correct. Do not post multiple messages.
