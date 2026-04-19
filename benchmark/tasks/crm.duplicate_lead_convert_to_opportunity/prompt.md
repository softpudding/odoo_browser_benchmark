# Duplicate a lead and convert the copy to an opportunity

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

The Sales manager asked you to clone an existing qualification **Lead** record
and turn the copy into a real **Opportunity** with its own brand-new customer.
The original lead must remain untouched as a template for future
qualifications.

## What to do

### Step 1 — Open the seeded lead

1. From the CRM top menu, open **Leads → Leads**.
2. Open the lead named **Bench Template Lead** (type: Lead).

### Step 2 — Duplicate the lead via the cog / Actions menu

1. On the lead form, click the **cog / gear** icon in the control-panel to
   open the **Actions** dropdown.
2. Click **Duplicate** in the Actions menu. Odoo opens a copy of the lead
   whose name is `Bench Template Lead (copy)`.

### Step 3 — Rename the copy and save

1. Change the **Opportunity / Lead Name** (large title field at the top)
   from `Bench Template Lead (copy)` to exactly `Bench Cloned Opp`.
2. Click **Save** to commit the rename.

### Step 4 — Convert the copy to an Opportunity

1. With the saved `Bench Cloned Opp` lead still open, click the
   **Convert to Opportunity** button in the form header (top-left, next to
   Won / Lost).
2. The **Convert to opportunity** wizard opens. For **Conversion Action**,
   make sure **Convert to opportunity** is selected (NOT *Merge with
   existing opportunities* — the wizard may auto-pick merge because the
   duplicated lead still shares the template's email address; click the
   **Convert to opportunity** radio explicitly).
3. In the **Related Customer** radio group, click **"Link to an existing
   customer"** (the second radio option). The **Customer** autocomplete
   field appears.
4. Click the **Customer** autocomplete, type `Bench Cloned Customer`, and
   click the **Create "Bench Cloned Customer"** option at the bottom of the
   dropdown (this creates a brand-new customer record on the fly).
5. Click **Create Opportunity** to apply the wizard.

## Expected end state

- The original lead **Bench Template Lead** still exists unchanged, with
  `type = lead`.
- A second record **Bench Cloned Opp** now exists with `type = opportunity`
  and its Customer set to the newly-created **Bench Cloned Customer**.

## Rules

- Do **NOT** edit the original `Bench Template Lead` record — it must stay a
  Lead (not an Opportunity), and its name must not change.
- Do NOT create the new record from scratch with the **New** button — you
  must Duplicate the existing `Bench Template Lead` via the cog/Actions
  menu (this preserves the template's description/tags on the copy).
- In the wizard, you MUST pick **"Link to an existing customer"** and
  quick-create the customer — do not select "Create a new customer" (that
  radio auto-generates a customer from the lead's contact name, which would
  produce the wrong partner name).
- Do not archive, delete, or rename the original lead.
