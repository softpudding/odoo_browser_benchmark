"""Seed for mail.send_email_with_attachment_log_as_note.

Medium workflow (deep_ui_interaction): open a pre-seeded Contact, flip
the chatter from its default 'Log note' tab to 'Send message', type an
exact body, attach a pre-seeded text file via the paperclip (hidden
<input type=file>), and click Send so that a single
mail.message(message_type='comment', subtype_id=ref(mail.mt_comment))
with >=1 attachment is created.

Why this is hard for browser-use:
  - Chatter opens on 'Log note' by default — the 'Send message' tab
    must be clicked explicitly. Agents frequently skip this and their
    post is saved with subtype_id=mail.mt_note, which check.py rejects.
  - The paperclip triggers a hidden <input type="file"> that needs an
    OS file picker. Browser-use cannot reliably drive native file
    dialogs; even when it tries to bypass, the runner does not pass
    `available_file_paths` through, so set_input_files succeeds only
    when an oracle / human uses Playwright directly.

Seed responsibilities:
  - Idempotent cleanup of any lingering 'Bench Chatter Co' partner +
    its chatter messages + its stale attachments.
  - Create the partner fresh so the task's post registers as the sole
    chatter comment on the contact.
  - Ensure seed_artifacts/welcome_kit.txt exists on disk for the agent
    to upload.
"""

import os


PARTNER_NAME = "Bench Chatter Co"
PARTNER_EMAIL = "info@benchchatter.test"
ATTACHMENT_FILENAME = "welcome_kit.txt"
ATTACHMENT_BODY = (
    "Bench Chatter Co \u2014 Welcome Kit\n"
    "==============================\n\n"
    "Thank you for joining! Here is a short overview of what you can expect:\n\n"
    "1. Dedicated account manager\n"
    "2. Quarterly business review calls\n"
    "3. 24/7 support email: support@benchchatter.test\n\n"
    "\u2014 The Bench Chatter Co team\n"
)
TASK_ID = "mail.send_email_with_attachment_log_as_note"


def _ensure_attachment_on_disk():
    try:
        import benchmark
        bench_dir = os.path.dirname(os.path.abspath(benchmark.__file__))
    except Exception:
        bench_dir = os.path.join(os.getcwd(), "benchmark")
    artifact_dir = os.path.join(bench_dir, "tasks", TASK_ID, "seed_artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    path = os.path.join(artifact_dir, ATTACHMENT_FILENAME)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(ATTACHMENT_BODY)


def setup(env):
    # --- Cleanup prior runs --------------------------------------------------
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", PARTNER_NAME),
    ])
    if partners:
        # Delete any mail.message(s) + activities + stale attachments tied
        # to these partner rows so every re-run starts clean.
        env["mail.activity"].search([
            ("res_model", "=", "res.partner"),
            ("res_id", "in", partners.ids),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "res.partner"),
            ("res_id", "in", partners.ids),
        ]).unlink()
        stale_att = env["ir.attachment"].search([
            ("res_model", "=", "res.partner"),
            ("res_id", "in", partners.ids),
        ])
        # Some attachments may be linked as mail attachments; unlink is safe.
        stale_att.unlink()
        # Now unlink the partners themselves so no stale residue remains.
        try:
            partners.unlink()
        except Exception:
            # Partner may be referenced by other demo data — archive instead.
            partners.write({"active": False})

    # --- Recreate the target partner ----------------------------------------
    env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": PARTNER_EMAIL,
        "is_company": True,
        "company_type": "company",
        "phone": "+1 555 0100",
        "street": "100 Bench Road",
        "city": "Bench City",
    })

    # --- Drop any loose welcome_kit.txt attachment linked to any partner
    # (defensive; in case a prior run's partner_id was already reused).
    env["ir.attachment"].with_context(active_test=False).search([
        ("name", "=", ATTACHMENT_FILENAME),
        ("res_model", "=", "res.partner"),
    ]).unlink()

    # --- Ensure the seed artifact file exists on disk ------------------------
    _ensure_attachment_on_disk()
