"""Oracle for sale_loyalty.buy_x_get_y_reward_in_cart.

Pure Playwright UI flow:
  1. Log in, navigate to Sales > Quotations.
  2. Create a new quotation for 'Bench Promo Customer'.
  3. Add one order line: product 'Bench Promo Widget' with quantity 2
     (unit price defaults to 10.0 from the product).
  4. Save the quotation.
  5. Claim the Buy-2-Get-1-Free reward via the 'Claim Reward' button in
     the statusbar (opens the reward wizard for 'Bench BOGO'), then Apply.
  6. Confirm the quotation so the sale.order state becomes 'sale'.
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    click_add_a_line,
    click_create,
    click_status_button,
    login,
    modal_click_button,
    navigate,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    run_oracle,
)


PROGRAM_NAME = "Bench BOGO"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Widget"


def _claim_reward(page) -> None:
    """Open the reward wizard and apply the 'Bench BOGO' reward.

    The Claim Reward button is a statusbar action named
    'action_open_reward_wizard'. For a program with a single claimable
    reward the server may apply it directly (no modal opens). Otherwise
    a modal with a radio-list of rewards appears.
    """
    # Prefer the by-name selector: it is resilient to button label changes.
    btn = page.locator(
        "button[name='action_open_reward_wizard']:visible"
    )
    if btn.count() == 0:
        # Fallback: match by visible text in the statusbar / header.
        btn = page.locator(
            ".o_statusbar_buttons button:visible:has-text('Claim Reward'), "
            "button:visible:has-text('Claim Reward')"
        )
    btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # If a reward wizard modal opens, select the BOGO reward and apply.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # The wizard renders reward options as radio inputs / labels.
        # Pick the one that mentions the product (Free Product - ...).
        option = modal.locator(
            f"label:has-text('{PRODUCT_NAME}'), "
            f".o_field_widget input[type='radio'] + label:has-text('{PRODUCT_NAME}')"
        )
        if option.count() > 0:
            option.first.click()
            page.wait_for_timeout(300)
        else:
            # Fallback: click the first option (there is only one seeded reward).
            radios = modal.locator("input[type='radio']")
            if radios.count() > 0:
                radios.first.click()
                page.wait_for_timeout(300)

        modal_click_button(page, "Apply")
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


def oracle(page):
    login(page)

    # 1. Go to the Sales Quotations list view.
    navigate(page, "/odoo/sales")

    # 2. Start a new quotation.
    click_create(page)

    # 3. Set the customer.
    set_many2one(page, "partner_id", CUSTOMER_NAME)

    # 4. Add the paid order line: 'Bench Promo Widget', qty 2.
    click_add_a_line(page)
    set_o2m_many2one(page, 0, "product_template_id", PRODUCT_NAME)
    set_o2m_field(page, 0, "product_uom_qty", "2")

    # 5. Save — quotation moves to state 'draft' with a persisted order_line.
    save_form(page)

    # 6. Claim the BOGO free-product reward via the wizard.
    _claim_reward(page)

    # 7. Confirm the quotation → state 'sale'.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
