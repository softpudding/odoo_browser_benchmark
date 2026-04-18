"""Postcondition checks for website_sale.edit_product_image_gallery."""


PRODUCT_NAME = "Bench Gallery Mug"
EXPECTED_IMAGE_NAME = "Bench Side View"


def check(env):
    failures = []

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if len(products) != 1:
        return [f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(products)}"]

    product = products[0]

    # The product should remain published and its base fields untouched.
    if not product.is_published:
        failures.append("Product was unpublished; it must stay published")
    if abs(product.list_price - 19.0) > 0.0001:
        failures.append(f"Product list_price changed to {product.list_price}; expected 19.0")

    # Exactly one extra product.image should now be linked to this template.
    images = env["product.image"].search([
        ("product_tmpl_id", "=", product.id),
    ])
    named_matches = images.filtered(lambda r: (r.name or "").strip() == EXPECTED_IMAGE_NAME)

    if not named_matches:
        failures.append(
            f"No product.image with name '{EXPECTED_IMAGE_NAME}' found for "
            f"product '{PRODUCT_NAME}' (found {len(images)} total images: "
            f"{[r.name for r in images]})"
        )
    elif len(named_matches) > 1:
        failures.append(
            f"Expected exactly 1 product.image with name '{EXPECTED_IMAGE_NAME}', "
            f"found {len(named_matches)}"
        )
    else:
        img = named_matches[0]
        if not img.image_1920:
            failures.append(
                f"product.image '{EXPECTED_IMAGE_NAME}' has no image_1920 data; "
                "the agent must actually upload an image file"
            )

    if len(images) > 1:
        extras = [r.name for r in images if (r.name or "").strip() != EXPECTED_IMAGE_NAME]
        if extras:
            failures.append(
                f"Extra product.image records created beyond the expected one: {extras}"
            )

    return failures
