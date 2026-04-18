Go to the **Point of Sale** app and open the register **`Bench Loyalty POS`** (accept the default opening cash of 0 if asked).

1. Add **`Bench POS Item`** to the cart and set the quantity to **3** (€20 each — the cart subtotal should be **€60.00**).
2. Click the **Customer** button on the action pad and select the existing customer **`Loyal Larry`**. The customer name must now appear on the order header.
3. Open the **Rewards** popup (the on-screen "Rewards" button on the action pad, sometimes grouped inside the Actions / ellipsis popup on smaller screens). In the list, redeem the reward named **`10% on your order`** for program **`Bench Loyalty Program`** — this reward costs **50 points** of Larry's loyalty balance. After redeeming, a new reward line with a negative amount (around **`-6.00`**) must appear on the order.
4. Click **Payment**, choose the **`Bench Loyalty Cash`** payment method, then validate the payment so the receipt screen appears. The final order total must be **€54.00**.

## Rules

- Do not add any other product to the cart
- Do not change the unit price of `Bench POS Item`
- Do not change Larry's loyalty points manually; redeem through the Rewards popup
- Do not close the POS session after the sale
- Use the `Loyal Larry` customer that is already seeded — do NOT create a new customer
