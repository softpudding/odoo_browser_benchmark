# Configure an inbound CRM team alias and log a prospect lead

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

The "Inbound" sales team has already been created, but its email alias is
not configured and its mailbox-security policy is still the default. Marketing
just passed along an inbound prospect inquiry over the phone — you need to log
it as a lead (with the correct tag and priority) and record what the prospect
asked about.

## What to do

### Step 1 — Configure the team's Email Alias

1. From the CRM top menu, open **Configuration → Sales Teams**.
2. Open the team named **Inbound**.
3. In the **Team Details** group (left side of the form), find the
   **Email Alias** field (two inline inputs separated by `@`). Type
   `leads-inbound` into the left input (the alias name). Leave the right
   input (the domain) at its existing default value.
4. Just below the alias, find the **Accept Emails From** dropdown. Change
   it from its default **Everyone** to **Authenticated Partners**.
5. **Save** the team form.

### Step 2 — Create the lead manually

1. Go back to the CRM app (breadcrumb or top menu).
2. Switch the CRM pipeline to the **Leads** view (open the top menu
   **Leads → Leads**). If Leads is not visible on the top bar, it is under
   the **Leads** submenu.
3. Click **New** to create a lead. Fill in:
   - **Opportunity / Lead Name**: `Inbound Inquiry from Sample`
   - **Email**: `prospect@external.test`
4. Set **Priority** to **Medium** — click only the **first** star
   (leaving a single star filled). Do NOT click all three stars.
5. Add the existing tag **Website** in the **Tags** field (it is in the
   right-hand column of the lead form).
6. **Save** the lead.

### Step 3 — Log a chatter message on the lead

1. While still on the lead you just saved, scroll down to the chatter.
2. Click **Send message** (NOT "Log note").
3. Type this text exactly:

   `Asked about Bench Pro pricing.`

4. Click the **Send** button to post the message.

## Expected end state

- The `Inbound` sales team has email alias `leads-inbound` and
  **Accept Emails From** set to **Authenticated Partners**.
- Exactly one lead named `Inbound Inquiry from Sample` exists with email
  `prospect@external.test`, priority **Medium** (one star), and the
  **Website** tag.
- The lead has a regular chatter comment (not an internal note) whose body
  is `Asked about Bench Pro pricing.`.

## Rules

- Do not rename the `Inbound` team.
- Do not archive any team, lead, or opportunity.
- Do not create a second lead — create exactly one with the name above.
- The chatter text must appear as a **message** (Send message), not a
  **log note** — the distinction matters.
- Do not convert the lead into an opportunity.
- Do not set the priority to High (two stars) or Very High (three stars) —
  the correct value is exactly **one** star (Medium).
