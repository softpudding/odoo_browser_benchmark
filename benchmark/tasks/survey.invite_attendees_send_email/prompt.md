# Invite three attendees to an existing survey

You are in the Odoo 19 **Surveys** app logged in as **Administrator**.

An existing survey titled **`Bench Onboarding Quiz`** has already been created
and is configured with access mode **Invited people only**. Three recipient
contacts already exist in the database with these names and emails:

- **Alice Invitee** — `alice@x.com`
- **Bob Invitee** — `bob@y.com`
- **Carol Invitee** — `carol@z.com`

Your job is to invite all three of them to take the survey in a single send.

## What to do

1. Open the **Surveys** app (Surveys kanban / list at `/odoo/surveys`).
2. Click the **`Bench Onboarding Quiz`** card to open its form.
3. In the form header, click the **Send** button. This opens the
   **Share a Survey** dialog (the `survey.invite` wizard) with the
   **Send by Email** toggle already enabled.
4. In the **Recipients** field (a tag-input at the top of the dialog), add
   all three invitees **one by one**. For each invitee:
   - Click the Recipients input.
   - Type the email address (e.g. `alice@x.com`).
   - Wait for the autocomplete suggestion showing the matching partner
     (e.g. "Alice Invitee").
   - Click the suggestion so the recipient becomes a chip in the input.

   Repeat for `bob@y.com` and `carol@z.com`. When done, you should see three
   chips — one for each invitee.

5. Clear the auto-filled **Subject** field and replace its value with
   exactly:

   ```
   Please complete onboarding
   ```

6. Leave the email body and all other fields at their defaults (do NOT
   change the template, body, deadline, or attachment).
7. Click the **Send** button in the dialog footer. The dialog closes and
   you are returned to the survey form.

## Rules

- All three recipients must be added before sending. Do not send with
  fewer than three chips in the Recipients field.
- The Subject must read exactly `Please complete onboarding` (no quotes,
  no trailing period, no extra words).
- Do not modify the survey itself (title, questions, access mode, active
  flag, required-login setting).
- Do not press **Close** or the dialog's **X** icon before sending — you
  must press **Send** so `survey.invite.action_invite` fires and one
  `survey.user_input` row is created per invited partner.
- Do not create a second survey or additional contacts.
