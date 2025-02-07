import requests


# data = {"email":"test3@od.ua", "password":"testpasw", "full_name":"sasa"}
data = {"email":"test2@od.ua", "password":"testpasw"}

# Отправка запроса на добавление компании
# response = requests.post("http://127.0.0.1:8000/register", json=data)
response = requests.post("http://127.0.0.1:8000/login", json=data)

res = response.json()
print(response.status_code)
print(res)