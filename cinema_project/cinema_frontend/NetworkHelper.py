import requests
from requests.auth import HTTPBasicAuth


class NetworkHelper:
    """
    Клас для роботи з зовнішнім REST API колеги по команді.
    
    ІНСТРУКЦІЯ ПО НАЛАШТУВАННЮ:
    1. Встановіть requests: pip install requests
    2. Змініть BASE_URL на URL API вашого колеги
    3. Змініть USERNAME та PASSWORD на облікові дані колеги
    4. Запустіть проект колеги на іншому порті (наприклад 8001)
    """
    
    def __init__(self, base_url='http://localhost:8001', username='admin', password='admin'):
        """
        Ініціалізація NetworkHelper з параметрами підключення.
        
        Args:
            base_url: Базова URL адреса API (наприклад http://localhost:8001)
            username: Ім'я користувача для авторизації
            password: Пароль для авторизації
        """
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {
            'Content-Type': 'application/json',
        }
    
    def get_list(self, endpoint):
        """
        Отримати список об'єктів з API.
        
        Args:
            endpoint: Назва endpoint (наприклад 'movies', 'genres')
        
        Returns:
            list: Список об'єктів або порожній список у випадку помилки
        """
        try:
            url = f"{self.base_url}/{endpoint}/"
            response = requests.get(url, auth=self.auth, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching list from {endpoint}: {e}")
            return []
    
    def get_item_by_id(self, endpoint, item_id):
        """
        Отримати конкретний об'єкт за ID.
        
        Args:
            endpoint: Назва endpoint (наприклад 'movies', 'genres')
            item_id: ID об'єкта
        
        Returns:
            dict: Об'єкт або None у випадку помилки
        """
        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.get(url, auth=self.auth, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching item {item_id} from {endpoint}: {e}")
            return None
    
    def create_item(self, endpoint, data):
        """
        Створити новий об'єкт через API.
        
        Args:
            endpoint: Назва endpoint (наприклад 'movies', 'genres')
            data: Словник з даними для створення об'єкта
        
        Returns:
            dict: Створений об'єкт або None у випадку помилки
        """
        try:
            url = f"{self.base_url}/{endpoint}/"
            response = requests.post(
                url, 
                json=data, 
                auth=self.auth, 
                headers=self.headers, 
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating item in {endpoint}: {e}")
            return None
    
    def update_item(self, endpoint, item_id, data):
        """
        Оновити існуючий об'єкт за ID.
        
        Args:
            endpoint: Назва endpoint (наприклад 'movies', 'genres')
            item_id: ID об'єкта для оновлення
            data: Словник з новими даними
        
        Returns:
            dict: Оновлений об'єкт або None у випадку помилки
        """
        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.put(
                url, 
                json=data, 
                auth=self.auth, 
                headers=self.headers, 
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating item {item_id} in {endpoint}: {e}")
            return None
    
    def delete_item(self, endpoint, item_id):
        """
        Видалити об'єкт за ID.
        
        Args:
            endpoint: Назва endpoint (наприклад 'movies', 'genres')
            item_id: ID об'єкта для видалення
        
        Returns:
            bool: True якщо видалення успішне, False у випадку помилки
        """
        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.delete(url, auth=self.auth, headers=self.headers, timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting item {item_id} from {endpoint}: {e}")
            return False


    def get_session(self):
        """
        Створити сесію для повторного використання з'єднань.
        Використовуйте цей метод для покращення продуктивності.
        """
        session = requests.Session()
        session.auth = self.auth
        session.headers.update(self.headers)
        return session