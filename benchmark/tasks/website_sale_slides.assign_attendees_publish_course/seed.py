"""Seed for website_sale_slides.assign_attendees_publish_course.

Creates:
  * `slide.channel` 'Bench 101'  — already published, visibility='members',
    enroll='invite' (the prerequisite course).
  * `slide.channel` 'Bench Onboarding' — draft, visibility='public',
    enroll='public', is_published=False (the target course).
  * Two partners 'Alice Attendee' + 'Bob Attendee' with emails.
  * A fake outgoing SMTP sink (aiosmtpd on 127.0.0.1:2525) and a matching
    `ir.mail_server` record, so the `Add Attendees` wizard (which forces
    send_email=True when visibility != 'public' or enroll_mode=True) can
    actually send without exploding the transaction.

The agent is expected to:
  1. set visibility='members' on Bench Onboarding (enroll auto-flips to
     'invite' — covered by the _compute_enroll compute),
  2. publish the course via the frontend `/slides/<slug>` admin systray
     toggle (the backend form's "Go to Website" button is a
     website_redirect_button — navigation only; the real toggle is the
     Owl systray one on the frontend page),
  3. then add `Bench 101` as a prerequisite — the prerequisite_channel_ids
     dropdown's domain filters by matching visibility AND matching
     website_published, so `Bench 101` only appears AFTER steps 1 and 2,
  4. send the Add Attendees wizard with Alice + Bob as recipients.
"""

import os
import socket
import subprocess
import time


SMTP_HOST = "127.0.0.1"
SMTP_PORT = 2525


def _port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def _find_repo_root():
    import sys
    for p in sys.path + [os.getcwd()]:
        if not p:
            continue
        cur = os.path.abspath(p)
        for _ in range(8):
            candidate = os.path.join(cur, ".venv", "bin", "python")
            if os.path.exists(candidate):
                return cur
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    return os.getcwd()


def _start_fake_smtp():
    if _port_open(SMTP_HOST, SMTP_PORT):
        return
    repo_root = _find_repo_root()
    python = os.path.join(repo_root, ".venv", "bin", "python")
    if not os.path.exists(python):
        python = "python3"
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
    for _ in range(50):
        if _port_open(SMTP_HOST, SMTP_PORT):
            return
        time.sleep(0.1)


def setup(env):
    Channel = env["slide.channel"].with_context(active_test=False)
    ChannelPartner = env["slide.channel.partner"].with_context(active_test=False)
    Partner = env["res.partner"].with_context(active_test=False)

    # --- Cleanup prior runs -------------------------------------------------
    # Drop any leftover attendee rows on our two courses.
    stale_channels = Channel.search([
        ("name", "in", ["Bench Onboarding", "Bench 101"]),
    ])
    if stale_channels:
        ChannelPartner.search([("channel_id", "in", stale_channels.ids)]).unlink()
        # prerequisite_channel_ids rel-table is cleaned via unlink of channels
        stale_channels.unlink()

    stale_partners = Partner.search([
        ("name", "in", ["Alice Attendee", "Bob Attendee"]),
    ])
    if stale_partners:
        # Drop any mail.mail referring to their emails from prior runs so the
        # state diff is clean.
        env["mail.mail"].with_context(active_test=False).search([
            ("email_to", "in", [p.email for p in stale_partners if p.email]),
        ]).unlink()
        stale_partners.unlink()

    env["ir.mail_server"].with_context(active_test=False).search([
        ("name", "=", "benchmark_fake_smtp"),
    ]).unlink()

    # --- Fake outgoing SMTP sink -------------------------------------------
    _start_fake_smtp()
    env["ir.mail_server"].create({
        "name": "benchmark_fake_smtp",
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "smtp_encryption": "none",
        "smtp_authentication": "login",
        "from_filter": False,
        "sequence": 1,
    })

    # --- Catchall ICPs + admin email ---------------------------------------
    admin = env.ref("base.user_admin")
    if not admin.partner_id.email:
        admin.partner_id.write({"email": "admin@bench.test"})
    env["ir.config_parameter"].sudo().set_param(
        "mail.catchall.domain", "bench.test"
    )
    env["ir.config_parameter"].sudo().set_param(
        "mail.default.from", "no-reply"
    )

    # --- Create the two partners -------------------------------------------
    alice = Partner.create({
        "name": "Alice Attendee",
        "email": "alice.attendee@bench.test",
    })
    bob = Partner.create({
        "name": "Bob Attendee",
        "email": "bob.attendee@bench.test",
    })
    assert alice.email and bob.email, "Seed partners must have emails"

    # --- Create the prerequisite course (already published, members-only) --
    # user_id is set to admin explicitly; otherwise it defaults to the
    # seeding user (__system__ / OdooBot) who would be auto-added as an
    # attendee via _action_add_members in slide.channel.create().
    bench_101 = Channel.create({
        "name": "Bench 101",
        "description_short": "<p>Primer that must be completed before onboarding.</p>",
        "channel_type": "training",
        "visibility": "members",
        "enroll": "invite",
        "is_published": True,
        "user_id": admin.id,
    })
    # Ensure NO attendees leaked in (admin auto-joins via create(), which we
    # explicitly revert to start with a clean slate for the check.py count).
    ChannelPartner.search([("channel_id", "=", bench_101.id)]).unlink()

    # --- Create the target course (draft, public default) ------------------
    onboarding = Channel.create({
        "name": "Bench Onboarding",
        "description_short": "<p>Standard onboarding for Bench engineers.</p>",
        "channel_type": "training",
        "visibility": "public",
        "enroll": "public",
        "is_published": False,
        "user_id": admin.id,
    })
    ChannelPartner.search([("channel_id", "=", onboarding.id)]).unlink()
