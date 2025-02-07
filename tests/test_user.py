import asyncio
import os
import sys
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sanic_testing.reusable import ReusableClient

from app import app
from utils.secret import def_email, def_name, def_password

app.config.DEBUG = True


def test_user(app):
    """Тест API пользователя с тестовой БД"""
    data = {"email": def_email, "password": def_password}

    client = ReusableClient(app)

    with client:

        # Тест логина
        _, response = client.post("user/login", json=data)
        assert response.status == 200
        token = response.json['token']
        headers = {"Authorization": token}

        # Тест получения информации о себе
        _, response_me = client.get("user/me", headers=headers)
        assert response_me.status == 200
        me_data = response_me.json
        assert me_data['email'] == def_email
        assert me_data['full_name'] == def_name


        # Тест получения счетов пользователя
        _, response_account = client.get("user/accounts", headers=headers)
        assert response_account.status == 200

        # Тест получения платежей пользователя
        _, response_payments = client.get("user/payments", headers=headers)
        assert response_payments.status == 200

# Запуск тестов
test_user(app)
