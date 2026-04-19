"""Seed an unpublished storable product for the website shop publish task.

Category: deep_ui_interaction (easy).
Creates a single storable product "Bench Gadget Pro" that is NOT yet published
and has list_price=0.0. The task asks the agent to set list_price=99.00 and
toggle is_published=True via the backend product form.
"""


PRODUCT_NAME = "Bench Gadget Pro"


def setup(env):
    # Cleanup any prior runs (including archived copies).
    env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    ).unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "is_storable": True,
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 0.0,
        "is_published": False,
    })
