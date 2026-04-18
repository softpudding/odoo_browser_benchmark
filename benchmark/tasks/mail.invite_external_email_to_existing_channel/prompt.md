# Invite an external email address to an existing Discuss channel

You are in the Odoo 19 **Discuss** app logged in as **Administrator**.

A private group channel named **`project-discussion`** already exists in the
sidebar. We want to invite an external collaborator — someone who does NOT
yet have a user account in this Odoo — by sending them an invitation email.

## What to do

1. Open the **Discuss** app.
2. In the left sidebar, click the **`project-discussion`** channel to open it.
3. In the channel header, click the **Invite People** action (the user-plus
   icon labelled "Invite People"). This opens the invite side panel titled
   **"Invite people"** with a search input placeholder **"Invite people or
   email"**.
4. In that search input, type the full external email address exactly:

   ```
   external-guest@bench.test
   ```

5. Wait for the list below the input to show a selectable row containing
   `external-guest@bench.test` with an envelope icon (it appears because no
   existing user matches that email — so Odoo offers to send an email
   invitation instead).
6. **Click that `external-guest@bench.test` row** so it appears as a selected
   chip above the **Invite to Group Chat** button.
7. Click the **Invite to Group Chat** button to send the email invitation.

## Rules

- The email must be exactly `external-guest@bench.test` (lowercase, that
  domain). Do not invent a different address.
- Do not invite any existing internal user (e.g., do not pick
  Administrator, Marc Demo, or any partner suggestion) — this task is
  specifically about the external-email invitation path, which sends a
  `mail.mail` to that address and creates a guest-invite link.
- Do not rename, archive, or delete the `project-discussion` channel.
- Do not post any messages in the channel. Only the side-panel invite action
  is required.
- Do not create a second channel with the same or different name.
