import pytest
from selenium import webdriver
from settings import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('/chromedriver/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.implicitly_wait(10)
    pytest.driver.get(link)
    yield
    pytest.driver.quit()


@pytest.fixture
def my_pets():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    pytest.driver.find_element_by_link_text('Мои питомцы').click()
    assert pytest.driver.find_element_by_tag_name('h2').text == "kate_27"