
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

'''
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
''' #проверка на слоган и инф-цию

def test_authorization_defautl_phone(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'standard_auth_btn')))
    driver.find_element(By.ID, 'standard_auth_btn').click() #клик по кнопке войти с паролем
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div[1]/div/form/div[1]/div[2]/div/span[2]').text == 'Мобильный телефон'
    #print('\n текст внутри поля - Мобильный телефон')

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

'''
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
''' #psw_INvalid

