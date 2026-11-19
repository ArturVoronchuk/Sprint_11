import random
import string

class UserGenerator:
    @staticmethod
    def random_string(length=10):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_user_payload():
    email = f"test_{UserGenerator.random_string()}@gmail.ru"
    password = UserGenerator.random_string()
    return {
        "email": email,
        "password": password,
        "submitPassword": password,
    }