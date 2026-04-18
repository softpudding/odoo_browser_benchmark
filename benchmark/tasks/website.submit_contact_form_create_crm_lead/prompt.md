# Submit the Contact Form to Create a CRM Lead

You are evaluating the website contact form pipeline. A custom contact form is
already published at the URL `/contactus-bench` on this Odoo site. The form is
wired so that a successful submission creates a **CRM Lead** record in the
backend.

Your task is to open that contact form page **in the frontend website**
(not the backend / Odoo app), fill out every field with the exact values
listed below, and submit the form. The submission should redirect you to the
"Thank You" page — that confirms the lead was created server-side.

## URL to open

Go to the frontend URL `/contactus-bench` (for example by typing the path into
the address bar after navigating to this Odoo instance's home page). The page
shows a heading "Contact Benchmark Industries" with a form containing the
fields Name, Phone Number, Email, Company, Subject, and Message, followed by a
blue **Submit** button.

## Field values to enter

Fill each form field with exactly this text (copy-paste to avoid typos):

| Form field   | Value                                |
|--------------|--------------------------------------|
| Name         | `Bench Prospect Q4`                  |
| Phone Number | `+15555551212`                       |
| Email        | `prospect@bench.test`                |
| Company      | `Bench Test Inc`                     |
| Subject      | `Requesting demo`                    |
| Message      | `Interested in the enterprise plan`  |

## Steps

1. Navigate to `/contactus-bench` in the browser (frontend URL, **not** an
   `/odoo/...` URL).
2. Type each value above into the corresponding form field.
3. Click the **Submit** button at the bottom of the form.
4. Wait until the page redirects to the "Thank You" confirmation page (URL
   `/contactus-thank-you` or a page that shows a thank-you message).

## Rules

- Do not navigate into the website builder / editor — just fill and submit the
  form on the frontend.
- Do not create the CRM Lead manually via the Odoo backend — it must come from
  the frontend form submission.
- All six fields must be populated before submitting.
- Do not reload the page or re-submit the form after the first successful
  submission; only one lead should be created.
