"""Seed a quotation with 20 product lines for deep-scroll editing.

Category 5: Deep UI interaction.
The target line (Ergonomic Footrest) is placed at position 16 out of 20,
requiring the agent to scroll within the nested o2many widget.
Distractors with similar names (Ergonomic Keyboard, Ergonomic Mouse Pad)
are placed earlier in the list to tempt mis-clicks.
"""

# 20 products — target is at index 15 (0-based), distractors at 3 and 7
PRODUCTS = [
    ("Executive Desk", 890.0, 2, 0),
    ("Mesh Office Chair", 450.0, 6, 5),
    ("Filing Cabinet 3-Drawer", 220.0, 4, 0),
    ("Ergonomic Keyboard", 75.0, 10, 0),        # distractor (similar name)
    ("Monitor Stand", 65.0, 8, 0),
    ("Whiteboard 120x90", 180.0, 3, 0),
    ("Desk Lamp LED", 55.0, 12, 0),
    ("Ergonomic Mouse Pad", 25.0, 15, 0),        # distractor (similar name)
    ("Cable Management Kit", 35.0, 20, 0),
    ("Privacy Screen Filter", 45.0, 6, 0),
    ("Acoustic Panel Set", 310.0, 4, 10),
    ("Standing Desk Converter", 380.0, 3, 0),
    ("Bookshelf Unit", 260.0, 2, 0),
    ("Visitor Chair", 175.0, 8, 0),
    ("Desk Organizer", 40.0, 10, 0),
    ("Ergonomic Footrest", 95.0, 5, 0),          # TARGET — qty 5->12, disc 0->8
    ("Conference Table", 1200.0, 1, 0),
    ("Projector Mount", 85.0, 4, 0),
    ("Coat Rack", 120.0, 3, 0),
    ("Reception Desk", 1500.0, 1, 5),
]


def setup(env):
    # --- Enable per-line discount field on SO form ---
    discount_group = env.ref("sale.group_discount_per_so_line", raise_if_not_found=False)
    admin = env.ref("base.user_admin")
    if discount_group:
        admin.write({"group_ids": [(4, discount_group.id)]})

    partner = env["res.partner"].search([("name", "=", "Summit Office Group")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Summit Office Group",
            "email": "procurement@summit.example.com",
        })

    # --- Create products ---
    products = {}
    for name, price, *_ in PRODUCTS:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            p = tmpl.product_variant_id
        else:
            p.product_tmpl_id.write({"list_price": price})
        products[name] = p

    # --- Cleanup ---
    env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", "LONG-ORDER-01"),
    ]).unlink()

    # --- Create quotation with 20 lines ---
    so = env["sale.order"].create({
        "name": "LONG-ORDER-01",
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": "LONG-ORDER-01",
    })

    for name, price, qty, discount in PRODUCTS:
        env["sale.order.line"].create({
            "order_id": so.id,
            "product_id": products[name].id,
            "product_uom_qty": qty,
            "price_unit": price,
            "discount": discount,
        })
