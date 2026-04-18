# crm.create_lead_from_email_alias_log_message — Odoo 19 quirks

## crm.team Email Alias and alias_contact widgets

- The Email Alias is **NOT** in a dedicated Settings panel — it lives in
  the main **Team Details** group on `crm.team` form (right after
  `user_id`), split across two inline `.oe_inline` inputs for
  `alias_name` and `alias_domain_id` with an `@` between them.
  Target by `.o_field_widget[name='alias_name']` — `name='alias_id'` is a
  different readonly mirror.
- The whole alias block is wrapped in `invisible="not use_leads and not
  use_opportunities"`. If the team has neither `use_leads` nor
  `use_opportunities` enabled, the alias fields are NOT rendered — seed
  must enable at least one.
- `alias_contact` (Selection `'everyone' | 'partners' | 'followers'`)
  renders as Odoo's **custom** `o_select_menu` widget — NOT a native HTML
  `<select>`. `set_selection` helper (which calls
  `select.select_option(label=...)`) times out. Pattern that works:

  ```python
  page.locator(".o_field_widget[name='alias_contact'] .o_select_menu_toggler").click()
  page.locator(".o_select_menu_menu .o_select_menu_item:has-text('Authenticated Partners')").click()
  ```

## crm.lead form name field is a textarea

`crm.lead.name` is rendered with `widget="text"` on the form — produces a
textarea, not an input. `oracle_helpers.fill_field` (queries
`.o_field_widget[name='name'] input`) will time out. Use `fill_text_field`
which queries `textarea`.

## Priority star indexing (Low / Medium / High)

`crm.lead.priority` is `[('0','Low'), ('1','Medium'), ('2','High'),
('3','Very High')]`. Widget renders **N-1 stars**. Click index 0 → `'1'`
(Medium / single star). Click index 2 → `'3'` (Very High / three stars).
Prompt phrasing matters: "click only the FIRST star (Medium)" reliably
yields priority='1'. "Set priority to Medium" without the explicit-first
modifier leaves agents likely to miss-click.

## Seed alias hygiene

- When the 'Inbound' team already has `alias_name == target`, seed must
  null it first (`team.write({'alias_name': False})`) so the task
  registers as a genuine state change.
- Alias names are unique per domain. If a stale alias from a prior run
  owns the target `alias_name`, releasing it is required before the agent
  can Save without `UniqueViolation`.
- `mail.alias.domain` must exist; `mail.alias.mixin._alias_get_creation_values`
  requires a default domain. Seed should create one if missing.

## Calibration trap stacking (hard tier)

The first pass of this task (alias + create lead + chatter only) passed
BU with F1=1.0 in 228s on a single run — chatter and alias-name edits are
too visually obvious. Hardened by stacking:
1. `alias_contact` dropdown (custom select-menu, non-default value)
2. Priority = single star (Medium, not three stars)
3. Mandatory `Website` tag with distractor `Web-Inquiry` in autocomplete

Post-hardening BU hit 5/5 state diff but silently skipped the tag step →
postcondition FAIL. The three orthogonal calibration traps are cheap to
add and produce the characteristic "state-diff perfect but one
postcondition missing" hard-tier failure mode.
