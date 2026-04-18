Your marketing team wants to showcase **Bench Happy Client** as a public customer reference on the company website.

The contact **Bench Happy Client** has already been seeded in the Contacts app with the required fields filled (country, website, "Implemented by" reference partner) so it qualifies to appear on the public `/customers` page. It is currently **unpublished**.

Complete all of the following, in order:

1. Open the **Contacts** app (URL `/odoo/contacts`).
2. Find and open the company contact **Bench Happy Client**.
3. From the contact form, click the **Go to Website** smart button in the top button box (the one with a red globe icon that says "Unpublished" in its tooltip) to preview the public customer page. You should land on `/partners/<slug>` (admin can preview it even while unpublished).
4. On that preview page, in the top systray, click the **Unpublished** toggle to flip it to **Published**. This publishes the customer reference.
5. Navigate to the public `/customers` page (you can simply go to `/customers` in the address bar) and confirm that **Bench Happy Client** now appears in the list of customer references.

# Rules

- Do not rename the contact.
- Do not change the contact's country, website, address, or "Implemented by" partner.
- Do not create or delete any other contacts.
- Do not unpublish the contact after publishing it.
- The final state must have `Bench Happy Client` visible on `/customers`.
