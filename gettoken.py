from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from requests import Session
import urllib.parse

options = Options()
options.binary_location = r'/usr/bin/firefox' # path to firefox on ur system
xpaths = {
    'войти': '/html/body/section/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/button',
    'логин': '/html/body/div[2]/div/div/form/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div/input',
    'пароль': '/html/body/div[2]/div/div/form/div/div[1]/div[2]/div[2]/div/div/div[2]/div/input'
}


def get_browser_info(browser, login: str, password: str):
    browser.get("https://qiwi.com/")
    wait = WebDriverWait(browser, 15)
    # нажатие на "Войти"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpaths['войти']))).click()
    # ввод логина и пароля
    wait.until(EC.presence_of_element_located((By.XPATH, xpaths['логин']))).send_keys(login)
    wait.until(EC.presence_of_element_located((By.XPATH, xpaths['пароль']))).send_keys(password)
    # получаем TOKEN HEAD и TOKEN TAIL
    while True:
        sleep(2)
        oauth_token_head = browser.execute_script("return window.localStorage.getItem(arguments[0]);", 'oauth-token-head')
        token_tail_web_qw = browser.get_cookie('token-tail-web-qw')
        if oauth_token_head is not None and token_tail_web_qw is not None:
            oauth_token_head = oauth_token_head.split('"access_token":"')[1].split('"')[0]
            token_tail_web_qw = token_tail_web_qw['value']
            browser.quit()
            return oauth_token_head, token_tail_web_qw


def get_url_encoded_data(dict_data: dict) -> str:
    return "&".join([urllib.parse.quote_plus(dict_1) + "=" + urllib.parse.quote_plus(dict_data[dict_1]) for dict_1 in dict_data])


def request_token_creation(qiwi_session: Session, qiwi_number: str, token_head: str):
    data = {
            'response_type': 'code',
            'client_id': 'qiwi_wallet_api',
            'client_software': 'WEB v4.96.0',
            'username': qiwi_number,
            'scope': 'read_person_profile read_balance read_payment_history accept_payments get_virtual_cards_requisites write_ip_whitelist',
            'token_head': token_head,
            'token_head_client_id': 'web-qw',
            }
    url = f"https://qiwi.com/oauth/authorize?{get_url_encoded_data(data)}"
    temp_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = qiwi_session.request("POST", url, headers=temp_headers)
    # print(resp.text)
    if 'error' in resp.json(): return resp.json()
    return resp.json()['code']


def confirm_token_creation(qiwi_session: Session, code: str, sms_code: str):
    data = {
            'grant_type': 'urn:qiwi:oauth:grant-type:vcode',
            'client_id': 'qiwi_wallet_api',
            'code': code,
            'vcode': sms_code
            }
    url = f"https://qiwi.com/oauth/token?{get_url_encoded_data(data)}"
    temp_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = qiwi_session.request("POST", url, headers=temp_headers)
    # print(resp.text)
    if 'error' in resp.json(): return resp.json()
    return resp.json()['access_token']


for login_password in open("gadzhi07.txt", "r").readlines():
    login, password = login_password.split(" ")
    browser = webdriver.Firefox(options=options)
    oauth_token_head, token_tail_web_qw = get_browser_info(browser, login[1:], password)
    qiwi_session = Session()
    qiwi_session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:110.0) Gecko/20100101 LibreWolf/110.0'
    qiwi_session.cookies['token-tail-web-qw'] = token_tail_web_qw
    code = request_token_creation(qiwi_session, login, oauth_token_head)
    if not isinstance(code, str):
        print(f"Ошибка для номера {login}: {code}")
        continue
    sms_code = input(f"СМС код отправлен на номер {login}, введите его: ")
    token = confirm_token_creation(qiwi_session, code, sms_code)
    if not isinstance(token, str):
        print(f"Ошибка для номера {login}: {token}")
        continue
    print(f"Токен для номера {login}:\n{token}")

