import requests
from requests.auth import HTTPBasicAuth


class NetworkHelper:

    
    def __init__(self, base_url='http://localhost:8001', username='admin', password='admin'):

        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {
            'Content-Type': 'application/json',
        }
    
    def get_list(self, endpoint):

        try:
            url = f"{self.base_url}/{endpoint}/"
            response = requests.get(url, auth=self.auth, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching list from {endpoint}: {e}")
            return []
    
    def get_item_by_id(self, endpoint, item_id):

        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.get(url, auth=self.auth, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching item {item_id} from {endpoint}: {e}")
            return None
    
    def create_item(self, endpoint, data):

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

        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.delete(url, auth=self.auth, headers=self.headers, timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting item {item_id} from {endpoint}: {e}")
            return False


    def get_session(self):

        session = requests.Session()
        session.auth = self.auth
        session.headers.update(self.headers)
        return session