"""Cleanup for crm.set_lost_reason_reassign_salesperson."""


def cleanup(env):
    env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", "Acme – Q3 renewal"),
    ]).unlink()
