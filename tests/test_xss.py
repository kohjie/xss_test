import pytest
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture()
def test_setup():
    # Declaring Global Variables
    global driver, username, wrong_password, correct_password, url
    # Setting Global Variable Values
    comment = "testpatientaccount"
    url = "http://localhost:5000"
    # Initializing ChromeDriver
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.binary_location = '/usr/bin/google-chrome'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=option)
    # Browse URL
    driver.get(url)
    yield


def test_failed_login(test_setup):
    sleep(2)
    # Enter Test Username & Password
    enter_username(username)
    enter_password(wrong_password)
    sleep(2)
    # Click Login Button
    driver.find_element(By.ID, "user_login").click()
    sleep(2)
    # Obtain Alert Element
    element = driver.find_element(By.XPATH, "//div[contains(@class,'alert alert-danger')]").text
    # Assert if alert is displayed
    assert element == 'Incorrect username/password.'
    print("Incorrect username /password caught")
    # Close ChromeDriver
    driver.close()


def test_success_login(test_setup):
    sleep(2)
    # Enter Test Username & Password
    enter_username(username)
    enter_password(correct_password)
    sleep(2)
    # Click Login Button
    driver.find_element(By.ID, "user_login").click()
    sleep(2)
    # Try Obtain Dashboard H1 Header
    try:
        element = driver.find_element(By.XPATH, "//h1[contains(text(),'Appointment')]").text
        # Assert if Appointment is displayed
        assert element == 'Appointment'
        print("Success")
    except NoSuchElementException:
        # If Incorrect Username / Password
        element = driver.find_element(By.XPATH, "//div[contains(@class,'alert alert-danger')]").text
        assert element == 'Incorrect username/password.'
        print("Incorrect username /password caught")
    driver.close()


def enter_username(username):
    driver.find_element(By.ID, "login_username").send_keys(username)


def enter_password(password):
    driver.find_element(By.ID, "login_password").send_keys(password)