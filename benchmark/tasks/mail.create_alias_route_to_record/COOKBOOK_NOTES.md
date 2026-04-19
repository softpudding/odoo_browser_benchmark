# mail.create_alias_route_to_record — Odoo 19 quirks

## Developer mode is a client-side session flag, not a server group

- `base.group_no_one` (Technical Features) is only *effective* when the
  browser session's `debug` flag is truthy. `res.users.has_group(...)`
  explicitly returns `False` for `base.group_no_one` when
  `request.session.debug` is falsy (see `odoo/addons/base/models/
  res_users.py:has_group`). Seeding the group on admin is required but
  not enough — the agent (or oracle) still has to flip the session flag
  through the UI.
- The Developer Tools widget (`res_config_dev_tool`) renders at the
  bottom of the base Settings form (`addons/base_setup/views/
  res_config_settings_views.xml:199`). Its "Activate the developer
  mode" link calls `router.pushState({ debug: 1 }, { reload: true })`,
  triggering a **full page reload**. Playwright must
  `wait_for_url("**debug=1**")` AND re-wait for `.o_action_manager`
  after the reload — `_wait_for_ready` alone is not sufficient.
- There are three variants of the link ("Activate the developer mode",
  "… (with assets)", "… (with tests assets)"). Plain
  `page.locator("a:has-text('Activate the developer mode')")` matches
  all three; use `.filter(has_not_text='assets').filter(has_not_text='tests')`
  or `#developer_tool a:first-of-type`.

## ir.model autocomplete

- `ir.model._description` is literal `"Lead"` for `crm.lead`, NOT
  `"Lead/Opportunity"`. Searching the `alias_model_id` many2one for
  "Lead/Opportunity" returns zero hits; the only autocomplete rows are
  the quick-create variants ("Create 'Lead/Opportunity'", "Create and
  edit..."). Click one and it will call `ir.model.name_create(...)`,
  spawning a new custom `x_<name>` model row. Use the technical name
  **`crm.lead`** (one unique result via
  `_rec_names_search = ['name', 'model']`).

## Filtering quick-create options from many2one autocomplete

- The autocomplete dropdown (`ul.o-autocomplete--dropdown-menu`) uses
  `<li class="o-autocomplete--dropdown-item">` for every option. The
  Create / Search-More variants get the **additional** class
  `o_m2o_dropdown_option` (directly on the `<li>`) — see
  `addons/web/static/src/views/fields/relational_utils.js:489`.
- Playwright's `has_not=page.locator(...)` filters by **descendants**,
  not by a class on the element itself. The reliable filter is the
  CSS pseudo-class on the same element:

  ```python
  items = page.locator(
      "ul.o-autocomplete--dropdown-menu "
      "li.o-autocomplete--dropdown-item:not(.o_m2o_dropdown_option)"
  ).filter(has_text="Lead")
  ```

  or iterate and check `item.get_attribute("class")` for
  `o_m2o_dropdown_option` before clicking.

## mail.alias form quirks

- The generic `mail.alias` form view (NOT the one embedded in
  `crm.team`) renders `alias_contact` as a native `<select>`, so
  `page.locator(...).select_option(label='Everyone')` works. Unlike
  `crm.team.alias_contact`, which uses Odoo's custom `o_select_menu`
  widget and requires the click-toggler-then-click-item pattern.
- `alias_defaults` is a plain Text field rendered as a `<textarea>`.
  After interacting with the m2o above, a leftover autocomplete
  dropdown or tooltip frequently covers the textarea; Playwright
  reports `subtree intercepts pointer events`. Dismiss via:

  ```python
  page.evaluate(
      "document.querySelectorAll('.o-tooltip, .tooltip, "
      ".o-autocomplete--dropdown-menu, .o-dropdown--menu')"
      ".forEach(el => el.remove())"
  )
  page.keyboard.press("Escape")
  ```

  then `click(force=True)` or `ta.evaluate('el => el.focus()')`.
- `alias_defaults` is stored as a string. The check parses it with
  `ast.literal_eval` and asserts the resulting dict contains the
  expected `team_id`. Empty string and `'{}'` are both rejected by a
  strict check that requires the key.

## Menu gating

- `mail_alias_menu` (under `base.menu_email` "Email") is gated by
  `groups="base.group_no_one"` — it only appears in Settings →
  Technical → Email after developer mode is on. Direct action URLs
  like `/odoo/action-mail.mail_alias_action` still resolve even
  without debug mode because the menu is only a view hint, but
  browser agents usually cannot "guess" the URL and rely on the menu.

## Seed hygiene

- `mail.alias.alias_name` is UNIQUE per `alias_domain_id`. Seed must
  release any stale alias with the target `alias_name` from prior runs
  (`stale.sudo().write({'alias_name': False})` then unlink) or the
  agent's Save hits a `UniqueViolation`.
- `mail.alias.mixin._alias_get_creation_values` fails when no
  `mail.alias.domain` exists. Seed creates a default domain if the
  base snapshot has none.
- `crm.team.use_leads=True` is required for the team to be a valid
  target of an `alias_defaults = {'team_id': ...}` routing — otherwise
  `mail.thread.message_process` would ignore incoming mail. Seed sets
  it explicitly.
