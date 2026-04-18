"""Seed for survey.invite_attendees_send_email.

Seeds a single-question survey 'Bench Onboarding Quiz' in access_mode='token'
(Invited people only) so the Share-a-Survey wizard (survey.invite) shows the
Recipients (many2many_tags_email), Additional emails, Subject and Body
fields by default (send_email auto-computes to True when
survey_access_mode='token').

Also seeds three res.partner records so the agent can pick them from the
Recipients autocomplete by typing the email (the survey.invite view has
`required="True"` on partner_ids with `no_quick_create`, so free-text emails
typed into the Recipients field do NOT create a partner — the agent must
pick pre-existing partners). Typing each email and picking the suggestion
turns the input into a chip, exercising the multi-select tag pattern.

survey.invite.action_invite creates one `mail.mail` per recipient via
`self.env['mail.mail'].sudo().create(mail_values)` and then the outbound
queue runs synchronously. Any SMTP error raised by sendmail propagates as
UserError and rolls back the whole transaction, losing the
`survey.user_input` rows alongside the `mail.mail`. To keep the test
deterministic we stand up a detached aiosmtpd Sink on 127.0.0.1:2525 and
register it as the outgoing ir.mail_server (pattern from
mail.invite_external_email_to_existing_channel).
"""

import os
import socket
import subprocess
import time


SURVEY_TITLE = "Bench Onboarding Quiz"
TARGET_PARTNERS = [
    ("Alice Invitee", "alice@x.com"),
    ("Bob Invitee", "bob@y.com"),
    ("Carol Invitee", "carol@z.com"),
]
SMTP_HOST = "127.0.0.1"
SMTP_PORT = 2525


def _ensure_survey_module(env):
    survey_mod = env["ir.module.module"].search([("name", "=", "survey")], limit=1)
    if survey_mod and survey_mod.state != "installed":
        survey_mod.button_immediate_install()


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
    """Idempotently start a detached aiosmtpd Sink on SMTP_HOST:SMTP_PORT."""
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
    _ensure_survey_module(env)
    if "survey.survey" not in env.registry:
        return

    # ---- Cleanup prior runs -------------------------------------------------
    Survey = env["survey.survey"].with_context(active_test=False)
    existing = Survey.search([("title", "=", SURVEY_TITLE)])
    if existing:
        existing.user_input_ids.unlink()
        existing.question_and_page_ids.unlink()
        existing.unlink()

    # Drop any mail.mail rows from a prior run whose subject is the target.
    env["mail.mail"].with_context(active_test=False).search([
        ("subject", "=", "Please complete onboarding"),
    ]).unlink()

    # Drop any prior partners with the target emails so the seed re-creates
    # them fresh (and the diff engine can match them unambiguously).
    for _name, email in TARGET_PARTNERS:
        env["res.partner"].with_context(active_test=False).search([
            ("email", "=ilike", email),
        ]).unlink()

    # ---- Fake SMTP sink so action_invite persists ---------------------------
    _start_fake_smtp()
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
    if not admin.partner_id.email:
        admin.partner_id.write({"email": "admin@bench.test"})
    env["ir.config_parameter"].sudo().set_param("mail.catchall.domain", "bench.test")
    env["ir.config_parameter"].sudo().set_param("mail.default.from", "no-reply")

    # ---- Survey -------------------------------------------------------------
    survey = Survey.create({
        "title": SURVEY_TITLE,
        "description": "<p>Quick onboarding quiz for new hires.</p>",
        "survey_type": "survey",
        "questions_layout": "one_page",
        # access_mode='token' → _compute_send_email defaults send_email to True
        # so Recipients / Additional emails / Subject / Body are visible
        # immediately when the wizard opens.
        "access_mode": "token",
        "users_login_required": False,
        "scoring_type": "no_scoring",
        "certification": False,
        "active": True,
    })

    env["survey.question"].create({
        "survey_id": survey.id,
        "title": "How confident do you feel about your onboarding so far?",
        "sequence": 10,
        "question_type": "simple_choice",
        "suggested_answer_ids": [
            (0, 0, {"value": "Very confident", "sequence": 0}),
            (0, 0, {"value": "Somewhat confident", "sequence": 1}),
            (0, 0, {"value": "Not confident", "sequence": 2}),
        ],
    })

    if not survey.access_token:
        survey.write({"access_token": survey._get_default_access_token()})

    # ---- Recipient partners -------------------------------------------------
    # The survey.invite form has `required="True"` on partner_ids with
    # `options="{'no_quick_create': True}"`; the agent must pick pre-existing
    # partners from autocomplete. Seed one per target email.
    Partner = env["res.partner"]
    for name, email in TARGET_PARTNERS:
        Partner.create({
            "name": name,
            "email": email,
            "company_type": "person",
        })
