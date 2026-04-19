"""Cleanup for account_followup.send_reminder_level_two_customers.

BLOCKED TASK — `account_followup` addon is not installed in this
Community checkout, so there is nothing to clean up. The guard below
turns this into a no-op that stays safe if the module ever becomes
available without the rest of the task being fleshed out.
"""


def cleanup(env):
    module = env["ir.module.module"].search(
        [("name", "=", "account_followup")], limit=1
    )
    if not module or module.state != "installed":
        return

    # Once the enterprise addon is vendored, cleanup would look like:
    #
    # partner = env["res.partner"].with_context(active_test=False).search(
    #     [("name", "=", "Bench Overdue Co")], limit=1
    # )
    # if partner:
    #     invoices = env["account.move"].with_context(active_test=False).search([
    #         ("partner_id", "=", partner.id),
    #         ("name", "in", ["OV/BENCH/001", "OV/BENCH/002", "OV/BENCH/003"]),
    #     ])
    #     for inv in invoices:
    #         if inv.state == "posted":
    #             inv.button_draft()
    #             inv.button_cancel()
    #         else:
    #             inv.button_cancel()
    #     invoices.sudo().unlink()
    #     # Clear follow-up trail so the next run starts clean
    #     partner.sudo().write({
    #         "followup_line_id": False,
    #         "followup_next_action_date": False,
    #     })
    #     partner.sudo().unlink()
    # env["product.product"].with_context(active_test=False).search(
    #     [("default_code", "=", "BENCH-FU-SVC")]
    # ).sudo().unlink()
