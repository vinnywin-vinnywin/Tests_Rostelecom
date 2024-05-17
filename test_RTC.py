
import time
from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeServise
from webdriver_manager.chrome import ChromeDriverManager
import data_RTC
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5) #вставить ожидание
    # Переходим на страницу авторизации https://lk.rt.ru/  https://b2c.passport.rt.ru/account_b2c/page
    driver.get('https://lk.rt.ru/')
    driver.maximize_window()
    yield driver

    driver.quit()

#проверка на слоган и инф-цию
def test_authorization_defautl_info(driver):
    assert driver.find_element(By.XPATH, '//*[@id="page-left"]/div/div[1]/svg') != '' #лого
    assert driver.find_element(By.TAG_NAME, 'h2').text == "Личный кабинет" #местонахождение - личный кабинет
    assert driver.find_element(By.TAG_NAME, 'p').text == "Персональный помощник в цифровом мире Ростелекома" #слоган
    print('\n на странице сразу')
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    assert driver.find_element(By.XPATH, '//*[@id="page-left"]/div/div[1]/svg') != ''  # лого
    assert driver.find_element(By.TAG_NAME, 'h2').text == "Личный кабинет"  # местонахождение - личный кабинет
    assert driver.find_element(By.TAG_NAME, 'p').text == "Персональный помощник в цифровом мире Ростелекома"  # слоган
    print('\n на странице после войти с паролем')

#по умолчанию выбрана авторизация по телефону
def test_authorization_defautl_phone(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div[1]/div/form/div[1]/div[2]/div/span[2]').text == 'Мобильный телефон'
    #print('\n текст внутри поля - Мобильный телефон')

#вход по номеру и паролю - позитивный тест
def test_authorization_phone_valid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_phone_valid) # Вводим номер телефона
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.current_url == 'https://start.rt.ru/?tab=main'

#вход по номеру и паролю - негативный тест
def test_authorization_phone_INvalid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    #недостаточно символов
    driver.find_element(By.ID, 'username').send_keys('012345678') # Вводим номер телефона
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main'     # Проверяем, что мы НЕ оказались на главной странице пользователя
    #текст вместо цифр
    driver.find_element(By.ID, 'username').send_keys('textтекст') # Вводим номер телефона
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main'     # Проверяем, что мы НЕ оказались на главной странице пользователя

#вход по почте и паролю - позитивный тест
def test_authorization_mail_valid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-mail').click()  #нажимаем на "почта"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_mail_valid) # Вводим email
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.current_url == 'https://start.rt.ru/?tab=main'

#вход по почте и паролю - негативный тест
def test_authorization_mail_INvalid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-mail').click()  #нажимаем на "почта"
    #корткое наименование
    driver.find_element(By.ID, 'username').send_keys('mail') # Вводим email
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя
    #спецсимволы
    driver.find_element(By.ID, 'username').send_keys('m@ail@mail.ru') # Вводим email
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя
    #несуществующий адрес
    driver.find_element(By.ID, 'username').send_keys('m000ail@mail.ru') # Вводим email
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя

#вход по логину и паролю - позитивный тест
def test_authorization_login_valid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-login').click()  #нажимаем на "логин"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_login_valid) # Вводим логин
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.current_url == 'https://start.rt.ru/?tab=main'

#вход по логину и паролю - негативный тест
def test_authorization_login_valid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-login').click()  #нажимаем на "логин"
    #короткий
    driver.find_element(By.ID, 'username').send_keys('lk_772730') # Вводим логин
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя
    #спецсимволы, он же несуществующий
    driver.find_element(By.ID, 'username').send_keys('lk_772_730') # Вводим логин
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя

#вход по счету и паролю - позитивный тест
def test_authorization_licevoi_valid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-ls').click()  #нажимаем на "лицевой счет"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_licevoi_valid) # Вводим лицевой счет
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.current_url == 'https://start.rt.ru/?tab=main'

#вход по счету и паролю - негативный тест
def test_authorization_licevoi_valid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 't-btn-tab-ls').click()  #нажимаем на "лицевой счет"
    #короткий
    driver.find_element(By.ID, 'username').send_keys('27801436299') # Вводим лицевой счет
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя
    #спецсимволы, он же несуществующий
    driver.find_element(By.ID, 'username').send_keys('278@0143/299') # Вводим лицевой счет
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid) # Вводим пароль
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    wdw(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"root"]/div/div/div[2]/div/div/div[2]/div[3]')))
    assert driver.current_url == 'https://start.rt.ru/?tab=main' # Проверяем, что мы оказались на главной странице пользователя

