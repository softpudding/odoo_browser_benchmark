"""Clean up artifacts from previous runs."""


APPLICANT_NAMES = [
    "Priya Nair",
    "Priya Nair (Referral)",
    "Priya Narayan",
]


def cleanup(env):
    applicants = env["hr.applicant"].with_context(active_test=False).search(
        [("partner_name", "in", APPLICANT_NAMES)]
    )
    if applicants:
        applicants.unlink()
