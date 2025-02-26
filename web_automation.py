"""MINI PROJECT-VERSION-1"""

"""
1.Check whether URL "https://www.guvi.in" is correct or not
2.Check whether the title of webpage is "GUVI | Learn to code in your native language or not"
3.check whether login button is clickable and visible
4.check whether sign-in button is clickable and visible
5.click URL using sign-up button to check whether the webpage exists or not
6.Log-in to Guvi account using valid username and password to verify the login is successful or not and Log-out from guvi account and verify it.
7.Log-in into guvi account using invalid username and password and catch the error message.

"""


from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep


class WebAutomation:
    def __init__(self, web_url,email, password, invalid_email, invalid_password):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.url = web_url
        self.email = email
        self.password = password
        self.invalid_email = invalid_email
        self.invalid_password = invalid_password
        self.driver.get(self.url)

    def start(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            sleep(3)
            return True
        except Exception as error:
            print(error)
            return False

    def fetch_url(self):
        try:
            return self.driver.current_url
        except Exception as e:
            return f"ERROR: Unable to fetch URL! {e}"

    def validate_url(self, expected_url):
        current_url = self.driver.current_url.rstrip("/")
        expected_url = expected_url.rstrip("/")
        if current_url == expected_url:
            print("Test case-1: URL validation passed!")
        else:
            print(f"Test case-1: URL validation failed! Expected: {expected_url}, Got: {current_url}")

    def validate_title(self, expected_title):
        current_title = self.driver.title
        assert expected_title == current_title, f"Expected '{expected_title}', got '{current_title}'"
        if current_title == expected_title:
            print(f"Test case-2: Title is valid and passed: {current_title}")
            return True
        else:
            print(f"Test case-2: Title is not valid and Failed: Expected '{expected_title}', Got '{current_title}'")
            return False

    def check_login_button(self, button_locator):
        results = {"visible": False, "clickable": False}
        try:
            # Add explicit wait for page load
            self.driver.implicitly_wait(10)

            # Wait for element to be present and visible
            wait = WebDriverWait(self.driver, 20)
            login_button = wait.until(
                EC.presence_of_element_located(button_locator)
            )

            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)

            # Check visibility
            if login_button.is_displayed():
                results["visible"] = True
                print("Test case-3: Login button is visible")

                # Check clickability
                wait.until(EC.element_to_be_clickable(button_locator))
                results["clickable"] = True
                print("Test case-3: Login button is clickable")
            else:
                print("Test case-3: Login button is not visible")

        except Exception as e:
            print(f"Test case-3: Error: {str(e)}")

        return results

    def check_sign_in_button(self, button_locator):
        results = {"visible": False, "clickable": False}
        try:
            sign_in_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(button_locator))
            if sign_in_button.is_displayed():
                results["visible"] = True
                print("Test case-4: Sign-in button is visible")
            else:
                print("Test case-4: Sign-in button is not visible")
                return results

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button_locator))
            results["clickable"] = True
            print("Test case-4: Sign-in button is clickable")
        except TimeoutException:
            print("Test case-4: Timeout waiting for the Sign-in button to appear or become clickable.")
        except Exception as e:
            print(f"Test case-4: Error: {str(e)}")
        return results

    def validate_sign_up_page(self, sign_up_button_locator, expected_url):
        try:
            # Wait for page load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(sign_up_button_locator)
            )

            sign_up_button = self.driver.find_element(*sign_up_button_locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_button)
            sign_up_button.click()

            # Wait for URL change
            WebDriverWait(self.driver, 10).until(
                lambda driver: "register" in driver.current_url
            )

            current_url = self.driver.current_url.rstrip("/")
            expected_url = expected_sign_up_url.rstrip("/")

            if current_url == expected_url:
                print(f"Test case-5: Web page exists and is reachable: {current_url}")
                return True
            else:
                print(f"Test case-5: Web page does not exist. Redirected to: {current_url}")
                return False
        except Exception as e:
            print(f"Test case-5: Error: {str(e)}")
            return False

    def login_page(self, email_locator, password_locator, sign_in_button_locator, success_element_locator):
        try:
            # Create WebDriverWait object
            self.driver.find_element(*email_locator).send_keys(self.email)
            wait = WebDriverWait(self.driver, 30)  # Increased wait time

            login_button = self.driver.find_element(*login_link_locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            login_button.click()

            # Wait for email field to be visible and interactable
            email_field = wait.until(EC.visibility_of_element_located(email_locator))
            email_field.clear()
            email_field.send_keys(self.email)

            # Wait for password field to be visible and interactable
            password_field = wait.until(EC.visibility_of_element_located(password_locator))
            password_field.clear()
            password_field.send_keys(self.password)

            # Wait for the sign-in button to be clickable
            login_button = wait.until(EC.element_to_be_clickable(login_button_locator))
            login_button.click()  # Perform click action

            # Wait for the dashboard heading to appear after login
            wait.until(EC.visibility_of_element_located(dashboard_text_locator))
            print("Test case-6: Login Success")
            return True

        except TimeoutException:
            print("Test Case-6: Login Failed - Timeout while waiting for elements")
        except NoSuchElementException:
            print("Test Case-6: Login Failed - Element not found")
        except Exception as e:
            print(f"Test Case-6: Login Failed - {str(e)}")
        return False

    def login_with_invalid_credentials(self):
        try:
            # Wait for elements to be present
            wait = WebDriverWait(self.driver, 10)

            dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @id='dropdown_title']")))
            dropdown_button.click()

            signout_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='dropdown_contents' and text()='Sign Out']")))
            signout_button.click() # Click without scrolling
            # Wait for URL change
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url.rstrip("/") == expected_url.rstrip("/")
            )

            current_url = self.driver.current_url.rstrip("/")
            login_url = expected_url.rstrip("/")
            if current_url == login_url:
                self.driver.execute_script("window.scrollTo(0, 0);")
                login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='login-btn']")))
                login_button.click()  # Click without scrolling


            email_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email']")))
            email_field.clear()
            email_field.send_keys(self.invalid_email)

            # Enter invalid password
            password_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @id='password']")))
            password_field.clear()
            password_field.send_keys(self.invalid_password)

            login_button = wait.until(EC.element_to_be_clickable(login_button_locator))
            login_button.click()  # Perform click action

            # Wait for error message
            error_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='invalid-feedback']")))
            print(f"Test Case-7:Success. Login Failed with Invalid Credentials ")
            return True

        except TimeoutException:
            print("Test Case-7: Failed - Timeout while waiting for elements")
        except NoSuchElementException:
            print("Test Case-7: Failed - Element not found")
        except Exception as e:
            print(f"Test Case-7: Failed - {str(e)}")
        return False

    def close_browser(self):
        self.driver.quit()




