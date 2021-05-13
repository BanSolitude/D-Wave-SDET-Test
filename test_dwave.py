import pytest
import time

from selenium import webdriver

from loginpage import LoginPage
from dashboardpage import DashboardPage

# Credentials used to log in
# Needs to be a registered user of leap
USERNAME = "danielsbusto@gmail.com"
PASSWORD = "[REDACTED]"
# Address of D-Wave's login page
LOGIN_URL = "https://cloud.dwavesys.com/leap/login/"


@pytest.fixture()
def login_page(request):
    """Opens a login page instance to be used by each function"""
    with webdriver.Chrome() as driver:
        driver.get(LOGIN_URL)
        login_page = LoginPage(driver)

        request.instance.login_page = login_page

        # Yield here to prevent the window from being closed before the test is actually run
        yield


@pytest.fixture(scope="class")
def dashboard(request):
    """
    Logins in to leap and lands on the dashboard page to be used by an entire test class
    Cannot use a login_page fixture as an argument as the scope is different
    """
    with webdriver.Chrome() as driver:
        driver.get(LOGIN_URL)

        login_page = LoginPage(driver)
        login_page.login(USERNAME, PASSWORD)

        dashboard = DashboardPage(login_page.driver)
        request.cls.dashboard = dashboard

        # Yield here to prevent the window from being closed before the test is actually run
        yield


@pytest.mark.usefixtures("login_page")
class TestLogin:
    """Tests the basic functionality of the login page"""

    def test_forgotpassword(self):
        """Tests that the forgot password link directs to the correct url"""
        password_reset_url = "https://cloud.dwavesys.com/leap/accounts/password_reset/"

        self.login_page.forgot_password.click()
        assert self.login_page.driver.current_url == password_reset_url

    def test_havingtrouble(self):
        """Tests that the having trouble link directs to the correct url"""
        login_article_url = "https://support.dwavesys.com/hc/en-us/articles/360002772833"

        self.login_page.having_trouble.click()
        assert self.login_page.driver.current_url == login_article_url

    def test_login_correctcredentials(self):
        """
        Tests that you get redirected to the landing page after successfully logging in
        Note: the account must be properly verified on the browser being used for testing
        """
        self.login_page.login(USERNAME, PASSWORD)
        assert self.login_page.driver.current_url == "https://cloud.dwavesys.com/leap/"

    def test_login_incorrectcredentials_showserror(self):
        """
        Tests that the login error is shown after entering an invalid password
        A new username is generated each run to ensure the user being tested is not locked out
        time.time() is used to ensure the usernames are unique
        The error.com domain is used to ensure the usernames don't match real users
        """
        self.login_page.login(f"{time.time()}@error.com", "password")
        assert self.login_page.login_error_visible()

    def test_login_lockout(self):
        """
        Tests that a lockout error is displayed if an incorrect password is entered 3 times
        A new username is generated each run to ensure the user being tested is not already locked out
        time.time() is used to ensure the usernames are unique
        The lockout.com domain is used to ensure the usernames don't match real users
        """
        username = f"{time.time()}@lockout.com"

        # loop to attempt to login thrice with the same name
        for _ in range(3):
            self.login_page.login(username, "password")

        assert self.login_page.locked_out_message_visible()

    def test_login_nopassword_resetsusername(self):
        """Tests that the username field is cleared after attempting to login without a password"""
        self.login_page.login(USERNAME, "")

        assert self.login_page.username.get_attribute("value") == ""

    def test_login_nopassword_samepage(self):
        """Tests that the user remains on the login page after trying to login incorrectly"""
        self.login_page.login(USERNAME, "")

        assert self.login_page.driver.current_url == LOGIN_URL

    def test_signup(self):
        """Tests the sign up link directs to the correct url"""
        self.login_page.sign_up.click()
        assert self.login_page.driver.current_url == "https://cloud.dwavesys.com/leap/signup/"


@pytest.mark.usefixtures("dashboard")
class TestDashboardValues:
    """Tests that the values displayed for the account on the left side are correct"""

    def test_verifyaccountname(self):
        """Tests that the name matches the user's inputted name"""
        assert self.dashboard.account_name == "Daniel Busto"

    def test_verifyaccounttype(self):
        """Check that the account type matches the user plan"""
        assert self.dashboard.account_type == "Trial Plan"

    def test_verifyrenewaldate(self):
        """Tests that the renewal date is one month after sign-up"""
        assert self.dashboard.renewal_date == "June 8, 2021 (UTC)"

    def test_verifyapitoken_hidden(self):
        """Tests that the API token value is set to dots by default"""
        assert self.dashboard.api_token == "••••••••••••••••••••••••••••••••••••••••••••"

    def test_verifyapitoken_revealed(self):
        """
        Tests that the API token value is correct after the show token button is pressed
        """
        self.dashboard.toggle_api_token_visibility()
        try:
            assert self.dashboard.api_token == "DEV-[REDACTED]"
        finally:
            # reset API token visibility to state before test, whether or not it passes
            self.dashboard.toggle_api_token_visibility()

    # The assignment specifically asked about verifying the project name
    # But trial accounts are not assigned a project, so it was not included
