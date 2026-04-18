"""Seed for project_todo.reorder_notes_add_due_dates_bulk.

Category: deep_ui_interaction (EASY).

Seeds three simple To-Do notes (no deadline) assigned to the admin user.
The agent must open each note and set its deadline. The default To-Do
kanban sorts by date_deadline ascending, so once all three deadlines
are set the notes naturally re-order by date.
"""


ALPHA = "Benchmark Note Alpha"
BETA = "Benchmark Note Beta"
GAMMA = "Benchmark Note Gamma"

NOTE_NAMES = [ALPHA, BETA, GAMMA]


def setup(env):
    # --- Cleanup prior runs ---
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", NOTE_NAMES),
    ]).unlink()

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if not admin:
        raise RuntimeError("admin user not found")

    # Create notes in a deterministic initial order with ascending sequence
    # values. No deadlines set — that's the agent's job.
    for idx, name in enumerate(NOTE_NAMES):
        env["project.task"].create({
            "name": name,
            "user_ids": [(6, 0, [admin.id])],
            "project_id": False,
            "date_deadline": False,
            "sequence": 10 * (idx + 1),
            "active": True,
            "description": f"<p>{name} — seeded for benchmark. Set the deadline.</p>",
        })
