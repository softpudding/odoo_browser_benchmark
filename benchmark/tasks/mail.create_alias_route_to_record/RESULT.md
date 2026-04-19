# mail.create_alias_route_to_record — evaluation record

| Field | Value |
|---|---|
| Task ID | `mail.create_alias_route_to_record` |
| Row | 422 |
| Difficulty | hard |
| Tier | 3 |
| Oracle | PASS (F1=1.0, 43.1s wall clock, 2/2 atomic edits matched, 0 postcondition failures) |
| Browser-Use | PASS (F1=1.0, 176.6s single-shot, 0 postcondition failures, 50 non-forbidden writes) — **calibration MISS** |
| Odoo modules | mail (`mail.alias`) + crm (`crm.team`, `crm.lead` as alias target) + settings form (Developer Tools widget) |

## Workflow

Seed creates the sales team `Bench Alias Team` (with `use_leads=True` so
lead routing is enabled), ensures a default `mail.alias.domain` exists,
releases any stale `mail.alias` with `alias_name='benchalias'` from prior
runs, and explicitly grants admin `base.group_no_one` so developer mode
actually unlocks the Technical menu once the client flag is toggled.

Agent flow:

1. On `/odoo/settings`, scroll to the bottom of the General Settings
   form, find the **Developer Tools** panel, click **Activate the
   developer mode**. The page reloads with `?debug=1`.
2. Navigate to Settings → Technical → Email → Aliases (action
   `mail.mail_alias_action`). Click **New**.
3. Fill `alias_name='benchalias'`; set `alias_model_id` to the
   `crm.lead` model (autocomplete label **Lead**, avoiding the
   "Create 'xxx'" quick-create entries); fill `alias_defaults` with the
   Python dict literal `{'team_id': <id>}` where `<id>` is the seeded
   team's database id; set `alias_contact` to **Everyone**. Save.

## Capability tested

The Technical submenu, and with it the entire `mail.alias` configuration
form, is hidden until the client session flag `debug` is toggled on via
the "Activate the developer mode" link in the Developer Tools section of
Settings. The agent must (a) recognise that the absence of the
Technical menu is intentional, (b) locate and click the dev-mode link
deep inside the settings form, (c) survive the hard page reload, then
(d) correctly fill four different widget types on the alias form,
including a Python-dict literal in a free-form textarea.

## Notes

**Calibration MISS.** Browser-use passed single-shot on the first real
attempt (F1=1.0, 176.6s, 50 non-forbidden writes, 0 postcondition
failures). BU had no trouble recognising the developer-mode gate,
finding the link in the Developer Tools panel, navigating to
Settings → Technical → Email → Aliases after the reload, and filling
the alias form. The `alias_defaults` Python dict field and the
`alias_model_id` disambiguation (Create-variant vs real model entry)
did not trip it up in this run.

**Cookbook quirks solidified:**

1. `ir.model._description` for `crm.lead` is `"Lead"` (not
   "Lead/Opportunity"). The alias form's `alias_model_id` many2one
   autocompletes by `ir.model._rec_names_search = ['name', 'model']`,
   so typing "Lead/Opportunity" returns **zero** real results and only
   the Create variants. The reliable query is the technical name
   `crm.lead` (unique match).
2. The many2one autocomplete dropdown uses `<li
   class="o-autocomplete--dropdown-item ...">` for every option; Create
   / Search-More variants get an extra `o_m2o_dropdown_option` class
   on the same `<li>`. Playwright's `:not(.o_m2o_dropdown_option)`
   selector reliably filters them out, but `has_not=page.locator(...)`
   does not (it only checks descendants, not self).
3. `base.group_no_one` on admin is only **effective** when the session
   `debug` flag is truthy; admin getting the group via seed is a
   necessary but not sufficient precondition. The user still has to
   click the dev-mode link (or append `?debug=1` to the URL) to unlock
   the Technical menu.
4. The Developer Tools widget (`res_config_dev_tool`) calls
   `router.pushState({ debug: 1 }, { reload: true })` — Playwright
   needs to wait explicitly for the URL to include `debug=1` and for
   `.o_action_manager` to re-render after the hard reload; a bare
   `_wait_for_ready` is not enough.
5. `alias_defaults` is a free-form Text field stored as a Python dict
   literal string. The check parses it with `ast.literal_eval` and
   asserts `team_id == seeded_team.id`. Empty `{}` is rejected.
6. After typing into `alias_model_id` the autocomplete can leave a
   floating dropdown/tooltip that intercepts pointer events on the
   textarea below — Playwright must dismiss `.o-tooltip`,
   `.o-autocomplete--dropdown-menu`, and `.o-dropdown--menu` before
   clicking `alias_defaults`.

**To escalate to a real BU-failing hard task (future iteration):**

- (i) Require the agent to type a *non-trivial* `alias_defaults`
  dict with two keys (e.g., `{'team_id': N, 'user_id': M}`) so a
  second lookup is needed.
- (ii) Require `alias_contact='followers'` AND add a follower via
  the chatter (double-value-edit plus cross-surface).
- (iii) Add a distractor `mail.alias` pre-seeded with a similar
  `alias_name` (e.g. `benchalias_old`) so the agent must create a
  NEW row rather than editing the distractor.
- (iv) Require setting `alias_force_thread_id` to a specific lead id
  so incoming mail lands on an existing record rather than creating
  one.
