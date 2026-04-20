"""Check website_hr_recruitment.publish_job_set_interview_form_and_archive_old_posting."""

def check(env):
    failures = []
    new = env["hr.job"].with_context(active_test=False).search([("name", "=", "Warehouse Interview Specialist")], limit=1)
    old = env["hr.job"].with_context(active_test=False).search([("name", "=", "Legacy Support Agent")], limit=1)
    if not new:
        return ["New job not found"]
    if not new.is_published:
        failures.append("New job is not published")
    if not new.survey_id or new.survey_id.title != "Bench Interview Form":
        failures.append("Interview survey not set to Bench Interview Form")
    if not old:
        failures.append("Legacy job not found")
    elif old.active:
        failures.append("Legacy job should be archived")
    return failures
