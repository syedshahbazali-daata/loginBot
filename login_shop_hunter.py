from playwright.sync_api import sync_playwright
from generalFuncations import *

EMAIL = "myers.grant@icloud.com"
PASSWORD = "Shophunter123"


def login_shop_hunter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://app.shophunter.io/login")

        # Fill in email and password
        page.fill('input[placeholder="Email Address"]', EMAIL)
        page.fill('input[placeholder="Password"]', PASSWORD)
        print("Filled in email and password")

        # Click the login button
        page.click('xpath=//button/text')
        print("Clicked the login button")

        # Wait for the license API request
        with page.expect_response("https://app.shophunter.io/prod/user/license") as response_info:
            page.wait_for_load_state("networkidle")  # Ensure the page is fully loaded

        # Get the response from the license API
        response = response_info.value
        authorization = response.request.headers["authorization"]
        print(f"Authorization: {authorization}")

        record = {
            "authorization": authorization
        }

        write_json_file("authorization.json", record)

        # Close the browser
        browser.close()

    return authorization



if __name__ == "__main__":
    
    login_shop_hunter()
