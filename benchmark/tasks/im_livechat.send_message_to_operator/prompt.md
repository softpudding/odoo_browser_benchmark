A live chat channel named `Bench Help` is configured and the Administrator is its only operator. Your job is to act as a visitor: open the public livechat widget for this channel, start a chat, and send a first message asking for help.

### Steps

1. Navigate to the public livechat support page for the `Bench Help` channel. This is the page that renders the embedded chat widget for the visitor. The URL is `/im_livechat/support/<channel_id>` where `<channel_id>` is the id of the `Bench Help` live chat channel — you can discover the id in the Live Chat back-office, or simply open the Live Chat app, click the `Bench Help` channel, and follow the `Go to Website` / widget URL.
2. Wait for the livechat widget to load. The floating `Chat with us` button (rendered inside the page's livechat widget, shadow DOM root `.o-livechat-root`) should appear at the bottom of the page.
3. Click the `Chat with us` button to open the chat window.
4. In the chat composer at the bottom of the widget, type exactly: `Hello, I need help`
5. Send the message (press Enter, or click the Send button).

### Expected outcome

- A brand-new `discuss.channel` of type `livechat`, linked to the `Bench Help` live chat channel, has been created.
- That channel contains at least one message whose body contains the word `help` — specifically the `Hello, I need help` text you just sent.
- The message was posted by you acting as a public visitor (not as the Administrator reply inside Discuss).

### Rules

- Do NOT create the chat session by directly calling ORM methods or posting messages via `/odoo/discuss`; the message MUST come in through the public livechat widget on the support page.
- Do NOT change the `Bench Help` channel configuration (no editing its name, operators, button text, or welcome message).
- Do NOT type any other message before the required one, and do NOT delete the channel afterwards.
- You do not have to wait for the operator to reply — once the `Hello, I need help` message is visible in the widget's chat thread, the task is done.
