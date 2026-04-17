# Configure three ticket tiers on an event

You are in the Odoo 19 **Events** app logged in as **Administrator**.

The upcoming event **Summer DevCon 2026** needs three ticket tiers
(Early Bird / Regular / VIP) added to its Tickets table before the
marketing email goes out.

## What to do

1. Open the **Events** app and open the event **Summer DevCon 2026**.
2. Go to the **Tickets** tab of the event form.
3. The tickets table is empty. Click **Add a line** three times (or add
   rows one-by-one) to create exactly **three** tickets with these
   values:

| Ticket name | Price | Maximum Attendees |
|-------------|-------|-------------------|
| `Early Bird` | `99.00` | `80` |
| `Regular`    | `149.00` | `200` |
| `VIP`        | `299.00` | `40` |

4. Save the event.

## Rules

- Create **exactly three** ticket tiers — no more, no fewer.
- Names must match exactly: `Early Bird`, `Regular`, `VIP`.
- Prices and seat limits must match exactly the table above.
- Do **not** modify any other fields on the event (dates, name,
  organizer, etc.).
- Do **not** create tickets on any other event.
