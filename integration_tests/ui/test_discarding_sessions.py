import time

from selenium.webdriver.common.alert import Alert

def test_session_has_discard_button(ui, ui_session):
    ui_session.click()
    ui.driver.find_element_by_css_selector('.discard-btn')

def test_session_no_button_for_non_admin(ui, ui_non_admin, ui_session): # pylint: disable=unused-argument
    ui_session.click()
    ui.assert_no_element('.discard-btn')

def test_session_discard_undo(ui, ui_session): # pylint: disable=unused-argument
    ui_session.click()
    button = ui.driver.find_element_by_css_selector('.discard-btn')
    button.click()
    alert = Alert(ui.driver)
    alert.send_keys("30")
    alert.accept()
    undo_button = ui.driver.find_element_by_css_selector('button.undo-discard-btn')
    ui.assert_no_element('.discard-btn')
    undo_button.click()
    button = ui.driver.find_element_by_css_selector('.discard-btn')
