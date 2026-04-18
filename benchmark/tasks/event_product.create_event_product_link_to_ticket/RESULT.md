ROW: 317
TASK_ID: event_product.create_event_product_link_to_ticket
DIFFICULTY: medium
SUMMARY: Create service product with service_tracking=event, then add event ticket linked to that product on Spring Summit.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## event_product.create_event_product_link_to_ticket

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Events, Sales, Inventory (event_product bridge) |
| **Workflow** | Agent navigates to Products list, creates a Service product 'Conference Pass Std' with list_price=100 and Service Tracking='Event Registration'. Then opens event 'Spring Summit', goes to the Tickets tab and adds a 'Standard Pass' ticket linked to that product (price=100, seats_max=200). |
| **Capability tested** | Cross-app workflow that requires picking the obscure 'Event Registration' option on a service product so it becomes eligible as an event ticket product. |
| **Notes** | Browser-use solved it on first run — calibrated EASIER than medium. The 'Service Tracking' selection appears on the product form because event_sale (auto-installed) removes the original `invisible` attribute. Two pre-existing 'Gift Card' product.template duplicates with different list_prices caused dup-key nondeterminism in the diff engine; fixed by adding (service_tracking, list_price) to the product.template match_key. |
