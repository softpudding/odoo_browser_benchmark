# website_forum.post_question_accept_answer — RESULT

## Oracle

- Command: `PYTHONPATH=. .venv/bin/benchmark-eval run website_forum.post_question_accept_answer --agent oracle --headless`
- Outcome: **PASS**
- StateDiffF1: **1.0** (precision=1.0, recall=1.0)
- Expected/observed/matching: 7/7/7 edits
- Postcondition failures: 0
- Wall clock: ~11.5 s
- Artifacts: `benchmark/reports/runs/website_forum.post_question_accept_answer__oracle__1776534696/`

## Browser-Use (single-shot BU calibration)

- Command: `PYTHONPATH=. .venv/bin/benchmark-eval run website_forum.post_question_accept_answer --agent browser-use --headless`
- Outcome: **FAIL** (strict FAIL)
- StateDiffF1: 0.0 (postcondition override — the raw diff match was 6/7, i.e. BU did create the admin answer correctly)
- Postcondition failures: **1** — `Canonical benchbot answer is NOT marked is_correct=True; the agent must click Accept on that answer.`
- Wall clock: 360.0 s (hit task `time_limit_sec`)
- Gave-up: true (timeout)
- Writes: 27 non-forbidden, 0 forbidden
- Artifacts: `benchmark/reports/runs/website_forum.post_question_accept_answer__browser-use__1776534732/`

### Calibration summary

BU reliably handles the easier sub-steps (navigating `/forum` → Bench Q&A,
logging in as admin, opening the seeded question, posting a 125-char
answer via the Your Answer textarea). The state diff captures all 6
expected `create` edits on the admin's new answer row.

BU then spends the entire remaining budget (≈50 steps, loop-detection
nudges firing from step 15 onward) hunting for the Accept checkmark on
the canonical benchbot answer. Tried selectors:
`a[data-href*='mark_as_best']`, `a[href*='mark_as_best']`,
`.fa-check-circle`, `.fa-check`, `.o_wforum_validate`,
`a[data-href*='validate']`, the More dropdown (which shows Edit /
Convert to Comment / Delete / Flag only), and eventually attempted to
log out and impersonate benchbot. None hit the real selector
`.o_wforum_validate_toggler` whose `data-href` posts to
`/forum/<forum>/post/<answer>/toggle_correct`.

Karma is NOT a confound: admin has `is_admin()` True, which bypasses
every `karma_answer_accept_*` threshold in
`forum.post._compute_post_karma_rights`. The only guard that would fire
is the self-accept block, but that's on admin's own answer, not on
benchbot's — so the Accept button IS present and clickable; BU just
cannot find it under the non-obvious class name.

State-diff calibration is clean: 6/7 expected edits match BU's observed
edits exactly (name, parent_id, forum_id, is_correct=null, state=active,
create_uid on the new admin answer). The only missing edit is the
`is_correct=True` flip on the canonical benchbot answer, which is what
the postcondition asserts.
