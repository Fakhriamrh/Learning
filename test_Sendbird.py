import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# Fixture for WebDriver initialization
@pytest.fixture(scope="module")
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

# Function for logging in and initial user settings 1
def login_and_setup1(driver, app_id1, user_id1, nickname1):
    driver.get("https://sendbird-uikit-react.netlify.app/url-builder")
    time.sleep(3)  # Wait for the page to load

    driver.find_element(By.NAME, "appId").send_keys(app_id1)
    driver.find_element(By.NAME, "userId").send_keys(user_id1)
    driver.find_element(By.NAME, "nickname").send_keys(nickname1)
    copy_button1 = driver.find_element(By.CSS_SELECTOR, "button.sticky-bottom-button[form='builder']")
    copy_button1
    time.sleep(3)  # Wait for the page to load


# Function to send text messages
def send_plain_text(driver, text):
    Send_text = driver.find_element(By.ID, "sendbird-message-input-text-field")
    Send_text.send_keys(text)
    Send_text.send_keys(Keys.ENTER)
    time.sleep(3)  # Wait for the page to load

# Function to send images
def send_picture(driver, file_path):
    file_path = os.path.abspath(file_path)
    Send_Picture = driver.find_element(By.CLASS_NAME, "sendbird-message-input--attach-input")
    Send_Picture.send_keys(file_path)
    time.sleep(3)  # Wait for the page to load

# Function to send text files
def send_text_file(driver, file_path):
    file_path = os.path.abspath(file_path)
    Send_File = driver.find_element(By.CLASS_NAME, "sendbird-message-input--attach-input")
    Send_File.send_keys(file_path)
    time.sleep(3)  # Wait for the page to load

# Test cases using Pytest
def test_create_user1(setup_driver):
    # Setting User 1
    app_id1 = "37C8DB25-8B44-435F-A528-5BA9B9965FD0"
    user_id1 = "1Testing"
    nickname1 = "User1"
    login_and_setup1(setup_driver, app_id1, user_id1, nickname1)
    # Change tab for User 1
    setup_driver.execute_script("window.open('');")
    Tab_For_User1 = setup_driver.window_handles[1]
    setup_driver.switch_to.window(Tab_For_User1)
    setup_driver.get("https://sendbird-uikit-react.netlify.app/group_channel?appId=37C8DB25-8B44-435F-A528-5BA9B9965FD0&userId=1Testing&nickname=User1")

    
def test_create_user2(setup_driver):
    # Setting User 2
    setup_driver.switch_to.window(setup_driver.window_handles[0])
    time.sleep(5)
    app_id2 = "37C8DB25-8B44-435F-A528-5BA9B9965FD0"
    user_id2 = "2Testing"
    nickname2 = "User2"
    Textbox_name = setup_driver.find_element(By.NAME, "appId")
    Textbox_name.clear()
    Textbox_name.send_keys(app_id2)
    Textbox_User = setup_driver.find_element(By.NAME, "userId")
    Textbox_User.clear()
    Textbox_User.send_keys(user_id2)
    Textbox_nickname = setup_driver.find_element(By.NAME, "nickname")
    Textbox_nickname.clear()
    Textbox_nickname.send_keys(nickname2)
    setup_driver.find_element(By.CSS_SELECTOR, "button.sticky-bottom-button[form='builder']").click()
    # Change tab for User 2
    setup_driver.execute_script("window.open('');")
    Tab_For_User2 = setup_driver.window_handles[2]
    setup_driver.switch_to.window(Tab_For_User2)
    setup_driver.get("https://sendbird-uikit-react.netlify.app/group_channel?appId=37C8DB25-8B44-435F-A528-5BA9B9965FD0&userId=2Testing&nickname=User2")
    time.sleep(3)
    setup_driver.find_element(By.XPATH, "//div[contains(@class,'sendbird-icon sendbird-icon-create sendbird-icon-color--primary')]//*[name()='svg']").click()
    time.sleep(3)
    setup_driver.find_element(By.CLASS_NAME, "sendbird-add-channel__rectangle").click()
    time.sleep(3)
    setup_driver.find_element(By.XPATH, "//label[contains(@for,'1Testing')]//span[contains(@class,'sendbird-checkbox--checkmark')]").click()
    time.sleep(3)     
    setup_driver.find_element(By.XPATH, "//button[contains(@class,'sendbird-button--primary sendbird-button--big')]").click()
    time.sleep(3)   

def test_sending_message_and_attachments_by_user2(setup_driver): 
    # Test sending messages and attachments by User 2
    send_plain_text(setup_driver, "Send Plain Text")

    file_path = '/tests/images/SendbirdTestPict.png'
    send_picture(setup_driver, file_path)
    time.sleep(3)

    file_path = '/Users/test_files/SendbirdTest.txt'
    send_text_file(setup_driver, file_path)
    time.sleep(3)
    
def test_switch_tab_to_user1(setup_driver): 
    # Switch tab to user 1 for validation
    Tab_For_User1 = setup_driver.window_handles[1]
    setup_driver.switch_to.window(Tab_For_User1)
    setup_driver.find_element(By.CLASS_NAME, 'sendbird-channel-preview[tabindex="0"]').click()
    
def test_validate_message_and_attachments_by_user1(setup_driver):
    # Validate text messages
    message_element = setup_driver.find_element(By.CSS_SELECTOR, 'div.sendbird-message-content__middle__message-item-body.sendbird-text-message-item-body.incoming')
    message_text = message_element.text
    expected_message = 'Send Plain Text'
    assert message_text == expected_message, f"Expected message '{expected_message}' but found '{message_text}'"

    # Image validation
    image_element = setup_driver.find_element(By.XPATH, "//div[@class='sendbird-image-renderer__image']").click()
    img_element = setup_driver.find_element(By.XPATH, "//img[@alt='SendbirdTestPict.png']")
    alt_attribute = img_element.get_attribute('alt')
    expected_alt_text = 'SendbirdTestPict.png'
    assert alt_attribute == expected_alt_text, f"Expected alt text '{expected_alt_text}' but found '{alt_attribute}'"

    # Validate text files
    try:
        span_element = setup_driver.find_element(By.XPATH, "//span[@class='sendbird-file-message-item-body__file-name__text sendbird-label sendbird-label--body-1 sendbird-label--color-onbackground-1']")
        span_text = span_element.text
        expected_text = 'SendbirdTest.txt'
        assert span_text == expected_text, f"Expected text '{expected_text}' but found '{span_text}'"
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

