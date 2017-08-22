import pytest

from munch import Munch
from ..utils import run_suite


@pytest.fixture(scope='session')
def recorded_session(integration_url):
    session_id = run_suite(integration_url)
    return Munch(id=session_id)

@pytest.fixture
def ui_session(recorded_session, ui): # pylint: disable=unused-argument
    return ui.driver.find_element_by_css_selector(f"a.item.session[href*='/#/sessions/{recorded_session.id}']")

@pytest.fixture
def ui(has_selenium, selenium, integration_url): # pylint: disable=unused-argument
    return _UI(selenium, integration_url)

@pytest.fixture
def ui_non_admin(ui, request):
    ui.logout()
    ui.login('guest', 'guest')

    @request.addfinalizer
    def cleanup():
        ui.logout()
        ui.login()

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
        self.admin_email = 'admin@localhost'
        self.admin_password = '12345678'
        self.login()

    def login(self, username=None, password=None):
        if username is None:
            username = self.admin_email
        if password is None:
            password = self.admin_password
        login_input = self.driver.find_element_by_id('username')
        login_input.send_keys(username)
        password_input = self.driver.find_element_by_id('password')
        password_input.send_keys(password)
        self.driver.find_element_by_class_name('btn-success').click()

    def logout(self):
        self.driver.find_element_by_css_selector("button.logout").click()

    def assert_no_element(self, css_selector):
        assert self.driver.find_elements_by_css_selector(css_selector) == []
