Go to the **Recruitment** app and open the **Applications** list
(Recruitment → Applications → All Applications, or URL path
`/odoo/recruitment-applications`). Switch to the **list view**.

You must send a job offer to the **senior** applicant who applied to
the **QA Lead** position and has the **Python** skill. Use the
following procedure.

## Steps

1. In the search bar, filter the list so it shows only applicants
   whose *Skills* contain **Python**. The way to do this in Odoo 19
   is to type `Python` in the search box and select the **Skills**
   entry from the autocomplete dropdown (NOT "Applicant", NOT
   "Tag", NOT "Job Position"). Several applicants remain after this
   filter — some of them apply to other jobs or are not seniors.

2. Read the list and identify the single applicant that satisfies
   ALL of the following:
   - Job Position = **QA Lead**
   - Tag (Category) = **Senior**
   - Skill = **Python** (implied by the filter)

3. Tick **only that applicant's row-checkbox** (exactly one row
   checked) — do NOT tick any other rows.

4. Open the **Actions** menu (the ⚙ / gear dropdown in the control
   panel — the one that only appears once at least one record is
   selected) and click **Send Email**. A modal dialog titled
   *Send Email* opens (model `applicant.send.mail`).

5. In the wizard, clear any pre-filled Subject input and type
   exactly:

   `Job Offer - QA Lead`

6. In the **body** editor below the subject, type a short message
   that explicitly mentions the start date. The body text MUST
   contain the literal string `2026-06-01` (used by automated
   checks). For example:

       Welcome aboard. Your expected start date is 2026-06-01.

7. Click the **Send** button at the bottom of the wizard.

8. The wizard closes. The chosen applicant's chatter now contains a
   new message whose subject is **Job Offer - QA Lead** and whose
   body contains **2026-06-01**. None of the other applicants may
   receive this email.

## Rules

- Tick exactly **one** applicant's checkbox — the one that satisfies
  all three conditions above.
- Do NOT modify, refuse, archive, or reorder any applicant record.
- Do NOT change stages, priorities, emails, phones, tags, or skills.
- The email wizard **Subject** must be exactly `Job Offer - QA Lead`
  (case-sensitive, no trailing punctuation).
- The email wizard **body** must contain the literal string
  `2026-06-01`.
- Use the *Skills* facet of the search filter — filtering only by
  tag name, job, or applicant name does not count.
