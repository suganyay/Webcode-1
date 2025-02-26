import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from web_automation import WebAutomation


@pytest.fixture(scope="class")
def setup_browser():
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get("https://www.guvi.in")
    driver.maximize_window()
    yield driver
    driver.quit()


class TestWebAutomation:

    # Testcase-1: validating the URL
    def test_validate_url(self, setup_browser):
        expected_url = "https://www.guvi.in"
        assert setup_browser.current_url.rstrip("/") == expected_url.rstrip("/"), "Test Case 1: URL validation failed!"

    # Testcase-2: Validating the title page
    def test_validate_title(self, setup_browser):
        expected_title = "GUVI | Learn to code in your native language"
        assert setup_browser.title == expected_title, "Test Case 2: Title validation failed!"

    # Testcase-3: login button visible and clickable
    def test_login_button_visibility_and_clickability(self, setup_browser):
        login_button_locator = (By.XPATH, "//a[@id='login-btn']")
        wait = WebDriverWait(setup_browser, 10)
        login_button = wait.until(EC.presence_of_element_located(login_button_locator))
        assert login_button.is_displayed(), "Test Case 3: Login button not visible!"
        assert wait.until(EC.element_to_be_clickable(login_button_locator)), "Test Case 3: Login button not clickable!"

    # Testcase-4 : Sign-in button visibility and clickability
    def test_sign_in_button_visibility_and_clickability(self, setup_browser):
        driver = setup_browser
        wait = WebDriverWait(driver, 10)

        sign_in_button_locator = (By.XPATH, "//a[@id='login-btn']")

        # ✅ Wait for the button to be visible and clickable
        sign_in_button = wait.until(EC.element_to_be_clickable(sign_in_button_locator))
        sign_in_button.click()

    # Testcase-5:validating the signup page
    def test_validate_sign_up_page(self, setup_browser):
        sign_up_button_locator = (By.XPATH, "//a[@href='/register/']")
        expected_url = "https://www.guvi.in/register"
        setup_browser.find_element(*sign_up_button_locator).click()
        WebDriverWait(setup_browser, 10).until(EC.url_contains("register"))
        assert setup_browser.current_url.rstrip("/") == expected_url.rstrip("/"), "Test Case 5: Sign-up page validation failed!"

    #Testcase-6: login with valid username and password
    def test_login_page(self, setup_browser):
        driver = setup_browser
        wait = WebDriverWait(driver, 10)

        email_locator = (By.XPATH, "//input[@type='email' or @name='email']")
        password_locator = (By.XPATH, "//input[@type='password' and @id='password']")
        sign_in_button_locator = (By.XPATH, "//a[@id='login-btn']")
        success_element_locator = (By.ID, "dashboard")  # Adjust as needed

        # ✅ Wait for elements before interacting
        wait.until(EC.presence_of_element_located(email_locator)).send_keys("sugan2211@gmail.com")
        wait.until(EC.presence_of_element_located(password_locator)).send_keys("YourPassword")

        # ✅ Click using JavaScript if normal click fails
        sign_in_button = wait.until(EC.element_to_be_clickable(sign_in_button_locator))
        driver.execute_script("arguments[0].click();", sign_in_button)  # JS click

        print(" Login attempted!")


    #Testcase-7:login with invalid username and password
    def test_login_with_invalid_credentials(self, setup_browser):
        driver = setup_browser
        wait = WebDriverWait(driver, 10)

        email_locator = (By.XPATH, "//input[@type='email' or @name='email']")
        password_locator = (By.XPATH, "//input[@type='password' and @id='password']")
        sign_in_button_locator = (By.XPATH, "//a[@id='login-btn']")
        error_message_locator = (By.XPATH, "//div[@class='invalid-feedback']")

        wait.until(EC.presence_of_element_located(email_locator)).send_keys("invalid_email@example.com")
        wait.until(EC.presence_of_element_located(password_locator)).send_keys("Invalid@password")

        sign_in_button = wait.until(EC.element_to_be_clickable(sign_in_button_locator))
        driver.execute_script("arguments[0].click();", sign_in_button)  # JS click for safety

        # Check for error message
        assert wait.until(EC.presence_of_element_located(error_message_locator)), "Error message not found!"

        print("Invalid login test passed!")



