"""Cleanup for project_todo.reorder_notes_add_due_dates_bulk."""


NOTE_NAMES = [
    "Benchmark Note Alpha",
    "Benchmark Note Beta",
    "Benchmark Note Gamma",
]


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", NOTE_NAMES),
    ]).unlink()
