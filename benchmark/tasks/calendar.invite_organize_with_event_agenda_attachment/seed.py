"""Seed for calendar.invite_organize_with_event_agenda_attachment.

Difficulty: hard (Category: deep_ui_interaction).
The agent must:
  - Create a calendar event 'Q2 Planning Session' on 2026-05-20 14:00-15:30.
  - Add the two pre-seeded contacts Alice Bench + Bob Bench as attendees.
  - Upload `agenda.txt` to the chatter attachments panel.

Why this is hard for browser-use: the chatter paperclip ("Attach files")
triggers a hidden ``<input type="file">`` which requires an OS-level file
dialog. Browser-use frequently cannot drive native file pickers and falls
back to pasting the file content into the composer or notes, which does
not create an ir.attachment linked to the event.

Seed responsibilities:
  - Wipe any prior 'Q2 Planning Session' events + linked ir.attachment(s).
  - Ensure contacts 'Alice Bench' and 'Bob Bench' exist as res.partner
    records so the agent can add them via autocomplete.
  - Make sure seed_artifacts/agenda.txt exists on disk so the agent can
    actually upload it.
"""

import os


EVENT_NAME = "Q2 Planning Session"
ATTENDEE_NAMES = ("Alice Bench", "Bob Bench")
AGENDA_FILENAME = "agenda.txt"
AGENDA_BODY = (
    "Q2 Planning Session - Agenda\n"
    "============================\n\n"
    "1. Review Q1 outcomes (15 min)\n"
    "2. Align on Q2 goals and owners (30 min)\n"
    "3. Risks and blockers roundtable (20 min)\n"
    "4. Next steps and decisions (25 min)\n"
)
TASK_ID = "calendar.invite_organize_with_event_agenda_attachment"


def _ensure_agenda_on_disk():
    """Make sure the agenda.txt artifact exists on disk for the agent."""
    try:
        import benchmark
        bench_dir = os.path.dirname(os.path.abspath(benchmark.__file__))
    except Exception:
        bench_dir = os.path.join(os.getcwd(), "benchmark")
    artifact_dir = os.path.join(bench_dir, "tasks", TASK_ID, "seed_artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    path = os.path.join(artifact_dir, AGENDA_FILENAME)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(AGENDA_BODY)


def setup(env):
    # Cleanup any leftover event(s) from previous runs (and their
    # attachments so cleanup is fully idempotent).
    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "calendar.event"),
            ("res_id", "in", events.ids),
        ])
        if attachments:
            attachments.unlink()
        events.unlink()

    # Ensure the two attendee partners exist. We match by exact name so
    # repeated runs don't accumulate duplicates.
    for name in ATTENDEE_NAMES:
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        if not partner:
            local = name.split()[0].lower()
            env["res.partner"].create({
                "name": name,
                "email": f"{local}.bench@example.com",
            })

    # Make the agenda file available on disk for the agent to upload.
    _ensure_agenda_on_disk()
