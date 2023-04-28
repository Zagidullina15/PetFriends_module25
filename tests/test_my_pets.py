from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def test_show_all_pets(my_pets):
    """Проверка, что на странице со списком моих питомцев присутствуют все питомцы"""
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    # Сохраняем в переменную statistic элементы статистики
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Сохраняем в переменную pets элементы карточек питомцев
    data_pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Получаем количество карточек питомцев
    num_cards = len(data_pets)

    # Проверяем, что количество питомцев из статистики совпадает с количеством карточек питомцев
    assert number == num_cards


def test_half_pets_have_photo(my_pets):
    """Проверка, что у половины моих питомцев есть фото"""
    pytest.driver.implicitly_wait(10)
    # Сохраняем в переменную statistic элементы статистики
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")
    # Сохраняем в переменную images атрибут img
    images = pytest.driver.find_elements_by_css_selector('.table.table-hover img')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Находим половину от количества питомцев
    half = number / 2

    # Находим количество питомцев с фотографией
    number_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_photos += 1

    # Проверяем, что количество питомцев с фотографией больше или равно половине количества питомцев
    assert number_photos >= half


def test_pets_with_all_info(my_pets):
    """Проверка, что у всех питомцев есть имя, возраст и порода"""
    pytest.driver.implicitly_wait(10)
    # Сохраняем в переменную data_pets элементы с данными о питомцах
    data_pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    for i in range(len(data_pets)):
        all_info = data_pets[i].text.replace('\n', '').replace('×', '').split(' ')
        assert len(all_info) == 3
        print(all_info)


def test_pets_all_info(my_pets):
    """Проверка, что у всех питомцев есть имя, возраст и порода"""
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_pets_have_different_name(my_pets):
    """Проверка, что у всех питомцев разные имена"""
    pytest.driver.implicitly_wait(10)
    # Сохраняем в переменную data_pets элементы с данными о питомцах
    data_pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    name_pets = []
    for i in range(len(data_pets)):
        name_pets.append(data_pets[i].text.replace('\n', '').split(' ')[0])
    set_name_pets = set(name_pets)
    # Если количество элементов равны, значит карточки с одинаковыми именами отсутствуют
    assert len(name_pets) == len(set_name_pets)


def test_no_duplicate_pets(my_pets):
    """Проверка, что на странице со списком моих питомцев нет повторяющихся питомцев"""
    pytest.driver.implicitly_wait(10)
    # Сохраняем в переменную data_pets элементы с данными о питомцах
    data_pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')

    list_data = []
    for i in range(len(data_pets)):
        list_data.append(data_pets[i].text.replace('\n', '').replace('×', '').split(' '))

    # Склеиваем имя, возраст и породу из списка list_data; получившиеся склеенные слова добавляем в строку
    # и между ними вставляем пробел
    row = ''
    for i in list_data:
        row += ''.join(i)
        row += ' '

    # Получаем список из строки row
    list_row = row.split()

    # Превращаем список в множество
    set_list_row = set(list_row)

    # Если количество элементов равны, значит карточки с одинаковыми данными отсутствуют
    assert len(set_list_row) == len(list_row)