# mail.invite_external_email_to_existing_channel — Run Result

| Field | Value |
|---|---|
| **Difficulty** | medium |
| **Tier** | 2 |
| **time_limit_sec** | 360 |
| **Oracle** | PASS (11.2s) |
| **Browser-use** | PASS (230.4s, single attempt, no ENV_CRASH retry) |
| **StateDiffF1** | 1.0 |
| **Strict** | PASS |
| **Postcondition failures** | 0 |
| **Forbidden ops** | 0 |

## Calibration

**Miscalibrated as medium — empirically passes browser-use on first try.** The
task design relies on a "non-default selectable row" (the envelope-icon email
fallback suggestion that only appears after typing a full valid email), but:

1. The prompt explicitly calls out the row as the target. Once BU reads
   "Click that `external-guest@bench.test` row so it appears as a selected
   chip", the distinction from other autocomplete items is direct.
2. The search input placeholder `Invite people or email` pre-primes the
   agent.
3. The "Invite to Group Chat" button is the only primary action in the
   panel after selection — no radio-button ambiguity.

BU solved it in 230s and logged its own correct summary: "typing the email,
selecting the external invitation suggestion, and clicking the 'Invite to
Group Chat' button." Ranking: this task tests a real distinct UI pathway
(the `invite_by_email` ORM method vs the more common `add_members`), but it
is **easier than the medium target** because the pathway is unambiguous
once the prompt is followed.

Keeping the task in the suite as a pathway-coverage item rather than a
difficulty trap.

## Cookbook quirks discovered

See COOKBOOK_NOTES.md for the full write-up. Summary:

- Odoo 19 invite-people side panel has **no "Email" tab** — single unified
  input that offers the email-fallback suggestion only after a *complete
  valid email* is typed and no partner email matches.
- `discuss.channel.invite_by_email` calls `mail.mail.send(raise_exception=True)`
  **synchronously in the same transaction**, so SMTP failure rolls back
  the mail.mail record. Tasks that need to verify the mail.mail artifact
  must seed a working outgoing mail server.
- A detached `aiosmtpd.controller.Controller(Sink())` spawned from seed.py
  (with `start_new_session=True`) works as a cheap throwaway SMTP sink
  accepting everything. Must also set `mail.catchall.domain` +
  `mail.default.from` ICPs and give admin `partner_id.email` a value or
  Odoo rejects `_build_email__` with "You must provide a sender address".
- The parent repo's `.claude/worktree-skeleton/.venv` ships with an
  `_editable_impl_odoo_benchmark.pth` that points to the *original*
  worktree path (e.g., `agent-a1452cb6`). Copying the skeleton into a new
  worktree therefore leaves the `benchmark` package resolving to the
  previous worktree — subprocess oracle scripts then fail with
  `ModuleNotFoundError: No module named 'benchmark'`. The bootstrap needs
  to rewrite that `.pth` file to point at the current worktree root.
- `benchmark_base.dump` at `/tmp/benchmark_snapshots/` can be stale — if
  the pool-runner's first eval ran against an uninitialised
  `benchmark_validate` DB, the resulting dump is a ~16 KB file that
  restores an empty DB. Subsequent seed scripts fail with
  `KeyError: 'res.users'`. Re-snapshot from any healthy per-task DB
  (`pg_dump -Fc -f /tmp/benchmark_snapshots/benchmark_base.dump <DB>`)
  fixes it.

## Blockers

None remaining. Task is committable.