#невозможность входа по неверному паролю - негативный тест
def test_authorization_psw_INvalid(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    #проверка с корректным телефоном
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_phone_valid) # Вводим номер телефона
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_INvalid) # Вводим не корректный пароль(!)
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    # #проверка что есть замечание о неверной паре
    #wdw(driver, 30).until(EC.presence_of_element_located((By.ID, 'form-error-message')))
    assert driver.current_url != 'https://start.rt.ru/?tab=main'
    print('\n не зашли по телефону')
    #проверка с корректной почтой
    driver.find_element(By.ID, 't-btn-tab-mail').click()  # нажимаем на "почта"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_mail_valid)  # Вводим email
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_INvalid)  # Вводим не корректный пароль(!)
    driver.find_element(By.ID, 'kc-login').click() # Нажимаем на кнопку входа в аккаунт
    assert driver.current_url != 'https://start.rt.ru/?tab=main'
    print('\n не зашли по эл.адрес')
    #проверка с корректным логином
    driver.find_element(By.ID, 't-btn-tab-login').click()  # нажимаем на "логин"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_login_valid)  # Вводим логин
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_INvalid)  # Вводим не корректный пароль(!)
    driver.find_element(By.ID, 'kc-login').click()  # Нажимаем на кнопку входа в аккаунт
    assert driver.current_url != 'https://start.rt.ru/?tab=main'
    print('\n не зашли по логину')
    #проверка с корректным лиц.счетом
    driver.find_element(By.ID, 't-btn-tab-ls').click()  # нажимаем на "лицевой счет"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_licevoi_valid)  # Вводим лицевой счет
    driver.find_element(By.ID, 'password').send_keys(data_RTC.data_psw_valid)  # Вводим не корректный пароль(!)
    driver.find_element(By.ID, 'kc-login').click()  # Нажимаем на кнопку входа в аккаунт
    assert driver.current_url != 'https://start.rt.ru/?tab=main'
    print('\n не зашли по лиц.счету')

#проверка необходимых элементов в блоках
def test_authorization_visible_form(driver):
    # Проверка разделения формы на два блока"
    left_block = driver.find_element(By.CSS_SELECTOR, "#page-left")
    right_block = driver.find_element(By.CSS_SELECTOR, "#page-right")
    assert left_block.is_displayed() and right_block.is_displayed()
    # Проверка наличия необходимых элементов в левом блоке
    #Меню выбора типа аутентификации
    wdw(left_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#page-right > div > div.card-container__wrapper > div > form > div.tabs-input-container > div.rt-tabs.rt-tabs--orange.rt-tabs--small.tabs-input-container__tabs"))
    wdw(left_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#t-btn-tab-phone"))
    wdw(left_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#t-btn-tab-mail"))
    wdw(left_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#t-btn-tab-login"))
    wdw(left_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#t-btn-tab-ls"))
    wdw(left_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, '#password'))
    # Проверка наличия необходимых элементов в правом блоке
    #Слоган и информация для клиента
    wdw(right_block, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#page-left > div > div.what-is"))
    assert 'Личный кабинет' in driver.find_element(By.CSS_SELECTOR, "#page-left > div > div.what-is").text

#Проверка переключения таба
def test_authorization_tab_step(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    # Проверяем, что таб "Телефон" выбран
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_phone_valid) # Вводим номер телефона
    driver.find_element(By.CSS_SELECTOR, '#password').click() #перевод курсора на поле ввода пароля
    time.sleep(5)
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, 't-btn-tab-phone').get_attribute('class')
    # Проверяем, что таб "Почта" выбран
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_mail_valid) # Вводим email
    driver.find_element(By.CSS_SELECTOR, '#password').click() #перевод курсора на поле ввода пароля
    time.sleep(5)
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, '#t-btn-tab-mail').get_attribute('class')
    # Проверяем, что таб "Логин" выбран
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_login_valid)  # Вводим логин
    driver.find_element(By.CSS_SELECTOR, '#password').click()  # перевод курсора на поле ввода пароля
    time.sleep(5)
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, '#t-btn-tab-login').get_attribute('class')
    # Проверяем, что таб "Лицевой счет" выбран
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    driver.find_element(By.ID, 'username').send_keys(data_RTC.data_licevoi_valid) # Вводим лицевой счет
    driver.find_element(By.CSS_SELECTOR, '#password').click()  # перевод курсора на поле ввода пароля
    time.sleep(5)
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, '#t-btn-tab-ls').get_attribute('class')

