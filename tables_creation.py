import psycopg2

# Задаємо параметри для підключення до бази даних
database_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

# Функція для створення таблиць
def create_table(create_table_sql):
    """
    Виконує створення таблиці за переданим SQL-запитом.
    :param create_table_sql: SQL-запит CREATE TABLE
    """
    conn = None
    try:
        # Підключення до бази даних
        conn = psycopg2.connect(**database_config)
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        print("Таблиця створена успішно!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Помилка створення таблиці: {error}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # SQL-запити для створення таблиць
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES status (id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users (id) ON DELETE CASCADE
    );
    """

    # Створення таблиць
    print("Створення таблиці users...")
    create_table(sql_create_users_table)
    
    print("Створення таблиці status...")
    create_table(sql_create_status_table)
    
    print("Створення таблиці tasks...")
    create_table(sql_create_tasks_table)
