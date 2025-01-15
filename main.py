from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

# Завантаження конфігурації
config = dotenv_values('.env')
if not config:
    raise FileNotFoundError(".env файл не знайдено або він порожній")

try:
    uri = f"mongodb+srv://{config['USER']}:{config['PASSWORD']}@cluster1.z0xs4cu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.mds
    print("Успішно підключено до MongoDB!")
except KeyError as e:
    raise KeyError(f"Відсутній ключ у конфігурації: {e}")
except ConnectionFailure as e:
    raise ConnectionFailure(f"Не вдалося підключитися до MongoDB: {e}")


# Спільна функція для перевірки існування кота
def find_cat_by_name(name):
    return db.cats.find_one({"name": name})


# Виведення всіх котів
def read():
    try:
        results = db.cats.find({})
        count = 0
        for result in results:
            print(result)
            count += 1
        if count == 0:
            print("База даних порожня.")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою даних: {e}")


# Виведення кота за ім'ям
def read_cat():
    name = input("Введіть ім'я кота: ").strip()
    if not name:
        print("Ім'я не може бути порожнім.")
        return
    try:
        result = find_cat_by_name(name)
        if result:
            print(result)
        else:
            print("Кіт за таким ім'ям не знайдений.")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою даних: {e}")


# Додавання кота
def create():
    name = input("Введіть ім'я кота: ").strip()
    if not name:
        print("Ім'я не може бути порожнім.")
        return
    if find_cat_by_name(name):
        print("Кіт за таким ім'ям вже існує.")
        return

    try:
        age = int(input("Введіть вік кота цифрами: "))
        features = input("Введіть особливості кота через крапку з комою ';': ").split("; ")
        cat = {"name": name, "age": age, "features": features}
        db.cats.insert_one(cat)
        print(f"Кота {name} додано до бази даних.")
    except ValueError:
        print("Некоректне значення для віку.")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою даних: {e}")


# Зміна імені кота
def update_name():
    name = input("Введіть ім'я кота: ").strip()
    if not name or not find_cat_by_name(name):
        print("Кота за таким ім'ям не знайдено.")
        return

    new_name = input("Введіть нове ім'я кота: ").strip()
    if not new_name or find_cat_by_name(new_name):
        print("Нове ім'я некоректне або вже використовується.")
        return

    try:
        result = db.cats.update_one({"name": name}, {"$set": {"name": new_name}})
        if result.modified_count > 0:
            print(f"Ім'я кота змінено на {new_name}.")
        else:
            print("Ім'я кота не змінено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з базою даних: {e}")


# Інші функції (оновлення віку, додавання/заміна особливостей, видалення котів) також можна оптимізувати подібним чином.

# Основна програма
def main():
    commands = {
        "1": read,
        "2": read_cat,
        "3": create,
        "4": update_name,
    }

    while True:
        print("\nКоманди:")
        print("1 - Вивести всі дані про котів")
        print("2 - Вивести інформацію про кота за ім'ям")
        print("3 - Додати нового кота")
        print("4 - Змінити ім'я кота")
        print("exit - Вихід з програми")

        command = input("Введіть команду: ").strip().lower()
        if command == "exit":
            print("Вихід з програми.")
            break
        action = commands.get(command)
        if action:
            action()
        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()
