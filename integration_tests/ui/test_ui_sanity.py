def test_logout(ui):
    driver = ui.driver
    driver.find_element_by_css_selector(".user-dropdown").click()
    driver.find_element_by_css_selector(".logout-button").click()
    assert driver.find_element_by_css_selector('.login-form')


def test_recorded_sessions_visible(ui_session):
    assert ui_session is not None
