# Assign salesperson, move stage, mark Won

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

The opportunity **Bench Big Deal** is a brand-new unassigned pipeline entry
for **Bench Buyer Co** that needs to be claimed by **Bench Rep** and closed
as a win.

## What to do

1. Open the **CRM** app's pipeline (Kanban).
2. Find the opportunity **Bench Big Deal** and open its form.
3. In the **Salesperson** field (near the top of the form, shown with a
   small avatar), set the owner to **Bench Rep**.
4. **Save** the form so the salesperson is committed.
5. In the **status bar** at the top of the form (the breadcrumb-like row of
   stage buttons: New, Qualified, Proposition, Won), click the **Won**
   button to mark this opportunity as won. This moves the stage to **Won**
   and sets probability to 100%.

After the task:
- The opportunity's **Salesperson** should be **Bench Rep**.
- The opportunity's **Stage** should be **Won** (probability **100%**).
- The opportunity must still be **active** (not archived, not Lost).

## Rules

- Do **not** change the customer (must stay **Bench Buyer Co**).
- Do **not** change the expected revenue (must stay **50000**).
- Do **not** click **Lost** — use the **Won** status bar button only.
- Do **not** archive, delete, or convert the opportunity back to a lead.
- Do **not** create any additional opportunities.
