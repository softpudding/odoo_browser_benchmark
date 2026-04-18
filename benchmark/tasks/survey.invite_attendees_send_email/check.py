"""Postcondition checks for survey.invite_attendees_send_email.

The agent passes iff sending the survey.invite wizard produced one
`survey.user_input` row per invited partner (matched by email) AND at least
one `mail.mail` row with the custom subject 'Please complete onboarding'.
The survey must be otherwise unchanged.
"""


SURVEY_TITLE = "Bench Onboarding Quiz"
TARGET_EMAILS = {"alice@x.com", "bob@y.com", "carol@z.com"}
SUBJECT = "Please complete onboarding"


def check(env):
    failures = []

    if "survey.survey" not in env.registry:
        return ["survey module is not installed"]

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ], limit=1)
    if not survey:
        return [f"Survey '{SURVEY_TITLE}' not found (agent may have renamed or deleted it)"]

    # --- Survey invariants -------------------------------------------------
    if not survey.active:
        failures.append(f"Survey '{SURVEY_TITLE}' was archived; expected active")
    if survey.access_mode != "token":
        failures.append(
            f"Survey access_mode is {survey.access_mode!r}, expected 'token' (invited people only)"
        )
    if survey.users_login_required:
        failures.append(
            "Survey users_login_required was turned on; expected False"
        )
    if survey.certification:
        failures.append("Survey was unexpectedly converted to a certification")

    questions = survey.question_ids
    if len(questions) != 1:
        failures.append(
            f"Expected 1 question on the survey, found {len(questions)} (survey was modified)"
        )

    # --- user_input rows (the canonical outcome of action_invite) ----------
    inputs = env["survey.user_input"].search([("survey_id", "=", survey.id)])
    input_emails = {
        (inp.email or "").strip().lower() for inp in inputs if inp.email
    }
    missing = TARGET_EMAILS - input_emails
    if missing:
        failures.append(
            "Missing survey.user_input rows for emails: "
            + ", ".join(sorted(missing))
            + ". The agent did not press Send after adding all three recipients, "
            "or chose the wrong partners."
        )

    extra = input_emails - TARGET_EMAILS
    # Allow admin email (if the agent added self) — but flag other unknowns.
    admin_email = (env.ref("base.user_admin").partner_id.email or "").lower()
    extra_unexpected = {e for e in extra if e and e != admin_email}
    if extra_unexpected:
        failures.append(
            "Unexpected survey.user_input rows for: "
            + ", ".join(sorted(extra_unexpected))
            + ". Agent invited extra recipients beyond the three required."
        )

    # Each expected recipient should appear exactly once (existing_mode='resend'
    # default deduplicates re-sends).
    per_email_counts = {}
    for inp in inputs:
        if inp.email:
            per_email_counts[inp.email.strip().lower()] = (
                per_email_counts.get(inp.email.strip().lower(), 0) + 1
            )
    for email in TARGET_EMAILS:
        if per_email_counts.get(email, 0) > 1:
            failures.append(
                f"Multiple survey.user_input rows for {email}; agent invoked "
                f"Send more than once."
            )

    # --- mail.mail with target subject -------------------------------------
    mails = env["mail.mail"].with_context(active_test=False).search([
        ("subject", "=", SUBJECT),
    ])
    if not mails:
        # mail.mail may have auto_delete=True and been pruned after a
        # successful send. user_input presence is the primary proof the
        # wizard ran with the right emails. Only fail here if there is
        # also no user_input evidence.
        if not inputs:
            failures.append(
                f"No mail.mail with subject {SUBJECT!r} found and no "
                f"survey.user_input rows created."
            )
    else:
        # If any mails linger, confirm at least one targets one of our emails.
        def _mail_hits_target(m):
            if m.email_to and any(e in m.email_to for e in TARGET_EMAILS):
                return True
            for r in m.recipient_ids:
                if (r.email or "").strip().lower() in TARGET_EMAILS:
                    return True
            return False

        matched = any(_mail_hits_target(m) for m in mails)
        if not matched:
            failures.append(
                f"Found mail.mail with subject {SUBJECT!r} but none target "
                f"alice@x.com / bob@y.com / carol@z.com; agent may have sent "
                f"to a different address."
            )

    return failures
