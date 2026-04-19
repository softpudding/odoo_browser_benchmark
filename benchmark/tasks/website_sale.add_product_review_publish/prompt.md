Post a customer review on the seeded product's shop page.

Starting from **`/shop`**:

1. The public shop shows a product card labeled **`Bench Review Item`**. Click the card (or its title) to open the product's shop page at `/shop/bench-review-item-<id>` (or similar slug URL).
2. Scroll to the bottom of the product page until you see the **`Customer Reviews`** section header (a collapsed section with a chevron icon on the right). Click it to expand the reviews area.
3. Inside the expanded reviews area, click the **`Add Review`** button. A modal titled **`Write a review`** opens with a star rating row and a message textarea.
4. In the modal:
   - **Rating**: make sure **4 out of 5 stars** are selected (4 is the default when the modal opens, but verify by counting that the first 4 stars are solid yellow/gold and only the 5th is an empty outline). Click the 4th star if you need to set it explicitly.
   - **Message**: type exactly `Great product` into the review textarea.
5. Click the **`Post review`** button (bottom-right of the modal) to submit.
6. The modal closes and a toast / notification may confirm the review was posted. The Customer Reviews section now shows the new review card with 4 solid stars and the body "Great product" authored by the current user.

## Rules

- Do **not** change the star count to anything other than 4.
- Do **not** modify the review text; it must be exactly `Great product` (no trailing period, no extra spaces).
- Do **not** submit multiple reviews — exactly one review row is expected on the product.
- Do **not** edit, rename, archive, or unpublish the product itself.
- Do **not** change the product price or any other product field.
- Leave the review published (do NOT delete it after posting).
