def test_session_interruption(ui, ui_interrupted_session):
    ui_interrupted_session.click()
    interrupted_test = ui.driver.find_element_by_css_selector('.item.test')
    css_classes = interrupted_test.get_attribute('class')
    assert 'success' not in css_classes
    assert 'fail' not in css_classes
    interrupted_test.click()
    assert 'errors' not in ui.driver.current_url
    [link] = ui.driver.find_elements_by_xpath("//*[contains(text(), 'Interruptions')]")
    link.click()
    error_boxes = ui.driver.find_elements_by_class_name('error-box')
    assert len(error_boxes) == 1
    [err] = error_boxes
    assert 'interruption' in err.get_attribute('class')
