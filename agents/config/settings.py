import os
from dotenv import load_dotenv

def get_api_key():
    """Возвращает API ключ из переменных окружения"""
    if os.path.exists('.env'):
        load_dotenv()
        return os.getenv('OPENROUTER_API_KEY')
