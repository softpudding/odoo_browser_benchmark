# Mark opportunity Lost with reason, and reassign

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

The opportunity **Acme – Q3 renewal** needs to be marked **Lost**
because the prospect chose a competitor. You also need to reassign
this record to salesperson **Mitchell Admin** for the post-mortem.

## What to do

1. Open the **CRM** app's pipeline.
2. Find the opportunity **Acme – Q3 renewal** and open it.
3. Change the **Salesperson** to **Mitchell Admin**.
4. Click the **Lost** button in the opportunity statusbar. A dialog
   opens asking for the Lost Reason.
5. In the dialog, select the Lost Reason **Too expensive** and click
   **Confirm** / **Mark as Lost**.

After the task:
- The opportunity should be archived (active=False).
- Its **Lost Reason** should be **Too expensive**.
- Its **Salesperson** (`user_id`) should be **Mitchell Admin**.

## Rules

- Do not delete the opportunity.
- Do not modify its name, partner, or revenue.
- Do not create any new opportunities.
