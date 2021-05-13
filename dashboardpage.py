class DashboardPage:
    """Encapsulates various features of D-Wave's landing page, which is a dashboard"""
    def __init__(self, driver):
        """
        :param driver: The webdriver used to drive the browser
        """
        self.driver = driver

    @property
    def account_name(self):
        """The string that is the name of the account's user"""
        path_to_account_name = "//div[contains(@class, 'avatar')]/following::div"
        account_name_elem = self.driver.find_element_by_xpath(path_to_account_name)
        return account_name_elem.text

    @property
    def account_type(self):
        """The string that is the account's type"""
        path_to_account_type = "//div[contains(@class, 'account-type-upgrade-btn-container')]/div[1]"
        account_type_elem = self.driver.find_element_by_xpath(path_to_account_type)
        return account_type_elem.text

    @property
    def renewal_date(self):
        """
        A string representation of the date the account needs to be renewed on,
        or the date the trial expires (for trial accounts)
        """
        path_to_renewal_date = "//div[contains(@class, 'renewal-expiry-heading')]/following::div"
        renewal_date_elem = self.driver.find_element_by_xpath(path_to_renewal_date)
        return renewal_date_elem.text

    @property
    def api_token(self):
        """
        The string that is the account's api token
        Is simply dots if the "Show API Key" button hasn't been pressed
        """
        path_to_api_token = "//input[contains(@class, 'component--ApiTokenField')]"
        api_token_elem = self.driver.find_element_by_xpath(path_to_api_token)
        return api_token_elem.get_attribute("value")

    def toggle_api_token_visibility(self):
        """Presses the API token button, which toggles the token between dots and the true value"""
        path_to_api_token_visibility = "//button[contains(@class, 'component--ApiTokenField-btn')]"
        api_token_visibility_btn = self.driver.find_element_by_xpath(path_to_api_token_visibility)
        api_token_visibility_btn.click()
