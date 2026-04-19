Create and publish a new event with two custom registration questions.

# Phase 1 — Create the event

1. Open the **Events** app (URL `/odoo/events`).
2. Click **New** to open a blank event form.
3. Fill in the event fields:
   - **Event Name**: `Bench 2026 Conference`
   - **Date**: start `07/15/2026 09:00:00`, end `07/16/2026 17:00:00`
4. Leave all other event fields at their defaults (do not change Organizer, Company, Limit Attendees, Tags, etc.).

# Phase 2 — Add two registration questions

On the event form, click the **Questions** tab in the notebook below the
event header. You will add **two** new questions to this event (these are
questions attendees answer when they register on the public website).

## Question 1 — Company

Add a question with these values:
- **Question**: `Company`
- **Type**: `Text Input`
- **Once per Order**: leave **unchecked** (ask once per attendee, NOT per order)
- **Mandatory**: **checked** (required answer)

## Question 2 — Experience Level

Add a second question with these values:
- **Question**: `Experience Level`
- **Type**: `Selection`
- **Once per Order**: leave **unchecked**
- **Mandatory**: **checked**
- On the question form (or nested answer list), add exactly these three
  answer choices in order:
  1. `Beginner`
  2. `Intermediate`
  3. `Expert`

Save the event form.

# Phase 3 — Publish the event

After saving, publish the event so the Questions appear on the public
registration form:

1. Click the **Unpublished** indicator (the `website_redirect_button`
   widget near the top of the event form). This opens the website
   preview of the event.
2. In the website preview top systray, click the **Unpublished** switch
   to flip it to **Published**.

The result: `is_published` / `website_published` are both `True` on the
event.

# Rules

- Do **not** create any additional events.
- Do **not** remove or modify the three default questions that Odoo
  auto-attaches to a new event (Name, Email, Phone). Keep them as-is —
  your two new questions are added **on top** of those defaults.
- Question 1 (`Company`) must have `question_type = 'text_box'` (Text
  Input), NOT Selection.
- Question 2 (`Experience Level`) must have `question_type = 'simple_choice'`
  (Selection) with exactly the three answers above — no more, no fewer.
- Both new questions must have `is_mandatory_answer = True` and
  `once_per_order = False`.
- Do not create any `event.registration` records.
