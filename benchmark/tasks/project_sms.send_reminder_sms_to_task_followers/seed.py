"""Seed for project_sms.send_reminder_sms_to_task_followers.

Category (MEDIUM): side_effect_trap — cog Actions Send SMS binding on
project.task list view exercises sms.composer in mass mode, producing
one sms.sms per selected record.

Creates:
  * Project `Bench SMS Project` (allow_recurring_tasks=False).
  * Two partners:
      - Bench Reviewer A (phone +16175551200, country US)
      - Bench Reviewer B (phone +16175551201, country US)
  * Two tasks on the project, each pinned to one reviewer as customer:
      - "Urgent Review Request — Reviewer A"
      - "Urgent Review Request — Reviewer B"

Module install:
  * `sms` is NOT in `benchmark/base_modules.txt`.  Installing `sms`
    auto-installs `project_sms` (manifest: auto_install=True,
    depends=['project', 'sms']).

Why two tasks (not one task + followers):
  * `project_sms` binds `sms.composer` via `binding_model_id=project.task`
    with `default_composition_mode='mass'`.  Mass mode sends ONE SMS per
    selected record, taking the number from the record's `partner_id` (via
    `_sms_get_recipients_info` → `_mail_get_partners`).  Followers are NOT
    recipients in mass mode.  To reach the "≥2 sms.sms" check deterministi-
    cally, we seed two tasks, each with a distinct partner/phone, and the
    prompt multi-selects both from the list.
"""

PROJECT_NAME = "Bench SMS Project"
REVIEWER_A_NAME = "Bench Reviewer A"
REVIEWER_A_PHONE = "+16175551200"
REVIEWER_A_EMAIL = "reviewer-a@benchsms.example"
REVIEWER_B_NAME = "Bench Reviewer B"
REVIEWER_B_PHONE = "+16175551201"
REVIEWER_B_EMAIL = "reviewer-b@benchsms.example"
TASK_A_NAME = "Urgent Review Request — Reviewer A"
TASK_B_NAME = "Urgent Review Request — Reviewer B"


def _ensure_modules(env):
    """Install `sms` if not installed.  `project_sms` auto-installs because
    it has auto_install=True and depends=[project (base), sms]."""
    for mod_name in ("sms", "project_sms"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()


def _cleanup(env):
    # Prior-run tasks (tasks on the target project, or with the target names)
    project = env["project.project"].with_context(active_test=False).search(
        [("name", "=", PROJECT_NAME)], limit=1,
    )

    # Delete any sms.sms rows tied to our seeded numbers / task messages first.
    if "sms.sms" in env.registry:
        env["sms.sms"].sudo().search([
            ("number", "in", [REVIEWER_A_PHONE, REVIEWER_B_PHONE]),
        ]).unlink()

    tasks = env["project.task"].with_context(active_test=False).search([
        "|",
        ("name", "in", [TASK_A_NAME, TASK_B_NAME]),
        ("project_id", "=", project.id if project else False),
    ])
    for task in tasks:
        msgs = env["mail.message"].search([
            ("model", "=", "project.task"),
            ("res_id", "=", task.id),
        ])
        if "sms.sms" in env.registry:
            env["sms.sms"].sudo().search([
                ("mail_message_id", "in", msgs.ids),
            ]).unlink()
        msgs.sudo().unlink()
    tasks.unlink()

    if project:
        # Stages are project-scoped; removing the project releases them,
        # but unlink any stray stages named 'Review' pinned to this project.
        stages = env["project.task.type"].search([
            ("project_ids", "in", [project.id]),
        ])
        stages.unlink()
        project.unlink()

    # Partners are reused across runs — update only (don't delete to avoid
    # dangling FK issues with any non-SMS records).


def setup(env):
    _ensure_modules(env)
    _cleanup(env)

    us_country = env.ref("base.us", raise_if_not_found=False)
    country_id = us_country.id if us_country else False

    def _upsert_partner(name, phone, email):
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        vals = {"name": name, "phone": phone, "email": email}
        if country_id:
            vals["country_id"] = country_id
        if partner:
            partner.write(vals)
        else:
            partner = env["res.partner"].create(vals)
        return partner

    reviewer_a = _upsert_partner(REVIEWER_A_NAME, REVIEWER_A_PHONE, REVIEWER_A_EMAIL)
    reviewer_b = _upsert_partner(REVIEWER_B_NAME, REVIEWER_B_PHONE, REVIEWER_B_EMAIL)

    project = env["project.project"].create({
        "name": PROJECT_NAME,
        "allow_recurring_tasks": False,
        "privacy_visibility": "employees",
    })

    # A default open stage keeps the kanban from collapsing the rows under a
    # None (unassigned) group.  Without a stage, project.task.type
    # group_expand collapses the None group and the tasks disappear from the
    # default kanban/list view unless the agent expands the group manually.
    stage = env["project.task.type"].create({
        "name": "Review",
        "sequence": 1,
        "fold": False,
        "project_ids": [(6, 0, [project.id])],
    })

    # Two tasks, one per reviewer.  partner_id drives mass-mode SMS
    # recipient discovery via _mail_get_partners().
    task_a = env["project.task"].create({
        "name": TASK_A_NAME,
        "project_id": project.id,
        "partner_id": reviewer_a.id,
        "stage_id": stage.id,
        "description": "Review quarterly report and confirm sign-off by EOD.",
    })
    task_b = env["project.task"].create({
        "name": TASK_B_NAME,
        "project_id": project.id,
        "partner_id": reviewer_b.id,
        "stage_id": stage.id,
        "description": "Review quarterly report and confirm sign-off by EOD.",
    })

    # Subscribe each reviewer as a follower on their own task, plus both
    # to the other task (so followers-style framing still holds even if
    # a human tester reads followers into the flow).  Functionally the
    # mass-mode composer does NOT use followers — only partner_id — but
    # adding followers is cheap and keeps the chatter realistic.
    task_a.message_subscribe(partner_ids=[reviewer_a.id, reviewer_b.id])
    task_b.message_subscribe(partner_ids=[reviewer_a.id, reviewer_b.id])
