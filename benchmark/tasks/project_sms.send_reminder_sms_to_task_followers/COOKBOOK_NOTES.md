# Cookbook notes — project_sms.send_reminder_sms_to_task_followers

Quirks uncovered while building this task. Folded into
`benchmark/ODOO19_PATTERNS.md § project_sms`.

## project_sms install is transitive

- `project_sms.__manifest__`: `auto_install=True`,
  `depends=['project','sms']`. Neither `sms` nor `project_sms` is in
  `benchmark/base_modules.txt`. `button_immediate_install('sms')` alone
  pulls `project_sms` in as part of dependency resolution; no need to
  install `project_sms` explicitly (seed does so defensively).

## Send SMS lives on cog Actions only — NOT in chatter

- The bridge registers `sms.composer` via
  `binding_model_id=project.task` with
  `binding_view_types="list,kanban,form"`. This surfaces exclusively in
  the cog Actions menu on list/kanban/form views of `project.task`.
- There is NO chatter-level Send SMS button in Odoo 19 Community for
  `project.task`. The user spec said "chatter → Send SMS"; that's
  inaccurate — the only entry point is cog Actions.

## Mass mode is one-sms-per-record, driven by partner_id

- The binding context is
  `{'default_composition_mode':'mass','default_mass_keep_log':True,'default_res_ids': active_ids}`.
- `sms.composer._action_send_sms_mass` iterates the selected records
  and calls `_prepare_recipient_values(records)` → each record's
  `_sms_get_recipients_info` returns its `partner_id` with the
  partner's phone. `message_follower_ids` is NOT consulted.
- To get N sms.sms rows from a single Send SMS action, seed N records
  (each with its own partner_id) and multi-select them all.

## project.task list view collapses when stage_id is null

- `project.task.stage_id` has `group_expand='_read_group_stage_ids'`.
  If a task has no stage, it is grouped under a virtual "None" column
  that is collapsed by default in the kanban view, and the list view
  inherits this collapse if it was last rendered as kanban in the same
  session.
- Oracle symptom: `.o_list_view .o_data_row` locator never resolves
  visible after switching to list, despite rows existing in the DB.
- Fix: seed a real `project.task.type` pinned to the project with
  `fold=False` and set `stage_id=<that stage>.id` on every seeded
  task. A single stage named "Review" is sufficient.

## Project kanban card click navigates straight to the tasks action

- `view_project_kanban` declares `<kanban action="action_view_tasks"
  type="object">` at the root, so any click on a card body invokes
  `action_view_tasks()` → `act_project_project_2_project_task_all`
  with `search_default_open_tasks=1`.
- URL lands at `/odoo/project/{project_id}/tasks`; breadcrumb shows
  the project name (not "Tasks"), so oracles should wait for
  `.o_action_manager .o_kanban_view, .o_list_view` rather than
  matching on breadcrumb text.

## Mass-mode composer footer buttons

- Primary highlighted: `button[name='action_send_sms']` labelled
  **Put in queue** — creates `sms.sms` rows with `state='outgoing'`
  but does NOT call `.send()`.
- Secondary: `button[name='action_send_sms_mass_now']` labelled
  **Send now** — writes `mass_force_send=True` then calls the same
  `action_send_sms` which now invokes `.send()`.
- Both paths persist `sms.sms` rows before any IAP call, so
  check.py/state_diff see the rows either way. The `state` field
  distinguishes queued-vs-attempted-send and is environment-dependent
  (flips to `error` without IAP credits); keep it in `ignore_fields`.

## Send-success detection is BU's weak spot here

- BU in this task correctly sent SMS to both recipients on the first
  Send Now click but then re-opened the Actions menu and re-invoked
  Send SMS one or two more times, creating duplicate `sms.sms` rows
  with identical entity_keys. Postconditions pass (≥2 matches with
  correct numbers) but state-diff precision drops to 0.333 from the
  extra creates.
- If you want strict-count enforcement, add `if len(matching) > 2:
  failures.append(...)` in check.py and lower the threshold. This
  task leaves the ≥2 form so the postcondition matches the user-
  specified check focus.
