# purchase.send_rfq_email_with_template_signature — result notes

## Run summary

| Agent | Wall clock | Steps | Success | F1 | Strict |
|---|---|---|---|---|---|
| oracle | 34.1s | n/a | True | 1.0 | PASS |
| browser-use | 89.1s | 13 | True | 1.0 | PASS |

BU solved in a single 13-step run (model `bu-1-0`). The task is calibrated
as hard but BU's current capability on non-default template selection is
high enough that it clears the bar on first attempt. Still a useful
benchmark entry because the `action_rfq_send` → compose-wizard →
template-switch → body-append → send-primary pipeline involves 6 discrete
actions and an Owl dropdown portaled out of the modal.

## Hard patterns exercised

1. **Non-default wizard choice**: agent must swap the pre-loaded template
   `Purchase: Request For Quotation` to `Purchase: Purchase Order` via
   the template selector dropdown (rendered as an ellipsis-v icon
   button at the bottom of the compose dialog — NOT a visible `<select>`
   control). The postcondition explicitly rejects the RFQ-template
   marker.
2. **Body edit with preservation**: agent must append
   `Please confirm by Friday.` to the end of the re-rendered template
   body without wiping the existing content.
3. **Sequencing trap**: the prompt warns that appending *before*
   switching the template causes the `onchange_template_id` to overwrite
   the typed text. BU handled this correctly.

## Calibration outcome

- Oracle and BU both PASS with F1=1.0, so the task is a *too-easy hard*.
- Retained at tier 3 because workflow length + wizard count fit the hard
  tier; leave in place as a regression test for BU capability on compose
  wizards.

## Seed calibration quirks

- Had to detach `report_template_ids` from both `email_template_edi_purchase`
  and `email_template_edi_purchase_done`. The default RFQ/PO templates
  attach a PDF report which tries to render via `wkhtmltopdf`. Without
  that binary the whole Send RFQ flow is replaced by an
  `Unable to find Wkhtmltopdf` Invalid Operation error dialog — no
  compose wizard ever appears.
- SMTP sink reused from row 323 (`aiosmtpd` Sink on `127.0.0.1:2525` +
  `ir.mail_server` pointing at it). Without a working outgoing server
  `mail.mail.send(raise_exception=True)` rolls back the transaction and
  the PO state never flips to `sent`.

## check.py assertions

- PO state == `sent` (rejects `purchase` = confirmed; distractor must
  stay `draft`).
- Exactly one `mail.message` on the target PO whose body contains BOTH
  `here is in attachment a purchase order` AND `please confirm by friday`
  (lowercase, whitespace-normalised).
- Body must NOT still contain the RFQ-template marker
  `here is in attachment a request for quotation`.
- Vendor / lines unchanged; no outgoing mail on the distractor.
