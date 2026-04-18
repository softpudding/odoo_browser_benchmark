# Add registration questions to an event

You are in the Odoo 19 **Events** app logged in as **Administrator**.

The event **Bench Tech Conference 2026** is scheduled but its registration
form is missing two questions that the marketing team needs for follow-up.
Add them to the event so attendees see them when registering.

## What to do

1. Open the **Events** app and open the event **Bench Tech Conference 2026**.
2. Switch to the **Questions** tab on the event form.
3. Add a new question with **Title** `What is your job title?` of type
   **Text Input**.
4. Add a second new question with **Title** `How many years of experience?`
   of type **Selection**, with exactly three answer options in this order:
   - `0-2`
   - `3-5`
   - `5+`
5. **Save** the event.

## Rules

- Both questions must be linked to the **Bench Tech Conference 2026** event.
- The titles must be EXACTLY `What is your job title?` and
  `How many years of experience?` (no trailing whitespace, no extra text).
- The first question must be type **Text Input** (`text_box`).
- The second question must be type **Selection** (`simple_choice`) and have
  EXACTLY the three answer options `0-2`, `3-5`, `5+` — no more, no less.
- Do **not** create or modify any other event.
- Do **not** delete any existing question.
