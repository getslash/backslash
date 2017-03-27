def test_logout(ui):
    ui.driver.find_element_by_css_selector('#navbar-collapse > form > button').click()
    assert ui.driver.find_element_by_css_selector('h1').text == 'Sign in Required'
    assert ui.driver.find_element_by_id('username')


def test_recorded_sessions_visible(recorded_session):
    pass
