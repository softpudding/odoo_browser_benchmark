# Cookbook additions from mail.invite_external_email_to_existing_channel

## Discuss invite-by-email: no "Email tab" in Odoo 19

The Discuss channel Invite People side panel
(`discuss.ChannelInvitation`) uses a **single unified search input**, not a
tabbed UI. The input's placeholder is `Invite people or email` when
`thread.allow_invite_by_email` is True (i.e., for `channel_type='group'`
or a public `channel` with no `group_public_id`), otherwise `Search people
to invite`.

When text is typed, two kinds of rows can appear:
- Existing internal-user partners matched by name/email (normal avatar).
- A single fallback **email row** with an envelope icon — returned by
  `res.partner.search_for_channel_invite` as the `selectable_email`
  key — ONLY when all of:
  1. the search text matches `single_email_re` (i.e., a *complete* valid
     email),
  2. no selectable partner matches,
  3. the channel's `_allow_invite_by_email()` returns True,
  4. no existing channel member has an email matching the typed address.

Clicking that row adds the literal email string to `state.selectedEmails`.
Clicking **Invite to Group Chat** (or **Invite** for public channels)
then calls `discuss.channel.invite_by_email(channel_id, emails=[...])`.

## invite_by_email requires a working SMTP + email_from

`discuss.channel.invite_by_email` does:

```python
self.env["mail.mail"].sudo().create(to_create).send(raise_exception=True)
```

The `raise_exception=True` means an SMTP failure propagates as
`MailDeliveryException` → `UserError`, which HTTP dispatcher rolls back,
so the `mail.mail` record does NOT persist. Additionally:

- `email_from` is set from `self.env.user.partner_id.email_formatted`. If
  `admin.partner_id.email` is empty, `_build_email__` raises
  `AssertionError: You must either provide a sender address explicitly or
  configure using the combination of mail.catchall.domain and
  mail.default.from ICPs`.

Seed pattern for tests that need `invite_by_email` (or any other
`raise_exception=True` mail flow) to actually persist a `mail.mail`:

```python
# 1. Give the acting user an email address.
admin.partner_id.write({"email": "admin@bench.test"})

# 2. Set catchall ICPs as a belt-and-suspenders default.
env["ir.config_parameter"].sudo().set_param("mail.catchall.domain", "bench.test")
env["ir.config_parameter"].sudo().set_param("mail.default.from", "no-reply")

# 3. Spawn a detached aiosmtpd sink and point ir.mail_server at it.
subprocess.Popen(
    [venv_python, "-c", (
        "from aiosmtpd.controller import Controller\n"
        "from aiosmtpd.handlers import Sink\n"
        "c = Controller(Sink(), hostname='127.0.0.1', port=2525)\n"
        "c.start()\n"
        "import time\n"
        "while True: time.sleep(60)\n"
    )],
    start_new_session=True,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
)
env["ir.mail_server"].create({
    "name": "benchmark_fake_smtp",
    "smtp_host": "127.0.0.1",
    "smtp_port": 2525,
    "smtp_encryption": "none",
    "smtp_authentication": "login",
    "sequence": 1,
})
```

`aiosmtpd` is in the venv (package `aiosmtpd`). The sink accepts and
discards — Odoo's `smtplib.SMTP.send_message` succeeds, `mail.state`
becomes `'sent'`, and the record sticks. The detached subprocess is left
running; orphan is harmless because the port is idempotently reused by
subsequent runs and Odoo's auto-isolated DB drops terminate any per-task
residue.

## aiosmtpd gotcha: don't overset sys.path

First attempt set `sys.path.insert(0, venv_site)` inside the spawned
script. That happened to work but was fragile across Python point
versions. Cleanest is to use the venv's own `python` binary — its
site-packages is resolved automatically.

## Worktree bootstrap gotcha: stale editable-install .pth

The parent repo's `.claude/worktree-skeleton/.venv` ships with a
`_editable_impl_odoo_benchmark.pth` file that points at whatever worktree
originally `uv pip install -e .`-ed the project. Copying the skeleton
into a fresh worktree leaves that pointer stale — `import benchmark`
resolves to the previous worktree, and the *current* worktree's
oracle.py / check.py subprocess scripts fail with `ModuleNotFoundError:
No module named 'benchmark'` because Python's default `sys.path` for a
subprocess script does NOT include its cwd (only the script's own
directory).

Fix inline in the task-creator workflow after copying .venv:

```bash
echo "$(pwd)" > .venv/lib/python3.12/site-packages/_editable_impl_odoo_benchmark.pth
```

## Stale benchmark_base.dump

`benchmark_base.dump` at `/tmp/benchmark_snapshots/` can be stale — e.g.
produced from an uninitialised `benchmark_validate`. Symptom: seed
stderr says `KeyError: 'res.users'` because the restored DB has only the
7 `orm_signaling_*` tables. Recover by re-dumping from any healthy
per-task DB:

```bash
pg_dump -Fc -f /tmp/benchmark_snapshots/benchmark_base.dump <working_db>
```

Any DB that has finished a successful eval run should be a safe source —
check `SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'`
returning ~900+ before dumping.
