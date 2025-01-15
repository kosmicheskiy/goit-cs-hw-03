import faker
import random
import psycopg2

# Конфігурація бази даних
database_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

# Кількість користувачів і завдань
NUMBER_USERS = 30
NUMBER_TASKS = 40


def generate_fake_data(number_users, number_tasks):
    fake = faker.Faker()

    # Статуси задач
    fake_status = [('new',), ('in progress',), ('completed',)]

    # Генеруємо унікальних користувачів
    fake_users = [(fake.name(), fake.unique.email()) for _ in range(number_users)]

    # Генеруємо завдання
    fake_tasks = [
        (
            fake.sentence(nb_words=6),         # title
            fake.text(max_nb_chars=200),      # description
            random.randint(1, 3),             # status_id
            random.randint(1, number_users)   # user_id
        )
        for _ in range(number_tasks)
    ]

    return fake_users, fake_status, fake_tasks


def insert_data_to_db(users, status, tasks):
    con = None
    try:
        con = psycopg2.connect(**database_config)
        cur = con.cursor()

        # Вставляємо дані
        cur.executemany('INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT DO NOTHING', users)
        cur.executemany('INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING', status)
        cur.executemany('INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)', tasks)

        # Фіксуємо зміни
        con.commit()
        print("Дані успішно додано до бази даних.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Помилка: {error}")
    
    finally:
        if con:
            cur.close()
            con.close()


if __name__ == '__main__':
    # Генеруємо та додаємо дані
    users, status, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    insert_data_to_db(users, status, tasks)