"""if __name__ == "__main__":
    web_url = "https://www.guvi.in"
    expected_url = "https://www.guvi.in"
    expected_sign_up_url = "https://www.guvi.in/register"
    dashboard_text_locator = (By.XPATH, "//h2[contains(text(), 'Browse Courses by Languages')]")
    expected_title = "GUVI | Learn to code in your native language"
    email = "sugan2211@gmail.com"
    password = "Sug@n2211"
    invalid_email = "invalid_email@example.com"
    invalid_password = "Invalid@password"

    login_button_locator = (By.XPATH, "//a[@id='login-btn']")
    login_link_locator = (By.XPATH,"//a[@href='/sign-in/']")
    sign_in_button_locator = (By.XPATH, "//button[@type='submit']")
    sign_up_button_locator = (By.XPATH, "//a[@href='/register/']")
    email_locator = (By.XPATH, "//input[@type='email' or @name='email']")
    password_locator = (By.XPATH, "//input[@type='password' and @id='password']")
    success_element_locator = (By.ID, "dashboard")

    automation = WebAutomation(web_url, email, password, invalid_email, invalid_password)

    automation.validate_url(expected_url)
    automation.validate_title(expected_title)
    automation.check_login_button(login_button_locator)
    automation.check_sign_in_button(sign_in_button_locator)
    automation.validate_sign_up_page(sign_up_button_locator, expected_url)
    automation.login_page(email_locator, password_locator, sign_in_button_locator, success_element_locator)
    automation.login_with_invalid_credentials()
    automation.close_browser()
"""