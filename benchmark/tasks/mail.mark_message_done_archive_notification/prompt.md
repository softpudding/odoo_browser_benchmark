# Mark an inbox notification as done

You are in the Odoo 19 **Discuss** app logged in as **Administrator**.

Your **Inbox** contains a notification from a colleague named
**Bench Notifier** about scheduled system maintenance. You need to
**mark that notification as done** so it is removed from the Inbox.

## What to do

1. Open the **Discuss** app.
2. In the left sidebar, click **Inbox** (at the top, under the Mailboxes
   section).
3. In the inbox list, find the message whose body contains:

   **"System maintenance scheduled for Saturday."**

4. Hover that message to reveal its action toolbar.
5. Click the **check icon** (titled **"Mark as Read"** / **"Mark as
   Done"**) in the message action toolbar. The message should disappear
   from the Inbox.

## Rules

- Mark exactly **one** notification as done — the Bench Notifier
  maintenance message.
- Do **not** delete, reply to, edit, or star the message. The original
  `mail.message` record must still exist; only the `mail.notification`
  for your user is being flagged read.
- Do **not** use "Mark all as read" — only mark the target notification.
