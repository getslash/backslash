from yarl import URL

def test_session_not_found(ui):
    ui.driver.get(str(URL(ui.driver.current_url).with_fragment('/sessions/blap')))
    assert ui.driver.find_element_by_css_selector(".error-details h1").text.lower() == 'not found'
