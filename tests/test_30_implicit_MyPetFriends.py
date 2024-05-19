import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    """ Установка неявных ожиданий для всего теста"""
    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    # Максимизируем окно браузера
    driver.maximize_window()
    yield driver

    driver.quit()


"""Неявное ожидание"""


def test_my_pets_implicit(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('zxcv@zx.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Кликаем на кнопку "Мои питомцы"
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # Проверяем содержимое раздела "Мои питомцы"
    assert driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').text == 'Мои питомцы'

    # Ищем все карточки питомцев на странице "Мои питомцы".
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    # Находим внутри каждой карточки фото, имя, вид и возраст
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


