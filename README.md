# get-qiwi-token
Скрипт для получения qiwi токена.

# Установка
Установите Firefox и python.

Далее [скачайте](https://github.com/mozilla/geckodriver/releases) и распакуйте архив в папке с файлами проекта.

Установите зависимости:
```
pip install -r requirements.txt
```
В файле gettoken.py замените options.binary_location на путь к firefox в вашей системе.

# Использование
В файл gadzhi07.txt запишите логины и пароли ваших аккаунтов.

Далее запустите файл gettoken.py:
```
python gettoken.py
```

У вас откроется браузер, нажмите "Войти".

Далее введите полученный СМС код в консоль и в консоль выведется токен.
