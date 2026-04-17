# Reply in-thread to a specific Discuss message

You are in the Odoo 19 **Discuss** app logged in as **Administrator**.

The team channel **#benchmarks-ops** already has a message from a
colleague asking whether the 3-AM nightly job can be rescheduled. You
need to **reply to that specific message as an in-thread reply**
(not a new top-level message in the channel).

## What to do

1. Open the **Discuss** app.
2. In the left sidebar (Channels section), click the channel
   **#benchmarks-ops**.
3. In the channel timeline, find the message:

   **"Can we move the 3 AM warehouse sync to 5 AM? It's colliding with
   EU backups."**

4. Hover the message and click the **Reply in Thread** action (the
   speech-bubble / reply icon in the message hover toolbar). A thread
   panel opens on the right.
5. In the thread panel, post exactly the following reply:

   ```
   Yes — rescheduling to 5 AM on weekdays, Ops will update the cron tonight.
   ```

6. Send the reply so it appears as a threaded reply under the original
   message.

## Rules

- The reply must be an **in-thread reply** — it must have its
  `parent_id` pointing at the target message. A new top-level message
  in the channel **does not count**.
- The reply must contain the exact sentence above.
- Do **not** edit, delete, or react to the original message — only reply
  to it.
- Do **not** post anything in any other channel.
