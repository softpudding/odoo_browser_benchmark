"""Seed for event.create_event_add_question_publish.

Category: deep UI interaction.

The agent creates a brand-new event from the Events list view, adds two
custom registration questions (one textbox + one simple_choice with three
nested answers) via the event form's Questions tab, then publishes the
event via the frontend website-preview systray toggle.

Seed does NOT create the target event — the agent creates it from scratch.
We only clean up prior runs so the task is idempotent, and we make sure
`website_event` is installed (needed for both the publish button and the
frontend registration form that surfaces the questions).
"""

EVENT_NAME = "Bench 2026 Conference"
Q1_TITLE = "Company"
Q2_TITLE = "Experience Level"
Q2_ANSWERS = ["Beginner", "Intermediate", "Expert"]


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        return
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # website_event is NOT in base snapshot; needed for is_published/
    # website_published + the website-preview systray toggle.
    _ensure_module(env, "website_event")

    # ----- Cleanup prior runs (child-first) -----
    # Delete any stray Question records with our exact titles (from prior
    # failed runs). These may be reusable (not attached to a live event)
    # or attached to a prior Bench 2026 Conference. We guard against
    # deleting questions that already have registration answers by
    # wrapping in a try/except — in practice there shouldn't be any.
    prior_questions = env["event.question"].with_context(active_test=False).search([
        ("title", "in", [Q1_TITLE, Q2_TITLE]),
    ])
    for q in prior_questions:
        try:
            q.sudo().unlink()
        except Exception:
            # If deletion fails (e.g. attendee-answer FK), archive instead
            try:
                q.sudo().write({"active": False})
            except Exception:
                pass

    # Delete any stray events with this name and all their child data.
    prior_events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    # Child-first: drop registrations, tickets, questions.
    prior_events.mapped("registration_ids").sudo().unlink()
    prior_events.mapped("event_ticket_ids").sudo().unlink()
    prior_events.sudo().unlink()
