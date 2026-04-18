Publish an eLearning course, lock it to enrolled attendees with a prerequisite,
and assign two existing contacts as attendees.

Background: Two draft courses already exist in the eLearning app:

- `Bench Onboarding` — the course you must configure in this task. It is
  currently unpublished with default visibility (Everyone).
- `Bench 101` — a pre-requisite primer course. It is already published and is
  already restricted to Course Attendees (visibility = Course Attendees,
  enroll = On Invitation).

Two contacts also already exist and must be added as attendees of
`Bench Onboarding`:

- `Alice Attendee` (email `alice.attendee@bench.test`)
- `Bob Attendee` (email `bob.attendee@bench.test`)

Steps to perform on `Bench Onboarding`:

1. From the eLearning app, open the `Bench Onboarding` course form.
2. Open the `Options` tab.
3. Under `Access Rights`, change `Show Course To` to `Course Attendees`.
   (This will automatically make the `Enroll Policy` become `On Invitation`
   — that is expected, leave it that way.)
4. Publish the course. The form header's "Go to Website" button navigates to
   the frontend `/slides/...` page for this course. From that frontend page,
   use the top-right `Unpublished` / `Published` toggle in the admin systray
   to publish the course (flip it to `Published`).
5. Come back to the backend form of `Bench Onboarding` (for example via the
   breadcrumbs / browser Back, or by re-opening the course from the
   eLearning app). Go back to the `Options` tab.
6. In `Access Rights`, in the `Prerequisites` many2many tags field, add
   `Bench 101`. (The dropdown filters prerequisites by matching visibility
   and published state, so `Bench 101` only becomes selectable after step 3
   and step 4 are done.)
7. Save the course.
8. Back in the course form header, click `Add Attendees`. This opens the
   Enroll Attendees email wizard. In the `Recipients` field, add both
   `Alice Attendee` and `Bob Attendee`. Leave the subject and body as
   provided by the template. Click `Send` to enroll them.
9. Finally, navigate to the public course page at `/slides/<course>` (for
   example by clicking `Go to Website` again on the form) to confirm the
   course is visible at the frontend URL.

End state to achieve:

- `Bench Onboarding` is published (`is_published=True`).
- `Bench Onboarding` has `visibility = 'members'` (Course Attendees) and
  `enroll = 'invite'`.
- `Bench Onboarding` has `Bench 101` in its prerequisite courses.
- `Bench Onboarding` has exactly two enrolled attendees: `Alice Attendee` and
  `Bob Attendee`, both with `member_status = 'joined'`.
- `Bench 101` is unchanged.

Rules:

- Use the EXACT spelling `Bench Onboarding`, `Bench 101`, `Alice Attendee`,
  `Bob Attendee` — do not rename or create new courses/partners.
- Do NOT archive either course. Do NOT delete `Bench 101` from the database.
- Do NOT add attendees by creating `slide.channel.partner` rows manually in a
  list view — use the header `Add Attendees` wizard on the course form.
- Do NOT toggle publication from the backend list view; use the frontend
  publish toggle on the `/slides/...` page after clicking `Go to Website`.
