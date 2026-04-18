# Cookbook notes — crm.assign_team_change_salesperson_log_activity

## crm.lead form: team_id is hidden on opportunities by default

In Odoo 19, the `crm.lead` form view (`crm.crm_lead_view_form`) has TWO copies
of the user_id/team_id group:

- One under `<group invisible="type == 'lead'">` — shows just `user_id` with
  the `many2one_avatar_leader_user` widget. Visible only on opportunities.
- One under `<group invisible="type == 'opportunity'">` — shows BOTH
  `user_id` and `team_id`. Visible only on leads.

So on an **opportunity**, `team_id` is **NOT** present in the main form
header. The only place it appears editable is under the **Contacts** notebook
tab (`<page name="lead" string="Contacts" invisible="type == 'lead'">`),
inside the **Ownership** group.

**Implication for tasks**: a "change Sales Team" instruction on an
opportunity must explicitly tell the agent to open the Contacts tab; agents
that scan only the form header will not find a `team_id` field. Oracle
scripts must do `click_tab(page, "Contacts")` before targeting
`.o_field_widget[name='team_id']`.

## Seeding new sales teams

The base snapshot only ships the `Sales` team (`sales_team.team_sales_department`)
plus inactive `Website` and `Point of Sale` teams. Tasks that need teams
named like "Direct Sales" or "Channel" must create them in seed.py:

```python
team = env["crm.team"].with_context(active_test=False).search(
    [("name", "=", "Channel")], limit=1
)
if not team:
    team = env["crm.team"].create({
        "name": "Channel",
        "sequence": 2,
        "company_id": False,
    })
```

To make the salesperson selectable in the team's domain (some many2one
widgets filter users by team membership), add the user to `member_ids`:

```python
team.write({"member_ids": [(4, sara.id)]})
```
