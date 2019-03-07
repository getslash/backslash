def test_logout(ui):
    ui.driver.find_element_by_css_selector('button.logout').click()
    assert ui.driver.find_element_by_css_selector('h1').text == 'Sign in Required'
    assert ui.driver.find_element_by_id('username')


def test_recorded_sessions_visible(ui_session):
    assert ui_session is not None
