
from db_config import get_db_connection

def execute_sql_file(filename):
    conn = None
    try:
        # Підключення до бази даних
        conn = get_db_connection()
        cursor = conn.cursor()

        # Читання SQL запитів з файлу
        with open(filename, 'r') as sql_file:
            sql_commands = sql_file.read()

        # Виконання SQL запитів
        cursor.execute(sql_commands)
        conn.commit()

        print("Таблиці успішно створено!")

    except Exception as error:
        print(f"Виникла помилка: {error}")

    finally:
        if conn:
            cursor.close()
            conn.close()

# Виклик функції для виконання SQL файлу
if __name__ == "__main__":
    execute_sql_file('create_tables.sql')
