# website_forum.upvote_question_mark_as_answer — RESULT

## Oracle

- Command: `PYTHONPATH=. .venv/bin/benchmark-eval run website_forum.upvote_question_mark_as_answer --agent oracle --headless`
- Outcome: **PASS**
- StateDiffF1: **1.0** (precision=1.0, recall=1.0)
- Expected/observed/matching: 6/6/6 edits
- Postcondition failures: 0
- Wall clock: ~15.5 s
- Artifacts: `benchmark/reports/runs/website_forum.upvote_question_mark_as_answer__oracle__1776601910/`

## Browser-Use (single-shot BU calibration)

- Command: `PYTHONPATH=. .venv/bin/benchmark-eval run website_forum.upvote_question_mark_as_answer --agent browser-use --headless`
- Outcome: **PASS** (strict PASS)
- StateDiffF1: **1.0** (6/6 matching edits, 0 missing, 0 extra)
- Postcondition failures: 0
- Wall clock: 55.8 s (9 steps)
- Gave-up: false
- Writes: 16 non-forbidden, 0 forbidden
- Artifacts: `benchmark/reports/runs/website_forum.upvote_question_mark_as_answer__browser-use__1776601968/`

### Calibration summary

Single-shot BU PASS in 55.8s / 9 steps, F1=1.0 — **task is calibrated
easier than "medium" anticipated**. The task is calibration risk: MEDIUM
per the brief, and the empirical BU result sits at the easy edge.

Why BU solved it:

- **Upvote button has a clean aria-label="Upvote"** on
  `button.vote_up` — BU's element scoring landed on it directly at step 8
  via `aria-label=Upvote` without any selector guessing.
- **Accept checkmark also has aria-label="Mark as Best Answer"** on
  `.o_wforum_validate_toggler` (rendered by the same template module). BU
  clicked it in the same step, again via aria-label, without hunting
  through the More dropdown as in row 394.
- Only ONE answer exists on the question, so no disambiguation between
  canonical vs decoy answers was required (unlike row 394).
- Admin `is_admin()` bypasses karma, and the self-post guards do not
  fire since the question + answer are both authored by benchbot.

Row 394 (post_question_accept_answer) has BU FAIL because (a) the
agent had to locate the Accept icon among TWO candidate benchbot
answers and distinguish canonical vs decoy, AND (b) the agent had to
first compose a 50-char answer through the Your Answer textarea. This
row 477 task omits both challenges (one answer, no posting) so it
collapses to a pair of aria-label-exposed clicks.

State-diff is clean: 6 expected edits, 6 observed, 6 matching. The
diff captures (1) `forum.post.is_correct=True` on the benchbot answer,
and (2) the 5 `create` edits on the new `forum.post.vote` row
(post_id, user_id, vote='1', forum_id, recipient_id).

### Notes for calibration tightening (future work)

To make this genuinely hard-tier (if re-targeted):

- Add 2-3 distractor answers (mode='discussions') so BU must pick the
  right one to Accept.
- Require the agent to ALSO downvote a decoy answer — two vote clicks
  with opposite polarity on different posts.
- Require the agent to first earn/grant karma to themselves (karma
  ladder trap).
- Remove the explicit "circle-check" wording from the prompt and use
  only "Accept" — BU sometimes fails when the visual hint is absent.

Kept as medium/tier:2 per spec (calibration risk was stated as
medium, and BU ≥50% PASS rate is compatible with medium difficulty).
