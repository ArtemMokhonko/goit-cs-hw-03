from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

def get_db_connection():
    """
    Встановлює з'єднання з базою даних MongoDB та повертає клієнт MongoDB.
    """
    config = dotenv_values('.env')
    try:
        uri = f"mongodb+srv://{config['USER']}:{config['PASSWORD']}@cluster0.ypwec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client.mds
    except ConnectionFailure:
        print('Щось пішло не так. Не вдалося підключитися до бази даних.')
        return None
    except ConfigurationError as e:
        print(f'Конфігураційна помилка: {e}')
        return None
    except Exception as e:
        print(f'Сталася помилка: {e}')
        return None



