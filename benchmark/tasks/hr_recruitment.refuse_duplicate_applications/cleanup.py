"""Clean up artifacts from previous runs."""


APPLICANT_NAMES = [
    "Priya Nair",
    "Priya Nair (Referral)",
    "Priya Narayan",
]
REASON_NAMES = [
    "Candidate withdrew after final review",
    "Candidate withdrew after phone review",
    "Candidate withdrew",
]


def cleanup(env):
    applicants = env["hr.applicant"].with_context(active_test=False).search(
        [("partner_name", "in", APPLICANT_NAMES)]
    )
    if applicants:
        applicants.unlink()
    env["hr.applicant.refuse.reason"].with_context(active_test=False).search(
        [("name", "in", REASON_NAMES)]
    ).unlink()
