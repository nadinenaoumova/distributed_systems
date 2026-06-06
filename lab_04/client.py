import requests
from cryptography.fernet import Fernet

# загрузка ключа
with open("encryption_key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

while True:

    print("\n1 - Добавить сообщение")
    print("2 - Показать сообщения")
    print("3 - Выход")

    choice = input("\nВыберите действие: ")

    # =====================
    # ДОБАВЛЕНИЕ СООБЩЕНИЯ
    # =====================

    if choice == "1":

        data = input(
            "Введите сообщение: "
        )

        encrypted = fernet.encrypt(
            data.encode()
        ).decode()

        resp = requests.post(
            "http://127.0.0.1:8000/api/data",
            json={
                "data": encrypted
            }
        )

        print(resp.json())

    # =====================
    # СОРТИРОВКА
    # =====================

    elif choice == "2":

        sort_order = input(
            "Сортировка (asc/desc): "
        )

        resp = requests.get(
            f"http://127.0.0.1:8000/messages?sort={sort_order}"
        )

        print("\nРезультат:")

        for item in resp.json():

            print(
                f"{item['id']} -> {item['message']}"
            )

    # =====================
    # ВЫХОД
    # =====================

    elif choice == "3":

        break

    else:

        print("Неверный выбор")
