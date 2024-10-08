from playwright.sync_api import sync_playwright
from datetime import datetime
import requests

EMAIL = "myers.grant@icloud.com"
PASSWORD = "Shophunter123"


def update_login_auth(authorization_code, message_status):
    payload = {

        "authorization": authorization_code,
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message_status
    }

    res = requests.post("https://67051d5c031fd46a830eb344.mockapi.io/api/1", json=payload)
    print(res.json())
    if res.status_code == 200:
        print("Login authentication updated successfully.")
    else:
        print("Failed to update login authentication.")


def login_shop_hunter():
    try:
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

            # Update the login authentication
            # update_login_auth(authorization, "Success")

            # Close the browser
            browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        update_login_auth("", "Failed")



if __name__ == "__main__":
    login_shop_hunter()
