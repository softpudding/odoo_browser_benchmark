A visitor has just started a new live chat session on the website and is waiting for an operator to respond. Your job is to handle the conversation from the Discuss back-office by replying with the pre-configured canned response.

### Pre-seeded state

- Live Chat channel `Bench Support` with admin as the registered operator and a default URL rule already exists.
- A canned response is available with shortcut `hello` and substitution text: `Hi, thanks for reaching out!`
- A live chat conversation is already open in Discuss titled `Visitor #BENCH-359` with one incoming message from the visitor: `Hi there`.

### Steps

1. From the Discuss app, open the live chat session `Visitor #BENCH-359` in the sidebar (under the Live Chat category).
2. Click into the message composer at the bottom.
3. Insert the canned response by typing the shortcut trigger `::hello` — the Discuss composer will show a suggestion popover. Select the `hello` canned response from the popover so the composer replaces `::hello` with the full substitution text `Hi, thanks for reaching out!`.
4. Send the message (press Enter, or click the Send button).

### Expected outcome

The live chat session `Visitor #BENCH-359` now has a new message from the Administrator (after the visitor's `Hi there`) whose content is exactly `Hi, thanks for reaching out!` — the exact canned-response substitution, not the literal shortcut.

### Rules

- Do NOT type the full substitution text manually — you must use the `::hello` canned-response shortcut and let the suggestion popover substitute the text.
- Do NOT send the literal text `::hello` or `:hello` as the message — that is not a valid reply; the suggestion popover must replace the shortcut first.
- Do NOT edit the canned response or the live chat channel configuration.
- Do NOT rename or close the conversation.
- Do NOT post any additional messages beyond the one canned-response reply.
