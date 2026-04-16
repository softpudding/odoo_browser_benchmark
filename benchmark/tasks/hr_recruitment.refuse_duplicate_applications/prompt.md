Open the Recruitment app.

Before refusing anything, open **Configuration -> Applications -> Refuse Reasons** and create a **new** refuse reason with:

- **Name:** `Candidate withdrew after final review`
- **Email Template:** `Benchmark Applicant Withdrawal Template`

There is already a similarly named refuse reason, so use the exact new name above and the exact template above.

Then work only on the applicant **Priya Nair** for the job **Operations Analyst**.

1. Create the new refuse reason `Candidate withdrew after final review`.
2. Return to the applications for `Operations Analyst` and open applicant `Priya Nair`.
3. Click **Refuse**.
4. In the **Refuse Reason** dialog:
   - set **Reason** to `Candidate withdrew after final review`
   - turn on **Refuse Duplicate Applications**
   - keep **Send Email** enabled
   - set **Subject** to exactly `Operations Analyst application update`
   - set the email body to exactly `We are closing your Operations Analyst applications after your withdrawal request.`
5. Click **Refuse**.

There is a duplicate application for the same candidate that should also be refused by the dialog once you enable duplicate handling.

**Rules:**
- Refuse the `Operations Analyst` application for `Priya Nair`
- The duplicate `Priya Nair (Referral)` application must also end up refused
- Both refused applications must use the same exact new reason
- Do not use the similarly named existing refuse reason
- Do not refuse or edit `Priya Narayan`
- Do not restore, delete, or create any applicants
