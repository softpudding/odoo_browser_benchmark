# Cookbook notes — website_forum.post_question_accept_answer

New Odoo 19 quirks discovered (and reinforced) while building this medium
task. Merged into `ODOO19_PATTERNS.md § website_forum`.

## `website_forum` not in base snapshot

- `website_forum` is NOT in `benchmark/base_modules.txt`. Seed must walk
  the same `button_immediate_install` pattern used for `sale_timesheet`,
  `stock_dropshipping`, `website_event`, etc:

  ```python
  mod = env["ir.module.module"].search([("name", "=", "website_forum")], limit=1)
  if mod and mod.state != "installed":
      mod.button_immediate_install()
  ```

- After install, `env["forum.forum"]` / `env["forum.post"]` /
  `env["forum.tag"]` become available.

## Self-accept guard is karma-independent

- The frontend controller `/forum/<forum>/post/<post>/toggle_correct`
  (`addons/website_forum/controllers/website_forum.py`) rejects any
  `request.env.uid == post.create_uid.id` regardless of karma or
  `is_admin()`. This is a hard block.
- Consequence: a task where "agent posts an answer AND accepts an answer"
  must seed a **different** user to author the answer that will be
  accepted. This task uses a seeded portal user `benchbot` (karma 5000)
  who owns the question + the two candidate answers. The agent's own
  posted answer is a distractor in terms of acceptability.

## Admin bypasses all karma thresholds via `is_admin()`

- `forum.post._compute_post_karma_rights` branches on
  `self.env.is_admin()` first and sets every `can_*` flag to True
  regardless of `karma_ask / karma_answer / karma_answer_accept_own /
  karma_answer_accept_all / karma_tag_create / karma_editor / ...`. So
  seeds do NOT need to inflate `admin.karma` for the forum flow. The
  only guard that still fires is the own-post block above.

## The Accept-checkmark selector is `.o_wforum_validate_toggler`

- Template `website_forum.question` renders the Accept icon as:

  ```xml
  <a ... class="o_wforum_validate_toggler btn ..."
     data-href="/forum/<forum>/post/<answer>/toggle_correct">
    <i class="fa fa-lg fa-check-circle-o"/>
  </a>
  ```

  When accepted, `fa-check-circle-o` swaps to `fa-check-circle
  text-success`. The `data-href` is posted via AJAX (not a real href);
  a BU agent looking for `a[href*='mark_as_best']` or `.o_wforum_validate`
  will miss it — the canonical attribute is `data-href*='toggle_correct'`
  and the canonical class is `o_wforum_validate_toggler`.
- Observed BU failure mode: BU tries every wrong selector variant, opens
  the More dropdown (Edit / Convert to Comment / Delete / Flag — no
  Accept), even tries to log out and switch user. Loop-detection nudges
  fire at step ≈15 and never recover. This is the intended calibration
  trap.

## Answer textarea has `minlength="50"`

- Template `post_answer` (`addons/website_forum/views/forum_forum_templates_post.xml`):
  `<textarea name="content" ... required="required" minlength="50" ... />`.
- Oracle bypasses this via JSON-RPC (the 50-char minimum is pure HTML
  validation on the frontend form, not a server constraint). Browser
  agents hit it; prompt must supply an answer string of at least 50
  chars.

## Forum `mode` gates answer count

- `mode='questions'` allows only 1 answer per question;
  `mode='discussions'` allows many. For a 2-seeded-answer setup (canonical
  + decoy) we must use `mode='discussions'`.

## State-diff match_key for forum.post

- `forum.post` has `name` + `parent_id` + `create_uid` as a near-unique
  tuple. If two seeded answers share the same `name` (e.g. both default
  to `Re: <question title>`), the state diff cannot distinguish them and
  `expected_state.json` entity_keys collide.
- This task pins distinct backend names for the two benchbot answers
  (`Bench Bot canonical answer` / `Bench Bot decoy answer`). The frontend
  only renders `content`, so distinctive names don't leak task structure.

## `is_correct` normalises to `null` on create, not `false`

- Fresh `forum.post` records emit `is_correct = null` (not `false`) in
  the create state-diff, same as the null-vs-false quirk documented for
  `blog.post.is_published`. `expected_state.json` uses `"norm_value":
  null` for the admin answer's `is_correct`.

## Oracle pattern

JSON-RPC shortcut:
1. `forum.forum.search_read` to find the seeded forum.
2. `forum.post.search_read` to find the seeded question (no parent).
3. `forum.post.search_read(parent_id=question.id)` + content-substring
   filter to find the canonical benchbot answer.
4. `forum.post.create` a new answer owned by admin
   (parent_id=question.id, content mentions `button_immediate_install`).
5. `forum.post.write({'is_correct': True})` on the canonical benchbot
   answer — direct write bypasses the controller own-post guard because
   the oracle is admin but the answer author is benchbot.

This yields 6 create edits (name, parent_id, forum_id, is_correct=null,
state=active, create_uid) + 1 set edit (is_correct=True on canonical
benchbot answer) = 7 total, all of which match BU output up to the
is_correct=True flip (which BU never achieves).
