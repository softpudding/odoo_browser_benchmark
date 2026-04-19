Open the **Live Chat** app.

## Step 1 — Create and configure the live chat channel

Create a new live chat channel with these exact values:

- **Channel Name**: `Bench Support`
- **Operators**: add the user `Administrator` (Mitchell Admin) as the only operator.
- **Welcome Message** (on the **Options** tab): `How can we help?`

Save the channel.

## Step 2 — Create a canned response for this channel

From the Live Chat app, open **Configuration → Canned Responses** and create a new canned response with these exact values:

- **Shortcut**: `:hi`
- **Substitution**: `Hi! How can I help you today?`

Save the canned response.

## Step 3 — Verify the widget shows the welcome message

Open the public live chat widget page for the `Bench Support` channel (in the Live Chat app, from the channel form click the **Go to Website** / **Web Page** smart link, or navigate to the channel's public support URL). Verify that the live chat widget loads and that the welcome message **`How can we help?`** appears in the widget.

You do **not** need to send or receive a real chat message — the channel configuration and the widget displaying the welcome message are enough.

**Rules:**
- Do not rename the channel after saving it.
- Do not remove or replace the Administrator operator.
- Do not create more than one channel named `Bench Support`.
- Do not create more than one canned response with the shortcut `:hi`.
- Do not delete any other existing live chat channel or canned response.
