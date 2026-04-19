Go to the backend **Delivery Methods** configuration page (**Sales > Configuration > Delivery Methods**, URL `/odoo/delivery-methods`).

Open the seeded delivery method **`Bench Ship`** (it already exists with Provider = Fixed Price and Fixed Price = 15.00).

You must enable a free-shipping threshold on this carrier:

1. On the `Bench Ship` form, locate the field labelled **"Free if order amount is above"** (this is a checkbox in the right-hand group). **Tick** the checkbox.
2. Once the checkbox is ticked, an **Amount** input appears next to it. Set the **Amount** to **`100.00`**.
3. **Save** the delivery method (cloud / save icon).

## Rules

- Do **not** change the **Delivery Method** name (`Bench Ship`).
- Do **not** change the **Provider**; it must remain **Fixed Price** (`delivery_type='fixed'`).
- Do **not** change the **Fixed Price** (it must stay at `15.00`). The free-shipping threshold is a separate field; do not confuse it with the price of the shipping line.
- Do **not** change the Delivery Product or create a new carrier.
- The free-shipping **Amount** must be exactly `100.00` — leaving it at the default `1000` or any other value is a failure.
- The free-shipping checkbox (`free_over`) must end up **ticked / True**.
