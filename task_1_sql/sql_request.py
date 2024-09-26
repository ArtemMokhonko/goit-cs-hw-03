import psycopg2
import json
import logging
from db_config import get_db_connection

# Налаштування логування
logging.basicConfig(filename='db_log.json', level=logging.INFO, format='%(message)s')

def log_to_json(data: dict) -> None:
    """
    Записує лог у форматі JSON.
    """
    with open('db_log.json', 'a', encoding='utf-8') as log_file:
        json.dump(data, log_file, ensure_ascii=False, indent=4)
        log_file.write('\n')

def execute_query(query: str, description: str, params=None):
    """
    Виконує SQL-запит до бази даних та логує результат або помилку.
    """
    log_data = {
        "description": description,
        "query": query,
        "status": "success",
        "error": None,
        "result": None
    }
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise psycopg2.OperationalError("Неможливо підключитися до бази даних.")

        cursor = conn.cursor()
        cursor.execute(query, params)
        
        # Перевірка типу запиту (SELECT або інший)
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
            log_data["result"] = result
            for row in result:
                print(row)
        else:
            conn.commit()
            print("Запит успішно виконаний.")
            log_data["result"] = "Запит успішно виконаний."

    except psycopg2.OperationalError as e:
        log_data["status"] = "error"
        log_data["error"] = f"Проблема з підключенням до бази даних: {e}"
        print(f"Проблема з підключенням до бази даних: {e}")

    except psycopg2.Error as e:
        log_data["status"] = "error"
        log_data["error"] = str(e)
        print(f"Виникла помилка: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        log_to_json(log_data)

with open('description.txt', 'r', encoding='utf-8') as f:
    descriptions = f.readlines()

with open('requests.sql', 'r') as f:
    sql_requests = f.readlines()

# Перевірка відповідності кількості описів та запитів
if len(descriptions) != len(sql_requests):
    print("Помилка: кількість описів не відповідає кількості SQL запитів.")
else:
    # Виконання кожного запиту з відповідним описом
    for i, (description, query) in enumerate(zip(descriptions, sql_requests)):
        print(f"\nОпис {i+1}: {description.strip()}")
        print(f"Виконую запит: {query.strip()}")
        execute_query(query.strip(), description.strip())  # Передаємо і опис, і запит
        print("-" * 50)
