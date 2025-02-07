import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sanic_testing.reusable import ReusableClient

from app import app
from utils.secret import admin_email, admin_password

app.config.DEBUG = True

def test_admin(app):

    data_login = {"email": admin_email, "password": admin_password}

    data_register = {"email":"user22@od.ru",
                     "password":"password2",
                     "full_name":"user2"}

    data_patch = {"old":{"email":"user22@od.ru",
                     "password":"password2",
                     "full_name":"user2"},
                  "new":{"email":"user2@odessa11111.ru"}}

    data_patch_re = {"old":{"email":"user2@odessa11111.ru",
                     "password":"password2",
                     "full_name":"user2"},
                  "new":{"email":"user22@od.ru"}}

    client = ReusableClient(app)

    with client:

        # тест логирования
        _, response_login = client.post("admin/login", json=data_login)
        assert response_login.status == 200

        # получение token
        res = response_login.json
        token = res['token']
        headers = {"Authorization": token}

        #  тест регистрации нового пользователя
        _, response = client.post("admin/register", headers=headers, json=data_register)
        assert response.status == 200
        response_register = response.json
        assert response_register['message'] == 'User registered successfully'

         # тест получения сведений о пользователях
        _, response_users = client.get("admin/all_users", headers=headers)
        assert response_users.status == 200

        #  тест редактирования данных о пользователе
        _, response_patch = client.patch("admin/patch", headers=headers, json=data_patch)
        assert response_patch.status == 200
        # возврат изменений
        _, response_patch = client.patch("admin/patch", headers=headers, json=data_patch_re)
        assert response_patch.status == 200


        # Тест получения информации о себе
        _, response_me = client.get("admin/me", headers=headers)
        assert response_me.status == 200

        # Тест удаления пользователя
        _, response_delete = client.delete("admin/delete/3", headers=headers)
        assert response_delete.status == 204

        # Тест получения списка пользователей и его счетов с балансами
        _, response_get = client.get("admin/payments", headers=headers)
        assert response_get.status == 200


test_admin(app)