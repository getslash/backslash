import pytest
import time

from munch import Munch
from ..utils import run_suite


@pytest.fixture(scope="session")
def recorded_session(integration_url):
    return _get_recorded_session(integration_url)


@pytest.fixture(scope="session")
def recorded_interrupted_session(integration_url):
    return _get_recorded_session(integration_url, name="interrupted", interrupt=True)


def _get_recorded_session(integration_url, **kwargs):
    session_id = run_suite(integration_url, **kwargs)
    return Munch(id=session_id)


@pytest.fixture
def ui_admin_login(request):
    return request.config.getoption("--admin-username")


@pytest.fixture
def ui_admin_password(request):
    return request.config.getoption("--admin-password")


@pytest.fixture
def ui_session(recorded_session, ui):  # pylint: disable=unused-argument
    assert recorded_session.id is not None
    ui.driver.refresh()
    return ui.find_session_link(recorded_session)


@pytest.fixture
def ui_interrupted_session(recorded_interrupted_session, ui):
    return ui.find_session_link(recorded_interrupted_session)


@pytest.fixture
def ui(
    has_selenium, selenium, integration_url, ui_admin_login, ui_admin_password
):  # pylint: disable=unused-argument
    return _UI(selenium, integration_url, ui_admin_login, ui_admin_password)


@pytest.fixture
def ui_non_admin(ui, request):
    ui.logout()
    ui.login("guest", "guest")

    @request.addfinalizer
    def cleanup():
        ui.logout()
        ui.login()


@pytest.fixture
def has_selenium(request):
    if request.config.getoption("driver") is None:
        pytest.skip("Selenium required")
    return True


class _UI:
    def __init__(self, selenium_driver, integration_url, admin_login, admin_password):
        self.driver = selenium_driver
        self.driver.implicitly_wait(10)
        self.url = integration_url
        self.driver.get(self.url)
        self.admin_email = admin_login
        self.admin_password = admin_password
        self.login()

    def login(self, username=None, password=None):
        if username is None:
            username = self.admin_email
        if password is None:
            password = self.admin_password

        for retry in range(3):
            if retry:
                self.driver.refresh()
                time.sleep(1)
            if self.is_logged_in():
                assert retry, "Attempt to log in when we are already logged in"
                break
            login_input = self.driver.find_element_by_id("username")
            login_input.send_keys(username)
            password_input = self.driver.find_element_by_id("password")
            password_input.send_keys(password)
            self.driver.find_element_by_class_name("btn-success").click()
            if self.is_logged_in():
                break

        else:
            assert False, "Could not log in!"

    def is_logged_in(self):
        logout_buttons = self.driver.find_elements_by_css_selector("button.logout")
        return bool(logout_buttons)

    def logout(self):
        logout_buttons = self.driver.find_elements_by_css_selector("button.logout")
        if logout_buttons:
            logout_buttons[0].click()
        self.driver.find_element_by_id("username")

    def assert_no_element(self, css_selector):
        assert self.driver.find_elements_by_css_selector(css_selector) == []

    def find_session_link(self, session):
        self.driver.refresh()
        return self.driver.find_element_by_xpath(
            f"//div[@data-session-id='{session.id}']"
        )
