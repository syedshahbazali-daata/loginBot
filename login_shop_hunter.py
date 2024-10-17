from playwright.sync_api import sync_playwright
from datetime import datetime
import requests

EMAIL = "myers.grant@icloud.com"
PASSWORD = "Shophunter123"


def update_login_auth(authorization_code, message_status):
    payload = {

        "authorization": authorization_code,
        "lastUpdated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "message": message_status
    }

    res = requests.post("https://67051d5c031fd46a830eb344.mockapi.io/api", json=payload,
                        headers={"Content-Type": "application/json"})
    print(res.text, "update_login_auth")
    
    res = requests.get("https://flasktest-render.onrender.com/api/get_authorization")
    print(res.text, "update_login_auth on flaskBackend")




def delete_login_auth():
    res = requests.delete("https://67051d5c031fd46a830eb344.mockapi.io/api/1")
    print(res.text, "delete_login_auth")


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

            delete_login_auth()
            update_login_auth(authorization, "Success")

            # Update the login authentication
            # update_login_auth(authorization, "Success")

            # Close the browser
            browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        delete_login_auth()
        update_login_auth("", "Failed")


if __name__ == "__main__":
    login_shop_hunter()
