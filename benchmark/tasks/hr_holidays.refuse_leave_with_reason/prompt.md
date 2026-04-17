# Refuse a time-off request with a reason

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

An employee has submitted a time-off request that must be refused because
it conflicts with a critical project deadline.

## What to do

1. Navigate to **Time Off → Managers → Time Off** (or the manager approval
   view) to see pending requests.
2. Find the pending request from **Marc Demo** for **Paid Time Off**
   dated **June 15 to June 17, 2026** with description
   **"Personal emergency"**.
3. Open the request and click **Refuse**.
4. On the same request, post a chatter message with this exact text:

   ```
   Denied: conflicts with critical project deadline
   ```

## Rules

- Refuse **only** the request from **Marc Demo** — do not refuse or modify
  any other leaves.
- Do **not** approve or validate the request.
- The chatter message must have that exact text as its body.
- Do **not** delete the request.
