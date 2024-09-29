from wrapper import mongo_wrapper


@mongo_wrapper
def read_all_cats(db):
    """
    Зчитує всі записи про котів з бази даних і виводить їх на екран.
    """
    results = list(db.cats.find({}))  
    if len(results) == 0:
        print("В базі немає записів")
    for result in results:
        print(result)

@mongo_wrapper
def find_cat_by_name(db):
    """
    Знаходить і виводить на екран інформацію про кота за його ім'ям.
    """
    name = input("Введіть ім'я кота: ")
    result = db.cats.find_one({"name": name})
    if result:
        print(result)
    else:
        print("Кіт за таким ім'ям не знайдений")

@mongo_wrapper
def update_cat_name(db):
    """
    Оновлює ім'я існуючого кота в базі даних.
    """
    name = input("Введіть ім'я кота: ")
    new_name = input("Введіть нове ім'я кота: ")
    if db.cats.find_one({"name": new_name}):
        print("Кіт за таким ім'ям вже є в базі")
        return
    result = db.cats.update_one({"name": name}, {"$set": {"name": new_name}})
    if result.modified_count > 0:
        print(f"Ім'я кота {name} змінено на {new_name}")
    else:
        print("Кота з таким ім'ям не знайдено")

@mongo_wrapper
def update_cat_age(db):
    """
    Оновлює вік існуючого кота в базі даних.
    """
    name = input("Введіть ім'я кота: ")
    new_age = int(input("Введіть новий вік кота цифрами: "))
    result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Вік кота {name} змінено на {new_age}")
    else:
        print("Кота з таким ім'ям не знайдено")

@mongo_wrapper
def add_cat_features(db):
    """
    Додає нові особливості до існуючого кота в базі даних.
    """    
    name = input("Введіть ім'я кота: ")
    features_input = input("Введіть нові особливості кота через крапку з комою ';': ")
    new_features = features_input.split("; ")
    result = db.cats.update_one({"name": name}, {"$push": {"features": {"$each": new_features}}})
    if result.modified_count > 0:
        print(f"Особливості кота {name} додано")
    else:
        print("Кота з таким ім'ям не знайдено")

@mongo_wrapper
def replace_cat_features(db):
    """
    Замінює особливості існуючого кота на нові в базі даних.
    """
    name = input("Введіть ім'я кота: ")
    features_input = input("Введіть нові особливості кота через крапку з комою ';': ")
    new_features = features_input.split("; ")
    result = db.cats.update_one({"name": name}, {"$set": {"features": new_features}})
    if result.modified_count > 0:
        print(f"Особливості кота {name} змінено на нові")
    else:
        print("Кота з таким ім'ям не знайдено")

@mongo_wrapper
def delete_cat(db):
    """
    Видаляє кота за його ім'ям з бази даних.
    """
    name = input("Введіть ім'я кота для видалення: ")
    result = db.cats.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кота {name} видалено")
    else:
        print(f"Кота {name} не знайдено")

@mongo_wrapper
def delete_all_cats(db):
    """
    Видаляє всіх котів з бази даних.
    """
    result = db.cats.delete_many({})  # Видаляємо всі записи
    if result.deleted_count > 0:
        print(f"Усіх котів видалено з бази. Видалено {result.deleted_count} записів.")
    else:
        print("В базі немає котів для видалення.")
