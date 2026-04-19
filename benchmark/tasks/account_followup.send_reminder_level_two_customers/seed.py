"""Seed for account_followup.send_reminder_level_two_customers.

BLOCKED TASK — the `account_followup` addon is NOT present in this
Odoo 19 Community checkout. The Follow-up Reports / Customer
Statement UI at `/odoo/action-account_followup.action_account_manual_followup`
is shipped exclusively in the Enterprise `account_followup` module.

Inspected the `odoo_benchmark` branch:
  - `addons/` contains `account`, `account_accountant` (Community
    artefacts), `snailmail_account`, but NO `account_followup`
    directory.
  - `grep -rn "account_followup" addons/` returns ZERO matches — no
    model, no view, no controller, no client action, no security rule.
  - The only follow-up-related artefact is
    `addons/account/views/res_config_settings_views.xml:115`:
        <setting id="send_invoices_followups"
                 help="Send invoices and payment follow-ups by post">
            <field name="module_snailmail_account"/>
        </setting>
    which references the orthogonal snailmail module, NOT the
    follow-up report workflow.
  - No `account_followup.followup.line` (configurable levels), no
    `account_followup.followup.report` client action, no
    `account_followup_manual_reminder` wizard, no per-partner
    `followup_status` / `followup_line_id` / `followup_next_action_date`
    fields.

Attempting to proceed would mean the agent navigates to the follow-up
report URL and gets a 404 / "Action not found" error, so there is no
value in seeding overdue invoices that can never be processed through
the intended UI. This seed raises a clear error so the eval pipeline
records the blocker instead of silently creating orphan records.
"""


def setup(env):
    # Detect whether the Enterprise-only account_followup addon has been
    # vendored. If it ever becomes available, flip the branch below to
    # run the real seed.
    module = env["ir.module.module"].search(
        [("name", "=", "account_followup")], limit=1
    )
    has_account_followup = bool(module) and module.state == "installed"
    if not has_account_followup:
        raise RuntimeError(
            "BLOCKED: the `account_followup` addon is not installed "
            "(Enterprise-only). The Follow-up Reports / Customer "
            "Statement screen is not reachable in this Odoo 19 "
            "Community checkout. See STATUS.md row 404 and RESULT.md "
            "for the re-enabling procedure."
        )

    # --- If / when enterprise addon is vendored, fill in the real seed ---
    # The sketch below documents what the real seed would do, kept as a
    # comment so future agents can flesh it out without rediscovering the
    # requirements.
    #
    # from datetime import timedelta
    # from odoo import fields as odoo_fields
    #
    # partner = env["res.partner"].search(
    #     [("name", "=", "Bench Overdue Co")], limit=1
    # ) or env["res.partner"].create({
    #     "name": "Bench Overdue Co",
    #     "email": "ap@bench-overdue.example",
    #     "is_company": True,
    #     "customer_rank": 1,
    # })
    #
    # # Ensure the level-2 follow-up line exists (Enterprise ships
    # # default levels but allow re-entry)
    # level_two = env["account_followup.followup.line"].search(
    #     [("delay", ">=", 30)], order="delay asc", limit=1
    # )
    # # Seeded levels: 15d (Reminder), 30d (Second Reminder), 60d (Final).
    #
    # # Cancel any stale invoices from prior runs
    # stale = env["account.move"].with_context(active_test=False).search([
    #     ("partner_id", "=", partner.id),
    #     ("name", "in", ["OV/BENCH/001", "OV/BENCH/002", "OV/BENCH/003"]),
    # ])
    # for inv in stale:
    #     if inv.state == "posted":
    #         inv.button_draft()
    #         inv.button_cancel()
    #     else:
    #         inv.button_cancel()
    #
    # today = odoo_fields.Date.context_today(env.user)
    # due = today - timedelta(days=45)
    # invoice_date = today - timedelta(days=60)
    #
    # product = env["product.product"].search(
    #     [("default_code", "=", "BENCH-FU-SVC")], limit=1
    # ) or env["product.product"].create({
    #     "name": "Bench Follow-up Service",
    #     "default_code": "BENCH-FU-SVC",
    #     "type": "service",
    #     "list_price": 500.0,
    # })
    #
    # for n, amount in enumerate([500.0, 750.0, 1000.0], start=1):
    #     inv = env["account.move"].create({
    #         "name": f"OV/BENCH/00{n}",
    #         "move_type": "out_invoice",
    #         "partner_id": partner.id,
    #         "invoice_date": invoice_date,
    #         "invoice_date_due": due,
    #         "invoice_line_ids": [(0, 0, {
    #             "product_id": product.id,
    #             "quantity": 1,
    #             "price_unit": amount,
    #         })],
    #     })
    #     inv.action_post()
    #
    # # After posting, the account_followup cron normally re-computes
    # # `followup_line_id` / `followup_next_action_date` on the partner.
    # # For a deterministic seed, force it synchronously:
    # partner._compute_followup_status()  # Enterprise-only method
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "account_followup is vendored into addons/."
    )
