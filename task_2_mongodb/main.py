from connection import get_db_connection
from cat_manager import *



def main():
    db = get_db_connection()
    if db is None:
        return
    
    commands = {
        "1": read_all_cats,
        "2": find_cat_by_name,
        "3": update_cat_name,
        "4": update_cat_age,
        "5": add_cat_features,
        "6": replace_cat_features,
        "7": delete_cat,
        "8": delete_all_cats
    }
    
    while True:
        print("""
        Введіть цифру від 1 до 9 для виконання команди:
        1 - Вивести всі дані про котів з бази
        2 - Вивести інформацію про кота за ім'ям
        3 - Оновити ім'я кота
        4 - Оновити вік кота
        5 - Додати особливості кота
        6 - Замінити особливості кота
        7 - Видалити кота за ім'ям
        8 - Видалити всіх котів
        exit - Вийти з програми
        """)
        command = input("Ваш вибір: ")
        if command.lower() == 'exit':
            print("Вихід із програми.")
            break
        if command in commands:
            commands[command](db)
        else:
            print("Невідома команда")


if __name__ == "__main__":
    main()
