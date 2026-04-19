# Create an inbound mail alias that routes to a CRM team's leads

You are in the Odoo 19 **Settings** app logged in as **Administrator**.

The sales team **Bench Alias Team** already exists in CRM, but there is no
inbound mail alias configured to route prospect emails into it as new leads.
You need to create a `mail.alias` that, when an email arrives at
`benchalias@<your-domain>`, creates a new `crm.lead` assigned to the
**Bench Alias Team**.

The alias configuration UI lives under **Settings → Technical → Email →
Aliases**, which is **only visible when developer mode is active**. You must
enable developer mode first.

## What to do

### Step 1 — Activate Developer Mode

1. You are already on the Settings page. Scroll all the way to the bottom
   of the General Settings until you see a **Developer Tools** section.
2. Click the **Activate the developer mode** link (the regular one, NOT
   "with assets" and NOT "with tests assets"). The page will reload with
   `?debug=1` in the URL. After the reload, a new **Technical** submenu
   appears in the Settings top menu bar.

### Step 2 — Open the Aliases list

1. In Settings, click the top menu **Technical**. In its dropdown, hover
   **Email** and click **Aliases**. You should land on a list view titled
   *Aliases* (model `mail.alias`).
2. Click **New** in the top-left to open a blank alias form.

### Step 3 — Fill the alias form

Fill in the form exactly as follows:

1. **Alias name** (the large inline input before the `@` at the top of the
   form): type `benchalias`. Leave the domain (the right-hand dropdown
   after `@`) at its existing default value.
2. **Document Model** (`alias_model_id` field): set to the `crm.lead`
   model. Type `crm.lead` into the field; the autocomplete shows one
   entry whose label is **Lead** (the `_description` of `crm.lead`).
   Click that entry. Do NOT pick any "Create ..." autocomplete option —
   that would create a brand-new `ir.model` row, which is wrong.
3. **Default Values** (`alias_defaults` field, a multi-line text area
   expecting a Python dict literal): type exactly
   `{'team_id': <TEAM_ID>}`, replacing `<TEAM_ID>` with the numeric
   database id of the **Bench Alias Team** sales team. To find that id,
   open a new browser tab, go to Settings → Technical → Database Structure
   → **Sales Teams** (or use the URL `/odoo/action-base.action_ir_model`
   is not needed — simpler: open the CRM app, click **Configuration →
   Sales Teams**, click the *Bench Alias Team* row, and read the ID off
   the URL — it is the integer after `&id=` or the last path segment of
   `/odoo/settings/.../<id>`). Return to the alias form and paste the
   value.
4. **Alias Contact Security** (`alias_contact` field): set to **Everyone**
   (the `everyone` option — incoming mail from any sender is accepted).
5. Leave every other field (Owner, Parent Model, Default Target Record,
   Custom Bounced Message, Alias Incoming Local) at its default.

### Step 4 — Save

Click the form **Save** button (cloud / floppy-disk icon in the top-left
breadcrumb area).

## Expected end state

- A `mail.alias` row exists with `alias_name` = `benchalias`.
- That alias has `alias_model_id` pointing to the `crm.lead` ir.model.
- That alias has `alias_defaults` containing the key `team_id` whose
  value equals the database id of the **Bench Alias Team** sales team.
- That alias has `alias_contact` = `everyone`.
- The **Bench Alias Team** sales team still exists (you did not rename,
  archive, or delete it).

## Rules

- Do NOT rename, archive, or delete the `Bench Alias Team` sales team.
- Do NOT create a second `mail.alias` with `alias_name='benchalias'` —
  exactly one must exist.
- Do NOT modify the team's own inline `alias_name` field on the team form
  — the alias you need lives in the generic Aliases list under
  Settings → Technical → Email → Aliases.
- Do NOT pick a different model than `crm.lead` (its display label is
  **Lead**). The CRM Team model (`crm.team`) is NOT the correct one.
- Do NOT set `alias_contact` to "Authenticated Partners" or "Followers"
  — the task calls for **Everyone**.
- The `alias_defaults` value must be a valid Python dict literal that
  parses (via `ast.literal_eval`). `{'team_id': N}` with the correct
  integer N is required; `{}` is NOT sufficient.
