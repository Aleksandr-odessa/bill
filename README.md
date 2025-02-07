# Aсинхронное веб приложение имитурующее работу со счетами.

Приложение создано с использованием:

• База данных - postgresql

• sqlalchemy - для работы с базой данных

• sanic - веб фреймворк

• docker compose


## Приложение можно запустить с помощью docker или локально.

## Настройка и запуск приложенияn
 
  ## Запуск с Docker
  
  ### 1. Клонируйте репозиторий:
  
  `git clone https://github.com/Aleksandr-odessa/bill.git`
  
  ### 2. Запустить контейнер с базой данных и сервисом приложения:
  
  ` docker compose up --build либо sudo docker compose up --build`

 #### Приложение доступно по адресу: 
 
 http://0.0.0.0:8000
 
 #### Документация доступна по адресу:
 
 http://0.0.0.0:8000/docs

### Для тестирования:

1. Запустить контейнеры
   
`docker-compose up --build -d`

2. Зайти внутрь контейнера приложения

`docker exec -it bankapi_app /bin/sh`

3. Перейти в директориб tests

`cd tests`

4.  Запусстить последовательно

`python test_admin.py`

`python test_user.py`

`python test_webhook.py`


  ## Запуск без Docker
  
  ### Запуск сервера:

  `python app.py `
  
#### Приложение доступно по адресу: 
 
 http://0.0.0.0:8000
 
 #### Документация доступна по адресу:
 
 http://0.0.0.0:8000/docs

### Для тестирования запустить команды:

`python test_admin.py`

`python test_user.py`

`python test_webhook.py`

 
Тестовые данные по умолчанию (прописаные в .env):

EMAIL_ADMIN = admin@od.ru

PASSWORD_ADMIN = admin

NAME_ADMIN = administrator

EMAIL_USER = user@od.ru

PASSWORD_USER = user_password

NAME_USER = user1

Пример, для secret_key gfdmhghif38yrf9ew0jkf32:

{
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "user_id": 1,
  "account_id": 1,
  "amount": 100,
  "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
}
