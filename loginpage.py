from selenium.common.exceptions import NoSuchElementException


class LoginPage:
    """
    Encapsulates various features of D-Wave's login page
    https://cloud.dwavesys.com/leap/login/
    """

    def __init__(self, driver):
        """
        :param driver: The webdriver used to drive the browser
        """
        self.driver = driver

    @property
    def log_in_button(self):
        """ The button that submits the login form """
        return self.driver.find_element_by_xpath("//input[@id='loginFormSubmit']")

    @property
    def username(self):
        """ The input for the user's email address"""
        return self.driver.find_element_by_name("username")

    @property
    def password(self):
        """The input for the user's password"""
        return self.driver.find_element_by_name("password")

    @property
    def forgot_password(self):
        """Link to the form used to reset a user's password"""
        return self.driver.find_element_by_xpath("//a[.='Forgot password?']")

    @property
    def having_trouble(self):
        """Link to help article on signing-in to Leap"""
        return self.driver.find_element_by_xpath("//a[.='Having trouble logging in?']")

    @property
    def resend_link(self):
        """Link to page to resend account activation link"""
        return self.driver.find_element_by_xpath("//a[.='Resend link']")

    @property
    def sign_up(self):
        """Link to the sign-up page"""
        return self.driver.find_element_by_xpath("//a[.='Sign up']")

    def locked_out_message_visible(self):
        """Message displayed when the user enters an incorrect password 3 times"""
        try:
            self.driver.find_element_by_xpath("//h1[.='Account Locked Out']")
        except NoSuchElementException:
            return False
        else:
            return True

    def login_error_visible(self):
        """
        The div containing an error message, displayed when the user enters
        an invalid username password combination
        """
        try:
            self.driver.find_element_by_xpath("//div[contains(@class, 'login-error')]")
        except NoSuchElementException:
            return False
        else:
            return True

    def login(self, username, password):
        """Enter a username and password and click the login button"""
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.log_in_button.click()
