"""Oracle for website.update_contact_info.

Navigate to the About Us page, open the website editor, change the phone
number to +1 555 987 6543, and save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/website")
    _wait_no_loading(page)

    # Navigate to the About Us page
    navigate(page, "/about-us")
    _wait_no_loading(page)

    # Click Edit to open the website editor
    page.click('button:has-text("Edit")')
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Find the phone number text and edit it
    # The phone number is in a <p> tag containing "+1 555 123 4567"
    page.locator('text="+1 555 123 4567"').click()
    page.wait_for_timeout(500)

    # Clear and type the new phone number
    page.locator('text="+1 555 123 4567"').fill("+1 555 987 6543")
    page.wait_for_timeout(500)

    # Click Save
    page.click('button:has-text("Save")')
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
