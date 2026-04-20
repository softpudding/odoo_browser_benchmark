Go to the **Live Chat** app.

Create a new live chat channel with these values:
- **Channel Name**: `Support Routing`
- **Notification Text**: `Talk to support now`
- **Agents**: `Administrator` and `Demo User`
- **Concurrent Sessions** / max sessions mode: set it to **Limited**
- **Max Sessions**: `1`

On the **Rules** page, add exactly one rule:
- **URL Regex**: `/support`
- **Action**: display the chat button (do not hide it)

Save the channel.

Rules:
- Create exactly one rule.
- Do not add more than those two agents.
- Keep max sessions limited to 1.
