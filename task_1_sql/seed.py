from faker import Faker
import psycopg2
from db_config import get_db_connection

# Ініціалізація Faker
fake = Faker()

# Додавання випадкових користувачів
def seed_users(n, cursor, conn):
    try:
        cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
        for _ in range(n):
            fullname = fake.name()
            email = fake.email()

            # Перевіряємо, чи існує вже користувач з цією електронною адресою
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone() is None:  # Якщо такий користувач не знайдений
                cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
            else:
                print(f"Користувач із email {email} вже існує, пропускаємо.")
        conn.commit()
    except psycopg2.Error as e:
        print(f"Виникла помилка при додаванні користувачів: {e}")
        conn.rollback()

# Додавання статусів завдань
def seed_status(cursor, conn):
    try:
        cursor.execute("TRUNCATE TABLE status RESTART IDENTITY CASCADE;")
        statuses = ['new', 'in progress', 'completed']
        for status in statuses:
            cursor.execute("INSERT INTO status (name) VALUES (%s)", (status,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Виникла помилка при додаванні статусів: {e}")
        conn.rollback()

# Додавання випадкових завдань
def seed_tasks(n, cursor, conn):
    try:
        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cursor.fetchall()]
        
        for _ in range(n):
            title = fake.sentence(nb_words=6)
            description = fake.text()
            status_id = fake.random.choice(status_ids)
            user_id = fake.random.choice(user_ids)
            cursor.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", 
                (title, description, status_id, user_id)
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Виникла помилка при додаванні завдань: {e}")
        conn.rollback()

# Основний блок програми
def main():
    try:
        # Підключення до бази даних
        conn = get_db_connection()
        if conn is None:
            raise psycopg2.OperationalError("Неможливо підключитися до бази даних.")
        
        cursor = conn.cursor()

        # Виклик функцій для заповнення бази даних
        seed_users(10, cursor, conn)
        seed_status(cursor, conn)
        seed_tasks(30, cursor, conn)

        # Закриття курсора та підключення
        cursor.close()
        conn.close()

    except psycopg2.OperationalError as e:
        print(f"Проблема з підключенням до бази даних: {e}")
    except psycopg2.Error as e:
        print(f"Виникла помилка при роботі з базою даних: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
