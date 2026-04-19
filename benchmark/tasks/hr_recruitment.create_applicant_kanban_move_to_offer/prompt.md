Go to the **Recruitment** app (URL path `/odoo/recruitment`).

On the main Recruitment kanban you will see the job position card for
**Bench Senior Dev**. The job pipeline has been pre-seeded with four
stages, left-to-right:

1. **Initial Qualification**
2. **Qualified**
3. **Contract Proposal**
4. **Contract Signed**

There is a **single candidate** to process. Do the following, **in
order**.

## 1. Open the job's Applications kanban

Click on the **Bench Senior Dev** job card (or the Applications link
inside its kanban card menu). This opens the Applications kanban
grouped by stage, restricted to that job. The four columns above are
visible in that order.

## 2. Create a new applicant in the "Initial Qualification" column

At the top of the **Initial Qualification** column there is a `+` /
**New** button. Click it. A quick-create row opens with a field for
the applicant's name — fill it with:

- **Name**: `Alice Applicant`

The quick-create only has name + job. To record the contact details,
**open the full form of the new applicant** (use the *Edit* link on
the quick-create row, or save the quick-create and then click the
newly-created card to open the form). On the form, fill:

- **Email**: `alice@bench.test`
- **Phone**: `+15555555555`

Make sure the applicant's **Job Position** is `Bench Senior Dev` and
the **Stage** is `Initial Qualification` (the status bar at the top of
the form).

Save the applicant (cloud icon, or navigate away — Odoo auto-saves).

## 3. Move the applicant from Initial Qualification to Contract Proposal

You must advance the applicant through **two** stages so it ends up in
**Contract Proposal**. Either of the following methods works — pick
the one that reliably commits the change:

- **Form status bar**: on the applicant form, the status bar shows the
  four stages as clickable buttons. Click **Qualified** (the applicant
  moves). Then click **Contract Proposal**. The status bar highlights
  the current stage.
- **Kanban drag**: from the Applications kanban, drag the applicant's
  card from **Initial Qualification** to **Qualified**, then from
  **Qualified** to **Contract Proposal**.

After this, **Alice Applicant** must be in the **Contract Proposal**
column of Bench Senior Dev — not Initial Qualification, not Qualified,
not Contract Signed.

## Rules

- The applicant's **Name** must be exactly `Alice Applicant`
  (case-sensitive, one space, no trailing punctuation).
- The applicant's **Email** must be exactly `alice@bench.test`.
- The applicant's **Phone** must be exactly `+15555555555` (no spaces,
  no dashes).
- The applicant must be on the **Bench Senior Dev** job, in stage
  **Contract Proposal**.
- Do **not** refuse, archive, or hire the applicant.
- Do **not** create any other applicants.
- Do **not** rename, archive, delete, or reorder any of the four
  stages.
