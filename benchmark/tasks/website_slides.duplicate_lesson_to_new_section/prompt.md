Duplicate an existing lesson into a new section of an eLearning course.

Background: A published course named `Bench Onboarding Course` already exists in
the eLearning app. It currently has one section named `Intro` containing one
video lesson named `Welcome Video`. Leave the existing `Intro` section and the
original `Welcome Video` lesson untouched.

Steps:

1. Open the eLearning app and go to the `Bench Onboarding Course`.
2. Open the course content list and add a NEW section named `Advanced`. The
   section must be created on the same course (it is a content row whose type
   is `Section`). Do not put any lesson directly into it yet.
3. Open the existing `Welcome Video` lesson form. Use the form's Actions /
   cog menu and click `Duplicate` to create a copy of the lesson.
4. On the duplicated lesson:
   - Change its section to `Advanced` (the duplicate must end up listed under
     the `Advanced` section in the course content list, not under `Intro` and
     not as an uncategorized lesson).
   - Rename it to `Advanced Welcome`.
5. Save the duplicate.

End state to achieve:

- The course `Bench Onboarding Course` has exactly two sections: `Intro` and
  `Advanced` (in that order).
- The original `Welcome Video` lesson is still in the `Intro` section,
  unchanged (still a published video lesson).
- A new lesson named `Advanced Welcome` exists in the `Advanced` section.
  It is a copy of `Welcome Video` (same video category) but with the new name.

Rules:

- Use the exact names above (`Advanced` for the section, `Advanced Welcome`
  for the duplicated lesson).
- Do NOT delete or rename `Welcome Video`. Do NOT move it out of `Intro`.
- Do NOT create the `Advanced Welcome` lesson from scratch — it must come
  from duplicating `Welcome Video` via the Actions / cog menu.
- Do not add any other sections or lessons.