#наличие кнопки "забыл пароль"
def test_forgot_password_link_displayed(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    # Проверка что отображается элемент "Забыл пароль"
    assert driver.find_element(By.ID, "forgot_password").text == 'Забыл пароль'

#поле ввода почты или телефона при авторизации по коду - ввод телефона
def tast_authorization_tmp_input_phone(driver):
    str = 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('8900')  # Вводим некорректный телефон
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('8900@//1234')  # Вводим некорректный телефон
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('август')  # Вводим некорректный телефон
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('factorial')  # Вводим некорректный телефон
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('8ю9q1234567')  # Вводим некорректный телефон
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #позитивная проверка
    driver.find_element(By.ID, 'address').send_keys(data_RTC.data_phone_valid) # Вводим phone
    driver.find_element(By.ID, 'card-title').click() #нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').is_displayed == 'none'

#поле ввода почты или телефона при авторизации по коду - ввод почты
def tast_authorization_tmp_input_mail(driver):
    str = 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('mail')  # Вводим некорректную почту
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('@//')  # Вводим некорректную почту
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('ma@il@mail.ru')  # Вводим некорректную почту
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #негативная проверка
    driver.find_element(By.ID, 'address').send_keys('mailmail.ru')  # Вводим некорректную почту
    driver.find_element(By.ID, 'card-title').click()  # нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').text == str
    #позитивная проверка
    driver.find_element(By.ID, 'address').send_keys(data_RTC.data_phone_valid) # Вводим почту
    driver.find_element(By.ID, 'card-title').click() #нажимаем на сторонее поле
    assert driver.find_element(By.ID, 'address-meta').is_displayed == 'none'

# проверка переключения элементов меню выбора типа ввода данных формы Восстановления пароля
def test_registration_tab_step(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 'forgot_password').click() #клик по Забыл пароль forgot_password
    #проверка, что мы на странице Восстановления пароля
    #assert driver.current_url == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=lk_b2c&tab_id=gG8_8isfI8c'
    #проверка переключения элементов меню выбора типа ввода данных
    driver.find_element(By.ID, 't-btn-tab-phone').click()  #нажимаем на "телефон"
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, 't-btn-tab-phone').get_attribute('class')
    driver.find_element(By.ID, 't-btn-tab-mail').click()  # нажимаем на "почту"
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, 't-btn-tab-mail').get_attribute('class')
    driver.find_element(By.ID, 't-btn-tab-login').click()  # нажимаем на "логин"
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, 't-btn-tab-login').get_attribute('class')
    driver.find_element(By.ID, 't-btn-tab-ls').click()  # нажимаем на "лицевой счет"
    assert 'rt-tab--active' in driver.find_element(By.CSS_SELECTOR, 't-btn-tab-ls').get_attribute('class')

#проверка наличия обязательных компонентов формы Восстановления пароля
def test_registration_form_visual(driver):
    wdw(driver, 30).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 'forgot_password').click() #клик по Забыл пароль forgot_password
    #проверка, что мы на странице Восстановления пароля
    #assert driver.current_url == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=lk_b2c&tab_id=gG8_8isfI8c'
    #проверка наличия меню выбора с необходимыми компонентами
    assert ('t-btn-tab-phone' and 't-btn-tab-mail' and 't-btn-tab-login' and 't-btn-tab-ls') \
           in driver.find_element(By.CSS_SELECTOR, 'rt-tab').get_attribute('class')

#Проверка создания пароля при восстановлении пароля через телефон
def test_registration_reset_psw_for_valid_phone(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 'forgot_password').click() #клик по кнопке Забыли пароль
    driver.find_element(By.CSS_SELECTOR, 'rt-input__mask-start').send_keys(data_RTC.data_phone_valid)
    time(45) #за это время необходимо вручную ввести капчу и нажать "Продолжить"
    driver.find_element(By.XPATH, '//*[@id="sms-reset-type"]/span/span[1]').click() #радиобаттон в восстановление по телефону
    #проверка, что указан вход по почте
    assert driver.find_element(By.XPATH, '//*[@id="email-reset-type"]/span/span[3]/span[1]').text == 'По номеру телефона'
    driver.find_element(By.ID, 'reset-form-submit').click() #клик по кнопке Продолжить
    time(45) #за это время необходимо вручную ввести код подтверждения из смс
#проверка ввода короткого пароля
    driver.find_element(By.ID, 'password-new').send_keys('1234567') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Длина пароля должна быть не менее 8 символов'
