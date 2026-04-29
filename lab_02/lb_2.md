# 📄 ЛАБОРАТОРНАЯ РАБОТА №2

## Проектирование и реализация клиент-серверной системы

### Вариант №14

---

## Выполнилa: Наумова Надежда Денисовна 
## Группа: ЦИБ-241


## 2. Цель работы

```text
изучить методы отправки и анализа HTTP-запросов с
использованием инструментов telnet и curl, освоить базовую настройку и
анализ работы HTTP-сервера nginx в качестве веб-сервера и обратного
прокси, а также изучить и применить на практике концепции архитектурного
стиля REST для создания веб-сервисов (API) на языке Python.
```

---

## 3. Теоретические сведения

```text
HTTP — протокол прикладного уровня для передачи данных между клиентом и сервером.

REST — архитектурный стиль построения API, использующий HTTP-методы:
GET, POST, PUT, DELETE.

Nginx — высокопроизводительный веб-сервер, который может выполнять роль:
- статического сервера
- обратного прокси
- балансировщика нагрузки
```

---

## 4. Вариант задания

```text
Вариант №14

1. HTTP-анализ с использованием curl. Получение данных о рейсах с сайта aeroflot.ru (анализ HTML или JS-запросов).
2. Разработка REST API (ресторанное меню). API для "Ресторанное меню" (сущность: id, dish_name,price, category).
3. Настройка Nginx как reverse proxy. Настроить Nginx как обратный прокси для Flask API.

```

---

## 5. Ход работы
Шаг 1. Анализ HTTP-запросов
1.1 Установка утилит
```sudo apt update
sudo apt install curl telnet -y
```
1.2 Отправка запроса к сайту (aeroflot.ru)
```curl -v https://www.aeroflot.ru
```
1.3 Анализ ответа
<img width="947" height="808" alt="image" src="https://github.com/user-attachments/assets/300fc004-7d63-47b4-8205-b44d5b4d6225" />
GET / HTTP/2 - Запрос главной страницы сайта по протоколу HTTP/2
HTTP/2 200 - Запрос выполнен успешно
server: nginx - Сервер работает на Nginx


Шаг 2. Установка и настройка Nginx
## 5.1 Установка и запуск Nginx

```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

Проверка:

```bash
http://localhost
```

Результат: страница “Welcome to nginx”

---

## 5.2 Разработка REST API (Flask)

### Установка зависимостей

```bash
mkdir ~/rest_api_lab
cd ~/rest_api_lab

python3 -m venv venv
source venv/bin/activate

pip install flask
```

---

### Код приложения (app.py)

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

menu = [
    {"id": 1, "dish_name": "Пицца", "price": 500, "category": "Основное"},
    {"id": 2, "dish_name": "Салат", "price": 300, "category": "Закуски"}
]

next_id = 3

@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

@app.route('/api/menu/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in menu if i['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/menu', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()

    new_item = {
        "id": next_id,
        "dish_name": data["dish_name"],
        "price": data.get("price", 0),
        "category": data.get("category", "Другое")
    }

    menu.append(new_item)
    next_id += 1

    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### Запуск

```bash
python3 app.py
```

---

## 5.3 Настройка Nginx (reverse proxy)

### Конфигурация

```nginx
server {
    listen 80;
    server_name _;

    location /api/ {
        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

### Перезапуск

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 5.4 Тестирование системы

---

### Получение всех блюд

```bash
curl http://localhost/api/menu
```

---

### Получение блюда по ID

```bash
curl http://localhost/api/menu/1
```

---

### Добавление блюда

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"dish_name":"Суп","price":250,"category":"Первое"}' \
http://localhost/api/menu
```

---

### Проверка через Nginx

```bash
curl http://localhost/api/menu
```

---

## 6. Результаты

* REST API успешно реализован на Flask
* Nginx настроен как reverse proxy
* Запросы перенаправляются с 80 порта на 5000
* Реализованы GET и POST методы

---

## 7. Вывод

```text
В ходе лабораторной работы были изучены принципы работы HTTP-протокола.

Разработано REST API на Flask.

Настроен Nginx как обратный прокси-сервер.

Получены практические навыки работы с клиент-серверной архитектурой.
```

---
