# Send a chatter message with an attachment on a Contact

You are in the Odoo 19 **Contacts** app logged in as **Administrator**.

A contact named **`Bench Chatter Co`** already exists (email
`info@benchchatter.test`). You need to send this contact a chatter
**message** (not an internal note) with our welcome kit attached.

## What to do

1. Open **Contacts** (top-level app).
2. Click the contact **`Bench Chatter Co`** to open its form.
3. Scroll to the chatter panel (on the right / below the form).
4. In the chatter, click the **Send message** tab. This is important —
   the chatter opens on **Log note** by default; you must click
   **Send message** so the post is a real outbound comment that notifies
   the contact.
5. In the composer body, type exactly:

   ```
   Attached our welcome kit
   ```

6. Click the **paperclip** icon (aria-label "Attach files") in the
   composer to open the file picker, and upload the pre-seeded file
   located at:

   ```
   benchmark/tasks/mail.send_email_with_attachment_log_as_note/seed_artifacts/welcome_kit.txt
   ```

   Wait for the attachment chip (showing `welcome_kit.txt`) to appear
   above the composer text area.
7. Click **Send** to post the message.

## Expected end state

- The `Bench Chatter Co` contact has a chatter post whose
  **message_type** is `comment` and whose **subtype** is the standard
  `mail.mt_comment` (the "Discussion" subtype attached to **Send
  message**), NOT `mail.mt_note` (which is what **Log note** uses).
- The post's body contains the exact text `Attached our welcome kit`.
- The post has at least one `ir.attachment` in `attachment_ids` named
  `welcome_kit.txt`.

## Rules

- Do NOT use **Log note** — the check specifically gates on
  `subtype_id = mail.mt_comment` (Send message), so a Log-note post
  will fail.
- Do NOT rename, archive, merge, or delete the contact.
- Do NOT schedule an activity, star the message, or mark it as To-Do —
  only the Send message + attachment is required.
- The attachment must be the provided `welcome_kit.txt` file. Do NOT
  paste the file content into the message body instead of uploading it,
  and do NOT use a different filename.
- Post exactly **one** message — do not spam the chatter with retries
  or duplicates.
