from faker import Faker
from db_config import get_db_connection

# Підключення до бази даних
conn = get_db_connection()
cursor = conn.cursor()

# Ініціалізація Faker
fake = Faker()

# Додавання випадкових користувачів
def seed_users(n):
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

# Додавання статусів завдань
def seed_status():
    cursor.execute("TRUNCATE TABLE status RESTART IDENTITY CASCADE;")
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cursor.execute("INSERT INTO status (name) VALUES (%s)", (status,))
    conn.commit()

# Додавання випадкових завдань
def seed_tasks(n):
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

# Виклик функцій для заповнення бази даних
seed_users(10)
seed_status()
seed_tasks(30)

# Закриття з'єднання
cursor.close()
conn.close()
