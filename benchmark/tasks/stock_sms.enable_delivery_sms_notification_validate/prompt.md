Enable the delivery **Text Confirmation** setting and validate a pending delivery so it triggers an SMS to the customer.

## Step 1 — Enable Text Confirmation for deliveries

1. Open the **Inventory** app.
2. Go to **Configuration > Settings**.
3. Under the **Operations** block, find the **Text Confirmation** setting and tick its checkbox (label: *Send an automatic confirmation Text Message when Delivery Orders are done*).
4. Leave the confirmation type set to **SMS** (the default).
5. Click **Save** in the control panel.

## Step 2 — Validate the pending delivery

1. From the Inventory dashboard, open the **Delivery Orders** card.
2. Open the transfer **S-BENCH-SMS-001** (customer: *Bench SMS Customer*, ordered quantity is already filled in).
3. Click **Validate**.
4. If a confirmation dialog titled **SMS** appears (*"You are about to confirm this Delivery Order by SMS Text Message"*), click **Confirm** to send the SMS. Do NOT click *Disable SMS* or *Cancel*.

## Rules

- Do not change the customer, the product, the quantities, or the phone number on the picking.
- Do not edit the picking's scheduled date or reference.
- Do not click *Disable SMS* in the confirmation dialog — that would turn the feature off.
- Send the SMS exactly once.
