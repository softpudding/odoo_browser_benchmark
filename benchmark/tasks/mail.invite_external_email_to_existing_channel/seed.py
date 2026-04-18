"""Seed data for mail.invite_external_email_to_existing_channel.

Admin is added to a pre-existing private group channel 'project-discussion'.
The task is to invite an EXTERNAL email address (no matching Odoo user /
partner) via the Discuss channel's Invite People side panel.

UI shape (Odoo 19): there is NO separate 'Email' tab in the invite
dialog. The invite side panel has a SINGLE unified search input that
accepts either existing-user names or free email addresses. If the typed
text is a valid email address AND no partner email matches it AND the
channel allows invite-by-email (channel_type in {'group', public
'channel'}), Odoo offers a 'selectable_email' fallback row (envelope icon)
that the agent must click. Clicking it and then 'Invite to Group Chat'
triggers discuss.channel.invite_by_email, which produces a mail.mail with
email_to set to the external address AND a user_notification mail.message
on the channel.

invite_by_email calls `.send(raise_exception=True)`, which tries to open
an SMTP connection synchronously — if that fails, the whole transaction
is rolled back and the mail.mail is NOT persisted. To make the end state
verifiable we seed:
  - An outgoing `ir.mail_server` pointing at localhost:<port>.
  - A detached sink SMTP subprocess (aiosmtpd) that accepts anything and
    discards it. It's left running; benchmark cleanup drops the DB so
    orphan subprocesses simply sit idle.

The hard calibration risk: (a) the email-fallback row only appears AFTER
a valid full email is typed (partial typing shows no suggestion);
(b) browser agents may instead pick an existing partner, create a new
channel from scratch, press Enter without clicking the fallback row, or
click 'Invite to Group Chat' before the email chip is selected.
"""

import os
import socket
import subprocess
import time


CHANNEL_NAME = "project-discussion"
EXTERNAL_EMAIL = "external-guest@bench.test"
SMTP_HOST = "127.0.0.1"
SMTP_PORT = 2525  # fixed — conflicts are unlikely on benchmark workers


def _port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def _find_repo_root():
    """Locate the worktree root by scanning sys.path for the .venv marker."""
    import sys
    for p in sys.path + [os.getcwd()]:
        if not p:
            continue
        # Heuristic: find a directory containing .venv/bin/python
        cur = os.path.abspath(p)
        for _ in range(8):
            candidate = os.path.join(cur, ".venv", "bin", "python")
            if os.path.exists(candidate):
                return cur
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    # Last resort: cwd
    return os.getcwd()


def _start_fake_smtp():
    """Idempotently start a background aiosmtpd sink on SMTP_HOST:SMTP_PORT.

    Skips if the port is already accepting connections (previous run's
    sink still alive). The subprocess is detached via start_new_session
    so it survives the seed's parent process exit.
    """
    if _port_open(SMTP_HOST, SMTP_PORT):
        return
    repo_root = _find_repo_root()
    python = os.path.join(repo_root, ".venv", "bin", "python")
    if not os.path.exists(python):
        python = "python3"
    # Let the subprocess inherit its own sys.path — aiosmtpd will be found
    # if the venv python is used. No manual site-packages fiddling.
    script = (
        "from aiosmtpd.controller import Controller\n"
        "from aiosmtpd.handlers import Sink\n"
        f"c = Controller(Sink(), hostname={SMTP_HOST!r}, port={SMTP_PORT})\n"
        "c.start()\n"
        "import time\n"
        "while True:\n"
        "    time.sleep(60)\n"
    )
    try:
        subprocess.Popen(
            [python, "-c", script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError:
        return
    # Wait up to 5 seconds for the port to open.
    for _ in range(50):
        if _port_open(SMTP_HOST, SMTP_PORT):
            return
        time.sleep(0.1)


def setup(env):
    # --- Cleanup any lingering records from previous runs -------------------
    env["discuss.channel"].with_context(active_test=False).search(
        [("name", "=", CHANNEL_NAME)]
    ).unlink()
    # Drop any mail.mail invite records from prior runs targeting the
    # external email so the diff/check sees only the CURRENT run's output.
    env["mail.mail"].with_context(active_test=False).search(
        [("email_to", "=ilike", EXTERNAL_EMAIL)]
    ).unlink()
    # Any orphan mail.guest left over from a prior run — safe to nuke.
    env["mail.guest"].with_context(active_test=False).search(
        [("email", "=ilike", EXTERNAL_EMAIL)]
    ).unlink()
    # Any res.partner left over from a prior run using the sentinel email —
    # we want an environment where NO partner email matches so the
    # email-fallback row actually appears.
    env["res.partner"].with_context(active_test=False).search(
        [("email", "=ilike", EXTERNAL_EMAIL)]
    ).unlink()

    # --- Fake outgoing SMTP sink --------------------------------------------
    _start_fake_smtp()
    # Remove any prior benchmark SMTP server records to avoid duplicates.
    env["ir.mail_server"].with_context(active_test=False).search(
        [("name", "=", "benchmark_fake_smtp")]
    ).unlink()
    env["ir.mail_server"].create({
        "name": "benchmark_fake_smtp",
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "smtp_encryption": "none",
        "smtp_authentication": "login",
        "from_filter": False,
        "sequence": 1,
    })

    admin = env.ref("base.user_admin")
    admin_partner = admin.partner_id
    # Ensure admin has an email_formatted so invite_by_email can set
    # mail_from on the outbound mail.mail. Without it Odoo raises
    # "must provide a sender address explicitly".
    if not admin_partner.email:
        admin_partner.write({"email": "admin@bench.test"})

    # Set catchall ICPs for safety — some Odoo paths still consult them
    # even when email_from is set on the mail.mail.
    env["ir.config_parameter"].sudo().set_param(
        "mail.catchall.domain", "bench.test"
    )
    env["ir.config_parameter"].sudo().set_param(
        "mail.default.from", "no-reply"
    )

    # Pre-create the OdooBot DM so visiting /odoo/discuss doesn't auto-create
    # it mid-run (otherwise it shows up as a stray discuss.channel diff row).
    odoobot = env.ref("base.partner_root")
    env["discuss.channel"].with_user(admin)._get_or_create_chat(
        partners_to=[odoobot.id]
    )

    # Create the pre-existing private group channel with admin as a member.
    # channel_type='group' is one of the two types where
    # _allow_invite_by_email() returns True.
    env["discuss.channel"].with_user(admin).create(
        {
            "name": CHANNEL_NAME,
            "channel_type": "group",
            "channel_member_ids": [(0, 0, {"partner_id": admin_partner.id})],
        }
    )
