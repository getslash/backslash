import pytest

from munch import Munch

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

from ..utils import run_suite


@pytest.fixture(scope='session')
def recorded_session(recorded_sessions):
    return recorded_sessions.successful


@pytest.fixture(scope='session')
def recorded_sessions(request, integration_url):
    run_suite(integration_url)

    return Munch({'successful': None})


@pytest.fixture
def ui(has_selenium, selenium, integration_url):
    return _UI(selenium, integration_url)

@pytest.fixture
def has_selenium(request):
    if request.config.getoption('driver') is None:
        pytest.skip('Selenium required')
    return True


class _UI:

    def __init__(self, selenium_driver, integration_url):
        self.driver = selenium_driver
        self.driver.implicitly_wait(10)
        self.url = integration_url
        self.driver.get(self.url)
        self.admin_email = 'admin@organization.com'
        self.admin_password = 'password'
        self.login()

    def login(self, did_setup=False):
        try:
            login_input = self.driver.find_element_by_id('username')
        except NoSuchElementException:
            if did_setup:
                raise
            self.setup()
            return self.login(did_setup=True)

        login_input.send_keys(self.admin_email)
        password_input = self.driver.find_element_by_id('password')
        password_input.send_keys(self.admin_password)
        self.driver.find_element_by_class_name('btn-success').click()

    def setup(self):

        admin_email = self.driver.find_element_by_id('admin-email')
        admin_email.send_keys(self.admin_email)
        for i in range(2):
            input = self.driver.find_element_by_id(f'admin-password-{i+1}')
            input.send_keys(self.admin_password)

        btn = self.driver.find_element_by_class_name('btn-lg')
        btn.click()