#проверка ввода пароля в нижнем регистре
    driver.find_element(By.ID, 'password-new').send_keys('123qwerty') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Пароль должен содержать хотя бы одну заглавную букву'
#проверка ввода пароля с кирилицей
    driver.find_element(By.ID, 'password-new').send_keys('123абв123') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Пароль должен содержать только латинские буквы'
#проверка ввода длинного пароля
    driver.find_element(By.ID, 'password-new').send_keys('123456789012345678901') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Длина пароля должна быть не более 20 символов'
#проверка ввода разных паролей ввода и его подтверждения
    driver.find_element(By.ID, 'password-new').send_keys('123_Qwert_//@') #вводим пароль
    driver.find_element(By.ID, 'password-confirm').send_keys('123_Qwert') #вводим отличающийся пароль подтверждение
    driver.find_element(By.ID, 't-btn-reset-pass').click() #попытка сохранить новый пароль
    assert driver.find_element(By.ID, 'password-confirm-meta').text == 'Пароли не совпадают'
    assert driver.current_url != 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate?execution=fc343b3b-9ff7-4786-bb30-e60caa7821cd&client_id=lk_b2c&tab_id=pGuwmPQMGrM'
#проверка корректного входа
    driver.find_element(By.ID, 'password-new').send_keys('123_Qwert') #вводим пароль
    driver.find_element(By.ID, 'password-confirm').send_keys('123_Qwert') #вводим пароль подтверждение
    assert driver.current_url == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate?execution=fc343b3b-9ff7-4786-bb30-e60caa7821cd&client_id=lk_b2c&tab_id=pGuwmPQMGrM'

#Проверка создания пароля при восстановлении пароля через почту
def test_registration_reset_psw_for_valid_mail(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    driver.find_element(By.ID, 'forgot_password').click() #клик по кнопке Забыли пароль
    driver.find_element(By.CSS_SELECTOR, 'rt-input__mask-start').send_keys(data_RTC.data_mail_valid)
    time(45) #за это время необходимо вручную ввести капчу и нажать "Продолжить"
    driver.find_element(By.XPATH, '//*[@id="sms-reset-type"]/span/span[2]').click() #радиобаттон в восстановление по телефону
    #проверка, что указан вход по почте
    assert driver.find_element(By.XPATH, '//*[@id="email-reset-type"]/span/span[3]/span[1]').text == 'По e-mail'
    driver.find_element(By.ID, 'reset-form-submit').click() #клик по кнопке Продолжить
    time(45) #за это время необходимо вручную ввести код подтверждения из письма
#проверка ввода короткого пароля
    driver.find_element(By.ID, 'password-new').send_keys('1234567') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Длина пароля должна быть не менее 8 символов'
#проверка ввода пароля в нижнем регистре
    driver.find_element(By.ID, 'password-new').send_keys('123qwerty') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Пароль должен содержать хотя бы одну заглавную букву'
#проверка ввода пароля с кирилицей
    driver.find_element(By.ID, 'password-new').send_keys('123абв123') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Пароль должен содержать только латинские буквы'
#проверка ввода длинного пароля
    driver.find_element(By.ID, 'password-new').send_keys('123456789012345678901') #вводим некоррекктный пароль
    driver.find_element(By.ID, 'password-confirm').click() #перевод курсора
    assert driver.find_element(By.ID, 'password-new-meta').text == 'Длина пароля должна быть не более 20 символов'
#проверка ввода разных паролей ввода и его подтверждения
    driver.find_element(By.ID, 'password-new').send_keys('123_Qwert_//@') #вводим пароль
    driver.find_element(By.ID, 'password-confirm').send_keys('123_Qwert') #вводим отличающийся пароль подтверждение
    driver.find_element(By.ID, 't-btn-reset-pass').click() #попытка сохранить новый пароль
    assert driver.find_element(By.ID, 'password-confirm-meta').text == 'Пароли не совпадают'
    assert driver.current_url != 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate?execution=fc343b3b-9ff7-4786-bb30-e60caa7821cd&client_id=lk_b2c&tab_id=pGuwmPQMGrM'
#проверка корректного входа
    driver.find_element(By.ID, 'password-new').send_keys('123_Qwert') #вводим пароль
    driver.find_element(By.ID, 'password-confirm').send_keys('123_Qwert') #вводим пароль подтверждение
    assert driver.current_url == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate?execution=fc343b3b-9ff7-4786-bb30-e60caa7821cd&client_id=lk_b2c&tab_id=pGuwmPQMGrM'

