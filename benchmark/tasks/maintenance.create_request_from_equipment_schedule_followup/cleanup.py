"""Cleanup for maintenance.create_request_from_equipment_schedule_followup."""


def cleanup(env):
    requests = env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Inspect Forklift Battery Cooling"),
    ])
    if requests:
        env["mail.activity"].search([
            ("res_model", "=", "maintenance.request"),
            ("res_id", "in", requests.ids),
        ]).unlink()
        requests.unlink()
